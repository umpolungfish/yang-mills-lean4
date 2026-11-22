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
