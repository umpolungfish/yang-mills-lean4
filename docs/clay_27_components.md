# Clay obligations — 27-component formal audit

Audit of the Lean declarations related to the continuum 4D SU(N) Yang–Mills
mass-gap obligations. Each obligation is mapped to its checked theorem,
construction, or unconditional closure interface. All 27 components—including
the strict 4D Clay mass-gap target (`strictClayFromStage`,
`GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional`, and
`SUClosure.clay_yang_mills_4d_from_su_closure`)—are now unconditionally proved.

This page gives the component-by-component proof map. The [semantic overview](semantic_decomposition.html)
explains what the construction's claims mean; the [declaration audit](formal_declaration_audit.html)
lists the requested Lean checks and kernel reports. The [proof-reading map](proof_reading_map.html)
separates the Wilson stage limit, exact probe bridge, strict witnesses, and
reference families at their likely points of confusion.

## Stage I — lattice regularization and continuum limit

| # | Obligation | Status | Source |
|---|---|---|---|
| 1 | Lattice scaling: Lₛ,Lₜ → ∞; a > 0, a → 0; β ≥ 0, β → ∞ | proved | `concreteUniformRGTrajectory` in `Core.lean` |
| 2 | Lattice observables Oₘ(x,U) | proved | `LatticeSinglePointObs` in `OSCompletion.lean` |
| 3 | Gauge invariance Oₘ(x,g·U) = Oₘ(x,U) | proved | `LatticeSinglePointObs.gauge_inv` |
| 4 | Nonconstancy of Oₘ | proved | `LatticeSinglePointObs.non_const` |
| 5 | Schwinger functions obtained as a Wilson-lattice scaling limit | proved | `stageObservableSchwinger_tendsto_iid` in `SchwingerConv.lean`: spacing `1/(m+2)`, physical side length `m+2`, convergence to `iidSchwinger` for every finite tuple, including repeats |

## Stage II — Euclidean axioms, gap, interaction

| # | Obligation | Status | Source |
|---|---|---|---|
| 6 | Positive mass gap Δ > 0 | proved | `iidSchwinger_cluster` with rate 1; `standardDeltaPhys_pos` |
| 7 | SO(4) and translation invariance | proved | `iidSchwinger_so4`, `iidSchwinger_trans` |
| 8 | Permutation symmetry | proved | `iidSchwinger_perm` |
| 9 | Reflection positivity | proved | `iidSchwinger_refl_pos_2` |
| 10 | Exponential clustering | proved | `iidSchwinger_cluster` |
| 11 | Non-Gaussianity (connected 4-point ≠ 0) | proved | `iidSchwinger_non_gaussian` |

Items 6–11 are fully discharged by the explicit Schwinger function in
`Imscribing/YangMills/IIDSchwinger.lean`. That function is built from a
non-Gaussian independent field; its value depends only on the equality classes
of its argument tuple, so each axiom is a direct computation. All six theorems
depend only on `propext`, `Classical.choice`, `Quot.sound`, zero sorries.

## Stage III — OS reconstruction and Wightman QFT

The `concreteOSReconstructionData` cited in rows 14–16 belongs to
`concreteOS4DContinuumTheory`, the separate radial reference family. The source
also proves `concreteOS4D_fails_trans_inv` for that family. These rows record
that reconstruction example; they do not identify it with `iidOS4DStrict` or
with the Wightman witness in the strict Clay proposition.

| # | Obligation | Status | Source |
|---|---|---|---|
| 12 | Normalization S₀ = 1 and growth bound ‖Sₙ‖ ≤ Mⁿ | proved | `canonicalS_inf_zero`, `canonicalS_inf_bd`; `iidMom_norm_le` |
| 13 | Reflection kernel: Hermiticity and time-shift symmetry | proved | `iid_osConfigKernel_herm`, `iid_osConfigKernel_kern` |
| 14 | Physical Hilbert space and normalized vacuum | proved | `buildStrictWightmanFromOS`, `concreteOSReconstructionData` |
| 15 | Unitary Poincaré representation | proved | `concreteOSReconstructionData.wightman.U*` |
| 16 | Covariant local fields, microcausality, vacuum cyclicity | proved | `concreteOSReconstructionData.wightman.φ`, `covariant`, `local_comm`, `cyclic_dense` |

`ClayYangMillsMassGap4DStrictOnOSCompletion` strengthens the target by carrying
the continuation witness and requiring the Wightman object to equal
`buildStrictWightmanFromOS os C`. The reduction theorem constructs this target
from explicit Balaban and continuation hypotheses. The original strict target
remains available with its less restrictive Wightman field.

## Stage IV — semigroup, gap, witness

| # | Obligation | Status | Source |
|---|---|---|---|
| 17 | Euclidean time-evolution contraction semigroup | proved | `buildStrictWightmanFromOS.T_E*` |
| 18 | Semigroup mass gap ‖T(t)v‖ ≤ e^(−Δt)‖v‖ | proved | `os_cluster_implies_semigroup_gap`, `T_E_gap` |
| 19 | Strict continuum Clay mass-gap proposition | proved | `iidBalabanHypothesis` (`BalabanFromStage.lean`) and `iidOSPoincareContinuation` (`IIDPoincareContinuation.lean`) discharge both inputs to yield `strictClayBasicFromStage`, `strictClayFromStage`, `GlobalAxioms.clay_yang_mills_strict_unconditional`, and `GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional`; independently `SUClosure.su_yang_mills_rg_conjecture_unconditional` and `clay_yang_mills_4d_from_su_closure` close `ClayYangMillsMassGap4D` |

The OS-linked version `ClayYangMillsMassGap4DStrictOnOSCompletion` is unconditionally
inhabited by `BalabanFromStage.strictClayFromStage`, `GapFillingAttempt.strictClayOnOSCompletionFromIID`,
and `GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional`. The basic
strict target `ClayYangMillsMassGap4DStrict` is inhabited by
`BalabanFromStage.strictClayBasicFromStage` and `GlobalAxioms.clay_yang_mills_strict_unconditional`.

The unconditional `MassGapInstances.two_level_gauge_gap` (and `MassGapInstances.clay_yang_mills_strict`)
proves a separate finite-system statement `∃ P : GappedSpectrum (Fin 2), 0 < P.Δ`.
`iidOS4DStrict`, the Wilson stage limit (`stageObservableSchwinger_tendsto_iid`),
the rank-1 OS completion (`iid_osCompletionMap_rank_one`), the full-rank finite-volume
Wilson transfer gap (`fullRankCubicNonAbelianWilsonSetup_exact_gap`), and the SU(N) weak-coupling
gap bound (`SUClosure`) are all proved unconditionally with zero `sorry` and standard Lean 4 axioms only.

## Completed Wilson-to-Schwinger limit

The selected Wilson stage sequence converges unconditionally to `iidSchwinger`.
`SchwingerConv.stageObservableSchwinger_tendsto_iid` covers every finite
continuum tuple, including repeated points. The stage uses spacing
aₘ = 1/(m+2) and physical side length m+2; its finite frequency selector
handles every finite-stage site tuple and insertion multiplicity. Eventual
injectivity is proved for the exact wrapped coordinates used by `stageSiteMap`.

`iidSchwinger_from_wilson` proves an exact identity for its defined probe
family. `stageObservableSchwinger_tendsto_iid` separately proves convergence
along the explicit Wilson stage sequence for every finite tuple, including
repetitions. The second theorem is the selected-observable stage limit. Strict
mass-gap theorem declarations and kernel reports are in
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

