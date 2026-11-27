#!/usr/bin/env python3
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
src = path.read_text(encoding="utf-8")

replacements = [
    (
        """  have hneg : frobeniusNormSq (-((1 : Matrix (Fin N) (Fin N) ℂ))) = (N : ℝ) := by
    unfold frobeniusNormSq
    simp [Matrix.one_apply]""",
        """  have hneg : frobeniusNormSq (-((1 : Matrix (Fin N) (Fin N) ℂ))) = (N : ℝ) := by
    unfold frobeniusNormSq
    simp only [Matrix.neg_apply, norm_neg, Matrix.one_apply]
    have h_entry : ∀ i j : Fin N,
        ‖if i = j then (1 : ℂ) else 0‖ ^ 2 = if i = j then (1 : ℝ) else 0 := by
      intro i j; split_ifs <;> simp
    simp_rw [h_entry, Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte]
    simp""",
    ),
    (
        """    rw [star_sub, star_one, Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_sub,
      Matrix.one_mul, Matrix.mul_one, hA, two_smul]
    abel""",
        """    rw [star_sub, star_one, Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_sub]
    simp only [Matrix.one_mul, Matrix.mul_one]
    rw [hA, two_smul]
    abel""",
    ),
    (
        """      rcases hp with ⟨x, rfl | rfl | rfl⟩ <;>
        dsimp [cubicPlaquette, pathHolonomy] <;>
        have hle := frobeniusNormSq_plaq4_le _ _ _ _ <;>
        linarith [hU (x, _), hU (cubicShift L _ x, _)]""",
        """      have h16 : (16 : ℝ) / β = 4 * (1 / β + 1 / β + 1 / β + 1 / β) := by ring
      rw [h16]
      rcases hp with ⟨x, rfl | rfl | rfl⟩ <;>
        dsimp [cubicPlaquette, pathHolonomy] <;>
        refine (frobeniusNormSq_plaq4_le _ _ _ _).trans ?_
      · linarith only [hU (x, 0), hU (cubicShift L 0 x, 1), hU (cubicShift L 1 x, 0), hU (x, 1)]
      · linarith only [hU (x, 0), hU (cubicShift L 0 x, 2), hU (cubicShift L 2 x, 0), hU (x, 2)]
      · linarith only [hU (x, 1), hU (cubicShift L 1 x, 2), hU (cubicShift L 2 x, 1), hU (x, 2)]""",
    ),
    (
        """      rw [frobeniusNormSq_sub_rev 1 (W e : Matrix (Fin N) (Fin N) ℂ)] at hadd
      linarith [hU e, hW e]""",
        """      rw [frobeniusNormSq_sub_rev 1 (W e : Matrix (Fin N) (Fin N) ℂ)] at hadd
      calc frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))
          ≤ 2 * frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) +
            2 * frobeniusNormSq ((W e : Matrix (Fin N) (Fin N) ℂ) - 1) := by
              rw [hsub]; exact hadd
        _ ≤ 2 * (1 / β) + 2 * (1 / β) := by linarith only [hU e, hW e]
        _ = 4 / β := by ring""",
    ),
    (
        """    have h1 := wilsonAction_nonneg_of_nonneg hN hβ (cubicPlaquettes L) U
    have h2 := wilsonAction_nonneg_of_nonneg hN hβ (cubicPlaquettes L) U'
    linarith""",
        """    have h1 := wilsonAction_nonneg_of_nonneg hN hβ (cubicPlaquettes L) U
    have h2 := wilsonAction_nonneg_of_nonneg hN hβ (cubicPlaquettes L) U'
    linarith only [h1, h2]""",
    ),
    (
        """      _ = _ := by simp [Measure.real, MeasureTheory.measure_univ]""",
        """      _ = _ := by
          rw [MeasureTheory.integral_const, Measure.real_def, MeasureTheory.measure_univ,
            ENNReal.toReal_one, one_smul]""",
    ),
    (
        """  intro K B_link B_prod
  have hB_link_meas : MeasurableSet B_link := by""",
        """  intro K B_link B_prod
  haveI := suHaar_prob N
  have hB_link_meas : MeasurableSet B_link := by""",
    ),
    (
        """  have hB_prod_meas : MeasurableSet B_prod := by
    change MeasurableSet (Set.pi Set.univ fun _ => B_link)
    convert MeasurableSet.univ_pi fun _ => hB_link_meas""",
        """  have hB_prod_meas : MeasurableSet B_prod := by
    haveI : Countable (cubicTorus3 L).Link := Finite.countable
    change MeasurableSet (Set.pi Set.univ fun _ => B_link)
    exact MeasurableSet.univ_pi fun _ => hB_link_meas""",
    ),
    (
        """    apply Real.exp_le_exp.mpr
    linarith""",
        """    apply Real.exp_le_exp.mpr
    linarith only [h_act_U, h_act_U']""",
    ),
    (
        """      have h_mul := mul_le_mul hk1 hk2 (Real.exp_pos _).le
        ((linkChiLb_pos L β).le.trans (cubicLinkKineticKernel_bounds L N hN β hβ.le U W).1)
      rw [← Real.exp_add] at h_mul
      convert h_mul using 2
      ring""",
        """      have h_mul := mul_le_mul hk1 hk2 (Real.exp_pos _).le
        ((linkChiLb_pos L β).le.trans (cubicLinkKineticKernel_bounds L N hN β hβ.le U W).1)
      rw [← Real.exp_add] at h_mul
      have h_exp_eq : c_k = Real.exp (((3 * (L : ℝ) ^ 3) * (β / 2) - 3 * (L : ℝ) ^ 3 / (N : ℝ)) +
          ((3 * (L : ℝ) ^ 3) * (β / 2) - 3 * (L : ℝ) ^ 3 / (N : ℝ))) := by
        dsimp only [c_k]; congr 1; ring
      rw [h_exp_eq]
      exact h_mul""",
    ),
    (
        """      = Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) * (μ.real B_prod * c_k) := by
          dsimp only [c_k]
          rw [mul_left_comm, ← Real.exp_add]
          congr 2
          ring""",
        """      = Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) * (μ.real B_prod * c_k) := by
          dsimp only [c_k]
          rw [mul_left_comm, ← Real.exp_add,
            show -(24 * (L : ℝ) ^ 3 / (N : ℝ)) +
              ((3 * (L : ℝ) ^ 3) * β - 6 * (L : ℝ) ^ 3 / (N : ℝ)) =
              (3 * (L : ℝ) ^ 3) * β - 30 * (L : ℝ) ^ 3 / (N : ℝ) by ring]""",
    ),
    (
        """              simp [← Complex.normSq_eq_norm_sq, Complex.normSq_apply, Complex.mul_re,
                Complex.mul_im, sq]
              ring""",
        """              simp [← Complex.normSq_eq_norm_sq, Complex.normSq_apply, Complex.mul_re,
                Complex.mul_im, sq]""",
    ),
    (
        """      have h_re : RCLike.re ⟪(c_r : ℂ), ((∫ U', B_prod.indicator
          (fun U' => K_W U U' * c_r) U' ∂μ : ℝ) : ℂ)⟫_ℂ =
          c_r * ∫ U', B_prod.indicator (fun U' => K_W U U' * c_r) U' ∂μ := by
        simp [Complex.mul_re]
      rw [h_re]""",
        """      have h_re : RCLike.re ⟪(c_r : ℂ), ((∫ U', B_prod.indicator
          (fun U' => K_W U U' * c_r) U' ∂μ : ℝ) : ℂ)⟫_ℂ =
          c_r * ∫ U', B_prod.indicator (fun U' => K_W U U' * c_r) U' ∂μ := by
        simp [RCLike.inner_apply, Complex.mul_re]; ring
      refine h_re.trans ?_""",
    ),
    (
        """    have h_inner_eq : ⟪Ω, ψ i j⟫_ℂ = c * ⟪Ω, ψ i j⟫_ℂ := by
      rw [h_int1]
      calc ∫ U, (ω U : ℂ) * (entry i j U * (ω U : ℂ)) ∂μ
          = ∫ U, (ω (e_flip U) : ℂ) * (entry i j (e_flip U) * (ω (e_flip U) : ℂ)) ∂μ :=
              (hmp.integral_comp' (fun U => (ω U : ℂ) * (entry i j U * (ω U : ℂ)))).symm
        _ = ∫ U, c * ((ω U : ℂ) * (entry i j U * (ω U : ℂ))) ∂μ := by
              refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
              rw [hω_flip U, h_entry_flip U]; ring
        _ = c * ∫ U, (ω U : ℂ) * (entry i j U * (ω U : ℂ)) ∂μ :=
              MeasureTheory.integral_const_mul c _
        _ = c * ⟪Ω, ψ i j⟫_ℂ := by rw [← h_int1]""",
        """    have h_inner_eq : ⟪Ω, ψ i j⟫_ℂ = c * ⟪Ω, ψ i j⟫_ℂ := by
      rw [h_int1]
      calc ∫ U, (ω U : ℂ) * (entry i j U * (ω U : ℂ)) ∂μ
          = ∫ U, (ω (e_flip U) : ℂ) * (entry i j (e_flip U) * (ω (e_flip U) : ℂ)) ∂μ :=
              (hmp.integral_comp' (fun U => (ω U : ℂ) * (entry i j U * (ω U : ℂ)))).symm
        _ = ∫ U, c * ((ω U : ℂ) * (entry i j U * (ω U : ℂ))) ∂μ := by
              refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
              dsimp only
              rw [hω_flip U, h_entry_flip U]; ring
        _ = c * ∫ U, (ω U : ℂ) * (entry i j U * (ω U : ℂ)) ∂μ :=
              MeasureTheory.integral_const_mul c _""",
    ),
    (
        """    simp_rw [← MeasureTheory.integral_finset_sum Finset.univ (fun j _ => h_int_ij _ j)]""",
        """    have h_swap_i : ∀ i : Fin N,
        (∑ j : Fin N, ∫ U, ‖entry i j U‖ ^ 2 * ω U ^ 2 ∂μ) =
          ∫ U, ∑ j : Fin N, ‖entry i j U‖ ^ 2 * ω U ^ 2 ∂μ := fun i =>
      (MeasureTheory.integral_finset_sum Finset.univ fun j _ => h_int_ij i j).symm
    simp_rw [h_swap_i]""",
    ),
    (
        """    filter_upwards [h1, h2] with U hu1 hu2
    change RCLike.re ⟪⇑(ψ i j) U, ⇑(T_raw (ψ i j)) U⟫_ℂ = _
    rw [hu1, hu2]""",
        """    filter_upwards [h1, h2] with U hu1 hu2
    have hu1' : ⇑(T_raw (ψ i j)) U = wilsonIntegralFn L N β K_kin (ψ i j) U := hu1
    change RCLike.re ⟪⇑(ψ i j) U, ⇑(T_raw (ψ i j)) U⟫_ℂ = _
    rw [hu1', hu2]""",
    ),
]

for idx, (old, new) in enumerate(replacements, 1):
    count = src.count(old)
    assert count == 1, f"Hunk {idx} matched {count} times"
    src = src.replace(old, new, 1)

path.write_text(src, encoding="utf-8")
print("Patched Patch 5A successfully.")