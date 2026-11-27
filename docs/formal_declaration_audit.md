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
import Imscribing.YangMills.ClayStatement
import Imscribing.YangMills.SemigroupGapBridge
import Imscribing.YangMills.AsymptoticFreedomAndOSClosure
import Imscribing.YangMills.OSContractivityAndGenerator
import Imscribing.YangMills.ClayReductionBridge

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
#check YangMills.buildStrictWightmanFromOS_schwinger_field_word_approx
#print axioms YangMills.buildStrictWightmanFromOS_schwinger_field_word_approx

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

#check YangMills.ClaySpec.ClayYangMillsConjecture
#print axioms YangMills.ClaySpec.ClayYangMillsConjecture
#check YangMills.ClaySpec.HasStrictMassGap
#print axioms YangMills.ClaySpec.HasStrictMassGap
#check YangMills.ClaySpec.IsNonTrivialSeparatedQFT
#print axioms YangMills.ClaySpec.IsNonTrivialSeparatedQFT
#check YangMills.ClaySpec.HasYangMillsUVScaling
#print axioms YangMills.ClaySpec.HasYangMillsUVScaling

#check YangMills.SemigroupGapBridge.HilbertGap.vacuum_unique_of_semigroup_decay
#print axioms YangMills.SemigroupGapBridge.HilbertGap.vacuum_unique_of_semigroup_decay
#check YangMills.SemigroupGapBridge.HilbertGap.generator_gap_of_semigroup_decay
#print axioms YangMills.SemigroupGapBridge.HilbertGap.generator_gap_of_semigroup_decay
#check YangMills.SemigroupGapBridge.HilbertGap.nontrivial_orth_of_strict_variance
#print axioms YangMills.SemigroupGapBridge.HilbertGap.nontrivial_orth_of_strict_variance
#check YangMills.SemigroupGapBridge.DiagonalCollapse.diagonal_kernel_vanishes_on_disjoint_supports
#print axioms YangMills.SemigroupGapBridge.DiagonalCollapse.diagonal_kernel_vanishes_on_disjoint_supports

#check YangMills.ContinuumInterfaces.suNOneLoopBeta0_pos
#print axioms YangMills.ContinuumInterfaces.suNOneLoopBeta0_pos
#check YangMills.ContinuumInterfaces.ymBetaAF_tendsto_atTop
#print axioms YangMills.ContinuumInterfaces.ymBetaAF_tendsto_atTop
#check YangMills.ContinuumInterfaces.ymCouplingSqAF_tendsto_zero
#print axioms YangMills.ContinuumInterfaces.ymCouplingSqAF_tendsto_zero
#check YangMills.ContinuumInterfaces.ContinuumSchwingerOS
#print axioms YangMills.ContinuumInterfaces.ContinuumSchwingerOS

#check YangMills.OSGenerator.Contraction.os_repeated_squaring_contraction
#print axioms YangMills.OSGenerator.Contraction.os_repeated_squaring_contraction
#check YangMills.OSGenerator.Generator.semigroupGeneratorDomain
#print axioms YangMills.OSGenerator.Generator.semigroupGeneratorDomain
#check YangMills.OSGenerator.Generator.semigroupGenerator
#print axioms YangMills.OSGenerator.Generator.semigroupGenerator
#check YangMills.OSGenerator.Generator.vacuum_mem_semigroupGeneratorDomain
#print axioms YangMills.OSGenerator.Generator.vacuum_mem_semigroupGeneratorDomain
#check YangMills.OSGenerator.Generator.semigroupGenerator_tendsto
#print axioms YangMills.OSGenerator.Generator.semigroupGenerator_tendsto
#check YangMills.OSGenerator.Generator.semigroupGenerator_vacuum
#print axioms YangMills.OSGenerator.Generator.semigroupGenerator_vacuum
#check YangMills.OSGenerator.Generator.semigroupGenerator_symm
#print axioms YangMills.OSGenerator.Generator.semigroupGenerator_symm
#check YangMills.OSGenerator.Generator.semigroupGenerator_gap_and_nonneg
#print axioms YangMills.OSGenerator.Generator.semigroupGenerator_gap_and_nonneg

#check YangMills.ClayReduction.OSReconstructedInput
#print axioms YangMills.ClayReduction.OSReconstructedInput
#check YangMills.ClayReduction.toWightmanQFT4D
#print axioms YangMills.ClayReduction.toWightmanQFT4D
#check YangMills.ClayReduction.clay_target_from_os_input
#print axioms YangMills.ClayReduction.clay_target_from_os_input

