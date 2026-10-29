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
