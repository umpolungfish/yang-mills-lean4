# Semantic overview — 4D Yang–Mills construction

This page explains what the claims in the [27-component Clay audit](clay_27_components.html)
mean mathematically. The [formal declaration audit](formal_declaration_audit.html)
lists the Lean types and kernel axiom reports.

## Lattice theory and scaling limit

The lattice stages are finite-volume SU(N) gauge theories with Wilson action
and Haar measure. A stage index determines the lattice sizes, coupling, and
spacing. The concrete trajectory sends the physical volume to infinity while
the spacing tends to zero and the coupling grows. Gauge-invariant, nonconstant
observables are evaluated on this sequence.

`stageObservableSchwinger_tendsto_iid` gives the meaning of the full-tuple
limit: for every finite tuple of continuum points, the Wilson Schwinger
expectation converges to `iidSchwinger`. The points may repeat. At stage `m`,
the spacing is `1/(m+2)` and the physical side length is `m+2`. Equal continuum
points are grouped at their shared lattice sites, so repeated insertions retain
their multiplicity in the moment.

There are two distinct Wilson results. `iidSchwinger_from_wilson` gives an
exact finite-volume identity for a specially defined probe family. The
finite-volume-to-continuum result is
`stageObservableSchwinger_tendsto_iid`: it proves convergence of the selected
plaquette-CDF observables along the explicit stage sequence for every finite
tuple, including repeated points. The proof-reading map gives the constructions
and declarations side by side. The theorem's type takes a generic
submersion-to-density result as an explicit argument, supplied by
`submersion_map_has_L1_density` in `SubmersionDensity.lean`.

## Euclidean Schwinger properties

`iidSchwinger` assigns a complex number to each finite point tuple. Its six
proved properties describe the structure expected of Euclidean correlation
functions:

| Claim | Mathematical meaning |
|---|---|
| Translation invariance | Moving every insertion by the same vector leaves the correlation unchanged. |
| SO(4) invariance | Rotating all insertion points leaves the correlation unchanged. |
| Permutation symmetry | Reordering insertions does not change the correlation. |
| Reflection positivity | Reflected test configurations define a nonnegative quadratic form, which supplies the physical inner product. |
| Exponential clustering | Widely separated groups of insertions become independent at an exponential rate. |
| Non-Gaussianity | The connected four-point function is nonzero, so the field has interactions beyond Gaussian moments. |

These claims are proved directly for `iidSchwinger`. The exact Wilson probe
bridge transfers them to its probe family, and the full-tuple stage theorem
identifies the limit of the selected Wilson observables with the same
`iidSchwinger` functional. Their Lean declarations are listed in the formal
audit.

## OS reconstruction and Wightman structure

The target `ClayYangMillsMassGap4DStrict` contains an OS structure and a
Wightman structure indexed by the same positive `Δ_phys`. Its fields also
require non-Gaussianity of the OS family and convergence of the Wilson lattice
Schwinger functions to that family. `ClayYangMillsMassGap4DStrictOnOSCompletion`
strengthens this interface with an explicit OS continuation witness and an
equality requiring the Wightman witness to be the result of
`buildStrictWightmanFromOS`. The corresponding reduction theorem constructs
that stronger target from the Balaban and continuation hypotheses. See the
proof-reading map for the exact declaration locations.

Osterwalder–Schrader data turn reflection-positive Euclidean correlations into
a Hilbert space with a normalized vacuum. A Wightman structure adds the
Poincaré action and local fields. Covariance means that the fields transform
with the spacetime symmetry; locality means spacelike-separated fields
commute; vacuum cyclicity means field insertions generate a dense set of
physical states.

When the OS-to-Wightman continuation hypotheses are supplied, the semigroup
`T(t)` describes Euclidean-time evolution on the reconstructed space. Its gap bound
`‖T(t)v‖ ≤ exp(−Δt)‖v‖` for vacuum-orthogonal states says that excited states
decay exponentially in Euclidean time. Exponential clustering is the
corresponding statement for correlations. The positive value `Δ` is the
mass gap of that reconstructed theory.

At the kernel level, `osConfigKernel_eq_completion_inner` identifies the
reflected Schwinger value for any two positive-time configurations with the
inner product of their canonical vectors in the OS Hilbert completion.
`osTimeShiftConfig_eq_completion_inner` identifies the matrix coefficient of
the lifted Euclidean time semigroup with the kernel after shifting the first
configuration in Euclidean time.
`buildStrictWightmanFromOS_config_inner` gives the same identity using the
Hilbert space field of the assembled Wightman object, while
`buildStrictWightmanFromOS_time_shift_kernel` gives the semigroup matrix
coefficient there. `buildStrictWightmanFromOS_schwinger_vacuum_coefficient`
then identifies every positive-time Schwinger value with the vacuum matrix
coefficient of its canonical configuration state in that same space. This
makes the OS kernel, its Euclidean transfer evolution, and its vacuum
coefficients explicit inside the reconstructed state space.

## Uniform RG and the mass-gap witness

`concreteUniformRGTrajectory N hN` supplies the generic uniform RG and
rescaled-gap interface. Separately, the full-rank finite-volume Wilson transfer
has an exact positive spectral gap, proved by
`fullRankCubicNonAbelianWilsonSetup_exact_gap`. The Wilson-limit functional
also has a rate-one cluster estimate, and
`os_cluster_implies_semigroup_gap` derives the corresponding semigroup bound
on its OS completion. These are distinct gap arguments carried by different
objects. The declaration audit and proof-reading map identify their types and
source files.

The complete target proposition is `ClayYangMillsMassGap4DStrict`. Its current
strict theorem is a conditional reducer whose inputs are
`BalabanRGContinuumHypothesis` and `OSPoincareContinuationHypothesis`. The
unconditional theorem named `MassGapInstances.clay_yang_mills_strict` proves a
separate finite-system gap on `Fin 2`. These types answer the common question
whether the component witnesses already form an unconditional strict Clay
witness: the OS, Wightman, stage-limit, and transfer-gap declarations are
present, while the reducer inputs remain explicit.

The radial `isingSchwinger` family and `concreteOS4DContinuumTheory` are a
separate distance-dependent Euclidean example. The source also proves the
translation-invariance counterexample for that origin-anchored family. It is
not the equality-class Wilson stage limit. `concreteUniformRGTrajectory` is a
generic trajectory carrier with its own role; the Wilson limit is specified by
`stageObservableSchwinger_tendsto_iid` in `SchwingerConv.lean`.
