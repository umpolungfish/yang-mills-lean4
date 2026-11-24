# Formal declaration audit

This page records the Lean types and kernel axiom reports for the principal
Yang–Mills, RG, continuum, and Wightman declarations. Run the commands from the
repository root with Lean 4.28.0.

```lean
import Imscribing.YangMills.ContinuumClosure
import Imscribing.YangMills.GlobalAxioms
import Imscribing.YangMills.SchwingerConv
import Imscribing.YangMills.IIDSchwingerFromWilson
import Imscribing.YangMills.IIDOS
import Imscribing.YangMills.TrivialWightman

#check YangMills.clay_yang_mills_strict_from_balaban_and_os
#print axioms YangMills.clay_yang_mills_strict_from_balaban_and_os

#check YangMills.ClayYangMillsMassGap4DStrictOnOSCompletion
#check YangMills.clay_yang_mills_strict_on_os_completion_from_balaban_and_os
#print axioms YangMills.clay_yang_mills_strict_on_os_completion_from_balaban_and_os
#check YangMills.clay_yang_mills_strict_on_os_completion_implies_strict
#print axioms YangMills.clay_yang_mills_strict_on_os_completion_implies_strict

#check YangMills.osConfigKernel_eq_completion_inner
#print axioms YangMills.osConfigKernel_eq_completion_inner
#check YangMills.osTimeShiftConfig_eq_completion_inner
#print axioms YangMills.osTimeShiftConfig_eq_completion_inner
#check YangMills.buildStrictWightmanFromOS_config_inner
#print axioms YangMills.buildStrictWightmanFromOS_config_inner
#check YangMills.buildStrictWightmanFromOS_time_shift_kernel
#print axioms YangMills.buildStrictWightmanFromOS_time_shift_kernel
#check YangMills.buildStrictWightmanFromOS_schwinger_vacuum_coefficient
#print axioms YangMills.buildStrictWightmanFromOS_schwinger_vacuum_coefficient

#check YangMills.clay_yang_mills_from_rg_estimates
#print axioms YangMills.clay_yang_mills_from_rg_estimates

#check YangMills.unconditional_uniform_rescaled_lattice_mass_gap_and_rg_convergence
#print axioms YangMills.unconditional_uniform_rescaled_lattice_mass_gap_and_rg_convergence

#check YangMills.concreteOS4DContinuumTheory
#print axioms YangMills.concreteOS4DContinuumTheory

#check YangMills.concreteUniformRGTrajectory
#print axioms YangMills.concreteUniformRGTrajectory

#check YangMills.WightmanQFT4DStrict
#print axioms YangMills.WightmanQFT4DStrict

#check YangMills.yangMillsMassGap
#print axioms YangMills.yangMillsMassGap

#check YangMills.stageObservableSchwinger_tendsto_iid
#print axioms YangMills.stageObservableSchwinger_tendsto_iid

#check YangMills.stageObservable_not_ae_constant
#print axioms YangMills.stageObservable_not_ae_constant
#check YangMills.stageObservable_latticeSinglePointObs

#check YangMills.iidSchwinger_from_wilson
#print axioms YangMills.iidSchwinger_from_wilson

#check YangMills.iidOS4DStrict
#print axioms YangMills.iidOS4DStrict

#check YangMills.trivialWightman
#print axioms YangMills.trivialWightman

#check YangMills.fullRankCubicNonAbelianWilsonSetup_exact_gap
#print axioms YangMills.fullRankCubicNonAbelianWilsonSetup_exact_gap

#check MassGapInstances.clay_yang_mills_strict
#print axioms MassGapInstances.clay_yang_mills_strict
```

## Checked types

