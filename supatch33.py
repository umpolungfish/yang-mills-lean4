#!/usr/bin/env python3
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
src = path.read_text(encoding="utf-8")

anchor = "/-- **Explicit Spectral-Gap Upper Bound & Convergence to `0` (`0 sorry`):**"
assert src.count(anchor) == 1

helpers3 = """private lemma fullRank_dirichlet_step (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    {β : ℝ} (hβ_pos : 0 < β)
    (e_flip : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) ≃ᵐ
      GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ))
    (hmp : MeasureTheory.MeasurePreserving e_flip
      (latticeHaarMeasure L N) (latticeHaarMeasure L N))
    (h_flip_e0 : ∀ U, (e_flip U) ((0, 0, 0), 0) =
      centralElem N hN * U ((0, 0, 0), 0))
    (S : LatticeGaugeSetup (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
      (HaarGaugeSpace (latticeHaarMeasure L N)))
    (Ω : HaarGaugeSpace (latticeHaarMeasure L N))
    (ω : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℝ)
    (hgs : IsWilsonGroundState L N β hβ_pos.le
      (wilsonGramKernel L N (cubicLinkKineticKernel L N β))
      (continuous_wilsonGramKernel L N (cubicLinkKineticKernel L N β)
        (continuous_cubicLinkKineticKernel L N β)
        (linkChi_nn L N hN β hβ_pos.le) (linkChiUb L β) (linkChiUb_nonneg L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2))
      (wilsonGramKernel_nonneg L N (cubicLinkKineticKernel L N β)
        (linkChi_nn L N hN β hβ_pos.le))
      ((linkChiUb L β) ^ 2) (sq_nonneg _)
      (wilsonGramKernel_le L N (cubicLinkKineticKernel L N β)
        (continuous_cubicLinkKineticKernel L N β)
        (linkChi_nn L N hN β hβ_pos.le) (linkChiUb L β) (linkChiUb_nonneg L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2))
      Ω ω)
    (hS_Ω : S.Ω = Ω)
    (hS_T : S.T = ((‖fullRankTRaw L N β hβ_pos.le (cubicLinkKineticKernel L N β)
      (continuous_cubicLinkKineticKernel L N β) (linkChiLb L β) (linkChiLb_pos L β)
      (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).1)
      (linkChiUb L β) (linkChiUb_nonneg L β)
      (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2)‖⁻¹ : ℝ) : ℂ) •
      fullRankTRaw L N β hβ_pos.le (cubicLinkKineticKernel L N β)
        (continuous_cubicLinkKineticKernel L N β) (linkChiLb L β) (linkChiLb_pos L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).1)
        (linkChiUb L β) (linkChiUb_nonneg L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2))
    (hS_a : S.a = 1)
    (hω_flip : ∀ U, ω (e_flip U) = ω U) :
    (N : ℝ) - Real.exp (-S.Δ) * (N : ℝ) ≤
      (2 * ‖fullRankTRaw L N β hβ_pos.le (cubicLinkKineticKernel L N β)
        (continuous_cubicLinkKineticKernel L N β) (linkChiLb L β) (linkChiLb_pos L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).1)
        (linkChiUb L β) (linkChiUb_nonneg L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2)‖)⁻¹ *
        ∫ U, ∫ U', wilsonKernel β (cubicPlaquettes L)
          (wilsonGramKernel L N (cubicLinkKineticKernel L N β)) U U' * ω U * ω U' *
          frobeniusNormSq ((U ((0, 0, 0), 0) : Matrix (Fin N) (Fin N) ℂ) -
            (U' ((0, 0, 0), 0) : Matrix (Fin N) (Fin N) ℂ))
          ∂(latticeHaarMeasure L N) ∂(latticeHaarMeasure L N) ∧
    (∀ U, ∫ U', wilsonKernel β (cubicPlaquettes L)
        (wilsonGramKernel L N (cubicLinkKineticKernel L N β)) U U' * ω U'
        ∂(latticeHaarMeasure L N) =
      ‖fullRankTRaw L N β hβ_pos.le (cubicLinkKineticKernel L N β)
        (continuous_cubicLinkKineticKernel L N β) (linkChiLb L β) (linkChiLb_pos L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).1)
        (linkChiUb L β) (linkChiUb_nonneg L β)
        (fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2)‖ * ω U) ∧
    ∫ U, ω U ^ 2 ∂(latticeHaarMeasure L N) = 1 ∧
    ∫ U, ω U ∂(latticeHaarMeasure L N) ≤ 1 := by
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  let χ := cubicLinkKineticKernel L N β
  let K_kin := wilsonGramKernel L N χ
  let K_W := wilsonKernel β (cubicPlaquettes L) K_kin
  have hχ_cont := continuous_cubicLinkKineticKernel L N β
  have hχ_nn := linkChi_nn L N hN β hβ_pos.le
  have hχ_lb := fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).1
  have hχ_bd := fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2
  have hK_cont := continuous_wilsonGramKernel L N χ hχ_cont hχ_nn
    (linkChiUb L β) (linkChiUb_nonneg L β) hχ_bd
  have hK_nn := wilsonGramKernel_nonneg L N χ hχ_nn
  have hK_bd := wilsonGramKernel_le L N χ hχ_cont hχ_nn
    (linkChiUb L β) (linkChiUb_nonneg L β) hχ_bd
  let T_raw := fullRankTRaw L N β hβ_pos.le χ hχ_cont (linkChiLb L β) (linkChiLb_pos L β)
    hχ_lb (linkChiUb L β) (linkChiUb_nonneg L β) hχ_bd
  let lam0 : ℝ := ‖T_raw‖
  have hlam0_pos : 0 < lam0 := hgs.norm_pos
  have hω_eig : ∀ U, ∫ U', K_W U U' * ω U' ∂μ = lam0 * ω U := by
    have h_ae1 := wilsonIntegralOp_apply_ae L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd Ω
    have h_ae2 : ⇑((lam0 : ℂ) • Ω) =ᵐ[μ] fun U => ((lam0 * ω U : ℝ) : ℂ) := by
      filter_upwards [MeasureTheory.Lp.coeFn_smul (lam0 : ℂ) Ω, hgs.ae_eq] with U hsm hω
      simp only [Pi.smul_apply, smul_eq_mul] at hsm
      rw [hsm, hω]
      push_cast; rfl
    have h_eig_T : T_raw Ω = (lam0 : ℂ) • Ω := hgs.eig
    have h_fn_ae : wilsonIntegralFn L N β K_kin Ω =ᵐ[μ] fun U => ((lam0 * ω U : ℝ) : ℂ) := by
      filter_upwards [h_ae1, h_ae2] with U hu1 hu2
      have hu1' : ⇑(T_raw Ω) U = wilsonIntegralFn L N β K_kin Ω U := hu1
      rw [← hu1', h_eig_T]
      exact hu2
    have h_pt := eq_of_ae_continuous μ
      (wilsonIntegralFn_continuous L N β hβ_pos.le K_kin hK_cont hK_nn
        ((linkChiUb L β) ^ 2) hK_bd Ω)
      (Complex.continuous_ofReal.comp (continuous_const.mul hgs.ω_cont)) h_fn_ae
    intro U
    have hU := h_pt U
    have h_in : wilsonIntegralFn L N β K_kin Ω U = ((∫ U', K_W U U' * ω U' ∂μ : ℝ) : ℂ) := by
      dsimp [wilsonIntegralFn]
      calc ∫ U', ((K_W U U' : ℝ) : ℂ) * ⇑Ω U' ∂μ
          = ∫ U', ((K_W U U' * ω U' : ℝ) : ℂ) ∂μ := by
              refine MeasureTheory.integral_congr_ae ?_
              filter_upwards [hgs.ae_eq] with U' hω'
              rw [hω']; push_cast; rfl
        _ = ((∫ U', K_W U U' * ω U' ∂μ : ℝ) : ℂ) := integral_complex_ofReal
    rw [h_in] at hU
    exact Complex.ofReal_injective hU
  have h_om_sq : ∫ U, ω U ^ 2 ∂μ = 1 := by
    have hl2 := MeasureTheory.L2.integrable_inner (𝕜 := ℂ) Ω Ω
    have h1 : ‖Ω‖ ^ 2 = RCLike.re (⟪Ω, Ω⟫_ℂ) := by
      rw [inner_self_eq_norm_sq_to_K]
      simp [pow_two]
    rw [hgs.unit, one_pow, MeasureTheory.L2.inner_def, ← integral_re hl2] at h1
    have h_ae : (fun U => RCLike.re ⟪⇑Ω U, ⇑Ω U⟫_ℂ) =ᵐ[μ] fun U => ω U ^ 2 := by
      filter_upwards [hgs.ae_eq] with U hU
      rw [hU, inner_self_eq_norm_sq_to_K]
      simp [pow_two]
    rw [MeasureTheory.integral_congr_ae h_ae] at h1
    exact h1.symm
  have h_om_l1 : ∫ U, ω U ∂μ ≤ 1 := by
    have hl1 := l1_le_l2_prob μ Ω
    rw [hgs.unit] at hl1
    have h_ae : (fun U => ‖⇑Ω U‖) =ᵐ[μ] fun U => ω U := by
      filter_upwards [hgs.ae_eq] with U hU
      rw [hU, Complex.norm_real, Real.norm_of_nonneg (hgs.ω_pos U).le]
    rw [MeasureTheory.integral_congr_ae h_ae] at hl1
    exact hl1
  let e₀ : (cubicTorus3 L).Link := ((0, 0, 0), 0)
  let entry : Fin N → Fin N → G_L → ℂ := fun i j U =>
    ((U e₀ : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) i j
  have h_entry_cont : ∀ i j, Continuous (entry i j) := fun i j =>
    (continuous_apply j).comp ((continuous_apply i).comp
      (continuous_subtype_val.comp (continuous_apply e₀)))
  have h_entry_bd : ∀ i j U, ‖entry i j U‖ ≤ 2 := fun i j U => by
    rw [← sq_le_sq₀ (norm_nonneg _) (by positivity), ← Complex.normSq_eq_norm_sq,
      Complex.normSq_apply]
    have h := su_entry_re_im_bound (U e₀) i j
    nlinarith [h.1, h.2.1, h.2.2.1, h.2.2.2]
  obtain ⟨M_ω0, hM_ω0⟩ := isCompact_univ.exists_bound_of_continuousOn hgs.ω_cont.continuousOn
  let M_ω : ℝ := max M_ω0 0
  have hM_ω_nn : 0 ≤ M_ω := le_max_right _ _
  have hM_ω_bd : ∀ U : G_L, ‖ω U‖ ≤ M_ω := fun U =>
    (hM_ω0 U (Set.mem_univ U)).trans (le_max_left _ _)
  let ψ_fn : Fin N → Fin N → G_L → ℂ := fun i j U => entry i j U * (ω U : ℂ)
  have hψ_mem : ∀ i j, MeasureTheory.MemLp (ψ_fn i j) 2 μ := fun i j =>
    memLp_two_of_measurable_bound μ (ψ_fn i j)
      ((h_entry_cont i j).mul (Complex.continuous_ofReal.comp hgs.ω_cont)).measurable
      (2 * M_ω) (by positivity) fun U => by
        rw [norm_mul, Complex.norm_real]
        exact mul_le_mul (h_entry_bd i j U) (hM_ω_bd U) (norm_nonneg _) (by positivity)
  let ψ : Fin N → Fin N → HaarGaugeSpace μ := fun i j => (hψ_mem i j).toLp (ψ_fn i j)
  have hψ_orth : ∀ i j, ⟪ψ i j, S.Ω⟫_ℂ = 0 := by
    intro i j
    let c : ℂ := Complex.exp (2 * Real.pi * Complex.I / (N : ℂ))
    have h_entry_flip : ∀ U, entry i j (e_flip U) = c * entry i j U := by
      intro U
      dsimp [entry]
      rw [h_flip_e0 U]
      change ((c • (1 : Matrix (Fin N) (Fin N) ℂ)) *
          (U e₀ : Matrix (Fin N) (Fin N) ℂ)) i j =
        c * ((U e₀ : Matrix (Fin N) (Fin N) ℂ)) i j
      simp [Matrix.smul_mul]
    have hcoe := (hψ_mem i j).coeFn_toLp
    have h_int1 : ⟪Ω, ψ i j⟫_ℂ = ∫ U, (ω U : ℂ) * (entry i j U * (ω U : ℂ)) ∂μ := by
      rw [MeasureTheory.L2.inner_def]
      refine MeasureTheory.integral_congr_ae ?_
      filter_upwards [hgs.ae_eq, hcoe] with U hU1 hU2
      change ⟪⇑Ω U, ⇑(ψ i j) U⟫_ℂ = _
      rw [hU1, hU2]
      simp only [RCLike.inner_apply, Complex.star_def, Complex.conj_ofReal]
      ring
    have h_inner_eq : ⟪Ω, ψ i j⟫_ℂ = c * ⟪Ω, ψ i j⟫_ℂ := by
      rw [h_int1]
      calc ∫ U, (ω U : ℂ) * (entry i j U * (ω U : ℂ)) ∂μ
          = ∫ U, (ω (e_flip U) : ℂ) * (entry i j (e_flip U) * (ω (e_flip U) : ℂ)) ∂μ :=
              (hmp.integral_comp' (fun U => (ω U : ℂ) * (entry i j U * (ω U : ℂ)))).symm
        _ = ∫ U, c * ((ω U : ℂ) * (entry i j U * (ω U : ℂ))) ∂μ := by
              refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
              rw [hω_flip U, h_entry_flip U]; ring
        _ = c * ∫ U, (ω U : ℂ) * (entry i j U * (ω U : ℂ)) ∂μ :=
              MeasureTheory.integral_const_mul c _
        _ = c * ⟪Ω, ψ i j⟫_ℂ := by rw [← h_int1]
    have h_mul0 : (1 - c) * ⟪Ω, ψ i j⟫_ℂ = 0 := by linear_combination h_inner_eq
    have hc1 : 1 - c ≠ 0 := sub_ne_zero.mpr (Ne.symm (centralElem_ne_one N hN))
    have hΩψ : ⟪Ω, ψ i j⟫_ℂ = 0 := (mul_eq_zero.mp h_mul0).resolve_left hc1
    rw [hS_Ω, ← inner_conj_symm, hΩψ, map_zero]
  have hψ_norm_sum : ∑ i : Fin N, ∑ j : Fin N, ‖ψ i j‖ ^ 2 = (N : ℝ) := by
    have h_each : ∀ i j : Fin N,
        ‖ψ i j‖ ^ 2 = ∫ U, ‖entry i j U‖ ^ 2 * ω U ^ 2 ∂μ := by
      intro i j
      have hcoe := (hψ_mem i j).coeFn_toLp
      have hl2 := MeasureTheory.L2.integrable_inner (𝕜 := ℂ) (ψ i j) (ψ i j)
      have h_re : ‖ψ i j‖ ^ 2 = RCLike.re (⟪ψ i j, ψ i j⟫_ℂ) := by
        rw [inner_self_eq_norm_sq_to_K]; simp [pow_two]
      rw [h_re, MeasureTheory.L2.inner_def, ← integral_re hl2]
      refine MeasureTheory.integral_congr_ae ?_
      filter_upwards [hcoe] with U hU
      change RCLike.re ⟪⇑(ψ i j) U, ⇑(ψ i j) U⟫_ℂ = _
      rw [hU]
      have h_id : RCLike.re ⟪entry i j U * (ω U : ℂ), entry i j U * (ω U : ℂ)⟫_ℂ =
          ‖entry i j U * (ω U : ℂ)‖ ^ 2 := by
        rw [inner_self_eq_norm_sq_to_K]; simp [pow_two]
      rw [h_id, norm_mul, mul_pow, Complex.norm_real, Real.norm_eq_abs, sq_abs]
    simp_rw [h_each]
    have h_int_ij : ∀ i j : Fin N,
        MeasureTheory.Integrable (fun U => ‖entry i j U‖ ^ 2 * ω U ^ 2) μ := fun i j =>
      integrable_of_continuous_compact μ _
        (((h_entry_cont i j).norm.pow 2).mul (hgs.ω_cont.pow 2))
    have h_int_j : ∀ i : Fin N,
        MeasureTheory.Integrable (fun U => ∑ j : Fin N, ‖entry i j U‖ ^ 2 * ω U ^ 2) μ := fun i =>
      MeasureTheory.integrable_finset_sum Finset.univ fun j _ => h_int_ij i j
    simp_rw [← MeasureTheory.integral_finset_sum Finset.univ (fun j _ => h_int_ij _ j)]
    rw [← MeasureTheory.integral_finset_sum Finset.univ (fun i _ => h_int_j i)]
    have h_pt : (fun U : G_L => ∑ i : Fin N, ∑ j : Fin N, ‖entry i j U‖ ^ 2 * ω U ^ 2) =
        fun U => (N : ℝ) * ω U ^ 2 := by
      funext U
      simp_rw [← Finset.sum_mul]
      change frobeniusNormSq (U e₀ : Matrix (Fin N) (Fin N) ℂ) * ω U ^ 2 = (N : ℝ) * ω U ^ 2
      rw [frobeniusNormSq_su_eq]
    rw [h_pt, MeasureTheory.integral_const_mul, h_om_sq, mul_one]
  have h_st_ij : ∀ i j : Fin N,
      (⟪ψ i j, S.T (ψ i j)⟫_ℂ).re = lam0⁻¹ * ∫ U, ∫ U', K_W U U' * ω U * ω U' *
        (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ ∂μ := by
    intro i j
    rw [hS_T, ContinuousLinearMap.smul_apply, inner_smul_right, Complex.mul_re,
      Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
    congr 1
    have hl2 := MeasureTheory.L2.integrable_inner (𝕜 := ℂ) (ψ i j) (T_raw (ψ i j))
    rw [MeasureTheory.L2.inner_def]
    change RCLike.re (∫ U, ⟪ψ i j U, (T_raw (ψ i j)) U⟫_ℂ ∂μ) = _
    rw [← integral_re hl2]
    have h1 := wilsonIntegralOp_apply_ae L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd (ψ i j)
    have h2 := (hψ_mem i j).coeFn_toLp
    refine MeasureTheory.integral_congr_ae ?_
    filter_upwards [h1, h2] with U hu1 hu2
    change RCLike.re ⟪⇑(ψ i j) U, ⇑(T_raw (ψ i j)) U⟫_ℂ = _
    rw [hu1, hu2]
    dsimp [wilsonIntegralFn]
    have h_in_ae : (fun U' => ((K_W U U' : ℝ) : ℂ) * ⇑(ψ i j) U') =ᵐ[μ]
        fun U' => ((K_W U U' : ℝ) : ℂ) * ψ_fn i j U' := by
      filter_upwards [h2] with U' hu'; rw [hu']
    rw [MeasureTheory.integral_congr_ae h_in_ae]
    have h_inner_c : RCLike.re ⟪ψ_fn i j U, ∫ U', ((K_W U U' : ℝ) : ℂ) * ψ_fn i j U' ∂μ⟫_ℂ =
        RCLike.re (star (ψ_fn i j U) * ∫ U', ((K_W U U' : ℝ) : ℂ) * ψ_fn i j U' ∂μ) := by
      simp only [RCLike.inner_apply, Complex.star_def, Complex.mul_re, Complex.conj_re,
        Complex.conj_im]; ring
    rw [h_inner_c, ← MeasureTheory.integral_const_mul]
    have h_in_cont : Continuous (fun U' : G_L =>
        star (ψ_fn i j U) * (((K_W U U' : ℝ) : ℂ) * ψ_fn i j U')) :=
      continuous_const.mul ((Complex.continuous_ofReal.comp
        (continuous_cubicWilsonKernel_right L N β K_kin hK_cont U)).mul
        ((h_entry_cont i j).mul (Complex.continuous_ofReal.comp hgs.ω_cont)))
    have h_in_int := integrable_of_continuous_compact μ _ h_in_cont
    rw [← integral_re h_in_int]
    refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U' => ?_)
    dsimp only [ψ_fn]
    have h_pt_re : RCLike.re (star (entry i j U * (ω U : ℂ)) *
          (((K_W U U' : ℝ) : ℂ) * (entry i j U' * (ω U' : ℂ)))) =
        K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re := by
      simp only [RCLike.inner_apply, star_mul, Complex.star_def, Complex.conj_ofReal,
        Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, Complex.conj_re,
        Complex.conj_im]
      ring
    exact h_pt_re
  have h_gap_sum : ∑ i : Fin N, ∑ j : Fin N, (⟪ψ i j, S.T (ψ i j)⟫_ℂ).re ≤
      Real.exp (-S.Δ) * (N : ℝ) := by
    calc ∑ i : Fin N, ∑ j : Fin N, (⟪ψ i j, S.T (ψ i j)⟫_ℂ).re
        ≤ ∑ i : Fin N, ∑ j : Fin N, Real.exp (-(S.Δ * S.a)) * ‖ψ i j‖ ^ 2 := by
            refine Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => ?_
            exact S.gap (ψ i j) (hψ_orth i j)
      _ = Real.exp (-S.Δ) * ∑ i : Fin N, ∑ j : Fin N, ‖ψ i j‖ ^ 2 := by
            rw [hS_a, mul_one]
            simp_rw [← Finset.mul_sum]
      _ = Real.exp (-S.Δ) * (N : ℝ) := by rw [hψ_norm_sum]
  have h_pol : ∀ a b : ℂ, (⟪a, b⟫_ℂ).re = (1 / 2 : ℝ) * (‖a‖ ^ 2 + ‖b‖ ^ 2 - ‖a - b‖ ^ 2) := by
    intro a b
    simp only [RCLike.inner_apply, Complex.star_def, ← Complex.normSq_eq_norm_sq,
      Complex.normSq_apply, Complex.sub_re, Complex.sub_im, Complex.mul_re,
      Complex.conj_re, Complex.conj_im]
    ring
  have h_frob_cont_left : Continuous (fun p : G_L × G_L =>
      frobeniusNormSq ((p.1 e₀ : Matrix (Fin N) (Fin N) ℂ) -
        (p.2 e₀ : Matrix (Fin N) (Fin N) ℂ))) := by
    unfold frobeniusNormSq
    refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
    simp only [Matrix.sub_apply]
    exact (((continuous_apply j).comp ((continuous_apply i).comp
      (continuous_subtype_val.comp ((continuous_apply e₀).comp continuous_fst)))).sub
      ((continuous_apply j).comp ((continuous_apply i).comp
      (continuous_subtype_val.comp ((continuous_apply e₀).comp continuous_snd))))).norm.pow 2
  have h_KW_cont : Continuous (Function.uncurry K_W) :=
    continuous_cubicWilsonKernel L N β K_kin hK_cont
  have h_diff_cont_U : ∀ U' : G_L, Continuous (fun U : G_L =>
      K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) := fun U' =>
    (((h_KW_cont.comp (continuous_id.prodMk continuous_const)).mul hgs.ω_cont).mul
      continuous_const).mul (h_frob_cont_left.comp (continuous_id.prodMk continuous_const))
  have h_diff_cont_U' : ∀ U : G_L, Continuous (fun U' : G_L =>
      K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) := fun U =>
    (((h_KW_cont.comp (continuous_const.prodMk continuous_id)).mul continuous_const).mul
      hgs.ω_cont).mul (h_frob_cont_left.comp (continuous_const.prodMk continuous_id))
  have h_outer_diff_cont : Continuous (fun U : G_L =>
      ∫ U', K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ) := by
    refine MeasureTheory.continuous_of_dominated ?_ ?_
      (MeasureTheory.integrable_const (((linkChiUb L β) ^ 2) * M_ω ^ 2 * (4 * (N : ℝ)))) ?_
    · intro U
      exact (integrable_of_continuous_compact μ _ (h_diff_cont_U' U)).aestronglyMeasurable
    · intro U
      refine Filter.Eventually.of_forall fun U' => ?_
      have hb := wilsonKernel_cubic_le L N β hβ_pos.le K_kin hK_nn
        ((linkChiUb L β) ^ 2) hK_bd U U'
      have h_frob_le := frobeniusNormSq_su_sub_le (U e₀) (U' e₀)
      have h_frob_nn : 0 ≤ frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) :=
        frobeniusNormSq_nonneg _
      have h_nn : 0 ≤ K_W U U' * ω U * ω U' * frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) :=
        mul_nonneg (mul_nonneg (mul_nonneg hb.1 (hgs.ω_pos U).le) (hgs.ω_pos U').le) h_frob_nn
      rw [Real.norm_of_nonneg h_nn]
      have hω1 : ω U ≤ M_ω := by
        simpa [Real.norm_of_nonneg (hgs.ω_pos U).le] using hM_ω_bd U
      have hω2 : ω U' ≤ M_ω := by
        simpa [Real.norm_of_nonneg (hgs.ω_pos U').le] using hM_ω_bd U'
      calc K_W U U' * ω U * ω U' * frobeniusNormSq
            ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ))
          ≤ (((linkChiUb L β) ^ 2) * M_ω * M_ω) * (4 * (N : ℝ)) :=
            mul_le_mul (mul_le_mul (mul_le_mul hb.2 hω1 (hgs.ω_pos U).le (sq_nonneg _))
              hω2 (hgs.ω_pos U').le (mul_nonneg (sq_nonneg _) hM_ω_nn))
              h_frob_le h_frob_nn (mul_nonneg (mul_nonneg (sq_nonneg _) hM_ω_nn) hM_ω_nn)
        _ = ((linkChiUb L β) ^ 2) * M_ω ^ 2 * (4 * (N : ℝ)) := by ring
    · exact Filter.Eventually.of_forall h_diff_cont_U
  have h_sum_st : ∑ i : Fin N, ∑ j : Fin N, (⟪ψ i j, S.T (ψ i j)⟫_ℂ).re =
      (N : ℝ) - (2 * lam0)⁻¹ * ∫ U, ∫ U', K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ := by
    simp_rw [h_st_ij, ← Finset.mul_sum]
    have h_inner_int : ∀ i j U, MeasureTheory.Integrable
        (fun U' => K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re) μ := fun i j U =>
      integrable_of_continuous_compact μ _
        ((((h_KW_cont.comp (continuous_const.prodMk continuous_id)).mul continuous_const).mul
          hgs.ω_cont).mul (Complex.continuous_re.comp
            ((continuous_const : Continuous (fun _ : G_L => entry i j U)).inner
              (h_entry_cont i j))))
    have h_outer_cont : ∀ i j, Continuous (fun U : G_L =>
        ∫ U', K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ) := by
      intro i j
      refine MeasureTheory.continuous_of_dominated ?_ ?_
        (MeasureTheory.integrable_const (((linkChiUb L β) ^ 2) * M_ω ^ 2 * 4)) ?_
      · intro U; exact (h_inner_int i j U).aestronglyMeasurable
      · intro U
        refine Filter.Eventually.of_forall fun U' => ?_
        have hb := wilsonKernel_cubic_le L N β hβ_pos.le K_kin hK_nn
          ((linkChiUb L β) ^ 2) hK_bd U U'
        have h_e : ‖(⟪entry i j U, entry i j U'⟫_ℂ).re‖ ≤ 4 := by
          calc ‖(⟪entry i j U, entry i j U'⟫_ℂ).re‖
              ≤ ‖⟪entry i j U, entry i j U'⟫_ℂ‖ := Complex.abs_re_le_norm _
            _ ≤ ‖entry i j U‖ * ‖entry i j U'‖ := norm_inner_le_norm _ _
            _ ≤ 2 * 2 := mul_le_mul (h_entry_bd i j U) (h_entry_bd i j U') (norm_nonneg _)
                (by positivity)
            _ = 4 := by norm_num
        have hω1 : ω U ≤ M_ω := by
          simpa [Real.norm_of_nonneg (hgs.ω_pos U).le] using hM_ω_bd U
        have hω2 : ω U' ≤ M_ω := by
          simpa [Real.norm_of_nonneg (hgs.ω_pos U').le] using hM_ω_bd U'
        rw [norm_mul, norm_mul, norm_mul, Real.norm_of_nonneg hb.1,
          Real.norm_of_nonneg (hgs.ω_pos U).le, Real.norm_of_nonneg (hgs.ω_pos U').le]
        calc K_W U U' * ω U * ω U' * ‖(⟪entry i j U, entry i j U'⟫_ℂ).re‖
            ≤ (((linkChiUb L β) ^ 2) * M_ω * M_ω) * 4 :=
              mul_le_mul (mul_le_mul (mul_le_mul hb.2 hω1 (hgs.ω_pos U).le (sq_nonneg _))
                hω2 (hgs.ω_pos U').le (mul_nonneg (sq_nonneg _) hM_ω_nn))
                h_e (norm_nonneg _) (mul_nonneg (mul_nonneg (sq_nonneg _) hM_ω_nn) hM_ω_nn)
          _ = ((linkChiUb L β) ^ 2) * M_ω ^ 2 * 4 := by ring
      · exact Filter.Eventually.of_forall fun U' =>
          (((h_KW_cont.comp (continuous_id.prodMk continuous_const)).mul hgs.ω_cont).mul
            continuous_const).mul (Complex.continuous_re.comp
              ((h_entry_cont i j).inner continuous_const))
    have h_outer_int_ij : ∀ i j, MeasureTheory.Integrable (fun U =>
        ∫ U', K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ) μ := fun i j =>
      integrable_of_continuous_compact μ _ (h_outer_cont i j)
    have h_outer_int_j : ∀ i, MeasureTheory.Integrable (fun U => ∑ j : Fin N,
        ∫ U', K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ) μ := fun i =>
      MeasureTheory.integrable_finset_sum Finset.univ fun j _ => h_outer_int_ij i j
    simp_rw [← MeasureTheory.integral_finset_sum Finset.univ (fun j _ => h_outer_int_ij _ j)]
    rw [← MeasureTheory.integral_finset_sum Finset.univ (fun i _ => h_outer_int_j i)]
    have h_swap_in : ∀ U, (∑ i : Fin N, ∑ j : Fin N,
        ∫ U', K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ) =
        ∫ U', K_W U U' * ω U * ω U' * ((N : ℝ) - (1 / 2 : ℝ) * frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) ∂μ := by
      intro U
      have h_int_j : ∀ i, MeasureTheory.Integrable (fun U' => ∑ j : Fin N,
          K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re) μ := fun i =>
        MeasureTheory.integrable_finset_sum Finset.univ fun j _ => h_inner_int i j U
      simp_rw [← MeasureTheory.integral_finset_sum Finset.univ (fun j _ => h_inner_int _ j U)]
      rw [← MeasureTheory.integral_finset_sum Finset.univ (fun i _ => h_int_j i)]
      refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U' => ?_)
      simp_rw [← Finset.mul_sum, h_pol]
      have h_s1 : ∑ i : Fin N, ∑ j : Fin N, (1 / 2 : ℝ) *
          (‖entry i j U‖ ^ 2 + ‖entry i j U'‖ ^ 2 - ‖entry i j U - entry i j U'‖ ^ 2) =
          (1 / 2 : ℝ) * ((∑ i, ∑ j, ‖entry i j U‖ ^ 2) + (∑ i, ∑ j, ‖entry i j U'‖ ^ 2) -
            (∑ i, ∑ j, ‖entry i j U - entry i j U'‖ ^ 2)) := by
        simp_rw [← Finset.mul_sum, Finset.sum_sub_distrib, Finset.sum_add_distrib]
      rw [h_s1]
      change K_W U U' * ω U * ω U' * ((1 / 2 : ℝ) *
          (frobeniusNormSq (U e₀ : Matrix (Fin N) (Fin N) ℂ) +
            frobeniusNormSq (U' e₀ : Matrix (Fin N) (Fin N) ℂ) -
            frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ)))) = _
      rw [frobeniusNormSq_su_eq, frobeniusNormSq_su_eq]
      ring
    simp_rw [h_swap_in]
    have h_split_in : ∀ U, (∫ U', K_W U U' * ω U * ω U' * ((N : ℝ) - (1 / 2 : ℝ) *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) ∂μ) =
        lam0 * (N : ℝ) * ω U ^ 2 - (1 / 2 : ℝ) * ∫ U', K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ := by
      intro U
      have h_int1 : MeasureTheory.Integrable
          (fun U' => K_W U U' * ω U * ω U' * (N : ℝ)) μ :=
        integrable_of_continuous_compact μ _
          ((((h_KW_cont.comp (continuous_const.prodMk continuous_id)).mul continuous_const).mul
            hgs.ω_cont).mul continuous_const)
      have h_int2 : MeasureTheory.Integrable (fun U' => (1 / 2 : ℝ) *
          (K_W U U' * ω U * ω U' * frobeniusNormSq
            ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)))) μ :=
        (integrable_of_continuous_compact μ _ (h_diff_cont_U' U)).const_mul _
      have h_eq_fn : (fun U' => K_W U U' * ω U * ω U' * ((N : ℝ) - (1 / 2 : ℝ) *
            frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ)))) =
          fun U' => K_W U U' * ω U * ω U' * (N : ℝ) - (1 / 2 : ℝ) *
            (K_W U U' * ω U * ω U' * frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) := by
        funext U'; ring
      rw [h_eq_fn, MeasureTheory.integral_sub h_int1 h_int2,
        MeasureTheory.integral_const_mul (1 / 2 : ℝ)]
      congr 1
      have h_eq1 : (fun U' => K_W U U' * ω U * ω U' * (N : ℝ)) =
          fun U' => (ω U * (N : ℝ)) * (K_W U U' * ω U') := by funext U'; ring
      rw [h_eq1, MeasureTheory.integral_const_mul, hω_eig U]
      ring
    simp_rw [h_split_in]
    have h_o1 : MeasureTheory.Integrable (fun U : G_L => lam0 * (N : ℝ) * ω U ^ 2) μ :=
      integrable_of_continuous_compact μ _ (continuous_const.mul (hgs.ω_cont.pow 2))
    have h_o2 : MeasureTheory.Integrable (fun U : G_L => (1 / 2 : ℝ) *
        ∫ U', K_W U U' * ω U * ω U' * frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ) μ :=
      (integrable_of_continuous_compact μ _ h_outer_diff_cont).const_mul _
    rw [MeasureTheory.integral_sub h_o1 h_o2, MeasureTheory.integral_const_mul (lam0 * (N : ℝ)),
      h_om_sq, mul_one, MeasureTheory.integral_const_mul (1 / 2 : ℝ), mul_sub]
    have h_lam_cancel : lam0⁻¹ * (lam0 * (N : ℝ)) = (N : ℝ) := by
      rw [← mul_assoc, inv_mul_cancel₀ hlam0_pos.ne', one_mul]
    rw [h_lam_cancel]
    have h_half_cancel : lam0⁻¹ * ((1 / 2 : ℝ) * ∫ U, ∫ U', K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ) =
        (2 * lam0)⁻¹ * ∫ U, ∫ U', K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ := by
      ring
    rw [h_half_cancel]
  refine ⟨?_, hω_eig, h_om_sq, h_om_l1⟩
  linarith

"""

src = src.replace(anchor, helpers3 + anchor, 1)
path.write_text(src, encoding="utf-8")
print("Patched Patch 3/4 successfully.")