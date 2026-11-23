/-
  Wilson measure and plaquette-CDF observable definitions for the proposed
  Wilson-to-Schwinger bridge.

  Standard axioms only.
-/
import Mathlib
import Imscribing.YangMills.IIDSchwingerFromWilson
import Imscribing.YangMills.PlaquetteStep3
import Imscribing.YangMills.RademacherMulti
import Imscribing.YangMills.ProbIntegralTransform
import Imscribing.YangMills.SUNHaar

set_option maxHeartbeats 8000000
set_option maxRecDepth 20000

open scoped BigOperators ENNReal NNReal Matrix
open MeasureTheory Set Filter Topology Real

namespace YangMills

/-- Wilson measure: `dμ_Wilson = exp(-β S_W) / Z dμ_Haar`. -/
noncomputable def wilsonMeasure (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt] (β : ℝ)
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)] :
    Measure (GaugeField (cubicTorus4 Ls Lt) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :=
  (spacetimeHaarMeasure Ls Lt N).withDensity
    (fun U => ENNReal.ofReal (cubic4WilsonWeight Ls Lt N β U) /
      ENNReal.ofReal (cubic4PartitionFn Ls Lt N β))

/-- Wilson measure is absolutely continuous w.r.t. Haar measure. -/
theorem wilsonMeasure_abs_cont_haar (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt] (β : ℝ)
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)] (hβ : 0 ≤ β) :
    (wilsonMeasure Ls Lt N β : Measure (GaugeField (cubicTorus4 Ls Lt)
      (Matrix.specialUnitaryGroup (Fin N) ℂ))) ≪ spacetimeHaarMeasure Ls Lt N := by
  change (spacetimeHaarMeasure Ls Lt N).withDensity
    (fun U => ENNReal.ofReal (cubic4WilsonWeight Ls Lt N β U) /
      ENNReal.ofReal (cubic4PartitionFn Ls Lt N β)) ≪ _
  exact withDensity_absolutelyContinuous _ _

/-- The normalized Wilson density has total mass one. -/
theorem wilsonMeasure_isProbability (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt] (β : ℝ)
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)] (hβ : 0 ≤ β) :
    IsProbabilityMeasure (wilsonMeasure Ls Lt N β) := by
  let μ := spacetimeHaarMeasure Ls Lt N
  let w := cubic4WilsonWeight Ls Lt N β
  haveI : IsProbabilityMeasure μ := spacetimeHaarMeasure_prob Ls Lt N
  have hZpos : 0 < cubic4PartitionFn Ls Lt N β := cubic4PartitionFn_pos Ls Lt N β hβ
  have hw_int : Integrable w μ := by
    refine (integrable_const (1 : ℝ)).mono'
      (measurable_cubic4WilsonWeight Ls Lt N β).stronglyMeasurable.aestronglyMeasurable ?_
    filter_upwards with U
    have hw := cubic4WilsonWeight_bounds Ls Lt N β hβ U
    rw [Real.norm_eq_abs, abs_of_nonneg (by unfold w cubic4WilsonWeight; positivity)]
    exact hw.2
  have hw_nonneg : 0 ≤ᵐ[μ] w := by
    filter_upwards with U
    change 0 ≤ Real.exp _
    exact (Real.exp_pos _).le
  have hw_meas : Measurable (fun U => ENNReal.ofReal (w U)) :=
    ENNReal.measurable_ofReal.comp (measurable_cubic4WilsonWeight Ls Lt N β)
  constructor
  change (μ.withDensity
    (fun U => ENNReal.ofReal (w U) / ENNReal.ofReal (cubic4PartitionFn Ls Lt N β)))
      Set.univ = 1
  rw [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ]
  have hden : ENNReal.ofReal (cubic4PartitionFn Ls Lt N β) ≠ 0 :=
    ENNReal.ofReal_ne_zero_iff.mpr hZpos
  change (∫⁻ U, ENNReal.ofReal (w U) *
    (ENNReal.ofReal (cubic4PartitionFn Ls Lt N β))⁻¹ ∂μ) = 1
  rw [lintegral_mul_const _ hw_meas]
  rw [← ofReal_integral_eq_lintegral_ofReal hw_int hw_nonneg]
  have hint : (∫ U, w U ∂μ) = cubic4PartitionFn Ls Lt N β := rfl
  rw [hint]
  exact ENNReal.mul_inv_cancel hden ENNReal.ofReal_ne_top

