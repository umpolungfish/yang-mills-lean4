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
Wightman witnesses carry the same `Δ_phys` index. The declared fields do not
require a constructor equating the Wightman object with an OS reconstruction.
`iidOS4DStrict` supplies the strict OS family at rate `1`; `trivialWightman`
supplies a `WightmanQFT4DStrict 1`. `buildStrictWightmanFromOS` is the separate
reconstruction route when the Poincaré continuation data are supplied.

The conditional declarations
`clay_yang_mills_strict_from_balaban_and_os` and
`clay_yang_mills_from_rg_estimates` are reusable reduction interfaces with
their displayed inputs. In `GlobalAxioms.lean`, the strict theorem alias takes
both `BalabanRGContinuumHypothesis` and `OSPoincareContinuationHypothesis`.
The unconditional `MassGapInstances.clay_yang_mills_strict` has the distinct
type `∃ P : GappedSpectrum (Fin 2), 0 < P.Δ`; it does not inhabit
`ClayYangMillsMassGap4DStrict`. The OS family, Wightman structure, Wilson
stage limit, and finite-volume transfer gap each have unconditional
declarations in their respective modules. These pieces do not by themselves
provide the two hypotheses required by the strict Clay reduction.

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
