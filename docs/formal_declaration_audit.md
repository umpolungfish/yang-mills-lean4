# Formal declaration audit

This page records the Lean types and kernel axiom reports for the principal
Yang–Mills, RG, continuum, and Wightman declarations. Run the commands from the
repository root with Lean 4.28.0.

```lean
import Imscribing.YangMills.GlobalAxioms

#check YangMills.clay_yang_mills_strict_from_balaban_and_os
#print axioms YangMills.clay_yang_mills_strict_from_balaban_and_os

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
```

## Checked types

| Declaration | Lean type or result | Kernel axioms |
|---|---|---|
| `YangMills.clay_yang_mills_strict_from_balaban_and_os` | `ClayYangMillsMassGap4DStrict N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.clay_yang_mills_from_rg_estimates` | `SUYangMillsRGConjecture N hN → ClayYangMillsMassGap4D N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.unconditional_uniform_rescaled_lattice_mass_gap_and_rg_convergence` | Concrete uniform rescaled lattice gap and RG convergence data for every `N ≥ 2` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.concreteOS4DContinuumTheory` | `OS4DContinuumTheory 1`; the source separately proves `concreteOS4D_fails_trans_inv` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.concreteUniformRGTrajectory` | `UniformRGTrajectory N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WightmanQFT4DStrict` | `Type 1` structure indexed by `Δ_phys` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.yangMillsMassGap` | `YangMillsMassGap` | `propext`, `Classical.choice`, `Quot.sound` |

The Wilson stage convergence theorem is audited alongside these declarations
in `SchwingerConv.lean`: `stageObservableSchwinger_tendsto_iid` proves the full
finite-tuple limit, including repeated continuum points, with stage spacing
`1/(m+2)` and physical side length `m+2`.

`concreteOS4DContinuumTheory` is a separate checked OS declaration. The
translation-invariance counterexample is recorded by
`YangMills.concreteOS4D_fails_trans_inv`; it is not the Wilson stage limit.

## Reproduce

```bash
lake env lean --stdin <<'EOF'
import Imscribing.YangMills.GlobalAxioms
#check YangMills.yangMillsMassGap
#print axioms YangMills.yangMillsMassGap
EOF
```