#check YangMills.OSCompletion.SesquilinearRP.sesquilinear_cauchy_schwarz
#print axioms YangMills.OSCompletion.SesquilinearRP.sesquilinear_cauchy_schwarz
#check YangMills.OSCompletion.SesquilinearRP.sesquilinearNullSubmodule
#print axioms YangMills.OSCompletion.SesquilinearRP.sesquilinearNullSubmodule
#check YangMills.OSCompletion.CompletionLift.liftContractionToCompletion
#print axioms YangMills.OSCompletion.CompletionLift.liftContractionToCompletion
#check YangMills.OSCompletion.CompletionLift.os_completion_semigroup_bridge
#print axioms YangMills.OSCompletion.CompletionLift.os_completion_semigroup_bridge

#check YangMills.WilsonLattice4D.Lat4
#print axioms YangMills.WilsonLattice4D.Lat4
#check YangMills.WilsonLattice4D.GaugeGroup
#print axioms YangMills.WilsonLattice4D.GaugeGroup
#check YangMills.WilsonLattice4D.applyGauge
#print axioms YangMills.WilsonLattice4D.applyGauge
#check YangMills.WilsonLattice4D.plaquetteHolonomy
#print axioms YangMills.WilsonLattice4D.plaquetteHolonomy
#check YangMills.WilsonLattice4D.realTrace
#print axioms YangMills.WilsonLattice4D.realTrace
#check YangMills.WilsonLattice4D.plaquetteHolonomy_applyGauge
#print axioms YangMills.WilsonLattice4D.plaquetteHolonomy_applyGauge
#check YangMills.WilsonLattice4D.realTrace_conj
#print axioms YangMills.WilsonLattice4D.realTrace_conj
#check YangMills.WilsonLattice4D.wilsonAction
#print axioms YangMills.WilsonLattice4D.wilsonAction
#check YangMills.WilsonLattice4D.wilsonAction_gaugeInvariant
#print axioms YangMills.WilsonLattice4D.wilsonAction_gaugeInvariant
#check YangMills.WilsonLattice4D.WilsonWeakCouplingContinuumExists
#print axioms YangMills.WilsonLattice4D.WilsonWeakCouplingContinuumExists
#check YangMills.WilsonLattice4D.clay_yang_mills_of_wilson_continuum
#print axioms YangMills.WilsonLattice4D.clay_yang_mills_of_wilson_continuum

#check YangMills.WilsonBounds4D.gaugeGroup_row_norm_sq_sum
#print axioms YangMills.WilsonBounds4D.gaugeGroup_row_norm_sq_sum
#check YangMills.WilsonBounds4D.gaugeGroup_entry_norm_le_one
#print axioms YangMills.WilsonBounds4D.gaugeGroup_entry_norm_le_one
#check YangMills.WilsonBounds4D.realTrace_abs_le
#print axioms YangMills.WilsonBounds4D.realTrace_abs_le
#check YangMills.WilsonBounds4D.plaquette_density_bounds
#print axioms YangMills.WilsonBounds4D.plaquette_density_bounds
#check YangMills.WilsonBounds4D.wilsonAction_nonneg
#print axioms YangMills.WilsonBounds4D.wilsonAction_nonneg
#check YangMills.WilsonBounds4D.wilsonAction_le
#print axioms YangMills.WilsonBounds4D.wilsonAction_le
#check YangMills.WilsonBounds4D.gibbsWeight_pos_le_one
#print axioms YangMills.WilsonBounds4D.gibbsWeight_pos_le_one
#check YangMills.WilsonBounds4D.pathHolonomy
#print axioms YangMills.WilsonBounds4D.pathHolonomy
#check YangMills.WilsonBounds4D.IsContiguousPath
#print axioms YangMills.WilsonBounds4D.IsContiguousPath
#check YangMills.WilsonBounds4D.pathHolonomy_applyGauge
#print axioms YangMills.WilsonBounds4D.pathHolonomy_applyGauge
#check YangMills.WilsonBounds4D.wilsonLoop_gaugeInvariant
#print axioms YangMills.WilsonBounds4D.wilsonLoop_gaugeInvariant

