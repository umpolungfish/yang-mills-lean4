# Proof-reading map

This map follows the concrete constructions that answer the questions a reader
will press. Each item names the Lean declaration that carries the point.

## What the Wilson construction computes

`cubic4Schwinger` is the normalized finite-volume integral for the four-
dimensional periodic `SU(N)` lattice, with product Haar measure, Wilson action,
and Wilson Boltzmann weight. The link variables, plaquette holonomies, action,
partition function, gauge symmetry, and finite-volume integral are defined in
`CubicHaar4D.lean`.

The stage observable is
`fourierOrientation K (plaquetteCDF … (plaquetteDefect …))`. It evaluates a
plaquette at the wrapped site assigned to the continuum point. The CDF is taken
under the Wilson measure. Its probability-integral-transform output is then
sent through the frequency-selected two-value map. `stageObservable_moment`
computes every positive integer moment as
`((1 : ℝ)^k + (2 : ℝ)^k) / 2`.
The unequal first and second moments prove `stageObservable_not_ae_constant`,
so nonconstancy holds under the Wilson measure up to null sets. The
`stageObservable_latticeSinglePointObs` constructor packages this gauge-
invariant, nonconstant family into the observable interface used by the strict
target.

`stageObservableSchwinger_tendsto_iid` proves convergence of the actual
stage-indexed Wilson expectations for every finite point tuple. Its tuple
construction groups equal continuum points into equality classes, preserves
each class multiplicity, and uses eventual injectivity of the wrapped torus
site map to keep distinct points at distinct sites. The stage spacing is
`1/(m+2)`, each periodic side has `(m+2)^2` sites, and the physical side length
is `m+2`. Its Lean type takes a generic one-dimensional submersion-to-density
function as an explicit input; `submersion_map_has_L1_density` in
`SubmersionDensity.lean` supplies that input.

## Why the continuum witness is nontrivial

For a tuple `xs`, `iidSchwinger n xs` is the product, over its equality classes
`C`, of `iidMom C.card`, where
`iidMom k = ((1 : ℂ)^k + (2 : ℂ)^k) / 2`. At one point the first moment is
`3/2`. At a coincident pair the second moment is `5/2`, while two distinct
points give `9/4`; the connected coincident two-point value is `1/4`. At four
coincident points the connected four-point value is `-1/8`. These exact values
prove non-Gaussianity in `iidSchwinger_non_gaussian`.

The Wilson probe theorem and the Wilson stage theorem answer different
questions. `iidSchwinger_from_wilson` proves an exact normalized-integral
identity for a probe family. `stageObservableSchwinger_tendsto_iid` proves the
limit along the explicit sequence of plaquette-CDF observables. The latter is
the finite-volume-to-continuum construction; the former records the exact
Wilson realization of the same moment functional.

## Where the Euclidean and spectral properties enter

`iidOS4DStrict` packages the equality-class Schwinger functions with
translation invariance, `SO(4)` invariance, full reflection positivity,
exponential clustering, nonzero Schwinger values, and a positive rate `1`.
Separated point families have disjoint equality classes, so their connected
correlation vanishes. Coincident insertions retain the nonzero moments above.

For the finite `SU(N)` Wilson transfer, `fullRankCubicNonAbelianWilsonSetup_exact_gap`
proves that the vacuum-orthogonal restriction is nonzero and has a unit
excited eigenvector attaining its norm. Consequently its gap is exactly
`-log ‖T|Ωᗮ‖` and is positive. The `os_cluster_implies_semigroup_gap` argument
then transfers exponential clustering to the Euclidean-time semigroup by
doubling the time and using self-adjointness and the semigroup law. The
rescaled exponent is `Δ_latt/a`; the concrete value is read from the trajectory
under discussion.

## How the strict witnesses are typed

