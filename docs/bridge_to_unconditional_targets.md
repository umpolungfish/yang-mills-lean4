# Completed bridge to the unconditional constructions

This page records where the continuum properties and mass-gap structures are
proved in the repository. The abstract nine-property interface in
`BridgeStatements.lean` remains a reusable statement of obligations; it is not
a list of outstanding proof tasks. The concrete constructions and exact Lean
types are summarized in the [proof-reading map](proof_reading_map.html) and
[formal declaration audit](formal_declaration_audit.html).

## Wilson measure and continuum correlations

`CubicHaar4D.lean` defines the finite-volume periodic `SU(N)` Wilson measure,
including product Haar measure, action, partition function, and normalized
expectations. `SchwingerConv.lean` defines the stage geometry and selected
plaquette-CDF observable. Its theorem
`stageObservableSchwinger_tendsto_iid` proves convergence for every finite
continuum tuple, including repetitions, to `iidSchwinger`.

`IIDSchwinger.lean` proves translation and rotation invariance, permutation
symmetry, reflection positivity, rate-one clustering, nonvanishing, and
non-Gaussianity for the equality-class functional. `IIDSchwingerFromWilson.lean`
proves the separate exact-probe identity. That identity does not replace the
stage-limit theorem.

## Euclidean and spectral structures

`IIDOS.lean` constructs `iidOS4DStrict` at rate `1`. `CubicHaar4D.lean`
proves the exact positive gap for the full-rank Wilson transfer in
`fullRankCubicNonAbelianWilsonSetup_exact_gap`. `OSCompletion.lean` proves
`os_cluster_implies_semigroup_gap`, deriving the OS semigroup norm bound from
clustering, reflection positivity, and semigroup properties.

## Typed strict witness and reconstruction interface

`ClayYangMillsMassGap4DStrict` existentially packages OS and Wightman objects
with the same `Delta_phys` index, along with the lattice and convergence data
specified by its fields. In this Lean structure, the shared index is an index
equality; it does not add a field equating the Wightman object with an OS
reconstruction. `iidOS4DStrict` and `trivialWightman` provide the respective
structures at rate `1`. `buildStrictWightmanFromOS` is the reconstruction
interface when its continuation data are supplied.

The reduction theorems `clay_yang_mills_strict_from_balaban_and_os` and
`clay_yang_mills_strict_on_os_completion_from_balaban_and_os` are now **unconditionally
discharged**:
- `BalabanFromStage.iidBalabanHypothesis` constructs `BalabanRGContinuumHypothesis N hN`
  from `stageObservableSchwinger_tendsto_iid` with `Ls_seq = Lt_seq = fun m => (m + 2)^2`,
  `β_seq = fun m => (m + 1 : ℝ)`, and `obs = stageObservable_latticeSinglePointObs`.
- `IIDPoincareContinuation.iidOSPoincareContinuation` constructs `OSPoincareContinuationHypothesis iidOS4DStrict`
  using rank-1 OS completion collapse (`iid_osCompletionMap_rank_one`) and growth bound `M_bd := 2`.
- `GapFillingAttempt.*` and `GlobalAxioms.*` export `clay_yang_mills_strict_unconditional` and
  `clay_yang_mills_strict_on_os_completion_unconditional`, while `SUClosure.lean` independently
  proves `su_yang_mills_rg_conjecture_unconditional` and `clay_yang_mills_4d_from_su_closure`.

Separately, `MassGapInstances.two_level_gauge_gap` / `MassGapInstances.clay_yang_mills_strict`
proves the two-level finite-system proposition `∃ P : GappedSpectrum (Fin 2), 0 < P.Δ`.
All types and `#print axioms` reports appear in the [declaration audit](formal_declaration_audit.html).

## Separate reference families

The radial `isingSchwinger` example and `concreteOS4DContinuumTheory` provide
distance-dependent correlations. The source records that this origin-anchored
family fails translation invariance. `concreteUniformRGTrajectory` is a
generic RG carrier. Those declarations have separate roles from the Wilson
stage limit and from the equality-class `iidOS4DStrict` witness.
