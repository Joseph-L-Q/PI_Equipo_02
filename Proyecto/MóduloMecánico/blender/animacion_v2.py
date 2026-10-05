"""20 s presentation video of the mechanical module (v2), rendered headless with Eevee to a PNG sequence.

    Blender -b -P animacion_v2.py -- [--in DIR] [--png DIR] [--res WxH] [--samples N] [--only 1,120,300]

Frames go to DIR/f_0001.png ... ; a relaunch resumes (finished frames are skipped, 0-byte placeholders
from an interrupted frame are deleted first). --only renders just those frames (look checks).
Assemble the MP4 afterwards with ffmpeg (render_v2.sh does it).

Input: the per-instance STLs and manifest.json that cad/build.py writes to stl/ensamble_piezas/
(assembly position, mm; the right capsule comes at 0 deg tilt, the left one already tilted).
Timeline (30 fps, 600 frames, every key eased):
   0-4 s  assembled module turns 120 deg (isometric view)
   4-10 s exploded piece by piece in reverse assembly order, each piece with its label:
          M2 lid up, M6 bezels and M7 windows out along the optical axis, M5 caps back (and up, to clear
          the arm), M4 capsule bodies apart, M3 arms away from the box
  10-13 s exploded pause with a slow turn
  13-18 s reassembled in assembly order (labels leave as each piece goes home)
  18-20 s right capsule 0 -> 40 deg about its hinge; final title card
"""
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

FPS, SECONDS = 30, 20
MM = 0.001
FONT_DIR = Path("/System/Library/Fonts/Supplemental")


def srgb(h):
    """'#RRGGBB' -> linear RGBA (Blender base colours are linear)."""
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1.0,)


# Onshape-like palette. Red is the STEP's own COLOUR_RGB (0.85, 0.20, 0.18) of the PETG parts.
MATS = {  # colour, roughness, alpha, clearcoat
    "red": (srgb("#D9332E"), 0.38, 1.0),
    "black": (srgb("#1C1C1E"), 0.72, 1.0),
    "grey": (srgb("#C9CBCE"), 0.45, 1.0),
    "handle": (srgb("#9A9DA1"), 0.5, 1.0),
    "glass": (srgb("#BFDDF7"), 0.02, 0.38),
}
INK = srgb("#2B2D31")
ACCENT = srgb("#C0392B")
BACKDROP = srgb("#D7D9DC")

# Each step: part ids, label, explode offset per side in the capsule frame (axis, up) or world, timing.
# (mm; "axis" = outward along the optical axis, "up" = capsule up, perpendicular to it)
NAMES = {"M1": "Caja central", "M2": "Tapa con asa", "M3": "Brazo", "M4": "Cápsula",
         "M5": "Tapa de cápsula", "M6": "Bisel de ventana", "M7": "Ventana de acrílico"}
#          part, out (s), back (s), frame, (axis, up) or world xyz
STEPS = [("M2", 4.0, 16.4, "world", (0, 0, 95)),
         ("M6", 4.9, 15.6, "cap", (112, 0)),
         ("M7", 5.8, 14.8, "cap", (82, 0)),
         ("M5", 6.7, 14.6, "cap", (-22, 62)),
         ("M4", 7.6, 13.8, "cap", (48, 0)),
         ("M3", 8.5, 13.0, "world_x", (36,))]
MOVE_S = 1.25          # duration of each piece's move
TAG_ABOVE = {"M2": 1, "M6": 1, "M7": -1, "M5": 1, "M4": 1, "M3": -1}


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    here = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    o = {"in": str(here.parent / "stl" / "ensamble_piezas"), "png": str(here / "out" / "frames_v2"),
         "res": "1920x1080", "samples": "64", "only": "", "light": "0.11"}
    for i in range(0, len(argv) - 1, 2):
        o[argv[i].lstrip("-")] = argv[i + 1]
    w, h = (int(v) for v in o["res"].lower().split("x"))
    only = [int(v) for v in o["only"].split(",") if v]
    return Path(o["in"]), Path(o["png"]), (w, h), int(o["samples"]), only, float(o["light"])


f = lambda s: 1 + round(s * FPS)  # noqa: E731  seconds -> frame


def key(obj, path, frame, value, index=-1):
    if index < 0:
        setattr(obj, path, value)
    else:
        getattr(obj, path)[index] = value
    obj.keyframe_insert(data_path=path, frame=frame, index=index)


def fcurves():
    """All fcurves of all actions (Blender 5 layered actions: layers > strips > channelbags)."""
    for a in bpy.data.actions:
        for layer in a.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    yield from cb.fcurves


def ease_all():
    """Every key Bezier with auto-clamped handles: flat at each key, i.e. ease in and out."""
    for fc in fcurves():
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"