| Declaration | Lean type or result | Kernel axioms |
|---|---|---|
| `YangMills.clay_yang_mills_strict_from_balaban_and_os` | `BalabanRGContinuumHypothesis N hN → OSPoincareContinuationHypothesis B.os → ClayYangMillsMassGap4DStrict N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.clay_yang_mills_strict_on_os_completion_from_balaban_and_os` | Balaban and continuation inputs produce a strict witness whose Wightman object equals `buildStrictWightmanFromOS os C` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.clay_yang_mills_strict_on_os_completion_implies_strict` | The strengthened OS-completion target implies `ClayYangMillsMassGap4DStrict` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.osConfigKernel_eq_completion_inner` | Reflected Schwinger kernel equals the inner product of canonical OS completion vectors | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.osTimeShiftConfig_eq_completion_inner` | Lifted Euclidean semigroup matrix coefficient equals the time-shifted reflected kernel | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.buildStrictWightmanFromOS_config_inner` | The same kernel identity in the Hilbert space of the assembled Wightman object | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.buildStrictWightmanFromOS_time_shift_kernel` | The time-shifted kernel matrix coefficient in the assembled Wightman Hilbert space | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.buildStrictWightmanFromOS_schwinger_vacuum_coefficient` | Positive-time Schwinger value as the vacuum matrix coefficient of its canonical configuration state | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.clay_yang_mills_from_rg_estimates` | `SUYangMillsRGConjecture N hN → ClayYangMillsMassGap4D N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.unconditional_uniform_rescaled_lattice_mass_gap_and_rg_convergence` | Concrete uniform rescaled lattice gap and RG convergence data for every `N ≥ 2` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.concreteOS4DContinuumTheory` | `OS4DContinuumTheory 1`; the source separately proves `concreteOS4D_fails_trans_inv` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.concreteUniformRGTrajectory` | `UniformRGTrajectory N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WightmanQFT4DStrict` | `Type 1` structure indexed by `Δ_phys` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.yangMillsMassGap` | `YangMillsMassGap` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.stageObservableSchwinger_tendsto_iid` | Full finite-tuple limit of selected Wilson stage observables, including repeated points | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.stageObservable_not_ae_constant` | The stage observable is not almost surely constant under the Wilson measure | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.stageObservable_latticeSinglePointObs` | Packages Wilson stage observables as gauge-invariant, nonconstant `LatticeSinglePointObs` data | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.iidSchwinger_from_wilson` | Exact Wilson-probe bridge to `iidSchwinger` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.iidOS4DStrict` | Strict OS family with rate `1` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.trivialWightman` | `WightmanQFT4DStrict 1` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.fullRankCubicNonAbelianWilsonSetup_exact_gap` | Exact positive spectral gap for the full-rank finite-volume Wilson transfer | `propext`, `Classical.choice`, `Quot.sound` |
| `MassGapInstances.clay_yang_mills_strict` | `∃ P : GappedSpectrum (Fin 2), 0 < P.Δ` | `propext`, `Classical.choice`, `Quot.sound` |

The exact probe bridge and full-tuple stage limit are separate declarations.
The first proves an exact identity for its probe family. The second proves the
finite-volume-to-continuum limit for the selected stage observables, with
spacing `1/(m+2)` and physical side length `m+2`. Its explicit
submersion-to-density argument is supplied by
`submersion_map_has_L1_density` in `SubmersionDensity.lean`.

The strict Clay theorem has explicit RG and continuation inputs. The separate
unconditional finite-system mass-gap theorem proves a `GappedSpectrum (Fin 2)`
existence statement. The unconditional OS, Wightman, Wilson-limit, and
finite-volume transfer declarations listed here do not instantiate the strict
Clay theorem's inputs.

The original strict proposition leaves the Wightman witness independent of the
OS reconstruction. `ClayYangMillsMassGap4DStrictOnOSCompletion` adds the
object-level reconstruction equality, and its reduction theorem retains the
Balaban and continuation records as explicit inputs.

`concreteOS4DContinuumTheory` is a separate checked OS declaration. The
translation-invariance counterexample is recorded by
`YangMills.concreteOS4D_fails_trans_inv`; it is not the Wilson stage limit.
The [proof-reading map](proof_reading_map.html) gives the roles and source
locations of these distinct constructions.

## Reproduce

```bash
lake env lean --stdin <<'EOF'
import Imscribing.YangMills.GlobalAxioms
#check YangMills.yangMillsMassGap
#print axioms YangMills.yangMillsMassGap
EOF
```