/-- Plaquette defect: `X_p(U) = 1 - (1/N) Re Tr(U_p)` ∈ [0, 2]. -/
noncomputable def plaquetteDefect (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    (v : (cubicTorus4 Ls Lt).Site) (U : GaugeField (cubicTorus4 Ls Lt)
    (Matrix.specialUnitaryGroup (Fin N) ℂ)) : ℝ :=
  plaquetteDensity Ls Lt N v U

theorem plaquetteDefect_bounds (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    (hN : 1 ≤ N)
    (v : (cubicTorus4 Ls Lt).Site) (U : GaugeField (cubicTorus4 Ls Lt)
    (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    0 ≤ plaquetteDefect Ls Lt N v U ∧ plaquetteDefect Ls Lt N v U ≤ 2 := by
  have hloop := normWilsonLoop4_norm_le_one hN (cubic4Plaquette v 1 2) U
  have hreal : |(normWilsonLoop4 (cubic4Plaquette v 1 2) U).re| ≤ 1 :=
    (Complex.abs_re_le_norm _).trans hloop
  rw [abs_le] at hreal
  constructor <;> dsimp [plaquetteDefect, plaquetteDensity] <;> linarith

theorem measurable_plaquetteDefect (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (v : (cubicTorus4 Ls Lt).Site) :
    Measurable (fun U : GaugeField (cubicTorus4 Ls Lt)
      (Matrix.specialUnitaryGroup (Fin N) ℂ) => plaquetteDefect Ls Lt N v U) := by
  let p : LatticePlaquette (cubicTorus4 Ls Lt) :=
    ⟨v, cubic4Plaquette v 1 2, cubic4Plaquette_isPath v 1 2⟩
  have heq : (fun U : GaugeField (cubicTorus4 Ls Lt)
      (Matrix.specialUnitaryGroup (Fin N) ℂ) => plaquetteDefect Ls Lt N v U) =
      fun U => wilsonPlaquetteTerm p U := by
    funext U
    simp [plaquetteDefect, plaquetteDensity, p, normWilsonLoop4, wilsonPlaquetteTerm]
  rw [heq]
  exact measurable_wilsonPlaquetteTerm4 Ls Lt N p

theorem plaquetteWilson_pushforward_isProbability
    (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt] (β : ℝ) (hβ : 0 ≤ β)
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (v : (cubicTorus4 Ls Lt).Site) :
    IsProbabilityMeasure ((wilsonMeasure Ls Lt N β).map
      (fun U => plaquetteDefect Ls Lt N v U)) := by
  haveI : IsProbabilityMeasure (wilsonMeasure Ls Lt N β) :=
    wilsonMeasure_isProbability Ls Lt N β hβ
  exact Measure.isProbabilityMeasure_map
    (measurable_plaquetteDefect Ls Lt N v).aemeasurable

/-- Fourier orientation selector: `ψ_K(u) = 3/2 - r_K(u)/2 ∈ {1, 2}`. -/
noncomputable def fourierOrientation (K : ℕ) (u : ℝ) : ℝ :=
  (3 / 2 : ℝ) - (1 / 2 : ℝ) * rademacher K u

theorem fourierOrientation_range (K : ℕ) (u : ℝ) :
    fourierOrientation K u = 1 ∨ fourierOrientation K u = 2 := by
  unfold fourierOrientation rademacher
  split <;> norm_num

/-- CDF of plaquette defect under Wilson measure at stage m. -/
noncomputable def plaquetteCDF (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt] (β : ℝ)
    (hβ : 0 ≤ β)
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (v : (cubicTorus4 Ls Lt).Site) (t : ℝ) : ℝ :=
  ProbabilityTheory.cdf
    ((wilsonMeasure Ls Lt N β).map
      (fun U => plaquetteDefect Ls Lt N v U)) t

theorem plaquetteCDF_bounds (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt] (β : ℝ)
    (hβ : 0 ≤ β)
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (v : (cubicTorus4 Ls Lt).Site) (t : ℝ) :
    0 ≤ plaquetteCDF Ls Lt N β hβ v t ∧ plaquetteCDF Ls Lt N β hβ v t ≤ 1 := by
  exact ⟨ProbabilityTheory.cdf_nonneg _ _, ProbabilityTheory.cdf_le_one _ _⟩

/-- Wrap the integer lattice coordinate `⌊x/a⌋` into the periodic direction `Fin L`. -/
noncomputable def stateWrap (L : ℕ) [NeZero L] (a : ℝ) (ha : 0 < a)
    (x : ℝ) : Fin L :=
  Fin.ofNat L (Int.natMod (⌊x / a⌋) L)

/-- Map four real coordinates to the periodic spacetime lattice at spacing `a`. -/
noncomputable def stageSiteMap (Ls Lt : ℕ) [NeZero Ls] [NeZero Lt]
    (a : ℝ) (ha : 0 < a) (x : Space4) :
    (cubicTorus4 Ls Lt).Site :=
  (stateWrap Lt a ha (x 0), stateWrap Ls a ha (x 1),
    stateWrap Ls a ha (x 2), stateWrap Ls a ha (x 3))

/-- The observable: O_m(x, U) = ψ_{K_m}(F_m(X_{p(v_m(x))}(U))). -/
noncomputable def stageObservable (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (β : ℝ) (hβ : 0 ≤ β) (a : ℝ) (ha : 0 < a) (x : Space4) (K : ℕ)
    (U : GaugeField (cubicTorus4 Ls Lt) (Matrix.specialUnitaryGroup (Fin N) ℂ)) : ℝ := by
  let v := stageSiteMap Ls Lt a ha x
  exact fourierOrientation K
    (plaquetteCDF Ls Lt N β hβ v (plaquetteDefect Ls Lt N v U))

theorem stageObservable_range (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (β : ℝ) (hβ : 0 ≤ β) (a : ℝ) (ha : 0 < a) (x : Space4) (K : ℕ)
    (U : GaugeField (cubicTorus4 Ls Lt) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    stageObservable Ls Lt N β hβ a ha x K U = 1 ∨
      stageObservable Ls Lt N β hβ a ha x K U = 2 := by
  exact fourierOrientation_range K _

theorem measurable_fourierOrientation (K : ℕ) : Measurable (fourierOrientation K) := by
  exact measurable_const.sub (measurable_const.mul (rademacher_measurable K))

theorem measurable_stageObservable (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (β : ℝ) (hβ : 0 ≤ β) (a : ℝ) (ha : 0 < a) (x : Space4) (K : ℕ) :
    Measurable (fun U : GaugeField (cubicTorus4 Ls Lt)
      (Matrix.specialUnitaryGroup (Fin N) ℂ) =>
        stageObservable Ls Lt N β hβ a ha x K U) := by
  let v := stageSiteMap Ls Lt a ha x
  let ν := (wilsonMeasure Ls Lt N β).map
    (fun U => plaquetteDefect Ls Lt N v U)
  have hcdf : Measurable (ProbabilityTheory.cdf ν) :=
    (ProbabilityTheory.monotone_cdf ν).measurable
  unfold stageObservable
  exact (measurable_fourierOrientation K).comp
    (hcdf.comp (measurable_plaquetteDefect Ls Lt N v))

end YangMills