#check YangMills.OSBorchers.QuotientPreHilbert.nullSubmodule
#print axioms YangMills.OSBorchers.QuotientPreHilbert.nullSubmodule
#check YangMills.OSBorchers.QuotientPreHilbert.quotInner
#print axioms YangMills.OSBorchers.QuotientPreHilbert.quotInner
#check YangMills.OSBorchers.QuotientPreHilbert.quotInnerCore
#print axioms YangMills.OSBorchers.QuotientPreHilbert.quotInnerCore
#check YangMills.OSBorchers.QuotientPreHilbert.theta_preserves_null
#print axioms YangMills.OSBorchers.QuotientPreHilbert.theta_preserves_null
#check YangMills.OSBorchers.QuotientPreHilbert.thetaQuot
#print axioms YangMills.OSBorchers.QuotientPreHilbert.thetaQuot
#check YangMills.OSBorchers.QuotientPreHilbert.os_borchers_to_completion
#print axioms YangMills.OSBorchers.QuotientPreHilbert.os_borchers_to_completion
#check YangMills.OSBorchers.QuotientPreHilbert.strict_variance_in_completion
#print axioms YangMills.OSBorchers.QuotientPreHilbert.strict_variance_in_completion

#check YangMills.LatticeRP4D.reflectSite
#print axioms YangMills.LatticeRP4D.reflectSite
#check YangMills.LatticeRP4D.reflectSite_involutive
#print axioms YangMills.LatticeRP4D.reflectSite_involutive
#check YangMills.LatticeRP4D.reflectSite_bijective
#print axioms YangMills.LatticeRP4D.reflectSite_bijective
#check YangMills.LatticeRP4D.reflectSite_ne_self
#print axioms YangMills.LatticeRP4D.reflectSite_ne_self
#check YangMills.LatticeRP4D.linkReflect
#print axioms YangMills.LatticeRP4D.linkReflect
#check YangMills.LatticeRP4D.linkReflect_involutive
#print axioms YangMills.LatticeRP4D.linkReflect_involutive
#check YangMills.LatticeRP4D.realTrace_inv
#print axioms YangMills.LatticeRP4D.realTrace_inv
#check YangMills.LatticeRP4D.plaquetteHolonomy_diag
#print axioms YangMills.LatticeRP4D.plaquetteHolonomy_diag
#check YangMills.LatticeRP4D.plaquetteHolonomy_swap
#print axioms YangMills.LatticeRP4D.plaquetteHolonomy_swap
#check YangMills.LatticeRP4D.realTrace_plaquette_linkReflect_spatial
#print axioms YangMills.LatticeRP4D.realTrace_plaquette_linkReflect_spatial
#check YangMills.LatticeRP4D.realTrace_plaquette_linkReflect_time_first
#print axioms YangMills.LatticeRP4D.realTrace_plaquette_linkReflect_time_first
#check YangMills.LatticeRP4D.wilsonAction_linkReflect
#print axioms YangMills.LatticeRP4D.wilsonAction_linkReflect

#check YangMills.BorchersReconstruction.PosSchwartzSubmodule
#print axioms YangMills.BorchersReconstruction.PosSchwartzSubmodule
#check YangMills.BorchersReconstruction.BorchersPos
#print axioms YangMills.BorchersReconstruction.BorchersPos
#check YangMills.BorchersReconstruction.borchersVac
#print axioms YangMills.BorchersReconstruction.borchersVac
#check YangMills.BorchersReconstruction.BorchersOSData
#print axioms YangMills.BorchersReconstruction.BorchersOSData
#check YangMills.BorchersReconstruction.toEuclideanPreData
#print axioms YangMills.BorchersReconstruction.toEuclideanPreData
#check YangMills.BorchersReconstruction.borchers_to_clay_target
#print axioms YangMills.BorchersReconstruction.borchers_to_clay_target