def surface(name, col, rough, alpha):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = col
    b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = 0.5
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        b.inputs["Transmission Weight"].default_value = 0.6
        m.surface_render_method = "BLENDED"
        m.use_transparent_shadow = True
    return m


def ink(name, col):
    """Unlit text material with a keyframable opacity (Mix factor: 0 = invisible)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = col
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = 0.0
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m.surface_render_method = "BLENDED"
    m.use_transparent_shadow = True
    return m, mix.inputs[0], em.inputs["Color"]


def fade(sock, frames_values):
    for fr, v in frames_values:
        sock.default_value = v
        sock.keyframe_insert("default_value", frame=fr)


def text(name, body, size, font, col, parent=None, loc=(0, 0, 0), align="CENTER"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size
    cu.align_x, cu.align_y = align, "CENTER"
    try:
        cu.font = bpy.data.fonts.load(str(FONT_DIR / font), check_existing=True)
    except RuntimeError:
        pass  # Blender's built-in font
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    m, alpha, colour = ink(name + "_ink", col)
    cu.materials.append(m)
    if parent:
        ob.parent = parent
    ob.location = loc
    return ob, alpha, colour


def clean_mesh(ob):
    """Bake the importer's object scale into the vertices (metres), weld, smooth by angle."""
    ob.data.transform(ob.matrix_basis)
    ob.matrix_basis = Matrix.Identity(4)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.to_mesh(ob.data)
    bm.free()
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(32))
    ob.select_set(False)


def cyclorama(centre, floor_z, width=8.0, depth=6.0, height=4.0, r=1.2):
    """Floor that bends up into a back wall (studio cove): soft gradient, no horizon line."""
    prof = []
    for i in range(10):                          # flat floor from the front to the bend
        prof.append((-depth / 2 + i * (depth / 2) / 9, 0.0))
    for i in range(1, 17):                       # quarter circle
        a = i / 16 * math.pi / 2
        prof.append((r * math.sin(a), r * (1 - math.cos(a))))
    prof.append((r, height))
    me = bpy.data.meshes.new("cove")
    verts, faces = [], []
    for x in (-width / 2, width / 2):
        for y, z in prof:
            verts.append((centre.x + x, centre.y + y + 0.55, floor_z + z))
    n = len(prof)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    me.from_pydata(verts, [], faces)
    me.shade_smooth()
    ob = bpy.data.objects.new("cove", me)
    bpy.context.scene.collection.objects.link(ob)
    m = surface("backdrop", BACKDROP, 0.95, 1.0)
    ob.data.materials.append(m)
    return ob


def area(name, loc, target, energy, size, colour=(1, 1, 1)):
    li = bpy.data.lights.new(name, "AREA")
    li.energy, li.size, li.color = energy, size, colour
    ob = bpy.data.objects.new(name, li)
    ob.location = loc
    bpy.context.scene.collection.objects.link(ob)
    c = ob.constraints.new("TRACK_TO")
    c.target, c.track_axis, c.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
    return ob


