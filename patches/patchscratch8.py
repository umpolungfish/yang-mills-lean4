with open('input_file_7.txt', 'r', encoding='utf-8', errors='replace') as f:
    raw7 = f.read()
src = raw7[raw7.index('\n') + 1:]

p5a = [
    # 1. hneg in frobeniusNormSq_su_sub_le (lines 659-661)
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
    # 2. hmul in frobeniusNormSq_su_sub_one_eq (lines 699-701)
    (
        """    rw [star_sub, star_one, Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_sub,
      Matrix.one_mul, Matrix.mul_one, hA, two_smul]
    abel""",
        """    rw [star_sub, star_one, Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_sub]
    simp only [Matrix.one_mul, Matrix.mul_one]
    rw [hA, two_smul]
    abel""",
    ),
    # 3. wilsonAction_ball_le (lines 768-771)
    (
        """      rcases hp with ⟨x, rfl | rfl | rfl⟩ <;>
        dsimp [cubicPlaquette, pathHolonomy] <;>
        have hle := frobeniusNormSq_plaq4_le _ _ _ _ <;>
        linarith [hU (x, _), hU (cubicShift L _ x, _)]""",
        """      rcases hp with ⟨x, rfl | rfl | rfl⟩ <;>
        dsimp [cubicPlaquette, pathHolonomy] <;>
        refine (frobeniusNormSq_plaq4_le _ _ _ _).trans ?_
      · linarith only [hU (x, 0), hU (cubicShift L 0 x, 1), hU (cubicShift L 1 x, 0), hU (x, 1)]
      · linarith only [hU (x, 0), hU (cubicShift L 0 x, 2), hU (cubicShift L 2 x, 0), hU (x, 2)]
      · linarith only [hU (x, 1), hU (cubicShift L 1 x, 2), hU (cubicShift L 2 x, 1), hU (x, 2)]""",
    ),
    # 4. cubicLinkKineticKernel_ball_ge (lines 834-835)
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
    # 5. wilsonKernel_jump_le timeout (lines 956-978)
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
    # 6. latticeHaar_ball_ge (lines 1000-1017)
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
    # 7. wilsonKernel_ball_ge timeout (lines 1050-1095)
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
    # 8. lam0_ball_lb (lines 1144-1198)
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
        simp [RCLike.inner_apply, Complex.mul_re, mul_comm]
      refine h_re.trans ?_""",
    ),
    # 9. fullRank_dirichlet_step (lines 1431-1496)
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

for idx, (o, n) in enumerate(p5a, 1):
    assert src.count(o) == 1, f"p5a[{idx}] matched {src.count(o)}"
    src = src.replace(o, n, 1)

p5b = [
    # 10. fullRank_dirichlet_step inner sums & final linarith timeout
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
    # 11. fullRankCubic_gap_upper_bound fixes & linarith only timeouts
    (
        """  have h_flip_e0 : ∀ U, (e_flip U) ((0, 0, 0), 0) =
      centralElem N hN * U ((0, 0, 0), 0) := fun U => by
    dsimp [e_flip, sliceCenterFlipEquiv, sliceCenterFlip]
    rw [if_pos ⟨rfl, rfl⟩]""",
        """  have h_flip_e0 : ∀ U, (e_flip U) ((0, 0, 0), 0) =
      centralElem N hN * U ((0, 0, 0), 0) := fun U => by
    dsimp [e_flip, sliceCenterFlipEquiv, sliceCenterFlip]""",
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

for idx, (o, n) in enumerate(p5b, 1):
    assert src.count(o) == 1, f"p5b[{idx}] matched {src.count(o)}"
    src = src.replace(o, n, 1)

print("All p5a + p5b hunks verified cleanly!")