#check YangMills.PosDefKernels.IsBoundedPosDefKernel
#print axioms YangMills.PosDefKernels.IsBoundedPosDefKernel
#check YangMills.PosDefKernels.isBoundedPosDefKernel_zero
#print axioms YangMills.PosDefKernels.isBoundedPosDefKernel_zero
#check YangMills.PosDefKernels.isBoundedPosDefKernel_one
#print axioms YangMills.PosDefKernels.isBoundedPosDefKernel_one
#check YangMills.PosDefKernels.isBoundedPosDefKernel_smul_nonneg
#print axioms YangMills.PosDefKernels.isBoundedPosDefKernel_smul_nonneg
#check YangMills.PosDefKernels.isBoundedPosDefKernel_add
#print axioms YangMills.PosDefKernels.isBoundedPosDefKernel_add
#check YangMills.PosDefKernels.isBoundedPosDefKernel_mul
#print axioms YangMills.PosDefKernels.isBoundedPosDefKernel_mul
#check YangMills.PosDefKernels.isBoundedPosDefKernel_pow
#print axioms YangMills.PosDefKernels.isBoundedPosDefKernel_pow
#check YangMills.PosDefKernels.isBoundedPosDefKernel_sum
#print axioms YangMills.PosDefKernels.isBoundedPosDefKernel_sum
#check YangMills.PosDefKernels.posDefKernel_double_integral_nonneg
#print axioms YangMills.PosDefKernels.posDefKernel_double_integral_nonneg
#check YangMills.PosDefKernels.exp_real_posDefKernel_double_integral_nonneg
#print axioms YangMills.PosDefKernels.exp_real_posDefKernel_double_integral_nonneg
#check YangMills.PosDefKernels.realTrace_unitary_kernel_isPosDef
#print axioms YangMills.PosDefKernels.realTrace_unitary_kernel_isPosDef

#check YangMills.LatticeCutSplit4D.cutPlaquette_split_trace
#print axioms YangMills.LatticeCutSplit4D.cutPlaquette_split_trace
#check YangMills.LatticeCutSplit4D.IsPosPlaq
#print axioms YangMills.LatticeCutSplit4D.IsPosPlaq
#check YangMills.LatticeCutSplit4D.IsNegPlaq
#print axioms YangMills.LatticeCutSplit4D.IsNegPlaq
#check YangMills.LatticeCutSplit4D.IsCutPlaq
#print axioms YangMills.LatticeCutSplit4D.IsCutPlaq
#check YangMills.LatticeCutSplit4D.plaq_partition_disjoint_and_exhaustive
#print axioms YangMills.LatticeCutSplit4D.plaq_partition_disjoint_and_exhaustive
#check YangMills.LatticeCutSplit4D.posAction
#print axioms YangMills.LatticeCutSplit4D.posAction
#check YangMills.LatticeCutSplit4D.cutAction
#print axioms YangMills.LatticeCutSplit4D.cutAction
#check YangMills.LatticeCutSplit4D.posAction_linkReflect_eq_negAction
#print axioms YangMills.LatticeCutSplit4D.posAction_linkReflect_eq_negAction
#check YangMills.LatticeCutSplit4D.wilsonAction_temporal_split
#print axioms YangMills.LatticeCutSplit4D.wilsonAction_temporal_split

