# Clay construction — 27-component audit

Audit of the two-stage construction of a continuum 4D SU(N) Yang–Mills theory
with strictly positive mass gap. Each obligation is mapped to the Lean theorem
that discharges it, or to the hypothesis that still carries it.

## Stage I — lattice regularization and continuum limit

| # | Obligation | Status | Source |
|---|---|---|---|
| 1 | Lattice scaling $L_s,L_t\to\infty$, $a>0$, $a\to0$, $\beta\ge0$, $\beta\to\infty$ | available per RG trajectory | `concreteUniformRGTrajectory` in `Core.lean` |
| 2 | Lattice observables $O_m(x,U)$ | available | `LatticeSinglePointObs` in `OSCompletion.lean` |
| 3 | Gauge invariance $O_m(x,g\cdot U)=O_m(x,U)$ | proved | `LatticeSinglePointObs.gauge_inv` |
| 4 | Nonconstancy of $O_m$ | proved | `LatticeSinglePointObs.non_const` |
| 5 | Schwinger functions obtained as the Wilson-lattice scaling limit | hypothesis | `BalabanRGContinuumHypothesis.schwinger_conv` — the continuum limit of Wilson expectations is the open RG estimate |

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
| 13 | Reflection kernel: Hermiticity and time-shift symmetry | hypothesis | `OSPoincareContinuationHypothesis.h_herm`, `h_kern` |
| 14 | Physical Hilbert space and normalized vacuum | proved downstream of B/C | `buildStrictWightmanFromOS` |
| 15 | Unitary Poincaré representation | hypothesis | `OSPoincareContinuationHypothesis.U*` |
| 16 | Covariant local fields, microcausality, vacuum cyclicity | hypothesis | `OSPoincareContinuationHypothesis.φ`, `covariant`, `local_comm`, `cyclic_dense` |

## Stage IV — semigroup, gap, witness

| # | Obligation | Status | Source |
|---|---|---|---|
| 17 | Euclidean time-evolution contraction semigroup | proved downstream of B/C | `buildStrictWightmanFromOS.T_E*` |
| 18 | Semigroup mass gap $\|T(t)v\|\le e^{-\Delta t}\|v\|$ | proved downstream of B/C | `os_cluster_implies_semigroup_gap` via `T_E_gap` |
| 19 | Continuum Yang–Mills mass-gap witness | reduction | `clay_yang_mills_strict_from_balaban_and_os : ClayYangMillsMassGap4DStrict` |

## Boundary

Stage II is complete unconditionally in `IIDSchwinger.lean`. Stages I, III,
and IV are wired into the reduction theorem `clay_yang_mills_strict_from_balaban_and_os`,
which still takes `BalabanRGContinuumHypothesis` (B) and
`OSPoincareContinuationHypothesis` (C) as explicit arguments. Item 5 is the
hard analytic core: the Wilson-lattice scaling limit with $\beta\to\infty$,
$a\to0$. It is stored in the corpus as the open `SUYangMillsRGConjecture`.
Nothing here asserts it without a proof.

## Analytic rungs for item 5 (the Wilson scaling limit)

Item 5 is the hard analytic core and remains a hypothesis.  The following
rungs are proved unconditionally in Lean and supply the ingredients one would
assemble to attack it; they do **not** by themselves establish item 5.

| Rung | Theorem | File |
|---|---|---|
| 1 — multi-dimensional Rademacher annihilation | `radI_multidim` (Stone–Weierstrass + Fubini) | `RademacherMulti.lean` |
| 2 — probability integral transform | `map_cdf_eq_uniform_Ioc` | `ProbIntegralTransform.lean` |
| 3 — SU(N) topological group, compactness, Haar probability | `sunHaar`, `sun_compactSpace`, `sun_isTopologicalGroup` | `SUNHaar.lean` |
| 4 — submersion ⇒ L¹ density | `submersion_map_has_L1_density` (Jacobian + Radon–Nikodym) | `SubmersionDensity.lean` |
| Fubini splitting of `Measure.pi` | `integral_pi_split_at` | `PiFubini.lean` |

All of these depend only on `propext`, `Classical.choice`, `Quot.sound`, with
zero sorries.  The Wilson expectation itself is concrete — Haar measure on the
gauge group times the Boltzmann weight, normalized by the partition function
(`cubic4Schwinger` in `CubicHaar4D.lean`), with no `wilsonExpect` axiom.

`iidSchwinger_from_wilson` (`IIDSchwingerFromWilson.lean`) is the conditional
bridge: **if** the concrete Wilson Schwinger functions converge to
`iidSchwinger` (item 5), **then** the Wilson limit object
`wilsonLimitSchwinger` carries all six Euclidean axioms. The limit hypothesis is
used essentially — `wilsonLimitSchwinger` is defined as the `lim` of the Wilson
expectations and the hypothesis identifies it with `iidSchwinger` by uniqueness
of limits. `wilson_limit_glut` records that two different observation families
with the same limit hypothesis determine the same continuum object: a glut of
equivalent derivations of one theory. The convergence hypothesis itself is the
open analytic content and is not discharged here.

