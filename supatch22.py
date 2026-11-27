#!/usr/bin/env python3
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
src = path.read_text(encoding="utf-8")

anchor = "/-- **Explicit Spectral-Gap Upper Bound & Convergence to `0` (`0 sorry`):**"
assert src.count(anchor) == 1

helpers2 = """private lemma wilsonKernel_jump_le (L N : ℕ) [NeZero L] (hN : 1 ≤ N)
    {β : ℝ} (hβ : 0 ≤ β)
    (U U' : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonKernel β (cubicPlaquettes L) (wilsonGramKernel L N (cubicLinkKineticKernel L N β))
        U U' ≤
      Real.exp ((3 * (L : ℝ) ^ 3) * β - (β / (8 * (N : ℝ))) *
        ∑ e : (cubicTorus3 L).Link, frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))) := by
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  have h_act : Real.exp (-(1 / 2 : ℝ) * (wilsonAction β (cubicPlaquettes L) U +
      wilsonAction β (cubicPlaquettes L) U')) ≤ 1 := by
    rw [Real.exp_le_one_iff]
    have h1 := wilsonAction_nonneg_of_nonneg hN hβ (cubicPlaquettes L) U
    have h2 := wilsonAction_nonneg_of_nonneg hN hβ (cubicPlaquettes L) U'
    linarith
  have h_cont : Continuous (fun W : G_L =>
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) :=
    ((continuous_cubicLinkKineticKernel L N β).comp (continuous_const.prodMk continuous_id)).mul
      ((continuous_cubicLinkKineticKernel L N β).comp (continuous_const.prodMk continuous_id))
  have h_int : MeasureTheory.Integrable (fun W : G_L =>
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) μ :=
    integrable_of_continuous_compact μ _ h_cont
  have h_kin : wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' ≤
      Real.exp ((3 * (L : ℝ) ^ 3) * β - (β / (8 * (N : ℝ))) *
        ∑ e : (cubicTorus3 L).Link, frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))) := by
    unfold wilsonGramKernel
    calc ∫ W, cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W ∂μ
        ≤ ∫ _W, Real.exp ((3 * (L : ℝ) ^ 3) * β - (β / (8 * (N : ℝ))) *
            ∑ e : (cubicTorus3 L).Link, frobeniusNormSq
              ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))) ∂μ :=
          MeasureTheory.integral_mono h_int (MeasureTheory.integrable_const _)
            (fun W => cubicLinkKineticKernel_mul_le L N hN hβ U U' W)
      _ = _ := by simp [Measure.real, MeasureTheory.measure_univ]
  unfold wilsonKernel
  calc Real.exp (-(1 / 2 : ℝ) * (wilsonAction β (cubicPlaquettes L) U +
          wilsonAction β (cubicPlaquettes L) U')) *
        wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U'
      ≤ 1 * wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' :=
        mul_le_mul_of_nonneg_right h_act
          (wilsonGramKernel_nonneg L N (cubicLinkKineticKernel L N β)
            (fun X Y => (linkChiLb_pos L β).le.trans
              (cubicLinkKineticKernel_bounds L N hN β hβ X Y).1) U U')
    _ = wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' := one_mul _
    _ ≤ _ := h_kin

private lemma latticeHaar_ball_ge (L N : ℕ) [NeZero L] [NeZero N]
    {β : ℝ} (hβ : 0 < β) :
    let K : ℕ := Nat.ceil (4 * (N : ℝ) / (1 / Real.sqrt β)) + 1
    let B_link : Set (Matrix.specialUnitaryGroup (Fin N) ℂ) :=
      { A | frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ (1 / Real.sqrt β) ^ 2 }
    let B_prod : Set (GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :=
      Set.pi Set.univ (fun _ => B_link)
    MeasurableSet B_prod ∧
      (1 : ℝ) / ((K : ℝ) ^ (2 * N * N)) ^ (3 * L ^ 3) ≤
        (latticeHaarMeasure L N).real B_prod := by
  intro K B_link B_prod
  have hB_link_meas : MeasurableSet B_link := by
    have hc : Continuous (fun A : Matrix.specialUnitaryGroup (Fin N) ℂ =>
        frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1)) := by
      unfold frobeniusNormSq
      refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
      simp only [Matrix.sub_apply]
      exact (continuous_norm.comp (((continuous_apply j).comp
        ((continuous_apply i).comp continuous_subtype_val)).sub continuous_const)).pow 2
    exact measurableSet_Iic.preimage hc.measurable
  have hB_prod_meas : MeasurableSet B_prod := by
    change MeasurableSet (Set.pi Set.univ fun _ => B_link)
    convert MeasurableSet.univ_pi fun _ => hB_link_meas
  refine ⟨hB_prod_meas, ?_⟩
  have h_pi : latticeHaarMeasure L N B_prod = (suHaar N B_link) ^ (3 * L ^ 3) := by
    dsimp only [B_prod]
    erw [MeasureTheory.Measure.pi_pi (fun _ => suHaar N) _]
    rw [Finset.prod_const, Finset.card_univ, cubicLink_card]
  have h_real_eq : (latticeHaarMeasure L N).real B_prod = (suHaar N B_link).toReal ^ (3 * L ^ 3) := by
    rw [Measure.real_def, h_pi, ENNReal.toReal_pow]
  rw [h_real_eq]
  have h_ball := suHaar_ball_ge N (one_div_pos.mpr (Real.sqrt_pos.mpr hβ))
  have h_nonneg : 0 ≤ (1 : ℝ) / ((K : ℝ) ^ (2 * N * N)) := by positivity
  calc (1 : ℝ) / ((K : ℝ) ^ (2 * N * N)) ^ (3 * L ^ 3)
      = ((1 : ℝ) / ((K : ℝ) ^ (2 * N * N))) ^ (3 * L ^ 3) := by
          rw [div_pow, one_pow]
    _ ≤ (suHaar N B_link).toReal ^ (3 * L ^ 3) :=
          pow_le_pow_left₀ h_nonneg h_ball _

private lemma wilsonKernel_ball_ge (L N : ℕ) [NeZero L] (hN : 1 ≤ N)
    {β : ℝ} (hβ : 0 < β)
    (B_prod : Set (GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)))
    (hB_meas : MeasurableSet B_prod)
    (hB_sub : ∀ U ∈ B_prod, ∀ e,
      frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 1 / β)
    {U U' : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)}
    (hU : U ∈ B_prod) (hU' : U' ∈ B_prod) :
    (latticeHaarMeasure L N).real B_prod *
        Real.exp ((3 * (L : ℝ) ^ 3) * β - 30 * (L : ℝ) ^ 3 / (N : ℝ)) ≤
      wilsonKernel β (cubicPlaquettes L) (wilsonGramKernel L N (cubicLinkKineticKernel L N β))
        U U' := by
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  have h_act_U := wilsonAction_ball_le L N hN hβ U (hB_sub U hU)
  have h_act_U' := wilsonAction_ball_le L N hN hβ U' (hB_sub U' hU')
  have h_exp_act : Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) ≤
      Real.exp (-(1 / 2 : ℝ) * (wilsonAction β (cubicPlaquettes L) U +
        wilsonAction β (cubicPlaquettes L) U')) := by
    apply Real.exp_le_exp.mpr
    linarith
  let c_k : ℝ := Real.exp ((3 * (L : ℝ) ^ 3) * β - 6 * (L : ℝ) ^ 3 / (N : ℝ))
  have h_cont : Continuous (fun W : G_L =>
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) :=
    ((continuous_cubicLinkKineticKernel L N β).comp (continuous_const.prodMk continuous_id)).mul
      ((continuous_cubicLinkKineticKernel L N β).comp (continuous_const.prodMk continuous_id))
  have h_int : MeasureTheory.Integrable (fun W : G_L =>
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) μ :=
    integrable_of_continuous_compact μ _ h_cont
  have h_ind_le : ∀ W : G_L, B_prod.indicator (fun _ => c_k) W ≤
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W := by
    intro W
    by_cases hW : W ∈ B_prod
    · rw [Set.indicator_of_mem hW]
      have hk1 := cubicLinkKineticKernel_ball_ge L N hN hβ U W (hB_sub U hU) (hB_sub W hW)
      have hk2 := cubicLinkKineticKernel_ball_ge L N hN hβ U' W (hB_sub U' hU') (hB_sub W hW)
      have h_mul := mul_le_mul hk1 hk2 (Real.exp_pos _).le
        ((linkChiLb_pos L β).le.trans (cubicLinkKineticKernel_bounds L N hN β hβ.le U W).1)
      rw [← Real.exp_add] at h_mul
      convert h_mul using 2
      ring
    · rw [Set.indicator_of_notMem hW]
      have hnn1 := (linkChiLb_pos L β).le.trans
        (cubicLinkKineticKernel_bounds L N hN β hβ.le U W).1
      have hnn2 := (linkChiLb_pos L β).le.trans
        (cubicLinkKineticKernel_bounds L N hN β hβ.le U' W).1
      exact mul_nonneg hnn1 hnn2
  have h_ind_int : MeasureTheory.Integrable (B_prod.indicator (fun _ : G_L => c_k)) μ :=
    (MeasureTheory.integrable_const c_k).indicator hB_meas
  have h_kin_ge : μ.real B_prod * c_k ≤
      wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' := by
    unfold wilsonGramKernel
    calc μ.real B_prod * c_k
        = ∫ W, B_prod.indicator (fun _ => c_k) W ∂μ := by
            rw [MeasureTheory.integral_indicator hB_meas, MeasureTheory.setIntegral_const,
              smul_eq_mul]
      _ ≤ ∫ W, cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W ∂μ :=
            MeasureTheory.integral_mono h_ind_int h_int h_ind_le
  unfold wilsonKernel
  calc μ.real B_prod * Real.exp ((3 * (L : ℝ) ^ 3) * β - 30 * (L : ℝ) ^ 3 / (N : ℝ))
      = Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) * (μ.real B_prod * c_k) := by
          dsimp only [c_k]
          rw [mul_left_comm, ← Real.exp_add]
          congr 2
          ring
    _ ≤ Real.exp (-(1 / 2 : ℝ) * (wilsonAction β (cubicPlaquettes L) U +
          wilsonAction β (cubicPlaquettes L) U')) *
          wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' :=
          mul_le_mul h_exp_act h_kin_ge
            (mul_nonneg MeasureTheory.measureReal_nonneg (Real.exp_pos _).le)
            (Real.exp_pos _).le

private lemma lam0_ball_lb (L N : ℕ) [NeZero L] {β : ℝ} (hβ : 0 ≤ β)
    (K_kin : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) →
      GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℝ)
    (hK_cont : Continuous (Function.uncurry K_kin))
    (hK_nn : ∀ U U', 0 ≤ K_kin U U')
    (M_K : ℝ) (hM_K : 0 ≤ M_K) (hK_bd : ∀ U U', K_kin U U' ≤ M_K)
    (B_prod : Set (GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)))
    (hB_meas : MeasurableSet B_prod)
    (hB_pos : 0 < (latticeHaarMeasure L N).real B_prod)
    (c_min_W : ℝ) (hc_nn : 0 ≤ c_min_W)
    (h_ball_ge : ∀ U ∈ B_prod, ∀ U' ∈ B_prod,
      c_min_W ≤ wilsonKernel β (cubicPlaquettes L) K_kin U U') :
    (latticeHaarMeasure L N).real B_prod * c_min_W ≤
      ‖wilsonIntegralOp L N β hβ K_kin hK_cont hK_nn M_K hM_K hK_bd‖ := by
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  let T_raw := wilsonIntegralOp L N β hβ K_kin hK_cont hK_nn M_K hM_K hK_bd
  let K_W := wilsonKernel β (cubicPlaquettes L) K_kin
  let c_r : ℝ := 1 / Real.sqrt (μ.real B_prod)
  have hc_r_nn : 0 ≤ c_r := by positivity
  let φ_fn : G_L → ℂ := B_prod.indicator (fun _ => (c_r : ℂ))
  have hφ_meas : Measurable φ_fn := measurable_const.indicator hB_meas
  have hφ_bd : ∀ U, ‖φ_fn U‖ ≤ c_r := fun U => by
    dsimp only [φ_fn]
    by_cases hU : U ∈ B_prod
    · rw [Set.indicator_of_mem hU, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg hc_r_nn]
    · rw [Set.indicator_of_notMem hU, norm_zero]
      exact hc_r_nn
  have hφ_mem : MeasureTheory.MemLp φ_fn 2 μ :=
    memLp_two_of_measurable_bound μ φ_fn hφ_meas c_r hc_r_nn hφ_bd
  let φ : HaarGaugeSpace μ := hφ_mem.toLp φ_fn
  have hφ_sq : ‖φ‖ ^ 2 = 1 := by
    have hin : ⟪φ, φ⟫_ℂ = ((∫ U, ‖φ_fn U‖ ^ 2 ∂μ : ℝ) : ℂ) := by
      rw [MeasureTheory.L2.inner_def]
      have hcoe := hφ_mem.coeFn_toLp
      calc ∫ U, ⟪φ U, φ U⟫_ℂ ∂μ
          = ∫ U, ((‖φ_fn U‖ ^ 2 : ℝ) : ℂ) ∂μ := by
              refine MeasureTheory.integral_congr_ae ?_
              filter_upwards [hcoe] with U hU
              change ⟪⇑φ U, ⇑φ U⟫_ℂ = _
              rw [hU]
              simp [← Complex.normSq_eq_norm_sq, Complex.normSq_apply, Complex.mul_re,
                Complex.mul_im, sq]
              ring
        _ = _ := integral_complex_ofReal
    have hre : ‖φ‖ ^ 2 = ∫ U, ‖φ_fn U‖ ^ 2 ∂μ := by
      have hr := congrArg Complex.re hin
      rw [inner_self_eq_norm_sq_to_K] at hr
      simpa [pow_two] using hr
    rw [hre]
    have h_ind_sq : (fun U => ‖φ_fn U‖ ^ 2) = B_prod.indicator (fun _ => 1 / μ.real B_prod) := by
      funext U
      dsimp only [φ_fn]
      by_cases hU : U ∈ B_prod
      · rw [Set.indicator_of_mem hU, Set.indicator_of_mem hU, Complex.norm_real,
          Real.norm_eq_abs, abs_of_nonneg hc_r_nn]
        dsimp only [c_r]
        rw [one_div, inv_pow, Real.sq_sqrt hB_pos.le, one_div]
      · rw [Set.indicator_of_notMem hU, Set.indicator_of_notMem hU, norm_zero, zero_pow two_ne_zero]
    rw [h_ind_sq, MeasureTheory.integral_indicator hB_meas, MeasureTheory.setIntegral_const,
      smul_eq_mul, mul_one_div_cancel hB_pos.ne']
  have hφ_norm : ‖φ‖ = 1 := by
    have h1 : (‖φ‖ - 1) * (‖φ‖ + 1) = 0 := by linarith
    rcases mul_eq_zero.mp h1 with h | h <;> linarith [norm_nonneg φ]
  have h_ray_ub : (⟪φ, T_raw φ⟫_ℂ).re ≤ ‖T_raw‖ := by
    calc (⟪φ, T_raw φ⟫_ℂ).re ≤ ‖⟪φ, T_raw φ⟫_ℂ‖ := (le_abs_self _).trans (Complex.abs_re_le_norm _)
      _ ≤ ‖φ‖ * ‖T_raw φ‖ := norm_inner_le_norm _ _
      _ ≤ ‖φ‖ * (‖T_raw‖ * ‖φ‖) := mul_le_mul_of_nonneg_left (T_raw.le_opNorm φ) (norm_nonneg φ)
      _ = ‖T_raw‖ := by rw [hφ_norm]; ring
  have hl2 := MeasureTheory.L2.integrable_inner (𝕜 := ℂ) φ (T_raw φ)
  have h1 := wilsonIntegralOp_apply_ae L N β hβ K_kin hK_cont hK_nn M_K hM_K hK_bd φ
  have h2 := hφ_mem.coeFn_toLp
  have h_eq_fn : (fun U => (⟪φ U, (T_raw φ) U⟫_ℂ).re) =ᵐ[μ]
      fun U => (1 / μ.real B_prod) *
        B_prod.indicator (fun U => ∫ U', B_prod.indicator (fun U' => K_W U U') U' ∂μ) U := by
    filter_upwards [h1, h2] with U hu1 hu2
    change RCLike.re ⟪⇑φ U, ⇑(T_raw φ) U⟫_ℂ = _
    rw [hu1, hu2]
    dsimp [wilsonIntegralFn]
    have h_in_ae : (fun U' => ((K_W U U' : ℝ) : ℂ) * ⇑φ U') =ᵐ[μ]
        fun U' => ((B_prod.indicator (fun U' => K_W U U' * c_r) U' : ℝ) : ℂ) := by
      filter_upwards [h2] with U' hu'
      rw [hu']
      dsimp only [φ_fn]
      by_cases hU' : U' ∈ B_prod
      · simp [hU']
      · simp [hU']
    rw [MeasureTheory.integral_congr_ae h_in_ae, integral_complex_ofReal]
    by_cases hU : U ∈ B_prod
    · have hφU : φ_fn U = (c_r : ℂ) := Set.indicator_of_mem hU _
      rw [hφU, Set.indicator_of_mem hU]
      have h_re : RCLike.re ⟪(c_r : ℂ), ((∫ U', B_prod.indicator
          (fun U' => K_W U U' * c_r) U' ∂μ : ℝ) : ℂ)⟫_ℂ =
          c_r * ∫ U', B_prod.indicator (fun U' => K_W U U' * c_r) U' ∂μ := by
        simp [Complex.mul_re]
      rw [h_re]
      have h_ind_eq : B_prod.indicator (fun U' => K_W U U' * c_r) =
          fun U' => c_r * B_prod.indicator (fun U' => K_W U U') U' := by
        funext U'
        by_cases hU' : U' ∈ B_prod <;> simp [hU', mul_comm]
      rw [h_ind_eq, MeasureTheory.integral_const_mul, ← mul_assoc]
      have hc2 : c_r * c_r = 1 / μ.real B_prod := by
        dsimp only [c_r]
        rw [one_div_mul_one_div, Real.mul_self_sqrt hB_pos.le]
      rw [hc2]
    · have hφU : φ_fn U = 0 := Set.indicator_of_notMem hU _
      rw [hφU, Set.indicator_of_notMem hU]
      simp
  have h_outer_int : MeasureTheory.Integrable (fun U => (1 / μ.real B_prod) *
      B_prod.indicator (fun U => ∫ U', B_prod.indicator (fun U' => K_W U U') U' ∂μ) U) μ :=
    hl2.re.congr h_eq_fn
  have h_ray_eq : (⟪φ, T_raw φ⟫_ℂ).re = ∫ U, (1 / μ.real B_prod) *
      B_prod.indicator (fun U => ∫ U', B_prod.indicator (fun U' => K_W U U') U' ∂μ) U ∂μ := by
    rw [MeasureTheory.L2.inner_def]
    change RCLike.re (∫ U, ⟪φ U, (T_raw φ) U⟫_ℂ ∂μ) = _
    rw [← integral_re hl2]
    exact MeasureTheory.integral_congr_ae h_eq_fn
  have h_low_fn : ∀ U, (1 / μ.real B_prod) * B_prod.indicator (fun _ => μ.real B_prod * c_min_W) U ≤
      (1 / μ.real B_prod) *
        B_prod.indicator (fun U => ∫ U', B_prod.indicator (fun U' => K_W U U') U' ∂μ) U := by
    intro U
    refine mul_le_mul_of_nonneg_left ?_ (by positivity)
    by_cases hU : U ∈ B_prod
    · rw [Set.indicator_of_mem hU, Set.indicator_of_mem hU]
      have hK_int : MeasureTheory.Integrable (B_prod.indicator (fun U' => K_W U U')) μ :=
        (integrable_of_continuous_compact μ _
          (continuous_cubicWilsonKernel_right L N β K_kin hK_cont U)).indicator hB_meas
      have hc_int : MeasureTheory.Integrable (B_prod.indicator (fun _ : G_L => c_min_W)) μ :=
        (MeasureTheory.integrable_const c_min_W).indicator hB_meas
      calc μ.real B_prod * c_min_W
          = ∫ U', B_prod.indicator (fun _ => c_min_W) U' ∂μ := by
              rw [MeasureTheory.integral_indicator hB_meas, MeasureTheory.setIntegral_const,
                smul_eq_mul]
        _ ≤ ∫ U', B_prod.indicator (fun U' => K_W U U') U' ∂μ := by
              refine MeasureTheory.integral_mono hc_int hK_int fun U' => ?_
              by_cases hU' : U' ∈ B_prod
              · rw [Set.indicator_of_mem hU', Set.indicator_of_mem hU']
                exact h_ball_ge U hU U' hU'
              · rw [Set.indicator_of_notMem hU', Set.indicator_of_notMem hU']
    · rw [Set.indicator_of_notMem hU, Set.indicator_of_notMem hU]
  have h_const_int : MeasureTheory.Integrable
      (fun U : G_L => (1 / μ.real B_prod) * B_prod.indicator (fun _ => μ.real B_prod * c_min_W) U) μ :=
    ((MeasureTheory.integrable_const (μ.real B_prod * c_min_W)).indicator hB_meas).const_mul _
  calc μ.real B_prod * c_min_W
      = (1 / μ.real B_prod) * (μ.real B_prod * (μ.real B_prod * c_min_W)) := by
          field_simp [hB_pos.ne']
    _ = ∫ U, (1 / μ.real B_prod) * B_prod.indicator (fun _ => μ.real B_prod * c_min_W) U ∂μ := by
          rw [MeasureTheory.integral_const_mul, MeasureTheory.integral_indicator hB_meas,
            MeasureTheory.setIntegral_const, smul_eq_mul]
    _ ≤ (⟪φ, T_raw φ⟫_ℂ).re := by
          rw [h_ray_eq]
          exact MeasureTheory.integral_mono h_const_int h_outer_int h_low_fn
    _ ≤ ‖T_raw‖ := h_ray_ub

"""

src = src.replace(anchor, helpers2 + anchor, 1)
path.write_text(src, encoding="utf-8")
print("Patched Patch 2/3 successfully.")