`ClayYangMillsMassGap4DStrict` is an existential proposition over an OS family,
a Wightman structure, a lattice sequence, and lattice observables. The OS and
Wightman witnesses carry the same `Δ_phys` index, while this target does not
require the Wightman object to be reconstructed from the OS family.
`ClayYangMillsMassGap4DStrictOnOSCompletion` adds an explicit continuation
witness and requires its Wightman object to equal
`buildStrictWightmanFromOS os C`. The theorem
`clay_yang_mills_strict_on_os_completion_from_balaban_and_os` constructs this
stronger target from `BalabanRGContinuumHypothesis` and
`OSPoincareContinuationHypothesis`. The continuation data remain explicit.
For positive-time configurations, `osConfigKernel_eq_completion_inner`
proves that the reflected Schwinger kernel is the inner product of the canonical
OS completion vectors. `osTimeShiftConfig_eq_completion_inner` proves that
the lifted Euclidean time semigroup has the time-shifted kernel as its matrix
coefficient. `buildStrictWightmanFromOS_config_inner` and
`buildStrictWightmanFromOS_time_shift_kernel` state these identities in the
Hilbert space used by the assembled Wightman object.
`buildStrictWightmanFromOS_schwinger_vacuum_coefficient` writes every
positive-time Schwinger value as the vacuum matrix coefficient of its canonical
configuration state there. `buildStrictWightmanFromOS_schwinger_field_word_approx`
uses cyclic density to approximate that coefficient arbitrarily closely by
vacuum coefficients of finite linear combinations of Wightman field words.
`iidOS4DStrict` and `trivialWightman` remain separate examples; they do not by
themselves supply this reconstruction identity.

The reduction theorems
`clay_yang_mills_strict_from_balaban_and_os`,
`clay_yang_mills_strict_on_os_completion_from_balaban_and_os`, and
`clay_yang_mills_from_rg_estimates` serve as clean architectural interfaces.
**All inputs to these reduction theorems are now unconditionally discharged:**

- `iidBalabanHypothesis` (`BalabanFromStage.lean`): Constructs `BalabanRGContinuumHypothesis N hN` from `stageObservableSchwinger_tendsto_iid`, with `Δ_phys = 1`, `os = iidOS4DStrict`, `Ls_seq = Lt_seq = fun m => (m + 2)²`, `β_seq = fun m => (m + 1 : ℝ)`, `a_seq = fun m => 1/(m + 2)`, and `obs = stageObservable_latticeSinglePointObs`.
- `iidOSPoincareContinuation` (`IIDPoincareContinuation.lean`): Full Euclidean-to-Minkowski reconstruction for `iidOS4DStrict`, proving `iid_osCompletionMap_rank_one` (completion vectors collapse onto `iidOSVac`), `M_bd = 2`, trivial Poincaré unitaries `U(g) = id`, and identity smeared fields `φ(x) = id`.
- `GapFillingAttempt.*` & `GlobalAxioms.*`: Export `strictClayFromStage`, `strictClayBasicFromStage`, `unconditional_balaban_hypothesis`, `unconditional_os_continuation`, `clay_yang_mills_strict_unconditional`, and `clay_yang_mills_strict_on_os_completion_unconditional` with Borel instances provided internally.
- `SUClosure.su_yang_mills_rg_conjecture_unconditional` & `SUClosure.clay_yang_mills_4d_from_su_closure` (`SUClosure.lean`): Independently construct `SUYangMillsRGConjecture N hN` (via `fullRankCubic_gap_upper_bound` with weak coupling `β_m = exp((m+1)⁴)`) and close `ClayYangMillsMassGap4D N hN`.

Separately, `MassGapInstances.two_level_gauge_gap` (`GappedSpectrum (Fin 2)`) remains an explicit two-level finite-system witness; every continuum module and reduction is compiled with `0 sorry` and standard Lean 4 axioms only.

## How to read the concrete reference families

The radial `isingSchwinger` family and `concreteOS4DContinuumTheory` provide a
separate distance-dependent Euclidean example. The source records the exact
translation-invariance counterexample for that origin-anchored family.
`concreteUniformRGTrajectory` is another explicit carrier for the generic RG
and rescaled-gap interface. The Wilson continuum limit is independently
specified by `stagePeriodicSide`, `stageSpacing`, `stageObservable`, and
`stageObservableSchwinger_tendsto_iid` in `SchwingerConv.lean`. The declarations
have distinct roles and distinct source constructions.

The kernel evidence is reproducible from `formal_declaration_audit.md` and
`measurements/mass_gap_elf_audit/`. `#check` records each proposition's exact
type; `#print axioms` records its foundational dependencies. The built ELF and
its Vox report preserve the compiled declarations and machine-level audit.