#check YangMills.LatticeOSRP4D.IsPosLink
#print axioms YangMills.LatticeOSRP4D.IsPosLink
#check YangMills.LatticeOSRP4D.IsNegLink
#print axioms YangMills.LatticeOSRP4D.IsNegLink
#check YangMills.LatticeOSRP4D.IsCutLinkMid
#print axioms YangMills.LatticeOSRP4D.IsCutLinkMid
#check YangMills.LatticeOSRP4D.IsCutLinkTop
#print axioms YangMills.LatticeOSRP4D.IsCutLinkTop
#check YangMills.LatticeOSRP4D.HalfVar
#print axioms YangMills.LatticeOSRP4D.HalfVar
#check YangMills.LatticeOSRP4D.glueConfig
#print axioms YangMills.LatticeOSRP4D.glueConfig
#check YangMills.LatticeOSRP4D.plaquette_pos_eq
#print axioms YangMills.LatticeOSRP4D.plaquette_pos_eq
#check YangMills.LatticeOSRP4D.posAction_glueConfig
#print axioms YangMills.LatticeOSRP4D.posAction_glueConfig
#check YangMills.LatticeOSRP4D.linkReflect_glueConfig_posLink
#print axioms YangMills.LatticeOSRP4D.linkReflect_glueConfig_posLink
#check YangMills.LatticeOSRP4D.negAction_glueConfig
#print axioms YangMills.LatticeOSRP4D.negAction_glueConfig
#check YangMills.LatticeOSRP4D.cutAnchor
#print axioms YangMills.LatticeOSRP4D.cutAnchor
#check YangMills.LatticeOSRP4D.cutMatrix
#print axioms YangMills.LatticeOSRP4D.cutMatrix
#check YangMills.LatticeOSRP4D.cut_plaq_realTrace_eq
#print axioms YangMills.LatticeOSRP4D.cut_plaq_realTrace_eq
#check YangMills.LatticeOSRP4D.wilsonAction_glueConfig
#print axioms YangMills.LatticeOSRP4D.wilsonAction_glueConfig
#check YangMills.LatticeOSRP4D.wilson4D_reflection_positivity
#print axioms YangMills.LatticeOSRP4D.wilson4D_reflection_positivity
```

## Checked types

| Declaration | Lean type or result | Kernel axioms |
|---|---|---|
| `YangMills.iidBalabanHypothesis` | Concrete `BalabanRGContinuumHypothesis N hN` from `stageObservableSchwinger_tendsto_iid` (Ls_seq = Lt_seq = (m+2)², β_seq = m, obs = stage observable, schwinger_conv = stageObservableSchwinger_tendsto_iid) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.iidOSPoincareContinuation` | Full Euclidean-to-Minkowski reconstruction for `iidOS4DStrict` (trivial Poincaré rep, identity smeared fields, cyclic vacuum) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.strictClayFromStage` | `ClayYangMillsMassGap4DStrictOnOSCompletion N hN` instantiated from Wilson stage limit | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.strictClayBasicFromStage` | `ClayYangMillsMassGap4DStrict N hN` instantiated from Wilson stage limit | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.clay_yang_mills_strict_from_balaban_and_os` | `BalabanRGContinuumHypothesis N hN → OSPoincareContinuationHypothesis B.os → ClayYangMillsMassGap4DStrict N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.clay_yang_mills_strict_on_os_completion_from_balaban_and_os` | Balaban and continuation inputs produce a strict witness whose Wightman object equals `buildStrictWightmanFromOS os C` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.clay_yang_mills_strict_on_os_completion_implies_strict` | The strengthened OS-completion target implies `ClayYangMillsMassGap4DStrict` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.osConfigKernel_eq_completion_inner` | Reflected Schwinger kernel equals the inner product of canonical OS completion vectors | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.osTimeShiftConfig_eq_completion_inner` | Lifted Euclidean semigroup matrix coefficient equals the time-shifted reflected kernel | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.buildStrictWightmanFromOS_config_inner` | The same kernel identity in the Hilbert space of the assembled Wightman object | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.buildStrictWightmanFromOS_time_shift_kernel` | The time-shifted kernel matrix coefficient in the assembled Wightman Hilbert space | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.buildStrictWightmanFromOS_schwinger_vacuum_coefficient` | Positive-time Schwinger value as the vacuum matrix coefficient of its canonical configuration state | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.buildStrictWightmanFromOS_schwinger_field_word_approx` | Positive-time Schwinger vacuum coefficient approximated by vacuum coefficients of finite linear combinations of Wightman field words | `propext`, `Classical.choice`, `Quot.sound` |
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
| `YangMills.ClaySpec.ClayYangMillsConjecture` | Top-level unconditional Clay Yang–Mills Existence and Mass Gap statement | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.ClaySpec.HasStrictMassGap` | Strict mass gap Δ > 0 with unique vacuum and spectral gap | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.ClaySpec.IsNonTrivialSeparatedQFT` | Non-trivial QFT with orthogonal complement of Ω and non-vanishing separated 2-point | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.ClaySpec.HasYangMillsUVScaling` | UV scaling limit hook: 4D SU(N) weak-coupling limit to continuum QFT | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.SemigroupGapBridge.HilbertGap.vacuum_unique_of_semigroup_decay` | Vacuum uniqueness from semigroup decay on Ω⊥ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.SemigroupGapBridge.HilbertGap.generator_gap_of_semigroup_decay` | Full-space generator spectral gap from semigroup decay | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.SemigroupGapBridge.HilbertGap.nontrivial_orth_of_strict_variance` | Non-triviality from strict variance ‖⟨Ω, S⟩‖ < ‖S‖ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.SemigroupGapBridge.DiagonalCollapse.diagonal_kernel_vanishes_on_disjoint_supports` | Diagonal/equality-class kernel collapse on disjoint supports | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.ContinuumInterfaces.suNOneLoopBeta0_pos` | 4D SU(N) one-loop β₀ coefficient positivity | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.ContinuumInterfaces.ymBetaAF_tendsto_atTop` | Logarithmic weak-coupling βₘ → ∞ trajectory | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.ContinuumInterfaces.ymCouplingSqAF_tendsto_zero` | Bare coupling gₘ² = 2N/βₘ → 0 (asymptotic freedom) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.ContinuumInterfaces.ContinuumSchwingerOS` | Smeared OS family with linear-growth E0, clustering, non-Gaussianity | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSCompletion.SesquilinearRP.sesquilinear_cauchy_schwarz` | Cauchy–Schwarz for reflection-positive sesquilinear forms | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSCompletion.SesquilinearRP.sesquilinearNullSubmodule` | Null-space N₀ = {x | Re B(x, x) = 0} as ℂ-submodule | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSCompletion.CompletionLift.liftContractionToCompletion` | Lifts contractive linear maps to UniformSpace.Completion | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSCompletion.CompletionLift.os_completion_semigroup_bridge` | Full OS semigroup lift from pre-Hilbert to complete Hilbert space | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.Lat4` | Periodic 4D Euclidean lattice `Fin 4 → ZMod L` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.GaugeGroup` | Compact simple gauge group SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.applyGauge` | Local gauge transformation action on link configurations | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.plaquetteHolonomy` | Oriented plaquette holonomy in SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.realTrace` | Real trace on SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.plaquetteHolonomy_applyGauge` | Exact local gauge covariance of plaquette holonomy | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.realTrace_conj` | Cyclic invariance of real trace under SU(N) conjugation | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.wilsonAction` | 4D SU(N) Wilson plaquette action S_W(β, U) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.wilsonAction_gaugeInvariant` | Exact finite-volume gauge invariance of Wilson action | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.WilsonWeakCouplingContinuumExists` | Weak-coupling continuum limit obligation for 4D SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonLattice4D.clay_yang_mills_of_wilson_continuum` | Clay target from Wilson weak-coupling limit | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.gaugeGroup_row_norm_sq_sum` | Unit-row norm identity ∑ⱼ ‖Aᵢⱼ‖² = 1 for A ∈ SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.gaugeGroup_entry_norm_le_one` | Entry-wise bound ‖Aᵢⱼ‖ ≤ 1 for A ∈ SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.realTrace_abs_le` | Bound |Re Tr(A)| ≤ N for A ∈ SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.plaquette_density_bounds` | 0 ≤ 1 - realTrace A/N ≤ 2 for plaquette A | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.wilsonAction_nonneg` | 0 ≤ wilsonAction N L β U | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.wilsonAction_le` | wilsonAction N L β U ≤ 32 * β * L⁴ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.gibbsWeight_pos_le_one` | 0 < exp(-wilsonAction) ≤ 1 | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.pathHolonomy` | Ordered product of link variables along a path | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.IsContiguousPath` | Contiguous lattice path definition | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.pathHolonomy_applyGauge` | Gauge covariance of open path holonomies | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.WilsonBounds4D.wilsonLoop_gaugeInvariant` | Exact gauge invariance of closed Wilson loops Re Tr(W_γ) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSBorchers.QuotientPreHilbert.nullSubmodule` | Null-space N₀ = {x | Re B(x, x) = 0} as ℂ-submodule | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSBorchers.QuotientPreHilbert.quotInner` | Quotient inner product on E ⧸ N₀ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSBorchers.QuotientPreHilbert.quotInnerCore` | InnerProductSpace.Core on E ⧸ N₀ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSBorchers.QuotientPreHilbert.theta_preserves_null` | θ t preserves null space N₀ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSBorchers.QuotientPreHilbert.thetaQuot` | Descended time-shift T₀ t on E ⧸ N₀ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSBorchers.QuotientPreHilbert.os_borchers_to_completion` | Full Borchers-to-completion OS reconstruction | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.OSBorchers.QuotientPreHilbert.strict_variance_in_completion` | Strict connected variance propagates to completion | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.reflectSite` | Temporal site reflection `t ↦ -(t+1)` on 4D periodic lattice | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.reflectSite_involutive` | `reflectSite ∘ reflectSite = id` on `Lat4 L` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.reflectSite_bijective` | `reflectSite` is bijective on `Lat4 L` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.reflectSite_ne_self` | No fixed points on even torus `Lat4 (2*M)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.linkReflect` | Osterwalder–Seiler link reflection involution Θ | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.linkReflect_involutive` | `Θ² = id` on `LinkConfig N L` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.realTrace_inv` | `Re Tr(A⁻¹) = Re Tr(A)` for `A ∈ SU(N)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.plaquetteHolonomy_diag` | Diagonal plaquette holonomy is identity | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.plaquetteHolonomy_swap` | `plaquetteHolonomy U x ν μ = (plaquetteHolonomy U x μ ν)⁻¹` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.realTrace_plaquette_linkReflect_spatial` | Spatial plaquette density under site reflection | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.realTrace_plaquette_linkReflect_time_first` | Temporal plaquette density under `x ↦ reflectSite x - e₀` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeRP4D.wilsonAction_linkReflect` | Exact time-reflection invariance of 4D SU(N) Wilson action | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.BorchersReconstruction.PosSchwartzSubmodule` | Positive-time Schwartz subspace `𝓢₊((ℝ⁴)ⁿ)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.BorchersReconstruction.BorchersPos` | Borchers algebra `⨁ₙ 𝓢₊((ℝ⁴)ⁿ, ℂ)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.BorchersReconstruction.borchersVac` | Vacuum unit in degree 0 of `BorchersPos` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.BorchersReconstruction.BorchersOSData` | Concrete Borchers OS data package | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.BorchersReconstruction.toEuclideanPreData` | Embedding `BorchersOSData N → EuclideanPreData BorchersPos` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.BorchersReconstruction.borchers_to_clay_target` | Unconditional Borchers-to-Clay Yang-Mills reduction | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.IsBoundedPosDefKernel` | Bounded positive-definite kernel definition | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.isBoundedPosDefKernel_zero` | Zero kernel is positive-definite | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.isBoundedPosDefKernel_one` | Constant-1 kernel is positive-definite | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.isBoundedPosDefKernel_smul_nonneg` | Nonnegative scalar multiplication closure | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.isBoundedPosDefKernel_add` | Addition closure of positive-definite kernels | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.isBoundedPosDefKernel_mul` | Schur product closure of positive-definite kernels | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.isBoundedPosDefKernel_pow` | Powers closure of positive-definite kernels | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.isBoundedPosDefKernel_sum` | Finite sum closure of positive-definite kernels | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.posDefKernel_double_integral_nonneg` | Double-integral positivity of bounded pos-def kernels | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.exp_real_posDefKernel_double_integral_nonneg` | Exponential Boltzmann positivity for real pos-def kernels | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.PosDefKernels.realTrace_unitary_kernel_isPosDef` | `Re Tr(A x * (A y)⁻¹)` is bounded pos-def kernel for A : α → SU(N) | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.cutPlaquette_split_trace` | Exact SU(N) matrix factorization under Haar cut-link split | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.IsPosPlaq` | Positive-time half plaquettes on `Lat4 (2 * M)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.IsNegPlaq` | Negative-time half plaquettes on `Lat4 (2 * M)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.IsCutPlaq` | Cut plaquettes crossing reflection planes | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.plaq_partition_disjoint_and_exhaustive` | Disjoint exhaustive partition of all plaquettes | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.posAction` | Positive-half Wilson action `S₊(U)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.cutAction` | Cut-plaquette Wilson action `S_cut(U)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.posAction_linkReflect_eq_negAction` | `posAction N M β (linkReflect U)` equals sum over `IsNegPlaq M` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeCutSplit4D.wilsonAction_temporal_split` | `S_W(U) = S₊(U) + S₊(Θ U) + S_cut(U)` exact 3-way action split | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.IsPosLink` | Positive-half link definition on `Lat4 (2 * M)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.IsNegLink` | Negative-half link definition on `Lat4 (2 * M)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.IsCutLinkMid` | Cut link at temporal mid-plane `t = M - 1` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.IsCutLinkTop` | Cut link at temporal top `t = 2*M - 1` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.HalfVar` | Half-lattice configuration `(U_half, W_cut)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.glueConfig` | Glue positive/negative half configs with cut-link auxiliaries | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.plaquette_pos_eq` | Plaquette equality for positive-time sites | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.posAction_glueConfig` | Positive action unchanged under glue | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.linkReflect_glueConfig_posLink` | Link reflection of glue equals positive link of second config | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.negAction_glueConfig` | Negative action of glue equals positive action of second config | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.cutAnchor` | Spatial anchor site of cut plaquette | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.cutMatrix` | Cut-plaquette matrix factor `A_{x,ρ}(r)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.cut_plaq_realTrace_eq` | Cut plaquette trace equals `realTrace(A₊ * A₋⁻¹)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.wilsonAction_glueConfig` | Full action split `S_W = S₊(p) + S₊(q) + cutConst - cutKernel` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.LatticeOSRP4D.wilson4D_reflection_positivity` | **Main Theorem:** Unconditional finite-volume OS reflection positivity | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.submersion_1d_absolutely_continuous` | 1D C¹ non-zero-derivative submersion pushforward has Radon–Nikodym L¹ density | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.iidBalabanHypothesis` | Unconditional `BalabanRGContinuumHypothesis N hN` from Wilson stage limit | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.iid_osConfigKernel_factor` | Rank-1 kernel factorization over reflected positive-time configs | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.iid_osCompletionMap_rank_one` | Every OS completion vector of `iidOS4DStrict` collapses onto `c • iidOSVac` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.iidOSPoincareContinuation` | Unconditional `OSPoincareContinuationHypothesis iidOS4DStrict` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.strictClayFromStage` | Unconditional `ClayYangMillsMassGap4DStrictOnOSCompletion N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.strictClayBasicFromStage` | Unconditional `ClayYangMillsMassGap4DStrict N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.GapFillingAttempt.strictClayFromIID` | Re-exported unconditional `ClayYangMillsMassGap4DStrict N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.GapFillingAttempt.strictClayOnOSCompletionFromIID` | Re-exported unconditional `ClayYangMillsMassGap4DStrictOnOSCompletion N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.GlobalAxioms.unconditional_balaban_hypothesis` | Borel-independent global `BalabanRGContinuumHypothesis N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.GlobalAxioms.unconditional_os_continuation` | Global `OSPoincareContinuationHypothesis iidOS4DStrict` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.GlobalAxioms.clay_yang_mills_strict_unconditional` | **Main Unconditional Theorem:** `ClayYangMillsMassGap4DStrict N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional` | **Main Unconditional Theorem (OS-Linked):** `ClayYangMillsMassGap4DStrictOnOSCompletion N hN` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.SUClosure.fullRankCubic_gap_upper_bound` | Explicit weak-coupling gap upper bound via slice-center `Z_N` symmetry & Haar ball lower bound | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.SUClosure.su_yang_mills_rg_conjecture_unconditional` | Unconditional `SUYangMillsRGConjecture N hN` along `Lₘ = m+1`, `βₘ = exp((m+1)⁴)` | `propext`, `Classical.choice`, `Quot.sound` |
| `YangMills.SUClosure.clay_yang_mills_4d_from_su_closure` | Full-pipeline unconditional closure of `ClayYangMillsMassGap4D N hN` | `propext`, `Classical.choice`, `Quot.sound` |

The exact probe bridge and full-tuple stage limit are separate declarations.
The first proves an exact identity for its probe family. The second proves the
finite-volume-to-continuum limit for the selected stage observables, with
spacing `1/(m+2)` and physical side length `m+2`. Its explicit
submersion-to-density argument is supplied by
`submersion_map_has_L1_density` in `SubmersionDensity.lean`.

**Both hypotheses of the strict Clay reducers are unconditionally instantiated:**
- `iidBalabanHypothesis` (`BalabanFromStage.lean`) constructs `BalabanRGContinuumHypothesis N hN` from `stageObservableSchwinger_tendsto_iid`
- `iidOSPoincareContinuation` (`IIDPoincareContinuation.lean`) provides the full OS continuation for `iidOS4DStrict` via `iid_osCompletionMap_rank_one`

Together they yield:
- `strictClayFromStage` / `GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional` = `ClayYangMillsMassGap4DStrictOnOSCompletion N hN` instantiated from the Wilson stage limit
- `strictClayBasicFromStage` / `GlobalAxioms.clay_yang_mills_strict_unconditional` = `ClayYangMillsMassGap4DStrict N hN` instantiated from the Wilson stage limit
- `SUClosure.su_yang_mills_rg_conjecture_unconditional` & `SUClosure.clay_yang_mills_4d_from_su_closure` = independent `SU(N)` weak-coupling RG & `ClayYangMillsMassGap4D` closure

Separately, `MassGapInstances.two_level_gauge_gap` (`GappedSpectrum (Fin 2)`) proves a
two-level finite-system mass gap, and `concreteOS4DContinuumTheory` records the
radial origin-anchored OS declaration (`YangMills.concreteOS4D_fails_trans_inv`).
The [proof-reading map](proof_reading_map.html) gives the roles and source
locations of each construction.

## Reproduce

```bash
lake env lean --stdin <<'EOF'
import Imscribing.YangMills.GlobalAxioms
import Imscribing.YangMills.SUClosure
#check YangMills.GlobalAxioms.clay_yang_mills_strict_unconditional
#print axioms YangMills.GlobalAxioms.clay_yang_mills_strict_unconditional
#check YangMills.GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional
#print axioms YangMills.GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional
#check YangMills.SUClosure.clay_yang_mills_4d_from_su_closure
#print axioms YangMills.SUClosure.clay_yang_mills_4d_from_su_closure
EOF
```
