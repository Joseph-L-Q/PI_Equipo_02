"""B-rep checks copied from cad/build.py (not imported: cad/ has its own params.py on sys.path)."""
import cadquery as cq
from OCP.BOPAlgo import BOPAlgo_ArgumentAnalyzer
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.ShapeFix import ShapeFix_Shape
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain

MIN_EDGE, MIN_FACE = 0.05, 0.01   # mm, mm2: below this Parasolid (Onshape) tends to flag slivers


def sanitize(wp):
    """clean() + ShapeFix_Shape + UnifySameDomain + ShapeFix_Shape, before any export."""
    sf = ShapeFix_Shape(wp.clean().val().wrapped)
    sf.SetPrecision(1e-6)
    sf.SetMaxTolerance(1e-3)
    sf.Perform()
    u = ShapeUpgrade_UnifySameDomain(sf.Shape(), True, True, True)
    u.Build()
    sf2 = ShapeFix_Shape(u.Shape())
    sf2.Perform()
    return cq.Shape.cast(sf2.Shape())


def brep_check(shape):
    """BRepCheck + BOPAlgo_ArgumentAnalyzer + sliver scan. Returns the dict; 'ok' says if it passed."""
    aa = BOPAlgo_ArgumentAnalyzer()
    aa.SetShape1(shape.wrapped)
    for m in ("SelfInterMode", "SmallEdgeMode", "RebuildFaceMode", "TangentMode", "MergeVertexMode",
              "MergeEdgeMode", "ContinuityMode", "CurveOnSurfaceMode"):
        setattr(aa, m, True)
    aa.Perform()
    c = dict(brep=BRepCheck_Analyzer(shape.wrapped, True).IsValid(), bop=not aa.HasFaulty(),
             solids=len(shape.Solids()), min_edge=min(e.Length() for e in shape.Edges()),
             min_face=min(f.Area() for f in shape.Faces()))
    c["ok"] = c["brep"] and c["bop"] and c["solids"] == 1 and c["min_edge"] >= MIN_EDGE and c["min_face"] >= MIN_FACE
    return c


def export_part(shape, stem, stl_dir, step_dir=None):
    """STL (and STEP if step_dir) of an already sanitized shape; the STEP must read back as the same solid."""
    out = cq.Workplane().add(shape)
    cq.exporters.export(out, str(stl_dir / f"{stem}.stl"), tolerance=0.05, angularTolerance=0.2)
    if step_dir is not None:
        cq.exporters.export(out, str(step_dir / f"{stem}.step"))
        back = cq.importers.importStep(str(step_dir / f"{stem}.step")).val()
        if not (BRepCheck_Analyzer(back.wrapped, True).IsValid()
                and abs(back.Volume() - shape.Volume()) < 1e-3 * shape.Volume()):
            raise SystemExit(f"STEP round trip failed for {stem}")


def mesh_checks(stl_path, bed, orient=None):
    """Closed STL, number of bodies, bbox on the bed and overhang area (> 45 deg) in the print orientation.
    orient = (axis 'X'|'Y'|'Z', degrees) applied before measuring; bed = (x, y, z)."""
    import math
    import trimesh
    m = trimesh.load(stl_path)
    res = {"watertight": bool(m.is_watertight), "bodies": len(m.split(only_watertight=False)),
           "vol_cm3": m.volume / 1000.0}
    if orient:
        ax, ang = orient
        vec = {"X": [1, 0, 0], "Y": [0, 1, 0], "Z": [0, 0, 1]}[ax]
        m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(ang), vec))
    ext = m.bounds[1] - m.bounds[0]
    res["bbox"] = tuple(float(e) for e in ext)
    res["fits_bed"] = bool(ext[0] <= bed[0] and ext[1] <= bed[1] and ext[2] <= bed[2])
    zmin = m.bounds[0][2]
    over = (m.face_normals[:, 2] < -0.7072) & (m.triangles_center[:, 2] > zmin + 0.3)
    res["overhang_mm2"] = float(m.area_faces[over].sum())
    return res


def min_thickness(stl_path, samples=1500, pct=1.0):
    """Wall thickness measured inward from a sample of face centres of the STL (ray to the opposite wall, plain
    numpy Moller-Trumbore: no rtree needed). Returns (pct-th percentile, min) in mm; compare the percentile with
    MIN_WALL (single rays grazing edges and fillets give spurious minima)."""
    import numpy as np
    import trimesh
    m = trimesh.load(stl_path)
    tri = m.triangles
    v0, e1, e2 = tri[:, 0], tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]
    rng = np.random.default_rng(0)
    idx = rng.choice(len(m.faces), size=min(samples, len(m.faces)), replace=False)
    out = []
    for i in idx:
        o = m.triangles_center[i] - m.face_normals[i] * 1e-4
        d = -m.face_normals[i]
        pv = np.cross(d, e2)
        det = np.einsum("ij,ij->i", e1, pv)
        ok = np.abs(det) > 1e-12
        inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
        tv = o - v0
        u = np.einsum("ij,ij->i", tv, pv) * inv
        qv = np.cross(tv, e1)
        v = (qv @ d) * inv
        t = np.einsum("ij,ij->i", e2, qv) * inv
        hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-3)
        hit[i] = False
        if hit.any():
            out.append(t[hit].min())
    out = np.array(out)
    return float(np.percentile(out, pct)), float(out.min())
