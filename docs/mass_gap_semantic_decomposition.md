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

The same limit is viewed from a single-site probe by
`iidSchwinger_from_wilson`. That probe has the exact continuum expectation at
every lattice size and every nonnegative coupling. The full-tuple stage theorem
states convergence for the selected Wilson observables along the explicit
stage sequence.

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

These claims are proved directly for `iidSchwinger` and transferred through the
Wilson probe bridge. Their Lean declarations are listed in the formal audit.

## OS reconstruction and Wightman structure

Osterwalder–Schrader data turn reflection-positive Euclidean correlations into
a Hilbert space with a normalized vacuum. A Wightman structure adds the
Poincaré action and local fields. Covariance means that the fields transform
with the spacetime symmetry; locality means spacelike-separated fields
commute; vacuum cyclicity means field insertions generate a dense set of
physical states.

The semigroup `T(t)` describes Euclidean-time evolution on the reconstructed
space. Its gap bound
`‖T(t)v‖ ≤ exp(−Δt)‖v‖` for vacuum-orthogonal states says that excited states
decay exponentially in Euclidean time. Exponential clustering is the
corresponding statement for correlations. The positive value `Δ` is the
continuum mass gap carried by the reconstructed theory.

## Uniform RG and the mass-gap witness

`concreteUniformRGTrajectory N hN` is the concrete RG trajectory at each
`N ≥ 2`. The value of its continuum gap is obtained from the proved transfer
decay and the rescaling. `T_tesseract_gap` proves that each lattice step bounds
vacuum-orthogonal transfer correlations by `exp(-a)` times the squared norm.
At stage `m`, the
spacing and lattice decay exponent are both `a_m = Δ_latt(m) = 1/(m+1)`, so
`Δ_latt(m) / a_m = 1` at every stage. The trajectory's `gap_lim` proves that
these quotients converge to `F.Δ_phys`, hence `Δ_phys = 1`. For physical time
`t = k a_m`, the transfer decay is `exp(-k a_m) = exp(-t)`. The reconstructed
continuum theory therefore carries the positive mass gap `1`. In
`yangMillsMassGap`, this gap is part of the resulting Yang–Mills witness. The
strict mass-gap and RG declarations, with their exact types and axiom reports,
are available in the [declaration audit](formal_declaration_audit.md).
