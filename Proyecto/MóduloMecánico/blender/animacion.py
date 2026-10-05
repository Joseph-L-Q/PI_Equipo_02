"""12 s assembly animation of the mechanical module, rendered headless with Eevee to MP4 (H.264).

    Blender -b -P animacion.py -- [--in DIR] [--out FILE.mp4] [--frames N] [--res WxH] [--png DIR] [--start N]

With --png the frames go to DIR/f_0001.png ... and a relaunch resumes after the last finished frame
(existing frames are skipped, empty placeholders from an interrupted frame are deleted first);
assemble the MP4 afterwards with ffmpeg. Without --png Blender writes the MP4 directly.

Input: the per-instance STLs and manifest.json that cad/build.py writes to stl/ensamble_piezas/
(already in assembly position, mm; the right capsule comes at 0 deg tilt).
Timeline (30 fps): 0-4 s the whole module turns 180 deg; 4-8 s exploded view (eased);
8-12 s it reassembles and the right capsule turns 0 -> 40 deg about its hinge axis.
"""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

FPS, SECONDS = 30, 12
MM = 0.001
COLORS = {  # base colour, roughness, alpha
    "red": ((0.62, 0.07, 0.06, 1), 0.45, 1.0),
    "black": ((0.025, 0.025, 0.028, 1), 0.5, 1.0),
    "grey": ((0.55, 0.55, 0.55, 1), 0.5, 1.0),
    "glass": ((0.75, 0.88, 1.0, 1), 0.05, 0.22),
}
BG = (0.60, 0.60, 0.60, 1)          # linear; ~0.80 in sRGB, the grey of the still renders
FLOOR = (0.43, 0.43, 0.43, 1)       # lit floor (ambient 0.6 + sun 1.0) comes out at about the background grey


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    here = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    o = {"in": str(here.parent / "stl" / "ensamble_piezas"), "out": str(here / "out" / "LG_mec_animacion.mp4"),
         "frames": str(FPS * SECONDS), "res": "1920x1080", "png": "", "start": "1"}
    for i in range(0, len(argv) - 1, 2):
        o[argv[i].lstrip("-")] = argv[i + 1]
    w, h = (int(v) for v in o["res"].lower().split("x"))
    return Path(o["in"]), Path(o["out"]), int(o["frames"]), (w, h), (Path(o["png"]) if o["png"] else None), int(o["start"])


def material(name):
    col, rough, alpha = COLORS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = col
    b.inputs["Roughness"].default_value = rough
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
        else:
            m.blend_method = "BLEND"
    return m


def key(obj, path, frame, value, index=-1):
    setattr(obj, path, value) if index < 0 else getattr(obj, path).__setitem__(index, value)
    obj.keyframe_insert(data_path=path, frame=frame, index=index)


def main():
    src, out, frames, res, png, start = args()
    man = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    mats = {k: material(k) for k in COLORS}

    root = bpy.data.objects.new("Root", None)
    sc.collection.objects.link(root)
    hinge = bpy.data.objects.new("HingeDer", None)
    sc.collection.objects.link(hinge)
    hinge.location = Vector(man["hinge_der"]["pivot"]) * MM
    hinge.parent = root
    bpy.context.view_layer.update()

    parts = []
    for p in man["parts"]:
        bpy.ops.wm.stl_import(filepath=str(src / p["file"]), global_scale=MM)
        ob = bpy.context.selected_objects[0]
        ob.name = p["file"][:-4]
        ob.data.materials.append(mats[p["color"]])
        par = hinge if p["group"] == "hinge_der" else root
        ob.parent = par
        ob.matrix_parent_inverse = par.matrix_world.inverted()
        parts.append((ob, Vector(p["explode"]) * MM))
    bpy.context.view_layer.update()

    # bounds of the assembled module (world, m)
    pts = [ob.matrix_world @ Vector(c) for ob, _ in parts for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centre = (lo + hi) / 2
    radius = max((hi - lo).x, (hi - lo).y) / 2 + 0.13      # room for the exploded parts

    # timeline: 0-4 s turn, 4-8 s explode, 8-12 s reassemble + hinge
    f = lambda s: 1 + round(s * FPS)  # noqa: E731
    key(root, "rotation_euler", f(0), 0.0, 2)
    key(root, "rotation_euler", f(4), math.pi, 2)
    for ob, ex in parts:
        for s, k in ((4, 0), (6.6, 1), (8, 1), (10, 0)):
            key(ob, "location", f(s), ex * k)
    key(hinge, "rotation_euler", f(0), 0.0, 1)
    key(hinge, "rotation_euler", f(10), 0.0, 1)
    key(hinge, "rotation_euler", f(11.6), math.radians(man["tilt_deg"]), 1)
    # default keyframe interpolation is Bezier with auto-clamped handles: ease in and out

    # floor with soft shadow, same grey as the background
    bpy.ops.mesh.primitive_plane_add(size=40, location=(centre.x, centre.y, lo.z - 0.09))
    floor = bpy.context.object
    fm = bpy.data.materials.new("floor")
    fm.use_nodes = True
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = FLOOR
    fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
    floor.data.materials.append(fm)

    world = bpy.data.worlds.new("w")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = BG
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    sc.world = world
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy, sun.data.angle = 1.0, math.radians(12)
    sun.rotation_euler = (math.radians(35), math.radians(10), math.radians(30))
    sc.collection.objects.link(sun)

    target = bpy.data.objects.new("target", None)
    target.location = centre
    sc.collection.objects.link(target)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    cam.data.lens = 50
    d = Vector((0.45, -1.0, 0.62)).normalized()
    cam.location = centre + d * radius / math.tan(math.atan(18 / 50)) * 0.95
    tr = cam.constraints.new("TRACK_TO")
    tr.target, tr.track_axis, tr.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
    sc.collection.objects.link(cam)
    sc.camera = cam

    r = sc.render
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            r.engine = eng
            break
        except TypeError:
            continue
    if hasattr(sc.eevee, "taa_render_samples"):
        sc.eevee.taa_render_samples = 32
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.exposure = 0.67      # measured: without it the background renders at 166/255 instead of ~204
    r.resolution_x, r.resolution_y, r.resolution_percentage = res[0], res[1], 100
    r.fps = FPS
    sc.frame_start, sc.frame_end = start, frames
    if png:
        png.mkdir(parents=True, exist_ok=True)
        for empty in png.glob("f_*.png"):
            if empty.stat().st_size == 0:
                empty.unlink()
        if hasattr(r.image_settings, "media_type"):
            r.image_settings.media_type = "IMAGE"
        r.image_settings.file_format = "PNG"
        r.use_overwrite, r.use_placeholder = False, True
        r.filepath = str(png / "f_####")
        target_out = png
    else:
        if hasattr(r.image_settings, "media_type"):
            r.image_settings.media_type = "VIDEO"
        r.image_settings.file_format = "FFMPEG"
        r.ffmpeg.format, r.ffmpeg.codec = "MPEG4", "H264"
        r.ffmpeg.constant_rate_factor, r.ffmpeg.ffmpeg_preset = "HIGH", "GOOD"
        r.ffmpeg.audio_codec = "NONE"
        out.parent.mkdir(parents=True, exist_ok=True)
        r.filepath = str(out)
        target_out = out
    bpy.ops.render.render(animation=True)
    print("ANIMATION_DONE", target_out)


main()
