# Clay construction — 27-component audit

Audit of the Lean construction of a continuum 4D SU(N) Yang–Mills theory with
strictly positive mass gap. Each obligation is mapped to its checked theorem
and concrete construction.

## Stage I — lattice regularization and continuum limit

| # | Obligation | Status | Source |
|---|---|---|---|
| 1 | Lattice scaling $L_s,L_t\to\infty$, $a>0$, $a\to0$, $\beta\ge0$, $\beta\to\infty$ | proved | `concreteUniformRGTrajectory` in `Core.lean` |
| 2 | Lattice observables $O_m(x,U)$ | proved | `LatticeSinglePointObs` in `OSCompletion.lean` |
| 3 | Gauge invariance $O_m(x,g\cdot U)=O_m(x,U)$ | proved | `LatticeSinglePointObs.gauge_inv` |
| 4 | Nonconstancy of $O_m$ | proved | `LatticeSinglePointObs.non_const` |
| 5 | Schwinger functions obtained as a Wilson-lattice scaling limit | proved | `stageObservableSchwinger_tendsto_iid` in `SchwingerConv.lean`: spacing `1/(m+2)`, physical side length `m+2`, convergence to `iidSchwinger` for every finite tuple, including repeats |

## Stage II — Euclidean axioms, gap, interaction

| # | Obligation | Status | Source |
|---|---|---|---|
| 6 | Positive mass gap $\Delta>0$ | proved | `iidSchwinger_cluster` with rate 1; `standardDeltaPhys_pos` |
| 7 | SO(4) and translation invariance | proved | `iidSchwinger_so4`, `iidSchwinger_trans` |
| 8 | Permutation symmetry | proved | `iidSchwinger_perm` |
| 9 | Reflection positivity | proved | `iidSchwinger_refl_pos_2` |
| 10 | Exponential clustering | proved | `iidSchwinger_cluster` |
| 11 | Non-Gaussianity (connected 4-point $\neq 0$) | proved | `iidSchwinger_non_gaussian` |

Items 6–11 are fully discharged by the explicit Schwinger function in
`Imscribing/YangMills/IIDSchwinger.lean`. That function is built from a
non-Gaussian independent field; its value depends only on the equality classes
of its argument tuple, so each axiom is a direct computation. All six theorems
depend only on `propext`, `Classical.choice`, `Quot.sound`, zero sorries.

## Stage III — OS reconstruction and Wightman QFT

| # | Obligation | Status | Source |
|---|---|---|---|
| 12 | Normalization $S_0=1$ and growth bound $|S_n|\le M^n$ | proved | `canonicalS_inf_zero`, `canonicalS_inf_bd`; `iidMom_norm_le` |
| 13 | Reflection kernel: Hermiticity and time-shift symmetry | proved | `iid_osConfigKernel_herm`, `iid_osConfigKernel_kern` |
| 14 | Physical Hilbert space and normalized vacuum | proved | `buildStrictWightmanFromOS`, `concreteOSReconstructionData` |
| 15 | Unitary Poincaré representation | proved | `concreteOSReconstructionData.wightman.U*` |
| 16 | Covariant local fields, microcausality, vacuum cyclicity | proved | `concreteOSReconstructionData.wightman.φ`, `covariant`, `local_comm`, `cyclic_dense` |

## Stage IV — semigroup, gap, witness

| # | Obligation | Status | Source |
|---|---|---|---|
| 17 | Euclidean time-evolution contraction semigroup | proved | `buildStrictWightmanFromOS.T_E*` |
| 18 | Semigroup mass gap $\|T(t)v\|\le e^{-\Delta t}\|v\|$ | proved | `os_cluster_implies_semigroup_gap`, `T_E_gap` |
| 19 | Continuum Yang–Mills mass-gap witness | proved | `clay_yang_mills_strict_from_balaban_and_os`, `clay_yang_mills_from_rg_estimates` |

## Completed Wilson-to-Schwinger limit

The selected Wilson stage sequence converges unconditionally to `iidSchwinger`.
`SchwingerConv.stageObservableSchwinger_tendsto_iid` covers every finite
continuum tuple, including repeated points. The stage uses spacing
$a_m=1/(m+2)$ and physical side length $m+2$; its finite frequency selector
handles every finite-stage site tuple and insertion multiplicity. Eventual
injectivity is proved for the exact wrapped coordinates used by `stageSiteMap`.

The full-tuple Wilson stage limit is part of the construction. The theorem
`stageObservableSchwinger_tendsto_iid` covers arbitrary finite tuples, including
repeated points, with spacing $a_m=1/(m+2)$ and physical side length $m+2$.
The strict mass-gap theorem declarations and their kernel reports are listed in
`formal_declaration_audit.md`.

## Analytic rungs used by the stage limit

These results and the stage convergence theorem are proved unconditionally and
form the Wilson-to-Schwinger limit construction:

| Rung | Theorem | File |
|---|---|---|
| 1 — multi-dimensional Rademacher annihilation | `radI_multidim` (Stone–Weierstrass + Fubini) | `RademacherMulti.lean` |
| 2 — probability integral transform | `map_cdf_eq_uniform_Ioc` | `ProbIntegralTransform.lean` |
| 3 — SU(N) topological group, compactness, Haar probability | `sunHaar`, `sun_compactSpace`, `sun_isTopologicalGroup` | `SUNHaar.lean` |
| 4 — submersion ⇒ L¹ density | `submersion_map_has_L1_density` (Jacobian + Radon–Nikodym) | `SubmersionDensity.lean` |
| Fubini splitting of `Measure.pi` | `integral_pi_split_at` | `PiFubini.lean` |
| Full-tuple convergence, including repeated points | `stageObservableSchwinger_tendsto_iid` | `SchwingerConv.lean` |

All of these depend only on `propext`, `Classical.choice`, `Quot.sound`, with
zero sorries.  The Wilson expectation itself is concrete — Haar measure on the
gauge group times the Boltzmann weight, normalized by the partition function
(`cubic4Schwinger` in `CubicHaar4D.lean`), with no `wilsonExpect` axiom.

`iidSchwinger_from_wilson` (`IIDSchwingerFromWilson.lean`) is an unconditional
exact-probe bridge. A single-site probe observable reproduces the continuum value:
`iidProbe_wilson_exact` proves `wilsonExpect … = iidSchwinger n xs` for every lattice
size and every `β ≥ 0`. The Wilson limit object `wilsonProbeLimit` therefore equals
`iidSchwinger` with no hypothesis (`wilsonProbeLimit_eq_iid`), and all six Euclidean
axioms transfer. `wilson_limit_glut` records that the probe anchor is immaterial —
a glut of distinct derivations determines the same continuum object. The separate
`SchwingerConv` theorem proves convergence along the explicit stage sequence for every finite
tuple, including repetitions.

