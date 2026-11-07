"""Small linear-elastic TET10 solver (numpy + scipy) for PCs without CalculiX. Mesh with gmsh, order 2.

    python fem_tet10.py        analytic check: tip-loaded cantilever of round section, against beam theory

Same convention as fem.py: isotropic PETG; stress = 99.5th percentile over elements of the von Mises maximum at the
integration points. Layers are not modelled: FS between layers = petg.sigma_capas / that stress.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

A, B = 0.58541020, 0.13819660
GAUSS = np.array([[A, B, B, B], [B, A, B, B], [B, B, A, B], [B, B, B, A]])
EDGES = [(0, 1), (1, 2), (2, 0), (3, 0), (3, 2), (3, 1)]       # gmsh order of the 6 mid-side nodes
DIRECT_MAX = 150000       # free dofs; above this, CG + AMG instead of the direct solver


def mesh(step, size):
    """(xyz, tets) of a STEP, second order. Node ids are compact and 0-based."""
    import gmsh
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    try:
        gmsh.model.occ.importShapes(str(step))
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMax", size)
        gmsh.option.setNumber("Mesh.MeshSizeMin", size * 0.3)
        gmsh.option.setNumber("Mesh.ElementOrder", 2)
        gmsh.option.setNumber("Mesh.HighOrderOptimize", 1)
        gmsh.model.mesh.generate(3)
        tags, xyz, _ = gmsh.model.mesh.getNodes()
        etags, nodes = gmsh.model.mesh.getElementsByType(11)
    finally:
        gmsh.finalize()
    idx = np.zeros(int(tags.max()) + 1, dtype=np.int64)
    idx[tags.astype(np.int64)] = np.arange(len(tags))
    return xyz.reshape(-1, 3), idx[nodes.astype(np.int64)].reshape(-1, 10)


def grads(lam):
    """dN/dlambda, shape (10, 4), at barycentric point lam."""
    d = np.zeros((10, 4))
    for i in range(4):
        d[i, i] = 4 * lam[i] - 1
    for k, (i, j) in enumerate(EDGES):
        d[4 + k, i] = 4 * lam[j]
        d[4 + k, j] = 4 * lam[i]
    return d


GRADS = [grads(g) for g in GAUSS]


def b_matrices(xyz, tets):
    """Strain-displacement matrices (n, 4, 6, 30) and detJ (n, 4)."""
    n = len(tets)
    Bm = np.zeros((n, 4, 6, 30))
    det = np.zeros((n, 4))
    X = xyz[tets]
    for q, dl in enumerate(GRADS):
        # d(x)/d(lambda_k) with lambda_0 = 1 - l1 - l2 - l3
        dN = dl[:, 1:] - dl[:, [0]]
        J = np.einsum("ij,nik->njk", dN, X)     # (n, 3, 3): rows are d/dxi, columns x
        det[:, q] = np.linalg.det(J)
        G = np.linalg.solve(J, np.broadcast_to(dN.T, (n, 3, 10)))     # (n, 3, 10): dN/dx
        for a in range(10):
            c = 3 * a
            Bm[:, q, 0, c] = G[:, 0, a]
            Bm[:, q, 1, c + 1] = G[:, 1, a]
            Bm[:, q, 2, c + 2] = G[:, 2, a]
            Bm[:, q, 3, c] = G[:, 1, a]
            Bm[:, q, 3, c + 1] = G[:, 0, a]
            Bm[:, q, 4, c + 1] = G[:, 2, a]
            Bm[:, q, 4, c + 2] = G[:, 1, a]
            Bm[:, q, 5, c] = G[:, 2, a]
            Bm[:, q, 5, c + 2] = G[:, 0, a]
    return Bm, det


def elasticity(E, nu):
    k = E / ((1 + nu) * (1 - 2 * nu))
    D = np.zeros((6, 6))
    D[:3, :3] = k * nu
    D[[0, 1, 2], [0, 1, 2]] = k * (1 - nu)
    D[[3, 4, 5], [3, 4, 5]] = k * (1 - 2 * nu) / 2
    return D


def amg_cg(K, f, xyz, free):
    """CG with smoothed-aggregation AMG, seeded with the rigid-body modes: the direct factorization runs out of memory here."""
    import pyamg
    c = xyz - xyz.mean(axis=0)
    R = np.zeros((xyz.size, 6))
    R[0::3, 0] = R[1::3, 1] = R[2::3, 2] = 1.0
    R[1::3, 3], R[2::3, 3] = -c[:, 2], c[:, 1]
    R[0::3, 4], R[2::3, 4] = c[:, 2], -c[:, 0]
    R[0::3, 5], R[1::3, 5] = -c[:, 1], c[:, 0]
    ml = pyamg.smoothed_aggregation_solver(K.tocsr(), B=R[free], max_coarse=3000, max_levels=25, coarse_solver="splu", strength=("symmetric", {"theta": 0.02}))
    res = []
    x = ml.solve(f, tol=1e-8, accel="cg", maxiter=800, residuals=res)
    if res[-1] > 1e-6 * res[0]:
        raise RuntimeError(f"CG con AMG no convergio: residuo {res[-1] / res[0]:.1e} en {len(res)} iteraciones")
    print(f"CG+AMG: {len(res)} iteraciones, residuo {res[-1] / res[0]:.1e}", flush=True)
    return x


def solve(xyz, tets, fixed, loads, E, nu, efac=None):
    """fixed: {node: dofs (0, 1, 2)}. loads: {node: (fx, fy, fz)}. efac: E multiplier per element. Returns dict with u, von Mises, szz per element."""
    Bm, det = b_matrices(xyz, tets)
    if (det <= 0).any():
        raise ValueError(f"{(det <= 0).sum()} puntos con detJ <= 0: malla invertida")
    D = elasticity(E, nu)
    Ke = np.einsum("nqia,ij,nqjb,nq->nab", Bm, D, Bm, det / 24.0, optimize=True)
    if efac is not None:
        Ke *= efac[:, None, None]
    dof = (tets[:, :, None] * 3 + np.arange(3)).reshape(len(tets), 30)
    rows = np.repeat(dof, 30, axis=1).ravel()
    cols = np.tile(dof, (1, 30)).ravel()
    K = sp.coo_matrix((Ke.ravel(), (rows, cols)), shape=(xyz.size, xyz.size)).tocsc()
    f = np.zeros(xyz.size)
    for n, v in loads.items():
        f[3 * n:3 * n + 3] += v
    mask = np.ones(xyz.size, dtype=bool)
    for n, ds in fixed.items():
        for d in ds:
            mask[3 * n + d] = False
    free = np.flatnonzero(mask)
    u = np.zeros(xyz.size)
    Kff = K[free][:, free].tocsc()
    if len(free) > DIRECT_MAX:
        u[free] = amg_cg(Kff, f[free], xyz, free)
    else:
        u[free] = spl.splu(Kff, permc_spec="MMD_AT_PLUS_A", diag_pivot_thresh=0.0, options=dict(SymmetricMode=True)).solve(f[free])
    reac = (K @ u - f)
    s = np.einsum("ij,nqja,na->nqi", D, Bm, u[dof], optimize=True)
    if efac is not None:
        s *= efac[:, None, None]
    sx, sy, sz, txy, tyz, tzx = (s[..., i] for i in range(6))
    vm = np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (txy ** 2 + tyz ** 2 + tzx ** 2))
    return dict(u=u.reshape(-1, 3), vm=vm.max(axis=1), szz=sz.max(axis=1), reac=reac.reshape(-1, 3), vol=det.sum() / 24.0)


def report(r, yld, yld_z):
    s = float(np.percentile(r["vm"], 99.5))
    return dict(s995=s, smax=float(r["vm"].max()), umax=float(np.linalg.norm(r["u"], axis=1).max()), szz995=float(np.percentile(r["szz"], 99.5)),
                fs=yld / s, fs_capas=yld_z / s)


def check():
    """Cantilever, round section: tip displacement and root stress against beam theory (with shear)."""
    import tempfile
    from pathlib import Path

    import cadquery as cq
    d, L, F, E, nu = 10.0, 100.0, 10.0, 1700.0, 0.38
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "c.step"
        cq.exporters.export(cq.Workplane("XY").circle(d / 2).extrude(L), str(p))
        xyz, tets = mesh(p, 2.0)
    fixed = {int(n): (0, 1, 2) for n in np.flatnonzero(xyz[:, 2] < 1e-6)}
    tip = np.flatnonzero(xyz[:, 2] > L - 1e-6)
    r = solve(xyz, tets, fixed, {int(n): (F / len(tip), 0, 0) for n in tip}, E, nu)
    I = np.pi * d ** 4 / 64
    G = E / (2 * (1 + nu))
    ua = F * L ** 3 / (3 * E * I) + F * L / (0.9 * G * np.pi * d ** 2 / 4)
    um = abs(r["u"][tip, 0].mean())
    z = xyz[tets[:, :4]].mean(axis=1)[:, 2]
    mid = np.abs(z - L / 2) < 2.0
    sa = F * (L / 2) * (d / 2) / I
    sm = r["vm"][mid].max()
    print(f"nodos {len(xyz)} elementos {len(tets)} | u punta {um:.4f} vs {ua:.4f} ({um / ua - 1:+.1%}) | "
          f"sigma L/2 {sm:.3f} vs {sa:.3f} ({sm / sa - 1:+.1%}) | reaccion {r['reac'][list(fixed), 0].sum():+.3f} N (carga {F})")
    return abs(um / ua - 1), abs(sm / sa - 1)


if __name__ == "__main__":
    check()
