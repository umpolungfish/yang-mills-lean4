#!/usr/bin/env python3
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
src = path.read_text(encoding="utf-8")

replacements = [
    (
        """    simp_rw [← MeasureTheory.integral_finset_sum Finset.univ (fun j _ => h_outer_int_ij _ j)]""",
        """    have h_swap_outer_i : ∀ i : Fin N,
        (∑ j : Fin N, ∫ U, ∫ U', K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ ∂μ) =
          ∫ U, ∑ j : Fin N, ∫ U', K_W U U' * ω U * ω U' *
            (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ ∂μ := fun i =>
      (MeasureTheory.integral_finset_sum Finset.univ fun j _ => h_outer_int_ij i j).symm
    simp_rw [h_swap_outer_i]""",
    ),
    (
        """      simp_rw [← MeasureTheory.integral_finset_sum Finset.univ (fun j _ => h_inner_int _ j U)]""",
        """      have h_swap_in_i : ∀ i : Fin N,
          (∑ j : Fin N, ∫ U', K_W U U' * ω U * ω U' * (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ) =
            ∫ U', ∑ j : Fin N, K_W U U' * ω U * ω U' *
              (⟪entry i j U, entry i j U'⟫_ℂ).re ∂μ := fun i =>
        (MeasureTheory.integral_finset_sum Finset.univ fun j _ => h_inner_int i j U).symm
      simp_rw [h_swap_in_i]""",
    ),
    (
        """  refine ⟨?_, hω_eig, h_om_sq, h_om_l1⟩
  linarith""",
        """  refine ⟨?_, hω_eig, h_om_sq, h_om_l1⟩
  change (N : ℝ) - Real.exp (-S.Δ) * (N : ℝ) ≤ (2 * lam0)⁻¹ * ∫ U, ∫ U', K_W U U' * ω U * ω U' *
    frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
      (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ
  linarith only [h_gap_sum, h_sum_st]""",
    ),
    (
        """  have h_flip_e0 : ∀ U, (e_flip U) ((0, 0, 0), 0) =
      centralElem N hN * U ((0, 0, 0), 0) := fun U => by
    dsimp [e_flip, sliceCenterFlipEquiv, sliceCenterFlip]
    rw [if_pos ⟨rfl, rfl⟩]
  obtain ⟨h_dir_le, hω_eig, h_om_sq, h_om_l1⟩ := fullRank_dirichlet_step L N hN hβ_pos
    e_flip hmp h_flip_e0 S Ω ω hgs rfl hS_T rfl hω_flip""",
        """  have h_flip_e0 : ∀ U, (e_flip U) ((0, 0, 0), 0) =
      centralElem N hN * U ((0, 0, 0), 0) := fun U => by
    dsimp [e_flip, sliceCenterFlipEquiv, sliceCenterFlip]
  obtain ⟨h_dir_le0, hω_eig0, h_om_sq, h_om_l1⟩ := fullRank_dirichlet_step L N hN hβ_pos
    e_flip hmp h_flip_e0 S Ω ω hgs rfl hS_T rfl hω_flip
  have h_dir_le : (N : ℝ) - Real.exp (-S.Δ) * (N : ℝ) ≤
      (2 * lam0)⁻¹ * ∫ U, ∫ U', K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U ((0, 0, 0), 0) : Matrix (Fin N) (Fin N) ℂ) -
          (U' ((0, 0, 0), 0) : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ := h_dir_le0
  have hω_eig : ∀ U, ∫ U', K_W U U' * ω U' ∂μ = lam0 * ω U := hω_eig0""",
    ),
    (
        """    calc 1 / ((K : ℝ) ^ (2 * N * N)) ^ (2 * links)
        = (1 / ((K : ℝ) ^ (2 * N * N)) ^ (3 * L ^ 3)) ^ 2 := by
            dsimp only [links]
            rw [div_pow, one_pow, ← pow_mul, mul_comm (3 * L ^ 3) 2]""",
        """    calc 1 / ((K : ℝ) ^ (2 * N * N)) ^ (2 * links)
        = (1 / ((K : ℝ) ^ (2 * N * N)) ^ (3 * L ^ 3)) ^ 2 := by
            dsimp only [links]
            rw [div_pow, one_pow, ← pow_mul, ← pow_mul]
            congr 2; ring""",
    ),
    (
        """        _ = 1 * Real.exp 0 := by
              rw [mul_one_div_cancel hK_ne, ← Real.exp_add]
              congr 2; ring""",
        """        _ = 1 * Real.exp 0 := by
              rw [mul_one_div_cancel hK_ne, ← Real.exp_add,
                show -(3 * (L : ℝ) ^ 3) * β + 30 * (L : ℝ) ^ 3 / (N : ℝ) +
                  ((3 * (L : ℝ) ^ 3) * β - 30 * (L : ℝ) ^ 3 / (N : ℝ)) = 0 by ring]""",
    ),
    (
        """      have h_t1 := mul_le_mul_of_nonneg_left h_e0_le hKWω_nn
      have h_t2 : 0 ≤ tailC * (ω U * ω U') := mul_nonneg (by positivity) hω_nn
      linarith""",
        """      have h_t1 := mul_le_mul_of_nonneg_left h_e0_le hKWω_nn
      have h_t2 : 0 ≤ tailC * (ω U * ω U') := mul_nonneg (by positivity) hω_nn
      linarith only [h_t1, h_t2]""",
    ),
    (
        """        have h_rpow : β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) =
            Real.exp (-((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β)) := by
          rw [Real.rpow_def_of_pos hβ_pos, neg_mul, mul_comm]
        rw [h_rpow, ← Real.exp_add]
        apply Real.exp_le_exp.mpr
        linarith""",
        """        have h_rpow : β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) =
            Real.exp (-((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β)) := by
          rw [Real.rpow_def_of_pos hβ_pos]
          congr 1; ring
        rw [h_rpow, ← Real.exp_add]
        apply Real.exp_le_exp.mpr
        linarith only [h_arg1]""",
    ),
    (
        """      linarith
  obtain ⟨M_ω0, hM_ω0⟩ := isCompact_univ.exists_bound_of_continuousOn hgs.ω_cont.continuousOn""",
        """      linarith only [h_t1, h_t2]
  obtain ⟨M_ω0, hM_ω0⟩ := isCompact_univ.exists_bound_of_continuousOn hgs.ω_cont.continuousOn""",
    ),
    (
        """    have h_om_nn : 0 ≤ ∫ U, ω U ∂μ := MeasureTheory.integral_nonneg fun U => (hgs.ω_pos U).le
    have h_sq_le : (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ 1 := by nlinarith
    have h_tail_le : tailC * (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ tailC := by
      rw [mul_assoc]
      calc tailC * ((∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ)) ≤ tailC * 1 :=
            mul_le_mul_of_nonneg_left h_sq_le (by positivity)
        _ = tailC := mul_one _
    linarith""",
        """    have h_om_nn : 0 ≤ ∫ U, ω U ∂μ := MeasureTheory.integral_nonneg fun U => (hgs.ω_pos U).le
    have h_sq_le : (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ 1 := by
      nlinarith only [h_om_nn, h_om_l1]
    have h_tail_le : tailC * (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ tailC := by
      rw [mul_assoc]
      calc tailC * ((∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ)) ≤ tailC * 1 :=
            mul_le_mul_of_nonneg_left h_sq_le (by positivity)
        _ = tailC := mul_one _
    linarith only [h_m, h_tail_le]""",
    ),
    (
        """              rw [← Real.exp_add]
              congr 3; ring
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
      nlinarith
    rw [mul_add, h_first] at h2
    linarith
  have h_exp_ge : 1 - err ≤ Real.exp (-S.Δ) := by
    have h_div : 1 - Real.exp (-S.Δ) ≤ err := by
      nlinarith [h_err_step, hN_pos]
    linarith
  have h_log := Real.log_le_log (by linarith : 0 < 1 - err) (Real.exp_pos (-S.Δ))
  rw [Real.log_exp] at h_log
  linarith""",
        """              rw [← Real.exp_add,
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
  linarith only [h_log]""",
    ),
]

for idx, (old, new) in enumerate(replacements, 1):
    count = src.count(old)
    assert count == 1, f"Hunk {idx} matched {count} times"
    src = src.replace(old, new, 1)

path.write_text(src, encoding="utf-8")
print("Patched Patch 5B successfully.")