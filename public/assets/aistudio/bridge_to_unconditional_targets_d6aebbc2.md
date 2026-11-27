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

The declaration `clay_yang_mills_strict_from_balaban_and_os` takes explicit
`BalabanRGContinuumHypothesis` and `OSPoincareContinuationHypothesis` inputs.
The RG reducer also has an explicit conjecture input. The repository's
unconditional `MassGapInstances.clay_yang_mills_strict` proves
`∃ P : GappedSpectrum (Fin 2), 0 < P.Δ`, a separate finite-system proposition.
The unconditional OS family, Wightman structure, stage limit, and Wilson
transfer-gap results are proved components. Their separate declarations do
not construct either input to the strict Clay reduction. The precise types and
kernel reports are in the [declaration audit](formal_declaration_audit.html).

## Separate reference families

The radial `isingSchwinger` example and `concreteOS4DContinuumTheory` provide
distance-dependent correlations. The source records that this origin-anchored
family fails translation invariance. `concreteUniformRGTrajectory` is a
generic RG carrier. Those declarations have separate roles from the Wilson
stage limit and from the equality-class `iidOS4DStrict` witness.