def main():
    src, png, res, samples, only, light = args()
    man = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    mats = {k: surface(k, *v) for k, v in MATS.items()}

    root = bpy.data.objects.new("Root", None)
    sc.collection.objects.link(root)
    hinge = bpy.data.objects.new("HingeDer", None)
    sc.collection.objects.link(hinge)
    hinge.location = Vector(man["hinge_der"]["pivot"]) * MM
    hinge.parent = root
    bpy.context.view_layer.update()

    parts = {}  # (part id, side) -> object
    for p in man["parts"]:
        bpy.ops.wm.stl_import(filepath=str(src / p["file"]), global_scale=MM)
        ob = bpy.context.selected_objects[0]
        ob.select_set(False)
        ob.name = p["file"][:-4]
        clean_mesh(ob)
        colour = "grey" if p["part"] == "M2" else p["color"]
        ob.data.materials.append(mats[colour])
        par = hinge if p["group"] == "hinge_der" else root
        ob.parent = par
        ob.matrix_parent_inverse = par.matrix_world.inverted()
        side = "der" if p["file"].endswith("der.stl") else "izq" if p["file"].endswith("izq.stl") else "-"
        parts[(p["part"], side)] = ob
    bpy.context.view_layer.update()

    # handle of the lid in a darker grey: faces above the lid plate (z > 30 + 6 mm)
    lid = parts[("M2", "-")]
    lid.data.materials.append(mats["handle"])
    for poly in lid.data.polygons:
        if poly.center.z > 0.036:
            poly.material_index = 1

    pts = [ob.matrix_world @ Vector(c) for ob in parts.values() for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centre = (lo + hi) / 2

    # capsule frames: right capsule axis +x (0 deg here), left one tilted nose-down by tilt_deg
    t = math.radians(man["tilt_deg"])
    frames = {"der": (Vector((1, 0, 0)), Vector((0, 0, 1))),
              "izq": (Vector((-math.cos(t), 0, -math.sin(t))), Vector((-math.sin(t), 0, math.cos(t))))}

    # ---------------------------------------------------------------- camera + on-screen text
    target = bpy.data.objects.new("target", None)
    target.location = centre + Vector((0.06, 0, 0.06))
    sc.collection.objects.link(target)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    cam.data.lens = 50
    cam.data.dof.use_dof = False
    sc.collection.objects.link(cam)
    d = Vector((0.30, -1.0, 0.62)).normalized()
    cam.location = centre + d * 1.55
    tr = cam.constraints.new("TRACK_TO")
    tr.target, tr.track_axis, tr.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
    sc.camera = cam
    bpy.context.view_layer.update()
    # a slow push-in over the whole clip, eased
    for s, dist in ((0, 1.55), (4, 1.80), (9.6, 2.08), (13, 2.08), (18, 1.62), (20, 1.50)):
        key(cam, "location", f(s), centre + d * dist)
    cam_rot = cam.matrix_world.to_quaternion()

    # screen-space overlay: children of the camera, 1 m in front of it (visible width 0.72 m at 50 mm)
    hud = bpy.data.objects.new("hud", None)
    sc.collection.objects.link(hud)
    hud.parent = cam
    hud.location = (0, 0, -1.0)

    # ---------------------------------------------------------------- piece-by-piece choreography
    rows = []  # legend rows in order of appearance
    for i, (pid, t_out, t_back, frame, vec) in enumerate(STEPS):
        for side in ("der", "izq", "-"):
            ob = parts.get((pid, side))
            if ob is None:
                continue
            if frame == "world":
                ex = Vector(vec)
            elif frame == "world_x":
                ex = Vector((vec[0] if side == "der" else -vec[0], 0, 0))
            else:
                ax, up = frames[side]
                ex = ax * vec[0] + up * vec[1]
            ex = ex * MM
            for s, k in ((0, 0), (t_out, 0), (t_out + MOVE_S, 1), (t_back, 1), (t_back + MOVE_S, 0)):
                key(ob, "location", f(s), ex * k)
            # 3D tag on the right-hand (or only) instance, facing the camera
            if side in ("der", "-"):
                bb = [Vector(c) for c in ob.bound_box]
                c = sum(bb, Vector()) / 8
                up = TAG_ABOVE[pid]
                zz = (max(v.z for v in bb) + 0.022) if up > 0 else (min(v.z for v in bb) - 0.026)
                tag, a, _ = text(f"tag_{pid}", pid, 0.026, "DIN Alternate Bold.ttf", ACCENT,
                                 parent=ob, loc=(c.x, c.y, zz))
                cr = tag.constraints.new("COPY_ROTATION")
                cr.target = cam
                fade(a, [(f(0), 0), (f(t_out + 0.3), 0), (f(t_out + 0.9), 1), (f(t_back - 0.1), 1), (f(t_back + 0.4), 0)])
        rows.append((pid, t_out, t_back))
    # M1 stays; its tag and row arrive once everything is off it
    box = parts[("M1", "-")]
    tag, a, _ = text("tag_M1", "M1", 0.026, "DIN Alternate Bold.ttf", ACCENT, parent=box, loc=(0, -0.07, 0.058))
    tag.constraints.new("COPY_ROTATION").target = cam
    fade(a, [(f(0), 0), (f(9.3), 0), (f(9.9), 1), (f(12.6), 1), (f(13.1), 0)])
    rows.append(("M1", 9.3, 12.6))

    # legend (left column): "M2  Tapa con asa"; the newest row is red, older ones settle to ink
    x0, y0, dy = -0.335, 0.150, 0.024
    head, ha, _ = text("legend_head", "DESPIECE · ORDEN DE MONTAJE INVERSO", 0.0115, "Arial Bold.ttf", INK,
                       parent=hud, loc=(x0, y0 + 0.030, 0), align="LEFT")
    fade(ha, [(f(0), 0), (f(3.8), 0), (f(4.4), 0.75), (f(12.4), 0.75), (f(13.0), 0)])
    head2, hb, _ = text("legend_head2", "MONTAJE", 0.0115, "Arial Bold.ttf", INK,
                        parent=hud, loc=(x0, y0 + 0.030, 0), align="LEFT")
    fade(hb, [(f(0), 0), (f(12.8), 0), (f(13.3), 0.75), (f(17.0), 0.75), (f(17.6), 0)])
    for j, (pid, t_in, t_out) in enumerate(rows):
        y = y0 - j * dy
        label = f"{pid}   {NAMES[pid]}"
        ob, a, colour = text(f"row_{pid}", label, 0.0150, "Arial.ttf", INK, parent=hud, loc=(x0, y, 0), align="LEFT")
        fade(a, [(f(0), 0), (f(t_in + 0.2), 0), (f(t_in + 0.7), 1), (f(t_out + 0.2), 1), (f(t_out + 0.7), 0)])
        nxt = rows[j + 1][1] if j + 1 < len(rows) else 10.6
        for fr, cval in ((f(t_in), ACCENT), (f(nxt + 0.2), ACCENT), (f(nxt + 0.6), INK),
                         (f(t_out - 0.4), INK), (f(t_out), ACCENT)):
            colour.default_value = cval
            colour.keyframe_insert("default_value", frame=fr)
        for s, dx in ((t_in + 0.2, -0.012), (t_in + 0.7, 0.0)):     # slide in from the left
            key(ob, "location", f(s), Vector((x0 + dx, y, 0)))

    # final title card
    title, ta, _ = text("title", "LanternGuard · Módulo sumergido", 0.040, "Arial Bold.ttf", INK,
                        parent=hud, loc=(0, -0.150, 0))
    fade(ta, [(f(0), 0), (f(18.4), 0), (f(19.3), 1)])
    for s, y in ((18.4, -0.165), (19.3, -0.150)):
        key(title, "location", f(s), Vector((0, y, 0)))
    sub, sa, _ = text("subtitle", "Proyecto Integrador · Equipo 02 · Módulo mecánico", 0.0135, "Arial.ttf", ACCENT,
                      parent=hud, loc=(0, -0.183, 0))
    fade(sa, [(f(0), 0), (f(18.8), 0), (f(19.6), 1)])

    # ---------------------------------------------------------------- turntable + hinge
    # -98 -> 22 deg: ends near broadside (the explosion along X reads in full) but turned enough
    # that the window discs are not seen edge-on
    for s, deg in ((0, -98), (4, 22), (10, 22), (13, 36), (18, 41), (20, 43)):
        key(root, "rotation_euler", f(s), math.radians(deg), 2)
    key(hinge, "rotation_euler", f(0), 0.0, 1)
    key(hinge, "rotation_euler", f(18), 0.0, 1)
    key(hinge, "rotation_euler", f(19.4), math.radians(man["tilt_deg"]), 1)
    ease_all()
    # the slow turn 10-20 s reads better without stopping at 13 and 18: linear-ish middle keys
    for fc in fcurves():
        if fc.data_path == "rotation_euler" and fc.array_index == 2 and len(fc.keyframe_points) == 6:
            for kp in fc.keyframe_points[3:5]:
                kp.handle_left_type = kp.handle_right_type = "AUTO"

    # ---------------------------------------------------------------- studio
    floor_z = lo.z - 0.004
    cyclorama(centre, floor_z)
    world = bpy.data.worlds.new("w")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = srgb("#E4E6E8")
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.35 * light
    sc.world = world
    c = centre
    area("key", c + Vector((-0.9, -1.1, 1.3)), target, 260 * light, 1.4, (1.0, 0.97, 0.93))
    area("fill", c + Vector((1.4, -0.9, 0.5)), target, 90 * light, 2.0, (0.93, 0.96, 1.0))
    area("rim", c + Vector((0.4, 1.3, 1.1)), target, 180 * light, 1.0)
    area("top", c + Vector((0, 0, 1.6)), target, 70 * light, 2.5)

    # ---------------------------------------------------------------- render settings
    r = sc.render
    r.engine = "BLENDER_EEVEE"
    e = sc.eevee
    e.taa_render_samples = samples
    e.use_raytracing = True
    e.ray_tracing_method = "SCREEN"
    e.use_fast_gi = True                       # horizon-scan AO / GI
    e.fast_gi_distance = 0.25
    e.use_shadows = True
    e.shadow_ray_count = 2
    e.shadow_step_count = 8
    e.use_overscan = True
    world.light_settings.distance = 0.25       # AO distance
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    r.resolution_x, r.resolution_y, r.resolution_percentage = res[0], res[1], 100
    r.fps = FPS
    r.film_transparent = False
    r.filter_size = 1.2
    sc.frame_start, sc.frame_end = 1, FPS * SECONDS
    png.mkdir(parents=True, exist_ok=True)
    if hasattr(r.image_settings, "media_type"):
        r.image_settings.media_type = "IMAGE"
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGB"
    r.image_settings.compression = 30

    if only:
        for fr in only:
            sc.frame_set(fr)
            r.filepath = str(png / f"check_{fr:04d}.png")
            bpy.ops.render.render(write_still=True)
            print("CHECK_DONE", r.filepath)
        return
    for empty in png.glob("f_*.png"):
        if empty.stat().st_size == 0:
            empty.unlink()
    r.use_overwrite, r.use_placeholder = False, True
    r.filepath = str(png / "f_####")
    bpy.ops.render.render(animation=True)
    print("ANIMATION_DONE", png)


main()
