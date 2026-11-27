#!/usr/bin/env python3
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
src = path.read_text(encoding="utf-8")

old_tail = """    rw [inv_eq_one_div, div_le_iff₀ hlam0_pos]
    calc (1 : ℝ) = rhs_inv * ((1 / ((K : ℝ) ^ (2 * N * N)) ^ (2 * links)) *
            Real.exp ((3 * (L : ℝ) ^ 3) * β - 30 * (L :"""

new_tail = """    rw [inv_eq_one_div, div_le_iff₀ hlam0_pos]
    calc (1 : ℝ) = rhs_inv * ((1 / ((K : ℝ) ^ (2 * N * N)) ^ (2 * links)) *
            Real.exp ((3 * (L : ℝ) ^ 3) * β - 30 * (L : ℝ) ^ 3 / (N : ℝ))) := h_prod_one.symm
      _ ≤ rhs_inv * lam0 := mul_le_mul_of_nonneg_left h_comb hrhs_nn
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  let e₀ : (cubicTorus3 L).Link := ((0, 0, 0), 0)
  let D : G_L → G_L → ℝ := fun U U' =>
    ∑ e : (cubicTorus3 L).Link, frobeniusNormSq
      ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))
  let tailC : ℝ := 4 * (N : ℝ) *
    (Real.exp ((3 * (L : ℝ) ^ 3) * β) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)))
  have hε_nn : 0 ≤ ε_sq := by
    dsimp only [ε_sq]
    have hlog_nn : 0 ≤ Real.log β := Real.log_nonneg hβ
    positivity
  have h_pt_ineq : ∀ U U' : G_L,
      K_W U U' * ω U * ω U' * frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
        K_W U U' * ω U * ω U' * (2 * ε_sq) + tailC * (ω U * ω U') := by
    intro U U'
    have hKW_nn : 0 ≤ K_W U U' := (wilsonKernel_cubic_le L N β hβ_pos.le K_kin hK_nn
      ((linkChiUb L β) ^ 2) hK_bd U U').1
    have hω_nn : 0 ≤ ω U * ω U' := mul_nonneg (hgs.ω_pos U).le (hgs.ω_pos U').le
    have hKWω_nn : 0 ≤ K_W U U' * ω U * ω U' := by
      rw [mul_assoc]; exact mul_nonneg hKW_nn hω_nn
    by_cases hD : D U U' ≤ 2 * ε_sq
    · have h_e0_le : frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤ 2 * ε_sq :=
        (Finset.single_le_sum (fun e _ => frobeniusNormSq_nonneg
            ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)))
          (Finset.mem_univ e₀)).trans hD
      have h_t1 := mul_le_mul_of_nonneg_left h_e0_le hKWω_nn
      have h_t2 : 0 ≤ tailC * (ω U * ω U') := mul_nonneg (by positivity) hω_nn
      linarith only [h_t1, h_t2]
    · push_neg at hD
      have h_frob_ub : frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤ 4 * (N : ℝ) :=
        frobeniusNormSq_su_sub_le (U e₀) (U' e₀)
      have h_jump := wilsonKernel_jump_le L N (by omega) hβ_pos.le U U'
      have h_exp_ub : Real.exp ((3 * (L : ℝ) ^ 3) * β - (β / (8 * (N : ℝ))) * D U U') ≤
          Real.exp ((3 * (L : ℝ) ^ 3) * β) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        have h_arg1 : (6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β ≤
            (β / (8 * (N : ℝ))) * D U U' := by
          have heq : (6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β =
              (β / (8 * (N : ℝ))) * (2 * ε_sq) := by
            dsimp only [ε_sq]
            field_simp [hN_pos.ne', hβ_pos.ne']
            ring
          rw [heq]
          exact mul_le_mul_of_nonneg_left hD.le (by positivity)
        have h_rpow : β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) =
            Real.exp (-((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β)) := by
          rw [Real.rpow_def_of_pos hβ_pos]
          congr 1; ring
        rw [h_rpow, ← Real.exp_add]
        apply Real.exp_le_exp.mpr
        linarith only [h_arg1]
      have hKW_ub : K_W U U' ≤
          Real.exp ((3 * (L : ℝ) ^ 3) * β) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) :=
        h_jump.trans h_exp_ub
      have h_t1 : 0 ≤ K_W U U' * ω U * ω U' * (2 * ε_sq) :=
        mul_nonneg hKWω_nn (by positivity)
      have h_t2 : K_W U U' * ω U * ω U' * frobeniusNormSq
            ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
          tailC * (ω U * ω U') := by
        calc K_W U U' * ω U * ω U' * frobeniusNormSq
              ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ))
            = (K_W U U' * frobeniusNormSq
                ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) *
                (ω U * ω U') := by ring
          _ ≤ ((Real.exp ((3 * (L : ℝ) ^ 3) * β) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
                (4 * (N : ℝ))) * (ω U * ω U') := by
                refine mul_le_mul_of_nonneg_right ?_ hω_nn
                exact mul_le_mul hKW_ub h_frob_ub (frobeniusNormSq_nonneg _) (by positivity)
          _ = tailC * (ω U * ω U') := by dsimp only [tailC]; ring
      linarith only [h_t1, h_t2]
  obtain ⟨M_ω0, hM_ω0⟩ := isCompact_univ.exists_bound_of_continuousOn hgs.ω_cont.continuousOn
  let M_ω : ℝ := max M_ω0 0
  have hM_ω_nn : 0 ≤ M_ω := le_max_right _ _
  have hM_ω_bd : ∀ U : G_L, ‖ω U‖ ≤ M_ω := fun U =>
    (hM_ω0 U (Set.mem_univ U)).trans (le_max_left _ _)
  have h_KW_cont : Continuous (Function.uncurry K_W) :=
    continuous_cubicWilsonKernel L N β K_kin hK_cont
  have h_frob_cont : Continuous (fun p : G_L × G_L =>
      frobeniusNormSq ((p.1 e₀ : Matrix (Fin N) (Fin N) ℂ) -
        (p.2 e₀ : Matrix (Fin N) (Fin N) ℂ))) := by
    unfold frobeniusNormSq
    refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
    simp only [Matrix.sub_apply]
    exact (((continuous_apply j).comp ((continuous_apply i).comp
      (continuous_subtype_val.comp ((continuous_apply e₀).comp continuous_fst)))).sub
      ((continuous_apply j).comp ((continuous_apply i).comp
      (continuous_subtype_val.comp ((continuous_apply e₀).comp continuous_snd))))).norm.pow 2
  have h_lhs_in : ∀ U, MeasureTheory.Integrable (fun U' : G_L =>
      K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) μ := fun U =>
    integrable_of_continuous_compact μ _
      ((((h_KW_cont.comp (continuous_const.prodMk continuous_id)).mul continuous_const).mul
        hgs.ω_cont).mul (h_frob_cont.comp (continuous_const.prodMk continuous_id)))
  have h_rhs_in : ∀ U, MeasureTheory.Integrable (fun U' : G_L =>
      K_W U U' * ω U * ω U' * (2 * ε_sq) + tailC * (ω U * ω U')) μ := fun U =>
    integrable_of_continuous_compact μ _
      (((((h_KW_cont.comp (continuous_const.prodMk continuous_id)).mul continuous_const).mul
        hgs.ω_cont).mul continuous_const).add
        (continuous_const.mul (continuous_const.mul hgs.ω_cont)))
  have h_in_le : ∀ U, (∫ U', K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ) ≤
      (2 * ε_sq * lam0) * ω U ^ 2 + tailC * (∫ U', ω U' ∂μ) * ω U := by
    intro U
    have h_m := MeasureTheory.integral_mono (h_lhs_in U) (h_rhs_in U) (h_pt_ineq U)
    have h_r1 : MeasureTheory.Integrable
        (fun U' : G_L => K_W U U' * ω U * ω U' * (2 * ε_sq)) μ :=
      integrable_of_continuous_compact μ _
        ((((h_KW_cont.comp (continuous_const.prodMk continuous_id)).mul continuous_const).mul
          hgs.ω_cont).mul continuous_const)
    have h_r2 : MeasureTheory.Integrable (fun U' : G_L => tailC * (ω U * ω U')) μ :=
      integrable_of_continuous_compact μ _
        (continuous_const.mul (continuous_const.mul hgs.ω_cont))
    rw [MeasureTheory.integral_add h_r1 h_r2] at h_m
    have h_eq1 : (∫ U', K_W U U' * ω U * ω U' * (2 * ε_sq) ∂μ) =
        (2 * ε_sq * lam0) * ω U ^ 2 := by
      have h_f : (fun U' => K_W U U' * ω U * ω U' * (2 * ε_sq)) =
          fun U' => (ω U * (2 * ε_sq)) * (K_W U U' * ω U') := by funext U'; ring
      rw [h_f, MeasureTheory.integral_const_mul, hω_eig U]
      ring
    have h_eq2 : (∫ U', tailC * (ω U * ω U') ∂μ) = tailC * (∫ U', ω U' ∂μ) * ω U := by
      have h_f : (fun U' => tailC * (ω U * ω U')) = fun U' => (tailC * ω U) * ω U' := by
        funext U'; ring
      rw [h_f, MeasureTheory.integral_const_mul]
      ring
    rw [h_eq1, h_eq2] at h_m
    exact h_m
  have h_outer_lhs_cont : Continuous (fun U : G_L =>
      ∫ U', K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ) := by
    refine MeasureTheory.continuous_of_dominated ?_ ?_
      (MeasureTheory.integrable_const (((linkChiUb L β) ^ 2) * M_ω ^ 2 * (4 * (N : ℝ)))) ?_
    · intro U; exact (h_lhs_in U).aestronglyMeasurable
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
    · exact Filter.Eventually.of_forall fun U' =>
        (((h_KW_cont.comp (continuous_id.prodMk continuous_const)).mul hgs.ω_cont).mul
          continuous_const).mul (h_frob_cont.comp (continuous_id.prodMk continuous_const))
  have h_outer_lhs_int : MeasureTheory.Integrable (fun U : G_L =>
      ∫ U', K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ) μ :=
    integrable_of_continuous_compact μ _ h_outer_lhs_cont
  have h_outer_rhs_int : MeasureTheory.Integrable (fun U : G_L =>
      (2 * ε_sq * lam0) * ω U ^ 2 + tailC * (∫ U', ω U' ∂μ) * ω U) μ :=
    integrable_of_continuous_compact μ _
      ((continuous_const.mul (hgs.ω_cont.pow 2)).add (continuous_const.mul hgs.ω_cont))
  have h_dbl_ub : (∫ U, ∫ U', K_W U U' * ω U * ω U' * frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ) ≤
      2 * ε_sq * lam0 + tailC := by
    have h_m := MeasureTheory.integral_mono h_outer_lhs_int h_outer_rhs_int h_in_le
    have h_o1 : MeasureTheory.Integrable (fun U : G_L => (2 * ε_sq * lam0) * ω U ^ 2) μ :=
      integrable_of_continuous_compact μ _ (continuous_const.mul (hgs.ω_cont.pow 2))
    have h_o2 : MeasureTheory.Integrable (fun U : G_L => tailC * (∫ U', ω U' ∂μ) * ω U) μ :=
      integrable_of_continuous_compact μ _ (continuous_const.mul hgs.ω_cont)
    rw [MeasureTheory.integral_add h_o1 h_o2, MeasureTheory.integral_const_mul (2 * ε_sq * lam0),
      h_om_sq, mul_one, MeasureTheory.integral_const_mul (tailC * ∫ U', ω U' ∂μ)] at h_m
    have h_om_nn : 0 ≤ ∫ U, ω U ∂μ := MeasureTheory.integral_nonneg fun U => (hgs.ω_pos U).le
    have h_sq_le : (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ 1 := by
      nlinarith only [h_om_nn, h_om_l1]
    have h_tail_le : tailC * (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ tailC := by
      rw [mul_assoc]
      calc tailC * ((∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ)) ≤ tailC * 1 :=
            mul_le_mul_of_nonneg_left h_sq_le (by positivity)
        _ = tailC := mul_one _
    linarith only [h_m, h_tail_le]
  have h_err_step : (N : ℝ) - Real.exp (-S.Δ) * (N : ℝ) ≤ (N : ℝ) * err := by
    have h1 := mul_le_mul_of_nonneg_left h_dbl_ub (by positivity : 0 ≤ (2 * lam0)⁻¹)
    have h2 : (N : ℝ) - Real.exp (-S.Δ) * (N : ℝ) ≤ (2 * lam0)⁻¹ * (2 * ε_sq * lam0 + tailC) :=
      h_dir_le.trans h1
    have h_first : (2 * lam0)⁻¹ * (2 * ε_sq * lam0) = ε_sq := by
      field_simp [hlam0_pos.ne']
    have h_second : (2 * lam0)⁻¹ * tailC ≤
        2 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
          ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
      calc (2 * lam0)⁻¹ * tailC
          = (2⁻¹ * tailC) * lam0⁻¹ := by ring
        _ ≤ (2⁻¹ * tailC) * (((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
              Real.exp (-(3 * (L : ℝ) ^ 3) * β + 30 * (L : ℝ) ^ 3 / (N : ℝ))) :=
              mul_le_mul_of_nonneg_left hlam0_inv_le (by positivity)
        _ = 2 * (N : ℝ) * (Real.exp ((3 * (L : ℝ) ^ 3) * β) *
              Real.exp (-(3 * (L : ℝ) ^ 3) * β + 30 * (L : ℝ) ^ 3 / (N : ℝ))) *
              ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
              β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
              dsimp only [tailC]; ring
        _ = 2 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
              ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
              β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
              rw [← Real.exp_add,
                show (3 * (L : ℝ) ^ 3) * β +
                  (-(3 * (L : ℝ) ^ 3) * β + 30 * (L : ℝ) ^ 3 / (N : ℝ)) =
                  30 * (L : ℝ) ^ 3 / (N : ℝ) by ring]
    have h_N_err : (N : ℝ) * err = 2 * ε_sq +
        8 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
          ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
          β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
      dsimp only [err]
      field_simp [hN_pos.ne']
    have h_big : 2 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
          ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) ≤
        8 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
          ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
      have h_pos_rest : 0 ≤ (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
          ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        positivity
      nlinarith only [h_pos_rest]
    rw [mul_add, h_first] at h2
    linarith only [h2, h_second, h_N_err, h_big, hε_nn]
  have h_exp_ge : 1 - err ≤ Real.exp (-S.Δ) := by
    have h_div : 1 - Real.exp (-S.Δ) ≤ err := by
      nlinarith only [h_err_step, hN_pos]
    linarith only [h_div]
  have h_log := Real.log_le_log (by linarith only [herr_lt] : 0 < 1 - err) (Real.exp_pos (-S.Δ))
  rw [Real.log_exp] at h_log
  linarith only [h_log]"""

assert src.count(old_tail) == 1, f"Matched {src.count(old_tail)} times"
src = src.replace(old_tail, new_tail, 1)

path.write_text(src, encoding="utf-8")
print("File completed successfully.")