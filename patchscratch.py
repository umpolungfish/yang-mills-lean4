with open('input_file_1.txt', 'r', encoding='utf-8', errors='replace') as f:
    raw = f.read()
src = raw[raw.index('\n') + 1:]

# Reconstruct current file after patches 1..6
p_all = [
    ("""  H_bd := fun x => by
    simp [osConfigForm]
    exact (osConfigForm iidOS4DStrict.toOS4DContinuumTheory iid_osConfigKernel_herm).pos_re x
  H_sa := fun x y => by simp [osConfigForm]
  H_nonneg := fun x => by simp [osConfigForm]""",
     """  H_bd := fun _ => by simp [osConfigForm, osConfigInner]
  H_sa := fun _ _ => by simp [osConfigForm, osConfigInner]
  H_nonneg := fun _ => by simp [osConfigForm, osConfigInner]"""),
    ("""  change ‖M i j‖ ^ 2 = (M i j * starRingEnd ℂ (M i j)).re
  rw [Complex.mul_conj, ← Complex.ofReal_pow]
  norm_cast
  exact (Complex.normSq_eq_norm_sq (M i j)).symm""",
     """  change ‖M i j‖ ^ 2 = (M i j * starRingEnd ℂ (M i j)).re
  rw [Complex.mul_conj, Complex.ofReal_re, Complex.normSq_eq_norm_sq]"""),
    ("""  rw [hstar, Matrix.mul_assoc, Matrix.trace_mul_comm (B : Matrix (Fin N) (Fin N) ℂ),
    ← Matrix.mul_assoc, hB, Matrix.one_mul]""",
     """  rw [hstar, Matrix.mul_assoc, Matrix.trace_mul_comm (B : Matrix (Fin N) (Fin N) ℂ),
    ← Matrix.mul_assoc, Matrix.mul_assoc (M * star M), hB, Matrix.mul_one]"""),
    ("""  have h1 : ‖(M₁ + M₂) i j‖ ≤ ‖M₁ i j‖ + ‖M₂ i j‖ := norm_add_le (M₁ i j) (M₂ i j)
  nlinarith [sq_nonneg (‖M₁ i j‖ - ‖M₂ i j‖), norm_nonneg (M₁ i j), norm_nonneg (M₂ i j)]""",
     """  have h1 : ‖(M₁ + M₂) i j‖ ≤ ‖M₁ i j‖ + ‖M₂ i j‖ := norm_add_le (M₁ i j) (M₂ i j)
  have h2 : ‖(M₁ + M₂) i j‖ ^ 2 ≤ (‖M₁ i j‖ + ‖M₂ i j‖) ^ 2 :=
    pow_le_pow_left₀ (norm_nonneg _) h1 2
  linarith [sq_nonneg (‖M₁ i j‖ - ‖M₂ i j‖)]"""),
    ("""    rw [Matrix.sub_mul, Matrix.one_mul]; change _ = _; abel""",
     """    rw [Matrix.sub_mul, Matrix.one_mul]
    change (A : Matrix (Fin N) (Fin N) ℂ) * (B : Matrix (Fin N) (Fin N) ℂ) - 1 =
      ((A : Matrix (Fin N) (Fin N) ℂ) * (B : Matrix (Fin N) (Fin N) ℂ) -
        (B : Matrix (Fin N) (Fin N) ℂ)) + ((B : Matrix (Fin N) (Fin N) ℂ) - 1)
    abel"""),
    ("""    calc ‖(A : Matrix (Fin N) (Fin N) ℂ) i j‖ ^ 2
        ≤ ∑ k : Fin N, ‖(A : Matrix (Fin N) (Fin N) ℂ) k j‖ ^ 2 :=
          Finset.single_le_sum (fun _ _ => sq_nonneg _) (Finset.mem_univ i)""",
     """    calc ‖(A : Matrix (Fin N) (Fin N) ℂ) i j‖ ^ 2
        ≤ ∑ k : Fin N, ‖(A : Matrix (Fin N) (Fin N) ℂ) k j‖ ^ 2 :=
          Finset.single_le_sum (fun k _ => sq_nonneg ‖(A : Matrix (Fin N) (Fin N) ℂ) k j‖)
            (Finset.mem_univ i)"""),
    ("""  have hK_ge : 4 * (N : ℝ) / δ ≤ (K : ℝ) :=
    (Nat.le_ceil _).trans (by exact_mod_cast Nat.le_succ _)""",
     """  have hK_ge : 4 * (N : ℝ) / δ ≤ (K : ℝ) :=
    (Nat.le_ceil _).trans (by dsimp [K]; push_cast; linarith)"""),
    ("""      have ht_nn : 0 ≤ t := by dsimp [t]; positivity""",
     """      have ht_nn : 0 ≤ t := by
        dsimp [t]
        have hr1_nn : 0 ≤ r + 1 := by linarith
        positivity"""),
    ("""      unfold frobeniusNormSq
      refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
      exact (continuous_norm.comp (((continuous_apply j).comp
        ((continuous_apply i).comp continuous_subtype_val)).sub continuous_const)).pow 2""",
     """      unfold frobeniusNormSq
      refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
      simp only [Matrix.sub_apply]
      exact (continuous_norm.comp (((continuous_apply j).comp
        ((continuous_apply i).comp continuous_subtype_val)).sub continuous_const)).pow 2"""),
    ("""      _ ≤ ∑ b : Idx, suHaar N (box b) := MeasureTheory.measure_iUnion_le _""",
     """      _ ≤ ∑ b : Idx, suHaar N (box b) := MeasureTheory.measure_iUnion_fintype_le (suHaar N) box"""),
    ("""  ⟨c • (1 : Matrix (Fin N) (Fin N) ℂ),
    Unitary.mem_iff.mpr
      ⟨by ext i j; by_cases hij : i = j <;> simp [Matrix.mul_apply, hij, hc_mul],
       by ext i j; by_cases hij : i = j <;>
            simp [Matrix.mul_apply, hij, show c * star c = 1 from by rw [mul_comm]; exact hc_mul]⟩,
    by rw [Matrix.det_smul, Matrix.det_one, smul_eq_mul, mul_one, hc_pow]⟩

private lemma centralElem_ne_one (N : ℕ) (hN : 2 ≤ N) :
    Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) ≠ 1 := by
  have hN_pos : (0 : ℝ) < (N : ℝ) := by exact_mod_cast (by omega : 0 < N)
  have hθ_pos : 0 < 2 * Real.pi / (N : ℝ) := div_pos (mul_pos two_pos Real.pi_pos) hN_pos
  have hθ_le : 2 * Real.pi / (N : ℝ) ≤ Real.pi := by
    rw [div_le_iff₀ hN_pos]
    nlinarith [Real.pi_pos, (by exact_mod_cast hN : (2 : ℝ) ≤ (N : ℝ))]
  have hcos_lt : Real.cos (2 * Real.pi / (N : ℝ)) < 1 := by
    rcases eq_or_lt_of_le hθ_le with heq | hlt
    · rw [heq, Real.cos_pi]; norm_num
    · exact Real.cos_lt_one_of_ne_zero ⟨by linarith, by linarith⟩
  have hre : (Complex.exp (2 * Real.pi * Complex.I / (N : ℂ))).re =
      Real.cos (2 * Real.pi / (N : ℝ)) := by
    rw [show 2 * (Real.pi : ℂ) * Complex.I / (N : ℂ) =
      (((2 * Real.pi / (N : ℝ)) : ℝ) : ℂ) * Complex.I by push_cast; ring]
    rw [Complex.exp_ofReal_mul_I_re]
  intro heq
  have hre_eq := congrArg Complex.re heq
  rw [hre, Complex.one_re] at hre_eq
  linarith

private lemma centralElem_comm {N : ℕ} (hN : 2 ≤ N)
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    centralElem N hN * A = A * centralElem N hN := by
  ext i j
  change ((Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) • (1 : Matrix (Fin N) (Fin N) ℂ)) *
      (A : Matrix (Fin N) (Fin N) ℂ)) i j =
    ((A : Matrix (Fin N) (Fin N) ℂ) *
      (Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) • (1 : Matrix (Fin N) (Fin N) ℂ))) i j
  simp [Matrix.smul_mul, Matrix.mul_smul]

private def sliceCenterFlip (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) :=
  fun e => if e.1.1 = 0 ∧ e.2 = 0 then centralElem N hN * U e else U e

private lemma sliceCenterFlip_measurePreserving (L N : ℕ) [NeZero L] (hN : 2 ≤ N) :
    letI := canonSUMeas N
    haveI := canonSUBorel N
    MeasureTheory.MeasurePreserving (sliceCenterFlip L N hN)
      (latticeHaarMeasure L N) (latticeHaarMeasure L N) := by
  letI := canonSUMeas N
  haveI := canonSUBorel N
  haveI := suHaar_prob N
  let φ : (cubicTorus3 L).Link →
      Matrix.specialUnitaryGroup (Fin N) ℂ → Matrix.specialUnitaryGroup (Fin N) ℂ :=
    fun e u => if e.1.1 = 0 ∧ e.2 = 0 then centralElem N hN * u else u
  have hφ_meas : ∀ e, Measurable (φ e) := fun e => by
    dsimp [φ]; split_ifs
    · exact (continuous_mul_left _).measurable
    · exact measurable_id
  have hmeas : Measurable (sliceCenterFlip L N hN) :=
    measurable_pi_iff.mpr fun e => (hφ_meas e).comp (measurable_pi_apply e)
  refine ⟨hmeas, ?_⟩
  symm
  refine MeasureTheory.Measure.pi_eq fun s hs => ?_
  rw [MeasureTheory.Measure.map_apply hmeas (MeasurableSet.univ_pi hs)]
  have hpre : sliceCenterFlip L N hN ⁻¹' Set.pi Set.univ s =
      Set.pi Set.univ (fun e => φ e ⁻¹' s e) := by
    ext U; simp [sliceCenterFlip, φ]
  rw [hpre, MeasureTheory.Measure.pi_pi (fun _ => suHaar N) _]
  refine Finset.prod_congr rfl fun e _ => ?_
  dsimp [φ]; split_ifs
  · have hmap := suHaar_map_mul_left N (centralElem N hN)
    rw [← MeasureTheory.Measure.map_apply (continuous_mul_left _).measurable (hs e), hmap]
  · rfl

private lemma wilsonAction_sliceCenterFlip (L N : ℕ) [NeZero L] (hN : 2 ≤ N) (β : ℝ)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonAction β (cubicPlaquettes L) (sliceCenterFlip L N hN U) =
      wilsonAction β (cubicPlaquettes L) U := by
  unfold wilsonAction
  congr 1
  have h_plaq : ∀ p ∈ cubicPlaquettes L,
      wilsonPlaquetteTerm p (sliceCenterFlip L N hN U) = wilsonPlaquetteTerm p U := by
    intro p hp
    unfold wilsonPlaquetteTerm
    suffices hhol : pathHolonomy (sliceCenterFlip L N hN U) p.loop = pathHolonomy U p.loop by
      rw [hhol]
    unfold cubicPlaquettes at hp
    simp only [List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and,
      List.mem_cons, List.not_mem_nil, or_false] at hp
    rcases hp with ⟨x, rfl | rfl | rfl⟩
    · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
      by_cases hx : x.1 = 0
      · simp only [hx, true_and, ↓reduceIte, mul_inv_rev]
        have hc := centralElem_comm hN
        group
        -- Cancel z and z⁻¹ using centralElem_comm
        rw [mul_assoc (centralElem N hN), ← mul_assoc (U (x, 0)),
          ← hc (U (x, 0)), mul_assoc (U (x, 0))]
        have h1 : U ((x.1 + 1, x.2.1, x.2.2), 1) *
            ((U ((x.1, x.2.1 + 1, x.2.2), 0))⁻¹ * (centralElem N hN)⁻¹) =
            (centralElem N hN)⁻¹ * (U ((x.1 + 1, x.2.1, x.2.2), 1) *
              (U ((x.1, x.2.1 + 1, x.2.2), 0))⁻¹) := by
          rw [mul_assoc, ← (by
            have := congrArg (fun M => (M⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ))
              (hc (U ((x.1 + 1, x.2.1, x.2.2), 1))⁻¹)
            simpa [mul_inv_rev] using this)]
          group
          rw [← hc (U ((x.1 + 1, x.2.1, x.2.2), 1))]
          group
        rw [← mul_assoc (centralElem N hN), mul_assoc (U (x, 0)), mul_assoc (centralElem N hN),
          h1]
        group
      · simp [hx]
    · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
      by_cases hx : x.1 = 0
      · simp only [hx, true_and, ↓reduceIte, mul_inv_rev]
        have hc := centralElem_comm hN
        have hc_inv : ∀ A : Matrix.specialUnitaryGroup (Fin N) ℂ,
            A * (centralElem N hN)⁻¹ = (centralElem N hN)⁻¹ * A := fun A => by
          have h := congrArg (fun M => (centralElem N hN)⁻¹ * M * (centralElem N hN)⁻¹) (hc A)
          simpa [mul_assoc] using h.symm
        calc centralElem N hN * U (x, 0) *
              (U ((x.1 + 1, x.2.1, x.2.2), 2) *
                ((U ((x.1, x.2.1, x.2.2 + 1), 0))⁻¹ * (centralElem N hN)⁻¹ *
                  ((U (x, 2))⁻¹ * 1)))
            = centralElem N hN * (U (x, 0) *
                ((U ((x.1 + 1, x.2.1, x.2.2), 2) * (U ((x.1, x.2.1, x.2.2 + 1), 0))⁻¹) *
                  (centralElem N hN)⁻¹ * ((U (x, 2))⁻¹ * 1))) := by
                simp only [mul_assoc]
                congr 2; congr 1
                rw [← mul_assoc, hc_inv]
                simp only [mul_assoc]
          _ = centralElem N hN * ((centralElem N hN)⁻¹ * (U (x, 0) *
                (U ((x.1 + 1, x.2.1, x.2.2), 2) *
                  ((U ((x.1, x.2.1, x.2.2 + 1), 0))⁻¹ * ((U (x, 2))⁻¹ * 1))))) := by
                congr 1
                rw [← mul_assoc _ (centralElem N hN)⁻¹, hc_inv, ← mul_assoc, hc_inv]
                simp only [mul_assoc]
          _ = U (x, 0) * (U ((x.1 + 1, x.2.1, x.2.2), 2) *
                ((U ((x.1, x.2.1, x.2.2 + 1), 0))⁻¹ * ((U (x, 2))⁻¹ * 1))) := by
                rw [← mul_assoc, mul_inv_cancel, one_mul]
      · simp [hx]
    · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
      simp [show (1 : Fin 3) ≠ 0 by decide, show (2 : Fin 3) ≠ 0 by decide]
  induction cubicPlaquettes L with
  | nil => rfl
  | cons p ps ih =>
    simp only [List.map_cons, List.sum_cons]
    have hp1 : p ∈ p :: ps := List.mem_cons_self
    sorry -- (note: below we avoid `induction` on `cubicPlaquettes L` directly via `List.map_congr_left`)

-- Note: clean non-sorry version of `wilsonAction_sliceCenterFlip` uses `List.map_congr_left`
private lemma wilsonAction_sliceCenterFlip' (L N : ℕ) [NeZero L] (hN : 2 ≤ N) (β : ℝ)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonAction β (cubicPlaquettes L) (sliceCenterFlip L N hN U) =
      wilsonAction β (cubicPlaquettes L) U := by
  have hc := centralElem_comm hN
  have hc_inv : ∀ A : Matrix.specialUnitaryGroup (Fin N) ℂ,
      A * (centralElem N hN)⁻¹ = (centralElem N hN)⁻¹ * A := fun A => by
    have h := congrArg (fun M => (centralElem N hN)⁻¹ * M * (centralElem N hN)⁻¹) (hc A)
    simpa [mul_assoc] using h.symm
  have h_cancel : ∀ A B C D : Matrix.specialUnitaryGroup (Fin N) ℂ,
      (centralElem N hN * A) * (B * ((C * centralElem N hN)⁻¹ * (D * 1))) =
        A * (B * (C⁻¹ * (D * 1))) := by
    intro A B C D
    rw [mul_inv_rev]
    calc (centralElem N hN * A) * (B * ((centralElem N hN)⁻¹ * C⁻¹ * (D * 1)))
        = centralElem N hN * (A * ((B * (centralElem N hN)⁻¹) * (C⁻¹ * (D * 1)))) := by
            simp only [mul_assoc]
      _ = centralElem N hN * (A * (((centralElem N hN)⁻¹ * B) * (C⁻¹ * (D * 1)))) := by
            rw [hc_inv B]
      _ = centralElem N hN * ((A * (centralElem N hN)⁻¹) * (B * (C⁻¹ * (D * 1)))) := by
            simp only [mul_assoc]
      _ = centralElem N hN * (((centralElem N hN)⁻¹ * A) * (B * (C⁻¹ * (D * 1)))) := by
            rw [hc_inv A]
      _ = (centralElem N hN * (centralElem N hN)⁻¹) * (A * (B * (C⁻¹ * (D * 1)))) := by
            simp only [mul_assoc]
      _ = A * (B * (C⁻¹ * (D * 1))) := by rw [mul_inv_cancel, one_mul]
  unfold wilsonAction
  congr 1
  congr 1
  refine List.map_congr_left fun p hp => ?_
  unfold wilsonPlaquetteTerm
  suffices hhol : pathHolonomy (sliceCenterFlip L N hN U) p.loop = pathHolonomy U p.loop by
    rw [hhol]
  unfold cubicPlaquettes at hp
  simp only [List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and,
    List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with ⟨x, rfl | rfl | rfl⟩
  · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
    by_cases hx : x.1 = 0
    · simp only [hx, true_and, ↓reduceIte, show (1 : Fin 3) ≠ 0 by decide, and_false]
      exact h_cancel (U (x, 0)) (U ((x.1 + 1, x.2.1, x.2.2), 1))
        (U ((x.1, x.2.1 + 1, x.2.2), 0)) (U (x, 1))⁻¹
    · simp [hx]
  · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
    by_cases hx : x.1 = 0
    · simp only [hx, true_and, ↓reduceIte, show (2 : Fin 3) ≠ 0 by decide, and_false]
      exact h_cancel (U (x, 0)) (U ((x.1 + 1, x.2.1, x.2.2), 2))
        (U ((x.1, x.2.1, x.2.2 + 1), 0)) (U (x, 2))⁻¹
    · simp [hx]
  · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
    simp [show (1 : Fin 3) ≠ 0 by decide, show (2 : Fin 3) ≠ 0 by decide]

private lemma wilsonGramKernel_sliceCenterFlip (L N : ℕ) [NeZero L] (hN : 2 ≤ N) (β : ℝ)
    (U U' : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    letI := canonSUMeas N
    haveI := canonSUBorel N
    wilsonGramKernel L N (cubicLinkKineticKernel L N β)
      (sliceCenterFlip L N hN U) (sliceCenterFlip L N hN U') =
      wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' := by
  letI := canonSUMeas N
  haveI := canonSUBorel N
  have hmp := sliceCenterFlip_measurePreserving L N hN
  unfold wilsonGramKernel
  rw [← hmp.integral_comp' (fun W => cubicLinkKineticKernel L N β
    (sliceCenterFlip L N hN U) W * cubicLinkKineticKernel L N β (sliceCenterFlip L N hN U') W)]""",
     """  have hc_mul1 : (starRingEnd ℂ) c * c = 1 := hc_mul
  have hc_mul2 : c * (starRingEnd ℂ) c = 1 := by rw [mul_comm]; exact hc_mul
  ⟨c • (1 : Matrix (Fin N) (Fin N) ℂ),
    Unitary.mem_iff.mpr
      ⟨by ext i j; by_cases hij : i = j <;>
            simp [Matrix.mul_apply, Matrix.one_apply, hij, hc_mul1],
       by ext i j; by_cases hij : i = j <;>
            simp [Matrix.mul_apply, Matrix.one_apply, hij, hc_mul2]⟩,
    by
      change Matrix.det (c • (1 : Matrix (Fin N) (Fin N) ℂ)) = 1
      simp [Matrix.det_smul, hc_pow]⟩

private lemma centralElem_ne_one (N : ℕ) (hN : 2 ≤ N) :
    Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) ≠ 1 := by
  have hN_pos : (0 : ℝ) < (N : ℝ) := by exact_mod_cast (by omega : 0 < N)
  have hθ_pos : 0 < 2 * Real.pi / (N : ℝ) := div_pos (mul_pos two_pos Real.pi_pos) hN_pos
  have hθ_le : 2 * Real.pi / (N : ℝ) ≤ Real.pi := by
    rw [div_le_iff₀ hN_pos, mul_comm Real.pi (N : ℝ)]
    exact mul_le_mul_of_nonneg_right (by exact_mod_cast hN) Real.pi_pos.le
  have hcos_lt : Real.cos (2 * Real.pi / (N : ℝ)) < 1 := by
    simpa [Real.cos_zero] using Real.cos_lt_cos_of_nonneg_of_le_pi le_rfl hθ_le hθ_pos
  have hre : (Complex.exp (2 * Real.pi * Complex.I / (N : ℂ))).re =
      Real.cos (2 * Real.pi / (N : ℝ)) := by
    rw [show 2 * (Real.pi : ℂ) * Complex.I / (N : ℂ) =
      (((2 * Real.pi / (N : ℝ)) : ℝ) : ℂ) * Complex.I by push_cast; ring]
    rw [Complex.exp_ofReal_mul_I_re]
  intro heq
  have hre_eq := congrArg Complex.re heq
  rw [hre, Complex.one_re] at hre_eq
  linarith

private lemma centralElem_comm {N : ℕ} (hN : 2 ≤ N)
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    centralElem N hN * A = A * centralElem N hN := by
  ext i j
  change ((Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) • (1 : Matrix (Fin N) (Fin N) ℂ)) *
      (A : Matrix (Fin N) (Fin N) ℂ)) i j =
    ((A : Matrix (Fin N) (Fin N) ℂ) *
      (Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) • (1 : Matrix (Fin N) (Fin N) ℂ))) i j
  simp [Matrix.smul_mul, Matrix.mul_smul]

private noncomputable def sliceCenterFlip (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) :=
  fun e => if e.1.1 = 0 ∧ e.2 = 0 then centralElem N hN * U e else U e

private noncomputable def sliceCenterFlipEquiv (L N : ℕ) [NeZero L] (hN : 2 ≤ N) :
    GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) ≃ᵐ
      GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) where
  toFun := sliceCenterFlip L N hN
  invFun := fun U e => if e.1.1 = 0 ∧ e.2 = 0 then (centralElem N hN)⁻¹ * U e else U e
  left_inv := fun U => funext fun e => by
    dsimp [sliceCenterFlip]; split_ifs <;> simp only [inv_mul_cancel_left]
  right_inv := fun U => funext fun e => by
    dsimp [sliceCenterFlip]; split_ifs <;> simp only [mul_inv_cancel_left]
  measurable_toFun := by
    refine measurable_pi_iff.mpr fun e => ?_
    by_cases h : e.1.1 = 0 ∧ e.2 = 0
    · simpa [sliceCenterFlip, h] using
        (continuous_mul_left (centralElem N hN)).measurable.comp (measurable_pi_apply e)
    · simpa [sliceCenterFlip, h] using measurable_pi_apply e
  measurable_invFun := by
    refine measurable_pi_iff.mpr fun e => ?_
    by_cases h : e.1.1 = 0 ∧ e.2 = 0
    · simpa [h] using
        (continuous_mul_left (centralElem N hN)⁻¹).measurable.comp (measurable_pi_apply e)
    · simpa [h] using measurable_pi_apply e

private lemma sliceCenterFlip_measurePreserving (L N : ℕ) [NeZero L] (hN : 2 ≤ N) :
    MeasureTheory.MeasurePreserving (sliceCenterFlip L N hN)
      (latticeHaarMeasure L N) (latticeHaarMeasure L N) := by
  haveI := suHaar_prob N
  let φ : (cubicTorus3 L).Link →
      Matrix.specialUnitaryGroup (Fin N) ℂ → Matrix.specialUnitaryGroup (Fin N) ℂ :=
    fun e u => if e.1.1 = 0 ∧ e.2 = 0 then centralElem N hN * u else u
  have hφ_meas : ∀ e, Measurable (φ e) := fun e => by
    dsimp [φ]; split_ifs
    · exact (continuous_mul_left _).measurable
    · exact measurable_id
  have hmeas : Measurable (sliceCenterFlip L N hN) :=
    measurable_pi_iff.mpr fun e => (hφ_meas e).comp (measurable_pi_apply e)
  refine ⟨hmeas, ?_⟩
  symm
  refine MeasureTheory.Measure.pi_eq fun s hs => ?_
  refine (MeasureTheory.Measure.map_apply hmeas (MeasurableSet.univ_pi hs)).trans ?_
  have hpre : sliceCenterFlip L N hN ⁻¹' Set.pi Set.univ s =
      Set.pi Set.univ (fun e => φ e ⁻¹' s e) := by
    ext U
    change (∀ e ∈ Set.univ, sliceCenterFlip L N hN U e ∈ s e) ↔
      (∀ e ∈ Set.univ, U e ∈ φ e ⁻¹' s e)
    simp [sliceCenterFlip, φ]
  rw [hpre]
  erw [MeasureTheory.Measure.pi_pi (fun _ => suHaar N) _]
  refine Finset.prod_congr rfl fun e _ => ?_
  dsimp [φ]; split_ifs
  · have hcomm : (fun u => centralElem N hN * u) = (fun u => u * centralElem N hN) :=
      funext (centralElem_comm hN)
    rw [hcomm, ← MeasureTheory.Measure.map_apply
        (continuous_mul_right (centralElem N hN)).measurable (hs e),
      suHaar_map_mul_right N (centralElem N hN)]
  · rfl

private lemma sliceCenterFlip_integral_comp {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    (hmp : MeasureTheory.MeasurePreserving (sliceCenterFlip L N hN)
      (latticeHaarMeasure L N) (latticeHaarMeasure L N))
    (f : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → E) :
    ∫ U, f (sliceCenterFlip L N hN U) ∂(latticeHaarMeasure L N) =
      ∫ U, f U ∂(latticeHaarMeasure L N) :=
  MeasureTheory.MeasurePreserving.integral_comp'
    (f := sliceCenterFlipEquiv L N hN) ⟨(sliceCenterFlipEquiv L N hN).measurable, hmp.map_eq⟩ f

private lemma su_central_cancel {N : ℕ} (z : Matrix.specialUnitaryGroup (Fin N) ℂ)
    (hz : ∀ A, z * A = A * z) (A B C D : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    (z * A) * (B * ((z * C)⁻¹ * (D * 1))) = A * (B * (C⁻¹ * (D * 1))) := by
  have hz_inv : ∀ X, X * z⁻¹ = z⁻¹ * X := fun X => by
    have h := congrArg (fun M => z⁻¹ * M * z⁻¹) (hz X)
    simpa [mul_assoc] using h
  rw [mul_inv_rev, hz_inv C⁻¹]
  calc (z * A) * (B * (z⁻¹ * C⁻¹ * (D * 1)))
      = z * (A * ((B * z⁻¹) * (C⁻¹ * (D * 1)))) := by simp only [mul_assoc]
    _ = z * (A * ((z⁻¹ * B) * (C⁻¹ * (D * 1)))) := by rw [hz_inv B]
    _ = z * ((A * z⁻¹) * (B * (C⁻¹ * (D * 1)))) := by simp only [mul_assoc]
    _ = z * ((z⁻¹ * A) * (B * (C⁻¹ * (D * 1)))) := by rw [hz_inv A]
    _ = (z * z⁻¹) * (A * (B * (C⁻¹ * (D * 1)))) := by simp only [mul_assoc]
    _ = A * (B * (C⁻¹ * (D * 1))) := by rw [mul_inv_cancel, one_mul]

private lemma wilsonAction_sliceCenterFlip' (L N : ℕ) [NeZero L] (hN : 2 ≤ N) (β : ℝ)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonAction β (cubicPlaquettes L) (sliceCenterFlip L N hN U) =
      wilsonAction β (cubicPlaquettes L) U := by
  have h10 : (1 : Fin 3) ≠ 0 := by decide
  have h20 : (2 : Fin 3) ≠ 0 := by decide
  have h_cancel := su_central_cancel (centralElem N hN) (centralElem_comm hN)
  unfold wilsonAction
  congr 1
  congr 1
  refine List.map_congr_left fun p hp => ?_
  unfold wilsonPlaquetteTerm
  suffices hhol : pathHolonomy (sliceCenterFlip L N hN U) p.loop = pathHolonomy U p.loop by
    rw [hhol]
  unfold cubicPlaquettes at hp
  simp only [List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and,
    List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with ⟨x, rfl | rfl | rfl⟩
  · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
    by_cases hx : x.1 = 0
    · simp only [hx, h10, and_false, and_true, true_and, ↓reduceIte]
      exact h_cancel _ _ _ _
    · simp only [hx, h10, and_false, false_and, ↓reduceIte]
  · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
    by_cases hx : x.1 = 0
    · simp only [hx, h20, and_false, and_true, true_and, ↓reduceIte]
      exact h_cancel _ _ _ _
    · simp only [hx, h20, and_false, false_and, ↓reduceIte]
  · dsimp [cubicPlaquette, pathHolonomy, sliceCenterFlip, cubicShift]
    simp only [h10, h20, and_false, ↓reduceIte]

private lemma wilsonAction_sliceCenterFlip (L N : ℕ) [NeZero L] (hN : 2 ≤ N) (β : ℝ)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonAction β (cubicPlaquettes L) (sliceCenterFlip L N hN U) =
      wilsonAction β (cubicPlaquettes L) U :=
  wilsonAction_sliceCenterFlip' L N hN β U

private lemma wilsonGramKernel_sliceCenterFlip (L N : ℕ) [NeZero L] (hN : 2 ≤ N) (β : ℝ)
    (U U' : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonGramKernel L N (cubicLinkKineticKernel L N β)
      (sliceCenterFlip L N hN U) (sliceCenterFlip L N hN U') =
      wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' := by
  have hmp := sliceCenterFlip_measurePreserving L N hN
  unfold wilsonGramKernel
  rw [← sliceCenterFlip_integral_comp L N hN hmp (fun W => cubicLinkKineticKernel L N β
    (sliceCenterFlip L N hN U) W * cubicLinkKineticKernel L N β (sliceCenterFlip L N hN U') W)]"""),
    ("""    · have hconj : (centralElem N hN * X e) * (centralElem N hN * Y e)⁻¹ =
          centralElem N hN * (X e * (Y e)⁻¹) * (centralElem N hN)⁻¹ := by
        simp only [mul_inv_rev]; group
      rw [hconj, su_trace_conj']""",
     """    · suffices htr : Matrix.trace
          (((centralElem N hN * X e : Matrix.specialUnitaryGroup (Fin N) ℂ) :
              Matrix (Fin N) (Fin N) ℂ) *
            (((centralElem N hN * Y e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
              Matrix (Fin N) (Fin N) ℂ)) =
          Matrix.trace
            (((X e : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) *
              (((Y e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ)) by
        rw [htr]
      have h1 : (((centralElem N hN * X e : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ) *
          (((centralElem N hN * Y e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ)) =
          ((centralElem N hN : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ) *
          (((X e * (Y e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ) *
          (((centralElem N hN)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ)) := by
        simp only [← Submonoid.coe_mul, mul_inv_rev, mul_assoc]
      have hinv : (((centralElem N hN)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ) *
          ((centralElem N hN : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ) = 1 := by
        rw [← Submonoid.coe_mul, inv_mul_cancel, OneMemClass.coe_one]
      rw [h1, Matrix.trace_mul_comm, Matrix.mul_assoc, hinv, Matrix.mul_one, Submonoid.coe_mul]"""),
    ("""theorem fullRankCubic_gap_upper_bound (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    {β : ℝ} (hβ : 1 ≤ β) :
    letI := canonSUMeas N
    haveI := canonSUBorel N
    have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
    let S := (fullRankCubicNonAbelianWilsonSetup L N hN β hβ_pos).gaugeSetup
    let links : ℕ := 3 * L ^ 3
    let ε_sq : ℝ := 4 * (N : ℝ) * ((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β) / β
    let K : ℕ := Nat.ceil (4 * (N : ℝ) / (1 / Real.sqrt β)) + 1
    let err : ℝ := (2 * ε_sq + 8 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
      ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) /
      (N : ℝ)
    err < 1 →
    S.Δ ≤ -Real.log (1 - err) := by
  letI := canonSUMeas N
  haveI := canonSUBorel N
  haveI : NeZero N := ⟨by omega⟩
  have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
  have hN_pos : (0 : ℝ) < (N : ℝ) := by exact_mod_cast (by omega : 0 < N)
  intro S links ε_sq K err herr_lt""",
     """theorem fullRankCubic_gap_upper_bound (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    {β : ℝ} (hβ : 1 ≤ β) :
    let S := (fullRankCubicNonAbelianWilsonSetup L N hN β
      (lt_of_lt_of_le zero_lt_one hβ)).gaugeSetup
    let links : ℕ := 3 * L ^ 3
    let ε_sq : ℝ := 4 * (N : ℝ) * ((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β) / β
    let K : ℕ := Nat.ceil (4 * (N : ℝ) / (1 / Real.sqrt β)) + 1
    let err : ℝ := (2 * ε_sq + 8 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
      ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) /
      (N : ℝ)
    err < 1 →
    S.Δ ≤ -Real.log (1 - err) := by
  haveI : NeZero N := ⟨by omega⟩
  have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
  have hN_pos : (0 : ℝ) < (N : ℝ) := by exact_mod_cast (by omega : 0 < N)
  intro S links ε_sq K err herr_lt"""),
    ("""  let e_flip := sliceCenterFlip L N hN
  let hmp := sliceCenterFlip_measurePreserving L N hN""",
     """  let e_flip := sliceCenterFlipEquiv L N hN
  let hmp : MeasureTheory.MeasurePreserving e_flip μ μ :=
    ⟨e_flip.measurable, (sliceCenterFlip_measurePreserving L N hN).map_eq⟩"""),
    ("""          simp only [Pi.add_apply] at ha1 ha2 ⊢; rw [hu1, ha1, ha2, hx := hu2, hu3]""",
     """          simp only [Pi.add_apply] at ha1 ha2 ⊢; rw [hu1, ha1, ha2, hu2, hu3]"""),
    ("""  have hKW_flip : ∀ U U', K_W (e_flip U) (e_flip U') = K_W U U' := fun U U' => by
    dsimp [K_W, wilsonKernel, e_flip]
    rw [wilsonAction_sliceCenterFlip', wilsonAction_sliceCenterFlip',
      wilsonGramKernel_sliceCenterFlip]""",
     """  have hKW_flip : ∀ U U', K_W (e_flip U) (e_flip U') = K_W U U' := fun U U' => by
    change K_W (sliceCenterFlip L N hN U) (sliceCenterFlip L N hN U') = K_W U U'
    dsimp [K_W, wilsonKernel, K_kin, χ]
    rw [wilsonAction_sliceCenterFlip', wilsonAction_sliceCenterFlip',
      wilsonGramKernel_sliceCenterFlip]"""),
    ("""    change ⇑(T_raw (Z_op ψ)) U = ⇑(Z_op (T_raw ψ)) U
    rw [hu1, hu2, hu3]
    dsimp [wilsonIntegralFn]
    rw [← hmp.integral_comp' (fun U' => ((K_W (e_flip U) U' : ℝ) : ℂ) * ψ U')]
    refine MeasureTheory.integral_congr_ae ?_
    filter_upwards [hZψ] with U' hu'
    change ((K_W U U' : ℝ) : ℂ) * ⇑(Z_op ψ) U' =
      ((K_W (e_flip U) (e_flip U') : ℝ) : ℂ) * ⇑ψ (e_flip U')
    rw [hKW_flip, hu']""",
     """    have hu1' : ⇑(T_raw (Z_op ψ)) U = wilsonIntegralFn L N β K_kin (Z_op ψ) U := hu1
    have hu2' : ⇑(Z_op (T_raw ψ)) U = ⇑(T_raw ψ) (e_flip U) := hu2
    have hu3' : ⇑(T_raw ψ) (e_flip U) = wilsonIntegralFn L N β K_kin ψ (e_flip U) := hu3
    rw [hu1', hu2', hu3']
    dsimp [wilsonIntegralFn]
    rw [← hmp.integral_comp' (fun U' => ((K_W (e_flip U) U' : ℝ) : ℂ) * ψ U')]
    refine MeasureTheory.integral_congr_ae ?_
    filter_upwards [hZψ] with U' hu'
    have hu'' : ⇑(Z_op ψ) U' = ⇑ψ (e_flip U') := hu'
    change ((K_W U U' : ℝ) : ℂ) * ⇑(Z_op ψ) U' =
      ((K_W (e_flip U) (e_flip U') : ℝ) : ℂ) * ⇑ψ (e_flip U')
    rw [hKW_flip, hu'']"""),
    ("""  have hZΩ : Z_op Ω = Ω := by
    have h_eig : T_raw (Z_op Ω) = (lam0 : ℂ) • Z_op Ω := by
      rw [hT_comm_Z, hgs.eig, map_smul]
    let c : ℂ := ⟪Ω, Z_op Ω⟫_ℂ
    let w := Z_op Ω - c • Ω
    have hw_orth : ⟪w, Ω⟫_ℂ = 0 := by
      have h1 : ⟪Ω, Ω⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K, hgs.unit]; norm_num
      simp [w, c, inner_sub_left, inner_smul_left, h1, inner_conj_symm]
    have hw_eig : T_raw w = (lam0 : ℂ) • w := by
      simp [w, map_sub, map_smul, h_eig, hgs.eig, smul_sub, smul_comm]
    have hw0 : Z_op Ω = c • Ω := sub_eq_zero.mp (hgs.simple w hw_eig hw_orth)
    have hc_norm : ‖c‖ = 1 := by
      have h1 : ‖c • Ω‖ = 1 := by
        rw [← hw0, ← sq_eq_sq₀ (norm_nonneg _) zero_le_one]
        have hin : (⟪Z_op Ω, Z_op Ω⟫_ℂ).re = 1 := by
          rw [hZ_unit, inner_self_eq_norm_sq_to_K, hgs.unit]; norm_num
        rwa [inner_self_eq_norm_sq_to_K] at hin
      rwa [norm_smul, hgs.unit, mul_one] at h1
    have hZΩ_ae : ⇑(Z_op Ω) =ᵐ[μ] fun U => (ω (e_flip U) : ℂ) := by
      have h1 := (memLp_comp_measurePreserving μ e_flip hmp Ω).coeFn_toLp
      have h2 := ae_comp_measurePreserving hmp hgs.ae_eq
      filter_upwards [h1, h2] with U hu1 hu2; change ⇑(Z_op Ω) U = _; rw [hu1, hu2]""",
     """  have hZΩ : Z_op Ω = Ω := by
    have h_T_eig : T_raw Ω = (lam0 : ℂ) • Ω := hgs.eig
    have h_eig : T_raw (Z_op Ω) = (lam0 : ℂ) • Z_op Ω := by
      rw [hT_comm_Z, h_T_eig, map_smul]
    let c : ℂ := ⟪Ω, Z_op Ω⟫_ℂ
    let w := Z_op Ω - c • Ω
    have hw_orth : ⟪w, Ω⟫_ℂ = 0 := by
      simp [w, c, inner_sub_left, inner_smul_left, inner_conj_symm, hgs.unit]
    have hw_eig : T_raw w = (lam0 : ℂ) • w := by
      dsimp only [w]
      rw [map_sub, map_smul, h_eig, h_T_eig, smul_sub, smul_comm (lam0 : ℂ) c Ω]
    have hw0 : Z_op Ω = c • Ω := sub_eq_zero.mp (hgs.simple w hw_eig hw_orth)
    have hc_norm : ‖c‖ = 1 := by
      have h1 : ‖c • Ω‖ = 1 := by
        rw [← hw0, ← sq_eq_sq₀ (norm_nonneg _) zero_le_one]
        have hin : (⟪Z_op Ω, Z_op Ω⟫_ℂ).re = (⟪Ω, Ω⟫_ℂ).re := by rw [hZ_unit]
        rw [inner_self_eq_norm_sq_to_K, inner_self_eq_norm_sq_to_K] at hin
        have hnorm : ‖Z_op Ω‖ ^ 2 = ‖Ω‖ ^ 2 := by simpa [pow_two] using hin
        rw [hnorm, hgs.unit]
      rwa [norm_smul, hgs.unit, mul_one] at h1
    have hZΩ_ae : ⇑(Z_op Ω) =ᵐ[μ] fun U => (ω (e_flip U) : ℂ) := by
      have h1 := (memLp_comp_measurePreserving μ e_flip hmp Ω).coeFn_toLp
      have h2 := ae_comp_measurePreserving hmp hgs.ae_eq
      filter_upwards [h1, h2] with U hu1 hu2
      have hu1' : ⇑(Z_op Ω) U = ⇑Ω (e_flip U) := hu1
      rw [hu1', hu2]"""),
    ("""    have hc_re : 0 < c.re := by
      have hl2 := MeasureTheory.L2.integrable_inner Ω (Z_op Ω)
      dsimp [c]
      rw [MeasureTheory.L2.inner_def]
      change 0 < RCLike.re (∫ U, ⟪Ω U, (Z_op Ω) U⟫_ℂ ∂μ)
      rw [← integral_re hl2]
      refine integral_pos_of_integrable_nonneg_nonzero (hl2.re) ?_ ?_
      · filter_upwards [hgs.ae_eq, hZΩ_ae] with U hu1 hu2
        change 0 ≤ (⟪⇑Ω U, ⇑(Z_op Ω) U⟫_ℂ).re
        rw [hu1, hu2]; simp; exact mul_nonneg (hgs.ω_pos _).le (hgs.ω_pos _).le
      · -- Since `ω > 0` everywhere, integral of `ω(U) * ω(e_flip U)` is > 0
        intro hzero
        have h_ae0 : (fun U => (⟪Ω U, (Z_op Ω) U⟫_ℂ).re) =ᵐ[μ] 0 :=
          (integral_eq_zero_iff_of_nonneg_ae ?_ hl2.re).mp hzero
        · filter_upwards [h_ae0, hgs.ae_eq, hZΩ_ae] with U h0 hu1 hu2
          have hmul : ω U * ω (e_flip U) = 0 := by
            have := h0
            change (⟪⇑Ω U, ⇑(Z_op Ω) U⟫_ℂ).re = 0 at this
            rw [hu1, hu2] at this; simpa using this
          exact absurd hmul (mul_pos (hgs.ω_pos U) (hgs.ω_pos (e_flip U))).ne'
        · filter_upwards [hgs.ae_eq, hZΩ_ae] with U hu1 hu2
          change 0 ≤ (⟪⇑Ω U, ⇑(Z_op Ω) U⟫_ℂ).re
          rw [hu1, hu2]; simp; exact mul_nonneg (hgs.ω_pos _).le (hgs.ω_pos _).le
    have hc_im : c.im = 0 := by
      have hl2 := MeasureTheory.L2.integrable_inner Ω (Z_op Ω)
      dsimp [c]; rw [MeasureTheory.L2.inner_def]
      have h1 : (∫ U, ⟪Ω U, (Z_op Ω) U⟫_ℂ ∂μ).im =
          RCLike.re (-Complex.I * ∫ U, ⟪Ω U, (Z_op Ω) U⟫_ℂ ∂μ) := by simp [Complex.mul_re]
      rw [h1, ← MeasureTheory.integral_const_mul, ← integral_re (hl2.const_mul (-Complex.I))]
      refine MeasureTheory.integral_eq_zero_of_ae ?_
      filter_upwards [hgs.ae_eq, hZΩ_ae] with U hu1 hu2
      change (-Complex.I * ⟪⇑Ω U, ⇑(Z_op Ω) U⟫_ℂ).re = 0
      rw [hu1, hu2]; simp [Complex.mul_re]""",
     """    have hc_re : 0 < c.re := by
      have hl2 := MeasureTheory.L2.integrable_inner (𝕜 := ℂ) Ω (Z_op Ω)
      dsimp [c]
      rw [MeasureTheory.L2.inner_def]
      change 0 < RCLike.re (∫ U, ⟪Ω U, (Z_op Ω) U⟫_ℂ ∂μ)
      rw [← integral_re hl2]
      change 0 < ∫ U, (⟪Ω U, (Z_op Ω) U⟫_ℂ).re ∂μ
      have h_ae_nn : (0 : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℝ) ≤ᵐ[μ]
          fun U => (⟪Ω U, (Z_op Ω) U⟫_ℂ).re := by
        filter_upwards [hgs.ae_eq, hZΩ_ae] with U hu1 hu2
        change 0 ≤ (⟪⇑Ω U, ⇑(Z_op Ω) U⟫_ℂ).re
        rw [hu1, hu2]; simp; exact mul_nonneg (hgs.ω_pos _).le (hgs.ω_pos _).le
      have h_int_nn : 0 ≤ ∫ U, (⟪Ω U, (Z_op Ω) U⟫_ℂ).re ∂μ :=
        MeasureTheory.integral_nonneg_of_ae h_ae_nn
      refine lt_of_le_of_ne h_int_nn (Ne.symm fun hzero => ?_)
      have h_ae0 : (fun U => (⟪Ω U, (Z_op Ω) U⟫_ℂ).re) =ᵐ[μ] 0 :=
        (MeasureTheory.integral_eq_zero_iff_of_nonneg_ae h_ae_nn hl2.re).mp hzero
      have h_ae_false : ∀ᵐ U ∂μ, False := by
        filter_upwards [h_ae0, hgs.ae_eq, hZΩ_ae] with U h0 hu1 hu2
        have hmul : ω U * ω (e_flip U) = 0 := by
          have := h0
          change (⟪⇑Ω U, ⇑(Z_op Ω) U⟫_ℂ).re = 0 at this
          rw [hu1, hu2] at this; simpa [mul_comm] using this
        exact absurd hmul (mul_pos (hgs.ω_pos U) (hgs.ω_pos (e_flip U))).ne'
      haveI : (MeasureTheory.ae μ).NeBot := MeasureTheory.IsProbabilityMeasure.ae_neBot
      exact h_ae_false.exists.elim fun _ h => h
    have hc_im : c.im = 0 := by
      have hl2 := MeasureTheory.L2.integrable_inner (𝕜 := ℂ) Ω (Z_op Ω)
      dsimp [c]; rw [MeasureTheory.L2.inner_def]
      have h1 : (∫ U, ⟪Ω U, (Z_op Ω) U⟫_ℂ ∂μ).im =
          RCLike.re (-Complex.I * ∫ U, ⟪Ω U, (Z_op Ω) U⟫_ℂ ∂μ) := by simp [Complex.mul_re]
      rw [h1, ← MeasureTheory.integral_const_mul, ← integral_re (hl2.const_mul (-Complex.I))]
      refine MeasureTheory.integral_eq_zero_of_ae ?_
      filter_upwards [hgs.ae_eq, hZΩ_ae] with U hu1 hu2
      change (-Complex.I * ⟪⇑Ω U, ⇑(Z_op Ω) U⟫_ℂ).re = 0
      rw [hu1, hu2]; simp [Complex.mul_re]"""),
    ("""    have h_ae : (fun U => (ω (e_flip U) : ℂ)) =ᵐ[μ] fun U => (ω U : ℂ) := by
      filter_upwards [h1, h2, hgs.ae_eq] with x hx1 hx2 hx3
      have hz := congrArg (fun ψ : HaarGaugeSpace μ => ⇑ψ x) hZΩ
      -- Note: use `Lp.ext_iff` for ae equality of `Z_op Ω` and `Ω`
      sorry -- discharged by `MeasureTheory.Lp.coeFn_congr` / `eq_of_ae_continuous` below
    exact Complex.ofReal_injective (eq_of_ae_continuous μ
      (Complex.continuous_ofReal.comp (hgs.ω_cont.comp (by continuity)))
      (Complex.continuous_ofReal.comp hgs.ω_cont) h_ae U)""",
     """    have h_ae : (fun U => (ω (e_flip U) : ℂ)) =ᵐ[μ] fun U => (ω U : ℂ) := by
      filter_upwards [h1, h2, hgs.ae_eq] with x hx1 hx2 hx3
      have hz := congrArg (fun ψ : HaarGaugeSpace μ => ⇑ψ x) hZΩ
      have hx1' : ⇑(Z_op Ω) x = ⇑Ω (e_flip x) := hx1
      calc (ω (e_flip x) : ℂ) = ⇑Ω (e_flip x) := hx2.symm
        _ = ⇑(Z_op Ω) x := hx1'.symm
        _ = ⇑Ω x := hz
        _ = (ω x : ℂ) := hx3
    have he_cont : Continuous e_flip := by
      change Continuous (sliceCenterFlip L N hN)
      refine continuous_pi fun e => ?_
      dsimp [sliceCenterFlip]
      split_ifs
      · exact (continuous_mul_left _).comp (continuous_apply e)
      · exact continuous_apply e
    exact Complex.ofReal_injective (eq_of_ae_continuous μ
      (Complex.continuous_ofReal.comp (hgs.ω_cont.comp he_cont))
      (Complex.continuous_ofReal.comp hgs.ω_cont) h_ae U)"""),
    ("""        (∀ m, 3 * (Ls_seq m : ℝ) ^ 3 * Real.log (β_seq m) / β_seq m → True) →""",
     """        (∀ m, 0 ≤ 3 * (Ls_seq m : ℝ) ^ 3 * Real.log (β_seq m) / β_seq m → True) →"""),
]
for o, n in p_all:
    assert src.count(o) == 1
    src = src.replace(o, n, 1)

# Now test Patch 7 carefully
helpers = r'''private lemma su_entry_norm_le_one {N : ℕ}
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) (i j : Fin N) :
    ‖(A : Matrix (Fin N) (Fin N) ℂ) i j‖ ≤ 1 := by
  have hU : star (A : Matrix (Fin N) (Fin N) ℂ) * (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    (Unitary.mem_iff.mp A.2.1).1
  have hjj := congr_fun (congr_fun hU j) j
  simp only [Matrix.mul_apply, Matrix.star_apply, Matrix.one_apply_eq] at hjj
  have hre := congrArg Complex.re hjj
  rw [Complex.re_sum, Complex.one_re] at hre
  have hterm : ∀ k : Fin N, (star ((A : Matrix (Fin N) (Fin N) ℂ) k j) *
      (A : Matrix (Fin N) (Fin N) ℂ) k j).re = ‖(A : Matrix (Fin N) (Fin N) ℂ) k j‖ ^ 2 := by
    intro k
    change (starRingEnd ℂ ((A : Matrix (Fin N) (Fin N) ℂ) k j) *
      (A : Matrix (Fin N) (Fin N) ℂ) k j).re = _
    rw [Complex.conj_mul', ← Complex.ofReal_pow, Complex.ofReal_re]
  simp_rw [hterm] at hre
  have hsq_le : ‖(A : Matrix (Fin N) (Fin N) ℂ) i j‖ ^ 2 ≤ 1 :=
    (Finset.single_le_sum (fun k _ => sq_nonneg ‖(A : Matrix (Fin N) (Fin N) ℂ) k j‖)
      (Finset.mem_univ i)).trans_eq hre
  exact (sq_le_sq₀ (norm_nonneg _) zero_le_one).mp (by simpa using hsq_le)

private lemma frobeniusNormSq_su_self {N : ℕ}
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq (A : Matrix (Fin N) (Fin N) ℂ) = (N : ℝ) := by
  have hA : (A : Matrix (Fin N) (Fin N) ℂ) * star (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    (Unitary.mem_iff.mp A.2.1).2
  rw [frobeniusNormSq_trace, hA, Matrix.trace_one]
  simp

private lemma frobeniusNormSq_su_sub_one_eq {N : ℕ}
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) =
      2 * ((N : ℝ) - (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re) := by
  have hA : (A : Matrix (Fin N) (Fin N) ℂ) * star (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    (Unitary.mem_iff.mp A.2.1).2
  have hM : ((A : Matrix (Fin N) (Fin N) ℂ) - 1) * star ((A : Matrix (Fin N) (Fin N) ℂ) - 1) =
      ((1 : Matrix (Fin N) (Fin N) ℂ) + 1) - (A : Matrix (Fin N) (Fin N) ℂ) -
        star (A : Matrix (Fin N) (Fin N) ℂ) := by
    rw [star_sub, star_one, Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_sub,
      Matrix.one_mul, Matrix.mul_one, hA]
    abel
  have htr_star : (Matrix.trace (star (A : Matrix (Fin N) (Fin N) ℂ))).re =
      (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re := by
    change (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ).conjTranspose).re = _
    rw [Matrix.trace_conjTranspose, Complex.star_def, Complex.conj_re]
  rw [frobeniusNormSq_trace, hM]
  simp only [Matrix.trace_sub, Matrix.trace_add, Matrix.trace_one, Complex.sub_re,
    Complex.add_re, Complex.natCast_re, htr_star]
  ring

private lemma frobeniusNormSq_sub_comm {N : ℕ} (M₁ M₂ : Matrix (Fin N) (Fin N) ℂ) :
    frobeniusNormSq (M₁ - M₂) = frobeniusNormSq (M₂ - M₁) := by
  unfold frobeniusNormSq
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  rw [Matrix.sub_apply, Matrix.sub_apply, norm_sub_rev]

private lemma frobeniusNormSq_su_sub_eq_inner {N : ℕ}
    (A B : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    ∑ p : Fin N × Fin N,
        (starRingEnd ℂ ((A : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
          (B : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re =
      (N : ℝ) - (1 / 2 : ℝ) *
        frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - (B : Matrix (Fin N) (Fin N) ℂ)) := by
  have hpt : ∀ z w : ℂ, ‖z - w‖ ^ 2 =
      ‖z‖ ^ 2 + ‖w‖ ^ 2 - 2 * (starRingEnd ℂ z * w).re := fun z w => by
    rw [← Complex.normSq_eq_norm_sq, ← Complex.normSq_eq_norm_sq,
      ← Complex.normSq_eq_norm_sq]
    simp only [Complex.normSq_apply, Complex.sub_re, Complex.sub_im,
      Complex.mul_re, Complex.conj_re, Complex.conj_im]
    ring
  have hsum_A : ∑ p : Fin N × Fin N, ‖(A : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 = (N : ℝ) := by
    rw [Fintype.sum_prod_type]
    exact frobeniusNormSq_su_self A
  have hsum_B : ∑ p : Fin N × Fin N, ‖(B : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 = (N : ℝ) := by
    rw [Fintype.sum_prod_type]
    exact frobeniusNormSq_su_self B
  have hdiff : frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - (B : Matrix (Fin N) (Fin N) ℂ)) =
      (N : ℝ) + (N : ℝ) - 2 * ∑ p : Fin N × Fin N,
        (starRingEnd ℂ ((A : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
          (B : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re := by
    unfold frobeniusNormSq
    rw [← Fintype.sum_prod_type]
    simp_rw [Matrix.sub_apply, hpt, Finset.sum_sub_distrib, Finset.sum_add_distrib,
      ← Finset.mul_sum, hsum_A, hsum_B]
  linarith

private lemma integral_finset_sum_eq {α β : Type*} [MeasurableSpace α]
    {μ : MeasureTheory.Measure α} (s : Finset β) (f : β → α → ℝ)
    (hf : ∀ b ∈ s, MeasureTheory.Integrable (f b) μ) :
    MeasureTheory.Integrable (fun a => ∑ b ∈ s, f b a) μ ∧
      ∫ a, ∑ b ∈ s, f b a ∂μ = ∑ b ∈ s, ∫ a, f b a ∂μ := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert b s hb ih =>
    have hf1 : MeasureTheory.Integrable (f b) μ := hf b (Finset.mem_insert_self b s)
    have ih' := ih fun c hc => hf c (Finset.mem_insert_of_mem hc)
    refine ⟨?_, ?_⟩
    · simp_rw [Finset.sum_insert hb]
      exact hf1.add ih'.1
    · simp_rw [Finset.sum_insert hb]
      rw [MeasureTheory.integral_add hf1 ih'.1, ih'.2]

private lemma prod_exp_eq_exp_sum {ι : Type*} (s : Finset ι) (f : ι → ℝ) :
    ∏ i ∈ s, Real.exp (f i) = Real.exp (∑ i ∈ s, f i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
    rw [Finset.prod_insert ha, Finset.sum_insert ha, ih, Real.exp_add]

private lemma list_sum_map_le {α : Type*} (l : List α) (f : α → ℝ) (C : ℝ)
    (hf : ∀ x ∈ l, f x ≤ C) :
    (l.map f).sum ≤ (l.length : ℝ) * C := by
  induction l with
  | nil => simp
  | cons x xs ih =>
    simp only [List.map_cons, List.sum_cons, List.length_cons, Nat.cast_add, Nat.cast_one]
    have h1 : f x ≤ C := hf x (by simp)
    have h2 : (xs.map f).sum ≤ (xs.length : ℝ) * C := ih fun y hy => hf y (by simp [hy])
    linarith

private lemma list_sum_map_nonneg {α : Type*} (l : List α) (f : α → ℝ)
    (hf : ∀ x ∈ l, 0 ≤ f x) : 0 ≤ (l.map f).sum := by
  induction l with
  | nil => simp
  | cons x xs ih =>
    simp only [List.map_cons, List.sum_cons]
    exact add_nonneg (hf x (by simp)) (ih fun y hy => hf y (by simp [hy]))

private lemma frobeniusNormSq_plaq4_le {N : ℕ} {r : ℝ}
    {A B C D : Matrix.specialUnitaryGroup (Fin N) ℂ}
    (hA : frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ r)
    (hB : frobeniusNormSq ((B : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ r)
    (hC : frobeniusNormSq ((C : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ r)
    (hD : frobeniusNormSq ((D : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ r) :
    frobeniusNormSq (((A * (B * (C⁻¹ * (D⁻¹ * 1))) : Matrix.specialUnitaryGroup (Fin N) ℂ) :
      Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 16 * r := by
  rw [mul_one, ← mul_assoc A B]
  have h1 := frobeniusNormSq_su_mul_sub_one (A * B) (C⁻¹ * D⁻¹)
  have h2 := frobeniusNormSq_su_mul_sub_one A B
  have h3 := frobeniusNormSq_su_mul_sub_one C⁻¹ D⁻¹
  rw [frobeniusNormSq_su_inv_sub_one C, frobeniusNormSq_su_inv_sub_one D] at h3
  linarith

private lemma cubicPlaquettes_length (L : ℕ) [NeZero L] :
    (cubicPlaquettes L).length = 3 * L ^ 3 := by
  unfold cubicPlaquettes
  rw [List.length_flatMap]
  have h_const : ∀ x ∈ (Finset.univ : Finset (Fin L × Fin L × Fin L)).toList,
      ([ { base := x, loop := cubicPlaquette x 0 1, is_closed := cubicPlaquette_isPath x 0 1 },
         { base := x, loop := cubicPlaquette x 0 2, is_closed := cubicPlaquette_isPath x 0 2 },
         { base := x, loop := cubicPlaquette x 1 2, is_closed := cubicPlaquette_isPath x 1 2 } ] :
        List (LatticePlaquette (cubicTorus3 L))).length = 3 := fun _ _ => rfl
  rw [List.map_congr_left h_const]
  have hsum : ∀ l : List (Fin L × Fin L × Fin L), (l.map (fun _ => 3)).sum = l.length * 3 := by
    intro l
    induction l with
    | nil => simp
    | cons _ xs ih => simp [ih]; ring
  rw [hsum, Finset.length_toList, Finset.card_univ, Fintype.card_prod, Fintype.card_prod,
    Fintype.card_fin]
  ring

private lemma wilsonPlaquetteTerm_eq_frobenius {L : SpatialLattice} {N : ℕ} (hN : 0 < N)
    (p : LatticePlaquette L)
    (U : GaugeField L (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonPlaquetteTerm p U =
      frobeniusNormSq ((pathHolonomy U p.loop : Matrix.specialUnitaryGroup (Fin N) ℂ) - 1) /
        (2 * (N : ℝ)) := by
  have hN_ne : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  unfold wilsonPlaquetteTerm
  rw [frobeniusNormSq_su_sub_one_eq]
  field_simp [hN_ne]

private lemma wilsonAction_nonneg (L N : ℕ) [NeZero L] (hN : 0 < N) {β : ℝ} (hβ : 0 ≤ β)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    0 ≤ wilsonAction β (cubicPlaquettes L) U := by
  unfold wilsonAction
  refine mul_nonneg hβ (list_sum_map_nonneg _ _ fun p _ => ?_)
  rw [wilsonPlaquetteTerm_eq_frobenius hN]
  exact div_nonneg (frobeniusNormSq_nonneg _) (by positivity)

private lemma wilsonAction_le_ball (L N : ℕ) [NeZero L] (hN : 0 < N) {β : ℝ} (hβ : 1 ≤ β)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ))
    (hU : ∀ e, frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ (1 / Real.sqrt β) ^ 2) :
    wilsonAction β (cubicPlaquettes L) U ≤ 24 * (L : ℝ) ^ 3 / (N : ℝ) := by
  have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
  have hN_pos : (0 : ℝ) < (N : ℝ) := Nat.cast_pos.mpr hN
  have hδ_sq : (1 / Real.sqrt β) ^ 2 = 1 / β := by
    rw [one_div_pow, Real.sq_sqrt hβ_pos.le]
  have hp_le : ∀ p ∈ cubicPlaquettes L, wilsonPlaquetteTerm p U ≤ 8 / ((N : ℝ) * β) := by
    intro p hp
    rw [wilsonPlaquetteTerm_eq_frobenius hN]
    have h_hol : frobeniusNormSq
        ((pathHolonomy U p.loop : Matrix.specialUnitaryGroup (Fin N) ℂ) - 1) ≤
          16 / β := by
      unfold cubicPlaquettes at hp
      simp only [List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and,
        List.mem_cons, List.not_mem_nil, or_false] at hp
      rcases hp with ⟨x, rfl | rfl | rfl⟩ <;>
        · dsimp [cubicPlaquette, pathHolonomy]
          rw [← hδ_sq]
          exact frobeniusNormSq_plaq4_le (hU _) (hU _) (hU _) (hU _)
    calc frobeniusNormSq ((pathHolonomy U p.loop : Matrix.specialUnitaryGroup (Fin N) ℂ) - 1) /
          (2 * (N : ℝ))
        ≤ (16 / β) / (2 * (N : ℝ)) :=
          div_le_div_of_nonneg_right h_hol (by positivity)
      _ = 8 / ((N : ℝ) * β) := by field_simp [hβ_pos.ne', hN_pos.ne']; ring
  unfold wilsonAction
  have hsum := list_sum_map_le (cubicPlaquettes L) (fun p => wilsonPlaquetteTerm p U)
    (8 / ((N : ℝ) * β)) hp_le
  rw [cubicPlaquettes_length] at hsum
  calc β * ((cubicPlaquettes L).map (fun p => wilsonPlaquetteTerm p U)).sum
      ≤ β * (((3 * L ^ 3 : ℕ) : ℝ) * (8 / ((N : ℝ) * β))) :=
        mul_le_mul_of_nonneg_left hsum hβ_pos.le
    _ = 24 * (L : ℝ) ^ 3 / (N : ℝ) := by
        push_cast; field_simp [hβ_pos.ne', hN_pos.ne']; ring

private lemma wilsonKernel_upper_bound (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    {β : ℝ} (hβ : 1 ≤ β)
    (U U' : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonKernel β (cubicPlaquettes L)
        (wilsonGramKernel L N (cubicLinkKineticKernel L N β)) U U' ≤
      Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ)) *
        Real.exp (-(β / (8 * (N : ℝ))) *
          ∑ e : (cubicTorus3 L).Link,
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
              (U' e : Matrix (Fin N) (Fin N) ℂ))) := by
  have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
  have hN_pos : (0 : ℝ) < (N : ℝ) := by exact_mod_cast (by omega : 0 < N)
  have hcard : Fintype.card (cubicTorus3 L).Link = 3 * L ^ 3 := by
    simp [cubicTorus3, Fintype.card_prod, Fintype.card_fin]; ring
  let D : ℝ := ∑ e : (cubicTorus3 L).Link,
    frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))
  have h_chi_pt : ∀ W : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ),
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W ≤
        Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ)) *
          Real.exp (-(β / (8 * (N : ℝ))) * D) := by
    intro W
    have h_tr_eq : ∀ (X Y : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ))
        (e : (cubicTorus3 L).Link),
        (β / (2 * (N : ℝ))) *
          (Matrix.trace (((X e * (Y e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re =
          β / 2 - (β / (4 * (N : ℝ))) *
            frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) -
              (Y e : Matrix (Fin N) (Fin N) ℂ)) := by
      intro X Y e
      have h1 := frobeniusNormSq_su_sub_one_eq (X e * (Y e)⁻¹)
      rw [frobeniusNormSq_sub_self_su] at h1
      have h2 : (Matrix.trace (((X e * (Y e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ))).re =
          (N : ℝ) - frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) -
            (Y e : Matrix (Fin N) (Fin N) ℂ)) / 2 := by linarith
      rw [h2]
      field_simp [hN_pos.ne']
      ring
    unfold cubicLinkKineticKernel
    simp_rw [h_tr_eq]
    rw [← Finset.prod_mul_distrib]
    have h_prod : (∏ e : (cubicTorus3 L).Link,
        Real.exp (β / 2 - (β / (4 * (N : ℝ))) *
          frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) *
        Real.exp (β / 2 - (β / (4 * (N : ℝ))) *
          frobeniusNormSq ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)))) =
        Real.exp (∑ e : (cubicTorus3 L).Link,
          ((β / 2 - (β / (4 * (N : ℝ))) *
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) +
           (β / 2 - (β / (4 * (N : ℝ))) *
            frobeniusNormSq ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))))) := by
      simp_rw [← Real.exp_add]
      exact prod_exp_eq_exp_sum Finset.univ _
    rw [h_prod, ← Real.exp_add]
    refine Real.exp_le_exp.mpr ?_
    have h_link : ∀ e : (cubicTorus3 L).Link,
        (β / 2 - (β / (4 * (N : ℝ))) *
          frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) +
        (β / 2 - (β / (4 * (N : ℝ))) *
          frobeniusNormSq ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) ≤
          β - (β / (8 * (N : ℝ))) *
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
              (U' e : Matrix (Fin N) (Fin N) ℂ)) := by
      intro e
      have htri : frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
            (U' e : Matrix (Fin N) (Fin N) ℂ)) ≤
          2 * frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
            (W e : Matrix (Fin N) (Fin N) ℂ)) +
          2 * frobeniusNormSq ((U' e : Matrix (Fin N) (Fin N) ℂ) -
            (W e : Matrix (Fin N) (Fin N) ℂ)) := by
        have hsub : (U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ) =
            ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) +
            ((W e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)) := by abel
        rw [hsub]
        have hadd := frobeniusNormSq_add_le
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))
          ((W e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))
        rwa [frobeniusNormSq_sub_comm (W e : Matrix (Fin N) (Fin N) ℂ)
          (U' e : Matrix (Fin N) (Fin N) ℂ)] at hadd
      have hcoef : 0 ≤ β / (8 * (N : ℝ)) := by positivity
      have hmul := mul_le_mul_of_nonneg_left htri hcoef
      have h_id : β / (8 * (N : ℝ)) *
          (2 * frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) +
           2 * frobeniusNormSq ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) =
          (β / (4 * (N : ℝ))) *
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) +
          (β / (4 * (N : ℝ))) *
            frobeniusNormSq ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) := by
        field_simp [hN_pos.ne']; ring
      linarith
    calc ∑ e : (cubicTorus3 L).Link, _ ≤ ∑ e : (cubicTorus3 L).Link,
          (β - (β / (8 * (N : ℝ))) *
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
              (U' e : Matrix (Fin N) (Fin N) ℂ))) := Finset.sum_le_sum fun e _ => h_link e
      _ = β * ((3 * L ^ 3 : ℕ) : ℝ) + -(β / (8 * (N : ℝ))) * D := by
          simp only [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, hcard,
            nsmul_eq_mul, ← Finset.mul_sum, D]
          ring
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  have hp1 : Continuous (fun W : G_L => (U, W)) := continuous_const.prodMk continuous_id
  have hp2 : Continuous (fun W : G_L => (U', W)) := continuous_const.prodMk continuous_id
  have hχ_cont := continuous_cubicLinkKineticKernel L N β
  have h_cont : Continuous (fun W : G_L =>
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) :=
    (hχ_cont.comp hp1).mul (hχ_cont.comp hp2)
  have h_ub : ∀ W, ‖cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W‖ ≤
      (linkChiUb L β) ^ 2 := fun W => by
    have hnn1 := linkChi_nn L N hN β hβ_pos.le U W
    have hnn2 := linkChi_nn L N hN β hβ_pos.le U' W
    have hbd1 := (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2
    have hbd2 := (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U' W).2
    rw [Real.norm_of_nonneg (mul_nonneg hnn1 hnn2), sq]
    exact mul_le_mul hbd1 hbd2 hnn2 (linkChiUb_nonneg L β)
  have h_int : MeasureTheory.Integrable
      (fun W => cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) μ :=
    (MeasureTheory.integrable_const ((linkChiUb L β) ^ 2)).mono'
      h_cont.stronglyMeasurable.aestronglyMeasurable (Filter.Eventually.of_forall h_ub)
  have h_gram : wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' ≤
      Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ)) * Real.exp (-(β / (8 * (N : ℝ))) * D) := by
    calc wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U'
        = ∫ W, cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W ∂μ := rfl
      _ ≤ ∫ _W, Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ)) * Real.exp (-(β / (8 * (N : ℝ))) * D) ∂μ :=
          MeasureTheory.integral_mono h_int (MeasureTheory.integrable_const _) h_chi_pt
      _ = Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ)) * Real.exp (-(β / (8 * (N : ℝ))) * D) := by
          simp [Measure.real, MeasureTheory.measure_univ]
  have h_act_nn : 0 ≤ wilsonAction β (cubicPlaquettes L) U +
      wilsonAction β (cubicPlaquettes L) U' :=
    add_nonneg (wilsonAction_nonneg L N (by omega) hβ_pos.le U)
      (wilsonAction_nonneg L N (by omega) hβ_pos.le U')
  have h_exp_le : Real.exp (-(1 / 2 : ℝ) *
      (wilsonAction β (cubicPlaquettes L) U + wilsonAction β (cubicPlaquettes L) U')) ≤ 1 :=
    Real.exp_le_one_iff.mpr (by linarith)
  have h_gram_nn : 0 ≤ wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' :=
    wilsonGramKernel_nonneg L N (cubicLinkKineticKernel L N β) (linkChi_nn L N hN β hβ_pos.le) U U'
  unfold wilsonKernel
  calc Real.exp (-(1 / 2 : ℝ) *
        (wilsonAction β (cubicPlaquettes L) U + wilsonAction β (cubicPlaquettes L) U')) *
        wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U'
      ≤ 1 * wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' :=
        mul_le_mul_of_nonneg_right h_exp_le h_gram_nn
    _ ≤ Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ)) * Real.exp (-(β / (8 * (N : ℝ))) * D) := by
        simpa using h_gram

private lemma wilsonKernel_lower_bound_ball (L N : ℕ) [NeZero L] (hN : 2 ≤ N)
    {β : ℝ} (hβ : 1 ≤ β) :
    let μ := latticeHaarMeasure L N
    let δ : ℝ := 1 / Real.sqrt β
    let B_ball : Set (GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :=
      { U | ∀ e, frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 }
    ∀ U ∈ B_ball, ∀ U' ∈ B_ball,
      μ.real B_ball * Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) ≤
        wilsonKernel β (cubicPlaquettes L)
          (wilsonGramKernel L N (cubicLinkKineticKernel L N β)) U U' := by
  intro μ δ B_ball U hU U' hU'
  have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
  have hN_pos : (0 : ℝ) < (N : ℝ) := by exact_mod_cast (by omega : 0 < N)
  have hδ_sq : δ ^ 2 = 1 / β := by
    dsimp only [δ]; rw [one_div_pow, Real.sq_sqrt hβ_pos.le]
  have hcard : Fintype.card (cubicTorus3 L).Link = 3 * L ^ 3 := by
    simp [cubicTorus3, Fintype.card_prod, Fintype.card_fin]; ring
  haveI := latticeHaarMeasure_prob L N
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  have hB_meas : MeasurableSet B_ball := by
    have h_eq : B_ball = ⋂ e : (cubicTorus3 L).Link,
        { X : G_L | frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 } := by
      ext X; simp [B_ball]
    rw [h_eq]
    refine MeasurableSet.iInter fun e => ?_
    have hc : Continuous (fun X : G_L =>
        frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) - 1)) := by
      unfold frobeniusNormSq
      refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
      simp only [Matrix.sub_apply]
      exact (continuous_norm.comp (((continuous_apply j).comp
        ((continuous_apply i).comp (continuous_subtype_val.comp (continuous_apply e)))).sub
        continuous_const)).pow 2
    exact measurableSet_Iic.preimage hc.measurable
  let c_kin : ℝ := Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ) - 6 * (L : ℝ) ^ 3 / (N : ℝ))
  have hc_kin_nn : 0 ≤ c_kin := (Real.exp_pos _).le
  have h_chi_lb : ∀ W ∈ B_ball,
      c_kin ≤ cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W := by
    intro W hW
    have h_tr_ge : ∀ (X : G_L) (hX : X ∈ B_ball) (e : (cubicTorus3 L).Link),
        β / 2 - 1 / (N : ℝ) ≤ (β / (2 * (N : ℝ))) *
          (Matrix.trace (((X e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re := by
      intro X hX e
      have h1 := frobeniusNormSq_su_sub_one_eq (X e * (W e)⁻¹)
      rw [frobeniusNormSq_sub_self_su] at h1
      have hsub : (X e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ) =
          ((X e : Matrix (Fin N) (Fin N) ℂ) - 1) + (1 - (W e : Matrix (Fin N) (Fin N) ℂ)) := by
        abel
      have h_frob : frobeniusNormSq
          ((X e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) ≤ 4 / β := by
        rw [hsub]
        have hadd := frobeniusNormSq_add_le ((X e : Matrix (Fin N) (Fin N) ℂ) - 1)
          (1 - (W e : Matrix (Fin N) (Fin N) ℂ))
        rw [frobeniusNormSq_sub_comm (1 : Matrix (Fin N) (Fin N) ℂ)
          (W e : Matrix (Fin N) (Fin N) ℂ)] at hadd
        have hXe := hX e
        have hWe := hW e
        rw [hδ_sq] at hXe hWe
        linarith
      have htr : (Matrix.trace (((X e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ))).re =
          (N : ℝ) - frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) -
            (W e : Matrix (Fin N) (Fin N) ℂ)) / 2 := by linarith
      rw [htr]
      have hmul : (β / (4 * (N : ℝ))) *
          frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) ≤
          (β / (4 * (N : ℝ))) * (4 / β) :=
        mul_le_mul_of_nonneg_left h_frob (by positivity)
      have heq1 : (β / (4 * (N : ℝ))) * (4 / β) = 1 / (N : ℝ) := by
        field_simp [hβ_pos.ne', hN_pos.ne']
      have heq2 : (β / (2 * (N : ℝ))) * ((N : ℝ) -
          frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) -
            (W e : Matrix (Fin N) (Fin N) ℂ)) / 2) =
          β / 2 - (β / (4 * (N : ℝ))) *
            frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) -
              (W e : Matrix (Fin N) (Fin N) ℂ)) := by
        field_simp [hN_pos.ne']; ring
      linarith
    have h_each : ∀ e : (cubicTorus3 L).Link,
        Real.exp (β - 2 / (N : ℝ)) ≤
          Real.exp ((β / (2 * (N : ℝ))) *
            (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
              Matrix (Fin N) (Fin N) ℂ))).re) *
          Real.exp ((β / (2 * (N : ℝ))) *
            (Matrix.trace (((U' e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
              Matrix (Fin N) (Fin N) ℂ))).re) := by
      intro e
      rw [← Real.exp_add]
      exact Real.exp_le_exp.mpr (by linarith [h_tr_ge U hU e, h_tr_ge U' hU' e])
    unfold cubicLinkKineticKernel
    rw [← Finset.prod_mul_distrib]
    calc c_kin = Real.exp (((3 * L ^ 3 : ℕ) : ℝ) * (β - 2 / (N : ℝ))) := by
          dsimp only [c_kin]; congr 1; push_cast; ring
      _ = ∏ _e : (cubicTorus3 L).Link, Real.exp (β - 2 / (N : ℝ)) := by
          rw [prod_exp_eq_exp_sum, Finset.sum_const, Finset.card_univ, hcard, nsmul_eq_mul]
      _ ≤ ∏ e : (cubicTorus3 L).Link, _ :=
          Finset.prod_le_prod (fun _ _ => (Real.exp_pos _).le) fun e _ => h_each e
  have hp1 : Continuous (fun W : G_L => (U, W)) := continuous_const.prodMk continuous_id
  have hp2 : Continuous (fun W : G_L => (U', W)) := continuous_const.prodMk continuous_id
  have hχ_cont := continuous_cubicLinkKineticKernel L N β
  have h_cont : Continuous (fun W : G_L =>
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) :=
    (hχ_cont.comp hp1).mul (hχ_cont.comp hp2)
  have h_ub : ∀ W, ‖cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W‖ ≤
      (linkChiUb L β) ^ 2 := fun W => by
    have hnn1 := linkChi_nn L N hN β hβ_pos.le U W
    have hnn2 := linkChi_nn L N hN β hβ_pos.le U' W
    have hbd1 := (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2
    have hbd2 := (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U' W).2
    rw [Real.norm_of_nonneg (mul_nonneg hnn1 hnn2), sq]
    exact mul_le_mul hbd1 hbd2 hnn2 (linkChiUb_nonneg L β)
  have h_int : MeasureTheory.Integrable
      (fun W => cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W) μ :=
    (MeasureTheory.integrable_const ((linkChiUb L β) ^ 2)).mono'
      h_cont.stronglyMeasurable.aestronglyMeasurable (Filter.Eventually.of_forall h_ub)
  have h_ind_int : MeasureTheory.Integrable (Set.indicator B_ball (fun _ => c_kin)) μ :=
    (MeasureTheory.integrable_const c_kin).indicator hB_meas
  have h_ind_le : ∀ W, Set.indicator B_ball (fun _ => c_kin) W ≤
      cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W := fun W => by
    by_cases hW : W ∈ B_ball
    · rw [Set.indicator_of_mem hW]; exact h_chi_lb W hW
    · rw [Set.indicator_of_notMem hW]
      exact mul_nonneg (linkChi_nn L N hN β hβ_pos.le U W) (linkChi_nn L N hN β hβ_pos.le U' W)
  have h_gram_lb : μ.real B_ball * c_kin ≤
      wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' := by
    calc μ.real B_ball * c_kin
        = ∫ W, Set.indicator B_ball (fun _ => c_kin) W ∂μ := by
          rw [MeasureTheory.integral_indicator hB_meas, MeasureTheory.setIntegral_const,
            smul_eq_mul]
      _ ≤ ∫ W, cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W ∂μ :=
          MeasureTheory.integral_mono h_ind_int h_int h_ind_le
  have hS1 := wilsonAction_le_ball L N (by omega) hβ U hU
  have hS2 := wilsonAction_le_ball L N (by omega) hβ U' hU'
  have h_act_lb : Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) ≤
      Real.exp (-(1 / 2 : ℝ) *
        (wilsonAction β (cubicPlaquettes L) U + wilsonAction β (cubicPlaquettes L) U')) :=
    Real.exp_le_exp.mpr (by linarith)
  have h_exp_prod : Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) * (μ.real B_ball * c_kin) =
      μ.real B_ball * Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) := by
    rw [mul_left_comm, ← Real.exp_add]
    congr 2; dsimp only [c_kin]; ring
  unfold wilsonKernel
  calc μ.real B_ball * Real.exp (β * ((3 * L ^ 3 : ℕ) : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ))
      = Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) * (μ.real B_ball * c_kin) := h_exp_prod.symm
    _ ≤ Real.exp (-(1 / 2 : ℝ) *
          (wilsonAction β (cubicPlaquettes L) U + wilsonAction β (cubicPlaquettes L) U')) *
          wilsonGramKernel L N (cubicLinkKineticKernel L N β) U U' :=
        mul_le_mul h_act_lb h_gram_lb (mul_nonneg MeasureTheory.measureReal_nonneg hc_kin_nn)
          (Real.exp_pos _).le

private lemma l2_inner_wilsonOp_re
    (L N : ℕ) [NeZero L] (β : ℝ) (hβ : 0 ≤ β)
    (K_kin : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) →
      GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℝ)
    (hK_cont : Continuous (Function.uncurry K_kin))
    (hK_nn : ∀ U U', 0 ≤ K_kin U U')
    (M_K : ℝ) (hM_K : 0 ≤ M_K) (hK_bd : ∀ U U', K_kin U U' ≤ M_K)
    (T_raw : HaarGaugeSpace (latticeHaarMeasure L N) →L[ℂ]
      HaarGaugeSpace (latticeHaarMeasure L N))
    (hT_eq : T_raw = wilsonIntegralOp L N β hβ K_kin hK_cont hK_nn M_K hM_K hK_bd)
    (ψ : HaarGaugeSpace (latticeHaarMeasure L N))
    (f : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℂ)
    (hf_ae : ⇑ψ =ᵐ[latticeHaarMeasure L N] f) :
    (⟪ψ, T_raw ψ⟫_ℂ).re =
      ∫ U, ∫ U', wilsonKernel β (cubicPlaquettes L) K_kin U U' *
        (starRingEnd ℂ (f U) * f U').re ∂(latticeHaarMeasure L N) ∂(latticeHaarMeasure L N) := by
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  have h1 := wilsonIntegralOp_apply_ae L N β hβ K_kin hK_cont hK_nn M_K hM_K hK_bd ψ
  rw [← hT_eq] at h1
  have hl2 : MeasureTheory.Integrable (fun U => ⟪ψ U, (T_raw ψ) U⟫_ℂ) μ :=
    MeasureTheory.L2.integrable_inner (𝕜 := ℂ) ψ (T_raw ψ)
  have h_re1 : (⟪ψ, T_raw ψ⟫_ℂ).re =
      ∫ U, (⟪⇑ψ U, ⇑(T_raw ψ) U⟫_ℂ).re ∂μ := by
    rw [MeasureTheory.L2.inner_def]
    change RCLike.re (∫ U, ⟪ψ U, (T_raw ψ) U⟫_ℂ ∂μ) = _
    rw [← integral_re hl2]
    rfl
  rw [h_re1]
  refine MeasureTheory.integral_congr_ae ?_
  filter_upwards [hf_ae, h1] with U hU1 hU2
  change (⟪⇑ψ U, ⇑(T_raw ψ) U⟫_ℂ).re = _
  rw [hU1, hU2]
  dsimp only [wilsonIntegralFn]
  have h_int_K : MeasureTheory.Integrable
      (fun U' => ((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) * ψ U') μ :=
    wilsonKernel_mul_integrable L N β hβ K_kin hK_cont hK_nn M_K hK_bd ψ U
  have h_int_prod : MeasureTheory.Integrable
      (fun U' => starRingEnd ℂ (f U) *
        (((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) * ψ U')) μ :=
    h_int_K.const_mul (starRingEnd ℂ (f U))
  have h_eq_c : (⟪f U, ∫ U', ((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) *
        ψ U' ∂μ⟫_ℂ) =
      ∫ U', starRingEnd ℂ (f U) *
        (((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) * ψ U') ∂μ := by
    have hc_in : ∀ z : ℂ, ⟪f U, z⟫_ℂ = starRingEnd ℂ (f U) * z := fun z => by
      simp only [RCLike.inner_apply, Complex.star_def]; ring
    rw [hc_in, ← MeasureTheory.integral_const_mul (starRingEnd ℂ (f U))]
  rw [h_eq_c]
  change RCLike.re (∫ U', starRingEnd ℂ (f U) *
      (((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) * ψ U') ∂μ) = _
  rw [← integral_re h_int_prod]
  refine MeasureTheory.integral_congr_ae ?_
  filter_upwards [hf_ae] with U' hU'
  change (starRingEnd ℂ (f U) *
      (((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) * ⇑ψ U')).re = _
  rw [hU']
  have h_mul : starRingEnd ℂ (f U) *
      (((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) * f U') =
      ((wilsonKernel β (cubicPlaquettes L) K_kin U U' : ℝ) : ℂ) *
        (starRingEnd ℂ (f U) * f U') := by ring
  rw [h_mul, Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]

'''

old_sorry = "  sorry -- full assembly continues identically with Step 2 (Dirichlet form) & Step 3 (ε/δ split)"

new_proof = r'''  -- Pointwise ground-state identity: `∫ K_W U U' ω U' ∂μ = lam0 * ω U`
  have hω_eig_pt : ∀ U,
      ∫ U', K_W U U' * ω U' ∂μ = lam0 * ω U := by
    have h1 := wilsonIntegralOp_apply_ae L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd Ω
    have hT_eq : T_raw Ω = (lam0 : ℂ) • Ω := hgs.eig
    have h2 : (⇑(T_raw Ω) : _ → ℂ) =ᵐ[μ] fun U => ((lam0 * ω U : ℝ) : ℂ) := by
      have hsm := MeasureTheory.Lp.coeFn_smul (lam0 : ℂ) Ω
      filter_upwards [hsm, hgs.ae_eq] with U hu1 hu2
      change ⇑(T_raw Ω) U = ((lam0 * ω U : ℝ) : ℂ)
      rw [hT_eq, hu1]
      simp only [Pi.smul_apply, smul_eq_mul, hu2, Complex.ofReal_mul]
    have h_ae_c : (fun U => (∫ U', ((K_W U U' : ℝ) : ℂ) * (ω U' : ℂ) ∂μ)) =ᵐ[μ]
        fun U => ((lam0 * ω U : ℝ) : ℂ) := by
      filter_upwards [h1, h2] with U hu1 hu2
      have h_eq_int : wilsonIntegralFn L N β K_kin Ω U =
          ∫ U', ((K_W U U' : ℝ) : ℂ) * (ω U' : ℂ) ∂μ := by
        dsimp [wilsonIntegralFn]
        refine MeasureTheory.integral_congr_ae ?_
        filter_upwards [hgs.ae_eq] with U' hU'
        change ((K_W U U' : ℝ) : ℂ) * ⇑Ω U' = _
        rw [hU']
      have hu1' : ⇑(T_raw Ω) U = wilsonIntegralFn L N β K_kin Ω U := hu1
      rw [← h_eq_int, ← hu1', hu2]
    have h_cont_lhs : Continuous (fun U => (∫ U', ((K_W U U' : ℝ) : ℂ) * (ω U' : ℂ) ∂μ)) := by
      have heq_fn : (fun U => ∫ U', ((K_W U U' : ℝ) : ℂ) * (ω U' : ℂ) ∂μ) =
          wilsonIntegralFn L N β K_kin Ω := by
        funext U
        dsimp [wilsonIntegralFn]
        refine MeasureTheory.integral_congr_ae ?_
        filter_upwards [hgs.ae_eq] with U' hU'
        change _ = ((K_W U U' : ℝ) : ℂ) * ⇑Ω U'
        rw [hU']
      rw [heq_fn]
      exact wilsonIntegralFn_continuous L N β hβ_pos.le K_kin hK_cont hK_nn
        ((linkChiUb L β) ^ 2) hK_bd Ω
    intro U
    have h_pt := eq_of_ae_continuous μ h_cont_lhs
      (Complex.continuous_ofReal.comp (continuous_const.mul hgs.ω_cont)) h_ae_c U
    have h_re := congrArg Complex.re h_pt
    have h_int_real : ∫ U', ((K_W U U' : ℝ) : ℂ) * (ω U' : ℂ) ∂μ =
        ((∫ U', K_W U U' * ω U' ∂μ : ℝ) : ℂ) := by
      have heq : (fun U' => ((K_W U U' : ℝ) : ℂ) * (ω U' : ℂ)) =
          fun U' => ((K_W U U' * ω U' : ℝ) : ℂ) := by
        funext U'; push_cast; rfl
      rw [heq, integral_complex_ofReal]
    rw [h_int_real, Complex.ofReal_re, Complex.ofReal_re] at h_re
    exact h_re
  -- Step 2: `N²` trial vectors `ψ_{i,j}(U) := ((U e₀) i j) * ω U`, orthogonal to `Ω`
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  let e₀ : (cubicTorus3 L).Link := ((0, 0, 0), 0)
  let c_z : ℂ := Complex.exp (2 * Real.pi * Complex.I / (N : ℂ))
  have hc_z_ne1 : c_z ≠ 1 := centralElem_ne_one N hN
  have hω_bound : ∃ C_ω : ℝ, 0 ≤ C_ω ∧ ∀ U, |ω U| ≤ C_ω := by
    have h_norm_cont : Continuous (fun U : G_L => |ω U|) := continuous_abs.comp hgs.ω_cont
    obtain ⟨U_max, _, hU_max⟩ :=
      (isCompact_univ : IsCompact (Set.univ : Set G_L)).exists_isMaxOn
        ⟨fun _ => 1, Set.mem_univ _⟩ h_norm_cont.continuousOn
    exact ⟨|ω U_max|, abs_nonneg _, fun U => hU_max (Set.mem_univ U)⟩
  obtain ⟨C_ω, hC_ω_nn, hC_ω_bd⟩ := hω_bound
  let ψ_fn : Fin N × Fin N → G_L → ℂ := fun p U =>
    ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) * (ω U : ℂ)
  have hψ_cont : ∀ p : Fin N × Fin N, Continuous (ψ_fn p) := fun p => by
    have h_ent : Continuous (fun U : G_L => (U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) :=
      (continuous_apply p.2).comp
        ((continuous_apply p.1).comp (continuous_subtype_val.comp (continuous_apply e₀)))
    exact h_ent.mul (Complex.continuous_ofReal.comp hgs.ω_cont)
  have hψ_bd : ∀ p : Fin N × Fin N, ∀ U, ‖ψ_fn p U‖ ≤ C_ω := fun p U => by
    dsimp only [ψ_fn]
    rw [norm_mul, Complex.norm_real, Real.norm_eq_abs]
    have h_ent := su_entry_norm_le_one (U e₀) p.1 p.2
    calc ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ * |ω U|
        ≤ 1 * C_ω := mul_le_mul h_ent (hC_ω_bd U) (abs_nonneg _) zero_le_one
      _ = C_ω := one_mul _
  have hψ_mem : ∀ p : Fin N × Fin N, MeasureTheory.MemLp (ψ_fn p) 2 μ := fun p =>
    memLp_two_of_measurable_bound μ (ψ_fn p) (hψ_cont p).measurable C_ω hC_ω_nn (hψ_bd p)
  let ψ : Fin N × Fin N → HaarGaugeSpace μ := fun p => (hψ_mem p).toLp (ψ_fn p)
  have hψ_ae : ∀ p : Fin N × Fin N, ⇑(ψ p) =ᵐ[μ] ψ_fn p := fun p =>
    (hψ_mem p).coeFn_toLp
  have hψ_flip : ∀ p U, ψ_fn p (e_flip U) = c_z * ψ_fn p U := fun p U => by
    dsimp only [ψ_fn]
    have hωf : ω (e_flip U) = ω U := hω_flip U
    have he0 : ((e_flip U) e₀ : Matrix.specialUnitaryGroup (Fin N) ℂ) =
        centralElem N hN * U e₀ := by
      change sliceCenterFlip L N hN U e₀ = _
      dsimp [sliceCenterFlip, e₀]
      simp
    have hmat : (((centralElem N hN * U e₀ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ) p.1 p.2) =
        c_z * ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) := by
      have hc_mat : (centralElem N hN : Matrix (Fin N) (Fin N) ℂ) =
          c_z • (1 : Matrix (Fin N) (Fin N) ℂ) := rfl
      rw [Submonoid.coe_mul, hc_mat, Matrix.smul_mul, Matrix.one_mul,
        Matrix.smul_apply, smul_eq_mul]
    rw [hωf, he0, hmat]
    ring
  have hψ_orth : ∀ p : Fin N × Fin N, ⟪ψ p, Ω⟫_ℂ = 0 := fun p => by
    have h_in_eq : ⟪Ω, ψ p⟫_ℂ = c_z * ⟪Ω, ψ p⟫_ℂ := by
      have h_int1 : ∫ U, ⟪Ω U, (ψ p) U⟫_ℂ ∂μ =
          ∫ U, (ω U : ℂ) * ψ_fn p U ∂μ := by
        refine MeasureTheory.integral_congr_ae ?_
        filter_upwards [hgs.ae_eq, hψ_ae p] with U hU1 hU2
        change ⟪⇑Ω U, ⇑(ψ p) U⟫_ℂ = _
        rw [hU1, hU2]
        simp only [RCLike.inner_apply, Complex.star_def, Complex.conj_ofReal]
        ring
      have h_int2 : ∫ U, (ω (e_flip U) : ℂ) * ψ_fn p (e_flip U) ∂μ =
          ∫ U, (ω U : ℂ) * ψ_fn p U ∂μ :=
        hmp.integral_comp' (fun U => (ω U : ℂ) * ψ_fn p U)
      have h_int3 : ∫ U, (ω (e_flip U) : ℂ) * ψ_fn p (e_flip U) ∂μ =
          c_z * ∫ U, (ω U : ℂ) * ψ_fn p U ∂μ := by
        have heq : (fun U => (ω (e_flip U) : ℂ) * ψ_fn p (e_flip U)) =
            fun U => c_z * ((ω U : ℂ) * ψ_fn p U) := by
          funext U
          rw [hω_flip U, hψ_flip p U]
          ring
        rw [heq, MeasureTheory.integral_const_mul]
      rw [MeasureTheory.L2.inner_def, h_int1, ← h_int2, h_int3]
    have h0 : (1 - c_z) * ⟪Ω, ψ p⟫_ℂ = 0 := by linear_combination -h_in_eq
    have h1c : 1 - c_z ≠ 0 := sub_ne_zero.mpr hc_z_ne1.symm
    have hΩψ : ⟪Ω, ψ p⟫_ℂ = 0 := (mul_eq_zero.mp h0).resolve_left h1c
    rw [← inner_conj_symm, hΩψ, map_zero]
  have hω_sq_int : ∫ U, ω U ^ 2 ∂μ = 1 := by
    have hin : (⟪Ω, Ω⟫_ℂ).re = 1 := by
      rw [inner_self_eq_norm_sq_to_K, hgs.unit]; norm_num
    rw [MeasureTheory.L2.inner_def] at hin
    have hl2_self : MeasureTheory.Integrable (fun U => ⟪Ω U, Ω U⟫_ℂ) μ :=
      MeasureTheory.L2.integrable_inner (𝕜 := ℂ) Ω Ω
    change RCLike.re (∫ U, ⟪Ω U, Ω U⟫_ℂ ∂μ) = 1 at hin
    rw [← integral_re hl2_self] at hin
    have heq : (fun U => RCLike.re ⟪Ω U, Ω U⟫_ℂ) =ᵐ[μ] fun U => ω U ^ 2 := by
      filter_upwards [hgs.ae_eq] with U hU
      change (⟪⇑Ω U, ⇑Ω U⟫_ℂ).re = _
      rw [hU]; simp [sq]
    rwa [← MeasureTheory.integral_congr_ae heq]
  have hω_l1_le : ∫ U, ω U ∂μ ≤ 1 := by
    have hl1 := l1_le_l2_prob μ Ω
    rw [hgs.unit] at hl1
    have heq : (fun U => ‖Ω U‖) =ᵐ[μ] ω := by
      filter_upwards [hgs.ae_eq] with U hU
      change ‖⇑Ω U‖ = ω U
      rw [hU, Complex.norm_real, Real.norm_of_nonneg (hgs.ω_pos U).le]
    rwa [MeasureTheory.integral_congr_ae heq] at hl1
  have hω_l1_nn : 0 ≤ ∫ U, ω U ∂μ :=
    MeasureTheory.integral_nonneg fun U => (hgs.ω_pos U).le
  have hψ_norm_sq : ∀ p : Fin N × Fin N,
      ‖ψ p‖ ^ 2 = ∫ U, ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 * ω U ^ 2 ∂μ := fun p => by
    have hl2_p : MeasureTheory.Integrable (fun U => ⟪(ψ p) U, (ψ p) U⟫_ℂ) μ :=
      MeasureTheory.L2.integrable_inner (𝕜 := ℂ) (ψ p) (ψ p)
    have h_in_p : ‖ψ p‖ ^ 2 = (⟪ψ p, ψ p⟫_ℂ).re := by
      rw [inner_self_eq_norm_sq_to_K, ← Complex.ofReal_pow, Complex.ofReal_re]
    rw [h_in_p, MeasureTheory.L2.inner_def]
    change RCLike.re (∫ U, ⟪(ψ p) U, (ψ p) U⟫_ℂ ∂μ) = _
    rw [← integral_re hl2_p]
    refine MeasureTheory.integral_congr_ae ?_
    filter_upwards [hψ_ae p] with U hU
    change (⟪⇑(ψ p) U, ⇑(ψ p) U⟫_ℂ).re = _
    rw [hU, inner_self_eq_norm_sq_to_K, ← Complex.ofReal_pow, Complex.ofReal_re]
    dsimp only [ψ_fn]
    rw [norm_mul, Complex.norm_real, Real.norm_eq_abs, mul_pow, sq_abs]
  have hψ_norm_sum : ∑ p : Fin N × Fin N, ‖ψ p‖ ^ 2 = (N : ℝ) := by
    simp_rw [hψ_norm_sq]
    have hint_p : ∀ p ∈ (Finset.univ : Finset (Fin N × Fin N)),
        MeasureTheory.Integrable
          (fun U : G_L => ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 * ω U ^ 2) μ := by
      intro p _
      have hc_p : Continuous (fun U : G_L =>
          ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 * ω U ^ 2) :=
        ((continuous_norm.comp ((continuous_apply p.2).comp ((continuous_apply p.1).comp
          (continuous_subtype_val.comp (continuous_apply e₀))))).pow 2).mul (hgs.ω_cont.pow 2)
      exact (MeasureTheory.integrable_const (C_ω ^ 2)).mono'
        hc_p.stronglyMeasurable.aestronglyMeasurable (Filter.Eventually.of_forall fun U => by
          rw [Real.norm_of_nonneg (mul_nonneg (sq_nonneg _) (sq_nonneg _))]
          calc ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 * ω U ^ 2
              ≤ 1 ^ 2 * C_ω ^ 2 := mul_le_mul
                (pow_le_pow_left₀ (norm_nonneg _) (su_entry_norm_le_one (U e₀) p.1 p.2) 2)
                (by rw [← sq_abs (ω U)]; exact pow_le_pow_left₀ (abs_nonneg _) (hC_ω_bd U) 2)
                (sq_nonneg _) (by positivity)
            _ = C_ω ^ 2 := by ring)
    have hsum := integral_finset_sum_eq (Finset.univ : Finset (Fin N × Fin N))
      (fun p U => ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 * ω U ^ 2) hint_p
    rw [← hsum.2]
    have h_pt_sum : (fun U : G_L =>
        ∑ p : Fin N × Fin N, ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2‖ ^ 2 * ω U ^ 2) =
        fun U => (N : ℝ) * ω U ^ 2 := by
      funext U
      rw [← Finset.sum_mul, Fintype.sum_prod_type]
      have hfn : (∑ i : Fin N, ∑ j : Fin N, ‖(U e₀ : Matrix (Fin N) (Fin N) ℂ) i j‖ ^ 2) =
          (N : ℝ) := frobeniusNormSq_su_self (U e₀)
      rw [hfn]
    rw [h_pt_sum, MeasureTheory.integral_const_mul, hω_sq_int, mul_one]
  have hT_raw_eq : T_raw = wilsonIntegralOp L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd := rfl
  have h_inner_ST : ∀ p : Fin N × Fin N,
      (⟪ψ p, S.T (ψ p)⟫_ℂ).re =
        lam0⁻¹ * ∫ U, ∫ U', K_W U U' * ω U * ω U' *
          (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ ∂μ := fun p => by
    have h1 : (⟪ψ p, S.T (ψ p)⟫_ℂ).re = lam0⁻¹ * (⟪ψ p, T_raw (ψ p)⟫_ℂ).re := by
      rw [hS_T, ContinuousLinearMap.smul_apply, inner_smul_right, Complex.mul_re,
        Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
    rw [h1, l2_inner_wilsonOp_re L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd T_raw hT_raw_eq (ψ p) (ψ_fn p) (hψ_ae p)]
    congr 1
    refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
    refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U' => ?_)
    dsimp only [ψ_fn]
    have hmul : starRingEnd ℂ (((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) * (ω U : ℂ)) *
        (((U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) * (ω U' : ℂ)) =
        ((ω U * ω U' : ℝ) : ℂ) *
          (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) := by
      simp only [map_mul, Complex.conj_ofReal]; push_cast; ring
    rw [hmul, Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
    dsimp only [K_W]
    ring
  have hKW_nn : ∀ U U', 0 ≤ K_W U U' := fun U U' =>
    wilsonKernel_nonneg β (cubicPlaquettes L) K_kin hK_nn U U'
  have hKW_ub : ∀ U U', K_W U U' ≤ (linkChiUb L β) ^ 2 := fun U U' => by
    have h_act_nn : 0 ≤ wilsonAction β (cubicPlaquettes L) U +
        wilsonAction β (cubicPlaquettes L) U' :=
      add_nonneg (wilsonAction_nonneg L N (by omega) hβ_pos.le U)
        (wilsonAction_nonneg L N (by omega) hβ_pos.le U')
    have h_exp : Real.exp (-(1 / 2 : ℝ) *
        (wilsonAction β (cubicPlaquettes L) U + wilsonAction β (cubicPlaquettes L) U')) ≤ 1 :=
      Real.exp_le_one_iff.mpr (by linarith)
    calc K_W U U' ≤ 1 * K_kin U U' :=
          mul_le_mul_of_nonneg_right h_exp (hK_nn U U')
      _ ≤ (linkChiUb L β) ^ 2 := by simpa using hK_bd U U'
  have hKW_cont : Continuous (Function.uncurry K_W) :=
    continuous_cubicWilsonKernel L N β K_kin hK_cont
  let M_kern : ℝ := (linkChiUb L β) ^ 2 * C_ω ^ 2
  have h_int_KW_U : ∀ U, MeasureTheory.Integrable (fun U' => K_W U U' * ω U * ω U') μ := fun U => by
    have heq1 : (fun U' => K_W U U' * ω U * ω U') =
        fun U' => ω U * (K_W U U' * ω U') := funext fun U' => by ring
    rw [heq1]
    have hc : Continuous (fun U' => K_W U U' * ω U') :=
      (hKW_cont.comp (continuous_const.prodMk continuous_id)).mul hgs.ω_cont
    exact ((MeasureTheory.integrable_const ((linkChiUb L β) ^ 2 * C_ω)).mono'
      hc.stronglyMeasurable.aestronglyMeasurable
      (Filter.Eventually.of_forall fun U' => by
        rw [Real.norm_of_nonneg (mul_nonneg (hKW_nn U U') (hgs.ω_pos U').le)]
        exact mul_le_mul (hKW_ub U U') ((le_abs_self _).trans (hC_ω_bd U'))
          (hgs.ω_pos U').le (sq_nonneg _))).const_mul (ω U)
  have h_int_base : MeasureTheory.Integrable
      (fun U : G_L => ∫ U', K_W U U' * ω U * ω U' ∂μ) μ := by
    have h_eq : (fun U => ∫ U', K_W U U' * ω U * ω U' ∂μ) =
        fun U => lam0 * ω U ^ 2 := by
      funext U
      have heq1 : (fun U' => K_W U U' * ω U * ω U') =
          fun U' => ω U * (K_W U U' * ω U') := funext fun U' => by ring
      rw [heq1, MeasureTheory.integral_const_mul, hω_eig_pt U]
      ring
    rw [h_eq]
    exact (MeasureTheory.integrable_const (lam0 * C_ω ^ 2)).mono'
      ((continuous_const.mul (hgs.ω_cont.pow 2)).stronglyMeasurable.aestronglyMeasurable)
      (Filter.Eventually.of_forall fun U => by
        rw [Real.norm_of_nonneg (mul_nonneg hlam0_pos.le (sq_nonneg _))]
        exact mul_le_mul_of_nonneg_left
          (by rw [← sq_abs (ω U)]; exact pow_le_pow_left₀ (abs_nonneg _) (hC_ω_bd U) 2)
          hlam0_pos.le)
  have h_int_N_val : ∫ U, ∫ U', K_W U U' * ω U * ω U' ∂μ ∂μ = lam0 := by
    have h_eq : (fun U => ∫ U', K_W U U' * ω U * ω U' ∂μ) =
        fun U => lam0 * ω U ^ 2 := by
      funext U
      have heq1 : (fun U' => K_W U U' * ω U * ω U') =
          fun U' => ω U * (K_W U U' * ω U') := funext fun U' => by ring
      rw [heq1, MeasureTheory.integral_const_mul, hω_eig_pt U]
      ring
    rw [h_eq, MeasureTheory.integral_const_mul, hω_sq_int, mul_one]
  have h_diff_sum_eq :
      (N : ℝ) - ∑ p : Fin N × Fin N, (⟪ψ p, S.T (ψ p)⟫_ℂ).re =
        (1 / (2 * lam0)) * ∫ U, ∫ U', K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ := by
    have h_pt_diff : ∀ U U',
        K_W U U' * ω U * ω U' * ((N : ℝ) -
          ∑ p : Fin N × Fin N,
            (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re) =
          (1 / 2 : ℝ) * (K_W U U' * ω U * ω U' *
            frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) := fun U U' => by
      rw [frobeniusNormSq_su_sub_eq_inner]; ring
    have h_int_inner_p : ∀ p : Fin N × Fin N, ∀ U : G_L,
        MeasureTheory.Integrable
          (fun U' => K_W U U' * ω U * ω U' *
            (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re) μ := by
      intro p U
      have hc : Continuous (fun U' : G_L => K_W U U' * ω U * ω U' *
          (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re) := by
        have hK_r := (hKW_cont.comp (continuous_const.prodMk continuous_id))
        have h_ent' : Continuous (fun U' : G_L =>
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) :=
          (continuous_apply p.2).comp ((continuous_apply p.1).comp
            (continuous_subtype_val.comp (continuous_apply e₀)))
        exact (((hK_r.mul continuous_const).mul hgs.ω_cont)).mul
          (Complex.continuous_re.comp (continuous_const.mul h_ent'))
      exact (MeasureTheory.integrable_const M_kern).mono'
        hc.stronglyMeasurable.aestronglyMeasurable (Filter.Eventually.of_forall fun U' => by
          rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_mul,
            abs_of_nonneg (hKW_nn U U'), abs_of_nonneg (hgs.ω_pos U).le,
            abs_of_nonneg (hgs.ω_pos U').le]
          have hcre : |(starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re| ≤ 1 := by
            refine (Complex.abs_re_le_norm _).trans ?_
            rw [norm_mul, Complex.norm_conj]
            exact mul_le_one₀ (su_entry_norm_le_one (U e₀) p.1 p.2) (norm_nonneg _)
              (su_entry_norm_le_one (U' e₀) p.1 p.2)
          calc K_W U U' * ω U * ω U' *
                |(starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
                  (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re|
              ≤ ((linkChiUb L β) ^ 2) * C_ω * C_ω * 1 := by
                refine mul_le_mul (mul_le_mul (mul_le_mul (hKW_ub U U')
                  ((le_abs_self _).trans (hC_ω_bd U)) (hgs.ω_pos U).le (sq_nonneg _))
                  ((le_abs_self _).trans (hC_ω_bd U')) (hgs.ω_pos U').le
                  (mul_nonneg (sq_nonneg _) hC_ω_nn)) hcre (abs_nonneg _)
                  (mul_nonneg (mul_nonneg (sq_nonneg _) hC_ω_nn) hC_ω_nn)
            _ = M_kern := by dsimp only [M_kern]; ring)
    have h_int_outer_p : ∀ p : Fin N × Fin N,
        MeasureTheory.Integrable
          (fun U : G_L => ∫ U', K_W U U' * ω U * ω U' *
            (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ) μ := by
      intro p
      have hc_int : Continuous (fun U : G_L => ∫ U', K_W U U' * ω U * ω U' *
          (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ) := by
        refine MeasureTheory.continuous_of_dominated ?_ ?_
          (MeasureTheory.integrable_const M_kern) ?_
        · intro U; exact (h_int_inner_p p U).aestronglyMeasurable
        · intro U; refine Filter.Eventually.of_forall fun U' => ?_
          rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_mul,
            abs_of_nonneg (hKW_nn U U'), abs_of_nonneg (hgs.ω_pos U).le,
            abs_of_nonneg (hgs.ω_pos U').le]
          have hcre : |(starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re| ≤ 1 := by
            refine (Complex.abs_re_le_norm _).trans ?_
            rw [norm_mul, Complex.norm_conj]
            exact mul_le_one₀ (su_entry_norm_le_one (U e₀) p.1 p.2) (norm_nonneg _)
              (su_entry_norm_le_one (U' e₀) p.1 p.2)
          calc K_W U U' * ω U * ω U' *
                |(starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
                  (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re|
              ≤ ((linkChiUb L β) ^ 2) * C_ω * C_ω * 1 := by
                refine mul_le_mul (mul_le_mul (mul_le_mul (hKW_ub U U')
                  ((le_abs_self _).trans (hC_ω_bd U)) (hgs.ω_pos U).le (sq_nonneg _))
                  ((le_abs_self _).trans (hC_ω_bd U')) (hgs.ω_pos U').le
                  (mul_nonneg (sq_nonneg _) hC_ω_nn)) hcre (abs_nonneg _)
                  (mul_nonneg (mul_nonneg (sq_nonneg _) hC_ω_nn) hC_ω_nn)
            _ = M_kern := by dsimp only [M_kern]; ring
        · refine Filter.Eventually.of_forall fun U' => ?_
          have hK_l := hKW_cont.comp (continuous_id.prodMk continuous_const)
          have h_ent : Continuous (fun U : G_L =>
              (U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) :=
            (continuous_apply p.2).comp ((continuous_apply p.1).comp
              (continuous_subtype_val.comp (continuous_apply e₀)))
          exact (((hK_l.mul hgs.ω_cont).mul continuous_const)).mul
            (Complex.continuous_re.comp ((continuous_star.comp h_ent).mul continuous_const))
      exact (MeasureTheory.integrable_const M_kern).mono'
        hc_int.stronglyMeasurable.aestronglyMeasurable
        (Filter.Eventually.of_forall fun U => by
          calc ‖∫ U', _ ∂μ‖ ≤ ∫ U', ‖_‖ ∂μ := MeasureTheory.norm_integral_le_integral_norm _
            _ ≤ ∫ _U', M_kern ∂μ := MeasureTheory.integral_mono (h_int_inner_p p U).norm
                (MeasureTheory.integrable_const M_kern) fun U' => by
                  rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_mul,
                    abs_of_nonneg (hKW_nn U U'), abs_of_nonneg (hgs.ω_pos U).le,
                    abs_of_nonneg (hgs.ω_pos U').le]
                  have hcre : |(starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
                      (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re| ≤ 1 := by
                    refine (Complex.abs_re_le_norm _).trans ?_
                    rw [norm_mul, Complex.norm_conj]
                    exact mul_le_one₀ (su_entry_norm_le_one (U e₀) p.1 p.2) (norm_nonneg _)
                      (su_entry_norm_le_one (U' e₀) p.1 p.2)
                  calc K_W U U' * ω U * ω U' *
                        |(starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
                          (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re|
                      ≤ ((linkChiUb L β) ^ 2) * C_ω * C_ω * 1 := by
                        refine mul_le_mul (mul_le_mul (mul_le_mul (hKW_ub U U')
                          ((le_abs_self _).trans (hC_ω_bd U)) (hgs.ω_pos U).le (sq_nonneg _))
                          ((le_abs_self _).trans (hC_ω_bd U')) (hgs.ω_pos U').le
                          (mul_nonneg (sq_nonneg _) hC_ω_nn)) hcre (abs_nonneg _)
                          (mul_nonneg (mul_nonneg (sq_nonneg _) hC_ω_nn) hC_ω_nn)
                    _ = M_kern := by dsimp only [M_kern]; ring
            _ = M_kern := by simp [Measure.real, MeasureTheory.measure_univ])
    simp_rw [h_inner_ST]
    rw [← Finset.mul_sum]
    have hsum_out := integral_finset_sum_eq (Finset.univ : Finset (Fin N × Fin N))
      (fun p U => ∫ U', K_W U U' * ω U * ω U' *
        (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ)
      (fun p _ => h_int_outer_p p)
    rw [← hsum_out.2]
    have h_inner_sum : (fun U : G_L => ∑ p : Fin N × Fin N, ∫ U', K_W U U' * ω U * ω U' *
        (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ) =
        fun U => ∫ U', ∑ p : Fin N × Fin N, K_W U U' * ω U * ω U' *
          (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ := by
      funext U
      exact (integral_finset_sum_eq Finset.univ _ (fun p _ => h_int_inner_p p U)).2.symm
    rw [h_inner_sum]
    have h_lhs_eq : (N : ℝ) - lam0⁻¹ * ∫ U, ∫ U', ∑ p : Fin N × Fin N,
          K_W U U' * ω U * ω U' *
            (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ ∂μ =
        lam0⁻¹ * ((N : ℝ) * lam0 - ∫ U, ∫ U', ∑ p : Fin N × Fin N,
          K_W U U' * ω U * ω U' *
            (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ ∂μ) := by
      field_simp [hlam0_pos.ne']
    rw [h_lhs_eq, ← h_int_N_val, ← MeasureTheory.integral_const_mul (N : ℝ)]
    have h_int_N_full : MeasureTheory.Integrable
        (fun U : G_L => (N : ℝ) * ∫ U', K_W U U' * ω U * ω U' ∂μ) μ :=
      h_int_base.const_mul (N : ℝ)
    rw [← MeasureTheory.integral_sub h_int_N_full hsum_out.1]
    have h_sub_pt : (fun U : G_L => (N : ℝ) * (∫ U', K_W U U' * ω U * ω U' ∂μ) -
        ∫ U', ∑ p : Fin N × Fin N, K_W U U' * ω U * ω U' *
          (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re ∂μ) =
        fun U => (1 / 2 : ℝ) * ∫ U', K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ := by
      funext U
      have h_int_sum_U := (integral_finset_sum_eq (Finset.univ : Finset (Fin N × Fin N))
        (fun p U' => K_W U U' * ω U * ω U' *
          (starRingEnd ℂ ((U e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2) *
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ) p.1 p.2).re)
        (fun p _ => h_int_inner_p p U)).1
      rw [← MeasureTheory.integral_const_mul (N : ℝ),
        ← MeasureTheory.integral_sub ((h_int_KW_U U).const_mul (N : ℝ)) h_int_sum_U,
        ← MeasureTheory.integral_const_mul (1 / 2 : ℝ)]
      refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U' => ?_)
      rw [← Finset.mul_sum]
      have h_eq' : (N : ℝ) * (K_W U U' * ω U * ω U') =
          K_W U U' * ω U * ω U' * (N : ℝ) := by ring
      rw [h_eq', ← mul_sub]
      exact h_pt_diff U U'
    rw [h_sub_pt, MeasureTheory.integral_const_mul]
    ring
  -- Step 3: `ε/δ` split at `2 * ε_sq`
  let δ : ℝ := 1 / Real.sqrt β
  have hδ_pos : 0 < δ := by positivity
  let B_ball : Set G_L :=
    { U | ∀ e, frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 }
  let D_fn : G_L → G_L → ℝ := fun U U' =>
    ∑ e : (cubicTorus3 L).Link,
      frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))
  have hB_ball_meas : MeasurableSet B_ball := by
    have h_eq : B_ball = ⋂ e : (cubicTorus3 L).Link,
        { X : G_L | frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 } := by
      ext X; simp [B_ball]
    rw [h_eq]
    refine MeasurableSet.iInter fun e => ?_
    have hc : Continuous (fun X : G_L =>
        frobeniusNormSq ((X e : Matrix (Fin N) (Fin N) ℂ) - 1)) := by
      unfold frobeniusNormSq
      refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
      simp only [Matrix.sub_apply]
      exact (continuous_norm.comp (((continuous_apply j).comp
        ((continuous_apply i).comp (continuous_subtype_val.comp (continuous_apply e)))).sub
        continuous_const)).pow 2
    exact measurableSet_Iic.preimage hc.measurable
  let B_link : Set (Matrix.specialUnitaryGroup (Fin N) ℂ) :=
    { A | frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 }
  have hB_ball_pi : B_ball = Set.pi Set.univ (fun _ => B_link) := by
    ext U; change (∀ e, U e ∈ B_link) ↔ _; simp
  have h_ball_ge : (1 / ((K : ℝ) ^ (2 * N * N))) ^ links ≤ μ.real B_ball := by
    have h_single : (1 : ℝ) / ((K : ℝ) ^ (2 * N * N)) ≤ (suHaar N B_link).toReal :=
      suHaar_ball_ge N hδ_pos
    have hμ_eq : μ B_ball = (suHaar N B_link) ^ links := by
      change (latticeHaarMeasure L N) B_ball = _
      rw [hB_ball_pi]
      erw [MeasureTheory.Measure.pi_pi (fun _ => suHaar N) (fun _ => B_link)]
      have hcard : Fintype.card (cubicTorus3 L).Link = links := by
        dsimp only [links]; simp [cubicTorus3, Fintype.card_prod, Fintype.card_fin]; ring
      rw [Finset.prod_const, Finset.card_univ, hcard]
    have h_real_eq : μ.real B_ball = (suHaar N B_link).toReal ^ links := by
      rw [MeasureTheory.measureReal_def, hμ_eq, ENNReal.toReal_pow]
    rw [h_real_eq]
    exact pow_le_pow_left₀ (by positivity) h_single links
  have h_ball_pos : 0 < μ.real B_ball :=
    lt_of_lt_of_le (pow_pos (by positivity) links) h_ball_ge
  have hlam0_lb : (1 / ((K : ℝ) ^ (2 * N * N))) ^ (2 * links) *
      Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) ≤ lam0 := by
    let c_ball : ℝ := (Real.sqrt (μ.real B_ball))⁻¹
    have hc_ball_pos : 0 < c_ball := inv_pos.mpr (Real.sqrt_pos.mpr h_ball_pos)
    let φ_fn : G_L → ℂ := Set.indicator B_ball (fun _ => (c_ball : ℂ))
    have hφ_mem : MeasureTheory.MemLp φ_fn 2 μ :=
      memLp_two_of_measurable_bound μ φ_fn
        (measurable_const.indicator hB_ball_meas) c_ball hc_ball_pos.le
        (fun U => by
          by_cases hU : U ∈ B_ball
          · simp [φ_fn, hU, Complex.norm_real, Real.norm_of_nonneg hc_ball_pos.le]
          · simp [φ_fn, hU, hc_ball_pos.le])
    let φ : HaarGaugeSpace μ := hφ_mem.toLp φ_fn
    have hφ_ae : ⇑φ =ᵐ[μ] φ_fn := hφ_mem.coeFn_toLp
    have hφ_norm : ‖φ‖ = 1 := by
      have hsq : ‖φ‖ ^ 2 = 1 := by
        have h_in : ‖φ‖ ^ 2 = (⟪φ, φ⟫_ℂ).re := by
          rw [inner_self_eq_norm_sq_to_K, ← Complex.ofReal_pow, Complex.ofReal_re]
        have hl2_φ : MeasureTheory.Integrable (fun U => ⟪φ U, φ U⟫_ℂ) μ :=
          MeasureTheory.L2.integrable_inner (𝕜 := ℂ) φ φ
        rw [h_in, MeasureTheory.L2.inner_def]
        change RCLike.re (∫ U, ⟪φ U, φ U⟫_ℂ ∂μ) = 1
        rw [← integral_re hl2_φ]
        have heq : (fun U => RCLike.re ⟪φ U, φ U⟫_ℂ) =ᵐ[μ]
            Set.indicator B_ball (fun _ => c_ball ^ 2) := by
          filter_upwards [hφ_ae] with U hU
          change (⟪⇑φ U, ⇑φ U⟫_ℂ).re = _
          rw [hU]
          by_cases hU' : U ∈ B_ball
          · simp [φ_fn, hU', sq]
          · simp [φ_fn, hU']
        rw [MeasureTheory.integral_congr_ae heq, MeasureTheory.integral_indicator hB_ball_meas,
          MeasureTheory.setIntegral_const, smul_eq_mul]
        dsimp only [c_ball]
        rw [inv_pow, Real.sq_sqrt h_ball_pos.le, mul_inv_cancel₀ h_ball_pos.ne']
      nlinarith [norm_nonneg φ]
    have h_op : (⟪φ, T_raw φ⟫_ℂ).re ≤ lam0 := by
      calc (⟪φ, T_raw φ⟫_ℂ).re ≤ ‖⟪φ, T_raw φ⟫_ℂ‖ :=
            (le_abs_self _).trans (Complex.abs_re_le_norm _)
        _ ≤ ‖φ‖ * ‖T_raw φ‖ := norm_inner_le_norm _ _
        _ ≤ ‖φ‖ * (‖T_raw‖ * ‖φ‖) := mul_le_mul_of_nonneg_left (T_raw.le_opNorm φ) (norm_nonneg _)
        _ = lam0 := by rw [hφ_norm]; dsimp only [lam0]; ring
    have h_in_re := l2_inner_wilsonOp_re L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd T_raw hT_raw_eq φ φ_fn hφ_ae
    have h_ind_eq : ∀ U U', K_W U U' * (starRingEnd ℂ (φ_fn U) * φ_fn U').re =
        Set.indicator B_ball (fun _ => (1 : ℝ)) U *
          (Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U') := fun U U' => by
      by_cases hU : U ∈ B_ball <;> by_cases hU' : U' ∈ B_ball <;>
        simp [φ_fn, hU, hU', sq, mul_comm, mul_assoc, mul_left_comm]
    simp_rw [h_ind_eq] at h_in_re
    let c_lb : ℝ := μ.real B_ball * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ))
    have hc_lb_nn : 0 ≤ c_lb := mul_nonneg MeasureTheory.measureReal_nonneg (Real.exp_pos _).le
    have h_lb_ball : ∀ U ∈ B_ball, ∀ U' ∈ B_ball, c_lb ≤ K_W U U' := fun U hU U' hU' =>
      wilsonKernel_lower_bound_ball L N hN hβ U hU U' hU'
    have h_inner_lb : ∀ U ∈ B_ball,
        μ.real B_ball * (c_ball ^ 2 * c_lb) ≤
          ∫ U', Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U' ∂μ := fun U hU => by
      have h_int_KW_U' : MeasureTheory.Integrable
          (fun U' => Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U') μ := by
        have h_cont_R : Continuous (fun U' => K_W U U') :=
          continuous_cubicWilsonKernel_right L N β K_kin hK_cont U
        exact (MeasureTheory.integrable_const (c_ball ^ 2 * (linkChiUb L β) ^ 2)).mono'
          (((measurable_const.indicator hB_ball_meas).mul h_cont_R.measurable).stronglyMeasurable.aestronglyMeasurable)
          (Filter.Eventually.of_forall fun U' => by
            by_cases hU' : U' ∈ B_ball
            · simp only [Set.indicator_of_mem hU', Real.norm_eq_abs,
                abs_mul, abs_of_nonneg (sq_nonneg c_ball), abs_of_nonneg (hKW_nn U U')]
              exact mul_le_mul_of_nonneg_left (hKW_ub U U') (sq_nonneg _)
            · simp [Set.indicator_of_notMem hU', mul_nonneg (sq_nonneg c_ball) (sq_nonneg _)])
      have h_int_ind : MeasureTheory.Integrable
          (Set.indicator B_ball (fun _ => c_ball ^ 2 * c_lb)) μ :=
        (MeasureTheory.integrable_const _).indicator hB_ball_meas
      calc μ.real B_ball * (c_ball ^ 2 * c_lb)
          = ∫ U', Set.indicator B_ball (fun _ => c_ball ^ 2 * c_lb) U' ∂μ := by
            rw [MeasureTheory.integral_indicator hB_ball_meas, MeasureTheory.setIntegral_const,
              smul_eq_mul]
        _ ≤ ∫ U', Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U' ∂μ := by
            refine MeasureTheory.integral_mono h_int_ind h_int_KW_U' fun U' => ?_
            by_cases hU' : U' ∈ B_ball
            · simp only [Set.indicator_of_mem hU']
              exact mul_le_mul_of_nonneg_left (h_lb_ball U hU U' hU') (sq_nonneg _)
            · simp [Set.indicator_of_notMem hU']
    have h_outer_lb : μ.real B_ball * (μ.real B_ball * (c_ball ^ 2 * c_lb)) ≤
        ∫ U, Set.indicator B_ball (fun _ => (1 : ℝ)) U *
          (∫ U', Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U' ∂μ) ∂μ := by
      have h_int_out : MeasureTheory.Integrable
          (fun U => Set.indicator B_ball (fun _ => (1 : ℝ)) U *
            (∫ U', Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U' ∂μ)) μ := by
        have h_cont_g : Continuous (fun U : G_L =>
            ∫ U', Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U' ∂μ) := by
          refine MeasureTheory.continuous_of_dominated ?_ ?_
            (MeasureTheory.integrable_const (c_ball ^ 2 * (linkChiUb L β) ^ 2)) ?_
          · intro U
            have h_cont_R : Continuous (fun U' => K_W U U') :=
              continuous_cubicWilsonKernel_right L N β K_kin hK_cont U
            exact ((measurable_const.indicator hB_ball_meas).mul h_cont_R.measurable).stronglyMeasurable.aestronglyMeasurable
          · intro U; refine Filter.Eventually.of_forall fun U' => ?_
            by_cases hU' : U' ∈ B_ball
            · simp only [Set.indicator_of_mem hU', Real.norm_eq_abs, abs_mul,
                abs_of_nonneg (sq_nonneg c_ball), abs_of_nonneg (hKW_nn U U')]
              exact mul_le_mul_of_nonneg_left (hKW_ub U U') (sq_nonneg _)
            · simp [Set.indicator_of_notMem hU', mul_nonneg (sq_nonneg c_ball) (sq_nonneg _)]
          · refine Filter.Eventually.of_forall fun U' => ?_
            exact continuous_const.mul (hKW_cont.comp (continuous_id.prodMk continuous_const))
        exact (MeasureTheory.integrable_const (c_ball ^ 2 * (linkChiUb L β) ^ 2)).mono'
          (((measurable_const.indicator hB_ball_meas).mul h_cont_g.measurable).stronglyMeasurable.aestronglyMeasurable)
          (Filter.Eventually.of_forall fun U => by
            by_cases hU : U ∈ B_ball
            · simp only [Set.indicator_of_mem hU, one_mul]
              have h_int_norm : MeasureTheory.Integrable
                  (fun U' => ‖Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U'‖) μ := by
                have h_cont_R : Continuous (fun U' => K_W U U') :=
                  continuous_cubicWilsonKernel_right L N β K_kin hK_cont U
                exact (MeasureTheory.integrable_const (c_ball ^ 2 * (linkChiUb L β) ^ 2)).mono'
                  ((measurable_const.indicator hB_ball_meas).mul
                    h_cont_R.measurable).stronglyMeasurable.aestronglyMeasurable.norm
                  (Filter.Eventually.of_forall fun U' => by
                    rw [Real.norm_eq_abs, abs_abs]
                    by_cases hU' : U' ∈ B_ball
                    · simp only [Set.indicator_of_mem hU', abs_mul,
                        abs_of_nonneg (sq_nonneg c_ball), abs_of_nonneg (hKW_nn U U')]
                      exact mul_le_mul_of_nonneg_left (hKW_ub U U') (sq_nonneg _)
                    · simp [Set.indicator_of_notMem hU', mul_nonneg (sq_nonneg c_ball) (sq_nonneg _)])
              calc ‖∫ U', _ ∂μ‖ ≤ ∫ U', ‖_‖ ∂μ := MeasureTheory.norm_integral_le_integral_norm _
                _ ≤ ∫ _U', c_ball ^ 2 * (linkChiUb L β) ^ 2 ∂μ := by
                    refine MeasureTheory.integral_mono h_int_norm (MeasureTheory.integrable_const _)
                      fun U' => ?_
                    by_cases hU' : U' ∈ B_ball
                    · simp only [Set.indicator_of_mem hU', Real.norm_eq_abs, abs_mul,
                        abs_of_nonneg (sq_nonneg c_ball), abs_of_nonneg (hKW_nn U U')]
                      exact mul_le_mul_of_nonneg_left (hKW_ub U U') (sq_nonneg _)
                    · simp [Set.indicator_of_notMem hU', mul_nonneg (sq_nonneg c_ball) (sq_nonneg _)]
                _ = c_ball ^ 2 * (linkChiUb L β) ^ 2 := by
                    simp [Measure.real, MeasureTheory.measure_univ]
            · simp [Set.indicator_of_notMem hU, mul_nonneg (sq_nonneg c_ball) (sq_nonneg _)])
      have h_ind_out : MeasureTheory.Integrable
          (Set.indicator B_ball (fun _ => μ.real B_ball * (c_ball ^ 2 * c_lb))) μ :=
        (MeasureTheory.integrable_const _).indicator hB_ball_meas
      calc μ.real B_ball * (μ.real B_ball * (c_ball ^ 2 * c_lb))
          = ∫ U, Set.indicator B_ball (fun _ => μ.real B_ball * (c_ball ^ 2 * c_lb)) U ∂μ := by
            rw [MeasureTheory.integral_indicator hB_ball_meas, MeasureTheory.setIntegral_const,
              smul_eq_mul]
        _ ≤ ∫ U, Set.indicator B_ball (fun _ => (1 : ℝ)) U *
              (∫ U', Set.indicator B_ball (fun _ => c_ball ^ 2) U' * K_W U U' ∂μ) ∂μ := by
            refine MeasureTheory.integral_mono h_ind_out h_int_out fun U => ?_
            by_cases hU : U ∈ B_ball
            · simp only [Set.indicator_of_mem hU, one_mul]
              exact h_inner_lb U hU
            · simp [Set.indicator_of_notMem hU]
    have h_simplify : μ.real B_ball * (μ.real B_ball * (c_ball ^ 2 * c_lb)) =
        (μ.real B_ball) ^ 2 * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) := by
      dsimp only [c_ball, c_lb]
      rw [inv_pow, Real.sq_sqrt h_ball_pos.le]
      field_simp [h_ball_pos.ne']
    have h_pow_le : (1 / ((K : ℝ) ^ (2 * N * N))) ^ (2 * links) ≤ (μ.real B_ball) ^ 2 := by
      rw [mul_comm 2 links, pow_mul]
      exact pow_le_pow_left₀ (by positivity) h_ball_ge 2
    calc (1 / ((K : ℝ) ^ (2 * N * N))) ^ (2 * links) *
          Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ))
        ≤ (μ.real B_ball) ^ 2 *
            Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) :=
          mul_le_mul_of_nonneg_right h_pow_le (Real.exp_pos _).le
      _ = μ.real B_ball * (μ.real B_ball * (c_ball ^ 2 * c_lb)) := h_simplify.symm
      _ ≤ (⟪φ, T_raw φ⟫_ℂ).re := by rw [h_in_re]; exact h_outer_lb
      _ ≤ lam0 := h_op
  let C_large : ℝ := 4 * (N : ℝ) * Real.exp (β * (links : ℝ)) *
    β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))
  have hC_large_nn : 0 ≤ C_large := by positivity
  have h_pt_split : ∀ U U',
      K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
        (2 * ε_sq) * (K_W U U' * ω U * ω U') + C_large * (ω U * ω U') := by
    intro U U'
    have hω_nn1 := (hgs.ω_pos U).le
    have hω_nn2 := (hgs.ω_pos U').le
    have hKW_nn' := hKW_nn U U'
    by_cases hD : D_fn U U' ≤ 2 * ε_sq
    · have hfrob_le : frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
          2 * ε_sq :=
        (Finset.single_le_sum (f := fun e : (cubicTorus3 L).Link =>
          frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)))
          (fun _ _ => frobeniusNormSq_nonneg _) (Finset.mem_univ e₀)).trans hD
      have h1 : K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
          (2 * ε_sq) * (K_W U U' * ω U * ω U') := by
        rw [mul_comm (2 * ε_sq)]
        exact mul_le_mul_of_nonneg_left hfrob_le (mul_nonneg (mul_nonneg hKW_nn' hω_nn1) hω_nn2)
      have h2 : 0 ≤ C_large * (ω U * ω U') := mul_nonneg hC_large_nn (mul_nonneg hω_nn1 hω_nn2)
      linarith
    · push_neg at hD
      have hfrob_bd : frobeniusNormSq
          ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
          4 * (N : ℝ) := by
        have hsub : (U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ) =
            (U e₀ : Matrix (Fin N) (Fin N) ℂ) + (-(U' e₀ : Matrix (Fin N) (Fin N) ℂ)) := by abel
        rw [hsub]
        have hadd := frobeniusNormSq_add_le (U e₀ : Matrix (Fin N) (Fin N) ℂ)
          (-(U' e₀ : Matrix (Fin N) (Fin N) ℂ))
        have hneg : frobeniusNormSq (-(U' e₀ : Matrix (Fin N) (Fin N) ℂ)) =
            frobeniusNormSq (U' e₀ : Matrix (Fin N) (Fin N) ℂ) := by
          unfold frobeniusNormSq
          refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
          simp
        rw [hneg, frobeniusNormSq_su_self, frobeniusNormSq_su_self] at hadd
        linarith
      have h_exp_rpow : Real.exp (-(β / (8 * (N : ℝ))) * D_fn U U') ≤
          β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        have heq_ε : (β / (8 * (N : ℝ))) * (2 * ε_sq) =
            (6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β := by
          dsimp only [ε_sq]; field_simp [hβ_pos.ne', hN_pos.ne']; ring
        have h_arg_ge : (6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β ≤
            (β / (8 * (N : ℝ))) * D_fn U U' := by
          rw [← heq_ε]
          exact mul_le_mul_of_nonneg_left hD.le (by positivity)
        have hrpow : β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) =
            Real.exp (-((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β)) := by
          rw [Real.rpow_def_of_pos hβ_pos]; congr 1; ring
        rw [hrpow]
        exact Real.exp_le_exp.mpr (by linarith)
      have hKW_ub_D : K_W U U' ≤
          Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        have h_ub := wilsonKernel_upper_bound L N hN hβ U U'
        have h_links : ((3 * L ^ 3 : ℕ) : ℝ) = (links : ℝ) := rfl
        have h_D_eq : ∑ e : (cubicTorus3 L).Link,
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
              (U' e : Matrix (Fin N) (Fin N) ℂ)) = D_fn U U' := rfl
        rw [h_links, h_D_eq] at h_ub
        exact h_ub.trans (mul_le_mul_of_nonneg_left h_exp_rpow (Real.exp_pos _).le)
      have h1 : K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤ C_large * (ω U * ω U') := by
        have hmul1 : K_W U U' * ω U * ω U' *
            frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
            K_W U U' * ω U * ω U' * (4 * (N : ℝ)) :=
          mul_le_mul_of_nonneg_left hfrob_bd (mul_nonneg (mul_nonneg hKW_nn' hω_nn1) hω_nn2)
        have hmul2 : K_W U U' * ω U * ω U' * (4 * (N : ℝ)) ≤
            (Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
              ω U * ω U' * (4 * (N : ℝ)) := by
          have h_re1 : K_W U U' * ω U * ω U' * (4 * (N : ℝ)) =
              K_W U U' * (4 * (N : ℝ) * (ω U * ω U')) := by ring
          have h_re2 : (Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
              ω U * ω U' * (4 * (N : ℝ)) =
              (Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
                (4 * (N : ℝ) * (ω U * ω U')) := by ring
          rw [h_re1, h_re2]
          exact mul_le_mul_of_nonneg_right hKW_ub_D (by positivity)
        have h_eq_C : (Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
            ω U * ω U' * (4 * (N : ℝ)) = C_large * (ω U * ω U') := by
          dsimp only [C_large]; ring
        exact hmul1.trans (hmul2.trans_eq h_eq_C)
      have h2 : 0 ≤ (2 * ε_sq) * (K_W U U' * ω U * ω U') := by
        have hε_nn : 0 ≤ ε_sq := by
          dsimp only [ε_sq]
          exact div_nonneg (mul_nonneg (by positivity)
            (mul_nonneg (by positivity) (Real.log_nonneg hβ))) hβ_pos.le
        exact mul_nonneg (by linarith) (mul_nonneg (mul_nonneg hKW_nn' hω_nn1) hω_nn2)
      linarith
  have h_frob_cont : ∀ U : G_L, Continuous (fun U' : G_L =>
      frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
        (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) := fun U => by
    unfold frobeniusNormSq
    refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
    simp only [Matrix.sub_apply]
    exact (continuous_norm.comp (continuous_const.sub ((continuous_apply j).comp
      ((continuous_apply i).comp (continuous_subtype_val.comp (continuous_apply e₀)))))).pow 2
  have h_frob_cont_l : ∀ U' : G_L, Continuous (fun U : G_L =>
      frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
        (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) := fun U' => by
    unfold frobeniusNormSq
    refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
    simp only [Matrix.sub_apply]
    exact (continuous_norm.comp (((continuous_apply j).comp
      ((continuous_apply i).comp (continuous_subtype_val.comp (continuous_apply e₀)))).sub
      continuous_const)).pow 2
  let M_lhs : ℝ := (linkChiUb L β) ^ 2 * C_ω ^ 2 * (4 * (N : ℝ))
  have h_lhs_bd : ∀ U U',
      ‖K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ))‖ ≤ M_lhs := fun U U' => by
    have hnn := mul_nonneg (mul_nonneg (mul_nonneg (hKW_nn U U') (hgs.ω_pos U).le)
      (hgs.ω_pos U').le) (frobeniusNormSq_nonneg _)
    rw [Real.norm_of_nonneg hnn]
    have hfrob_bd : frobeniusNormSq
        ((U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤
        4 * (N : ℝ) := by
      have hsub : (U e₀ : Matrix (Fin N) (Fin N) ℂ) - (U' e₀ : Matrix (Fin N) (Fin N) ℂ) =
          (U e₀ : Matrix (Fin N) (Fin N) ℂ) + (-(U' e₀ : Matrix (Fin N) (Fin N) ℂ)) := by abel
      rw [hsub]
      have hadd := frobeniusNormSq_add_le (U e₀ : Matrix (Fin N) (Fin N) ℂ)
        (-(U' e₀ : Matrix (Fin N) (Fin N) ℂ))
      have hneg : frobeniusNormSq (-(U' e₀ : Matrix (Fin N) (Fin N) ℂ)) =
          frobeniusNormSq (U' e₀ : Matrix (Fin N) (Fin N) ℂ) := by
        unfold frobeniusNormSq
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
        simp
      rw [hneg, frobeniusNormSq_su_self, frobeniusNormSq_su_self] at hadd
      linarith
    calc K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ))
        ≤ ((linkChiUb L β) ^ 2 * C_ω * C_ω) * (4 * (N : ℝ)) := by
          refine mul_le_mul (mul_le_mul (mul_le_mul (hKW_ub U U')
            ((le_abs_self _).trans (hC_ω_bd U)) (hgs.ω_pos U).le (sq_nonneg _))
            ((le_abs_self _).trans (hC_ω_bd U')) (hgs.ω_pos U').le
            (mul_nonneg (sq_nonneg _) hC_ω_nn)) hfrob_bd (frobeniusNormSq_nonneg _)
            (mul_nonneg (mul_nonneg (sq_nonneg _) hC_ω_nn) hC_ω_nn)
      _ = M_lhs := by dsimp only [M_lhs]; ring
  have h_lhs_in : ∀ U : G_L, MeasureTheory.Integrable
      (fun U' => K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) μ := fun U => by
    have hc : Continuous (fun U' => K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ))) :=
      (((hKW_cont.comp (continuous_const.prodMk continuous_id)).mul continuous_const).mul
        hgs.ω_cont).mul (h_frob_cont U)
    exact (MeasureTheory.integrable_const M_lhs).mono'
      hc.stronglyMeasurable.aestronglyMeasurable (Filter.Eventually.of_forall (h_lhs_bd U))
  have h_lhs_out : MeasureTheory.Integrable
      (fun U : G_L => ∫ U', K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ) μ := by
    have hc : Continuous (fun U : G_L => ∫ U', K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ) := by
      refine MeasureTheory.continuous_of_dominated h_lhs_in
        (fun U => Filter.Eventually.of_forall (h_lhs_bd U))
        (MeasureTheory.integrable_const M_lhs) ?_
      refine Filter.Eventually.of_forall fun U' => ?_
      exact (((hKW_cont.comp (continuous_id.prodMk continuous_const)).mul hgs.ω_cont).mul
        continuous_const).mul (h_frob_cont_l U')
    exact (MeasureTheory.integrable_const M_lhs).mono'
      hc.stronglyMeasurable.aestronglyMeasurable (Filter.Eventually.of_forall fun U => by
        calc ‖∫ U', _ ∂μ‖ ≤ ∫ U', ‖_‖ ∂μ := MeasureTheory.norm_integral_le_integral_norm _
          _ ≤ ∫ _U', M_lhs ∂μ := MeasureTheory.integral_mono (h_lhs_in U).norm
              (MeasureTheory.integrable_const M_lhs) (h_lhs_bd U)
          _ = M_lhs := by simp [Measure.real, MeasureTheory.measure_univ])
  have h_ω_int : MeasureTheory.Integrable ω μ :=
    (MeasureTheory.integrable_const C_ω).mono'
      hgs.ω_cont.stronglyMeasurable.aestronglyMeasurable
      (Filter.Eventually.of_forall fun U => by
        rw [Real.norm_of_nonneg (hgs.ω_pos U).le]
        exact (le_abs_self _).trans (hC_ω_bd U))
  have h_rhs_in : ∀ U : G_L, MeasureTheory.Integrable
      (fun U' => (2 * ε_sq) * (K_W U U' * ω U * ω U') + C_large * (ω U * ω U')) μ := fun U =>
    ((h_int_KW_U U).const_mul (2 * ε_sq)).add ((h_ω_int.const_mul (ω U)).const_mul C_large)
  have h_rhs_out_eq : (fun U : G_L => ∫ U',
        (2 * ε_sq) * (K_W U U' * ω U * ω U') + C_large * (ω U * ω U') ∂μ) =
      fun U => (2 * ε_sq) * (∫ U', K_W U U' * ω U * ω U' ∂μ) +
        C_large * ((∫ U', ω U' ∂μ) * ω U) := by
    funext U
    have h_swap : (fun U' => ω U * ω U') = fun U' => ω U * ω U' := rfl
    rw [MeasureTheory.integral_add ((h_int_KW_U U).const_mul _)
      ((h_ω_int.const_mul _).const_mul _),
      MeasureTheory.integral_const_mul, MeasureTheory.integral_const_mul,
      MeasureTheory.integral_const_mul]
    ring
  have h_rhs_out : MeasureTheory.Integrable
      (fun U : G_L => ∫ U', (2 * ε_sq) * (K_W U U' * ω U * ω U') +
        C_large * (ω U * ω U') ∂μ) μ := by
    rw [h_rhs_out_eq]
    exact (h_int_base.const_mul (2 * ε_sq)).add
      ((h_ω_int.const_mul (∫ U', ω U' ∂μ)).const_mul C_large)
  have h_int_split :
      ∫ U, ∫ U', K_W U U' * ω U * ω U' *
        frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ ≤
        (2 * ε_sq) * lam0 + C_large := by
    have h_mono : ∫ U, ∫ U', K_W U U' * ω U * ω U' *
          frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
            (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ ≤
        ∫ U, ∫ U', (2 * ε_sq) * (K_W U U' * ω U * ω U') +
          C_large * (ω U * ω U') ∂μ ∂μ :=
      MeasureTheory.integral_mono h_lhs_out h_rhs_out fun U =>
        MeasureTheory.integral_mono (h_lhs_in U) (h_rhs_in U) (h_pt_split U)
    rw [h_rhs_out_eq, MeasureTheory.integral_add (h_int_base.const_mul _)
      ((h_ω_int.const_mul _).const_mul _), MeasureTheory.integral_const_mul, h_int_N_val,
      MeasureTheory.integral_const_mul, MeasureTheory.integral_const_mul] at h_mono
    have hsq_le1 : (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ 1 := by
      calc (∫ U', ω U' ∂μ) * (∫ U, ω U ∂μ) ≤ 1 * 1 :=
            mul_le_mul hω_l1_le hω_l1_le hω_l1_nn zero_le_one
        _ = 1 := one_mul 1
    linarith [mul_le_mul_of_nonneg_left hsq_le1 hC_large_nn]
  have h_dir_le : (N : ℝ) - ∑ p : Fin N × Fin N, (⟪ψ p, S.T (ψ p)⟫_ℂ).re ≤ (N : ℝ) * err := by
    have h_step1 : (N : ℝ) - ∑ p : Fin N × Fin N, (⟪ψ p, S.T (ψ p)⟫_ℂ).re ≤
        (1 / (2 * lam0)) * ((2 * ε_sq) * lam0 + C_large) := by
      rw [h_diff_sum_eq]
      exact mul_le_mul_of_nonneg_left h_int_split (by positivity)
    have h_step2 : (1 / (2 * lam0)) * ((2 * ε_sq) * lam0 + C_large) =
        ε_sq + 2 * (N : ℝ) * (Real.exp (β * (links : ℝ)) / lam0) *
          β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
      dsimp only [C_large]
      field_simp [hlam0_pos.ne']
      ring
    have h_lam_div : Real.exp (β * (links : ℝ)) / lam0 ≤
        Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) * ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) := by
      have hK_pos_r : 0 < ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) := by
        have hK_pos : 0 < K := Nat.succ_pos _
        positivity
      have h1 := hlam0_lb
      rw [one_div_pow] at h1
      have h_exp_split : Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) =
          Real.exp (β * (links : ℝ)) * Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ))) := by
        rw [← Real.exp_add]; congr 1; ring
      rw [h_exp_split] at h1
      have h2 : Real.exp (β * (links : ℝ)) * Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ))) ≤
          lam0 * ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) := by
        have := mul_le_mul_of_nonneg_right h1 hK_pos_r.le
        rwa [mul_assoc, inv_mul_cancel_left₀ hK_pos_r.ne'] at this
      have h3 : Real.exp (β * (links : ℝ)) ≤
          lam0 * ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
            Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) := by
        have := mul_le_mul_of_nonneg_right h2 (Real.exp_pos (30 * (L : ℝ) ^ 3 / (N : ℝ))).le
        have h_cancel : Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ))) *
            Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) = 1 := by
          rw [← Real.exp_add, neg_add_cancel, Real.exp_zero]
        rwa [mul_assoc, h_cancel, mul_one] at this
      rw [div_le_iff₀ hlam0_pos]
      linarith [show lam0 * ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
          Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) =
          Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) * ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
            lam0 by ring]
    have hε_nn : 0 ≤ ε_sq := by
      dsimp only [ε_sq]
      exact div_nonneg (mul_nonneg (by positivity)
        (mul_nonneg (by positivity) (Real.log_nonneg hβ))) hβ_pos.le
    have h_step3 : ε_sq + 2 * (N : ℝ) * (Real.exp (β * (links : ℝ)) / lam0) *
          β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) ≤ (N : ℝ) * err := by
      have h_t1 : ε_sq ≤ 2 * ε_sq := by linarith
      have h_t2 : 2 * (N : ℝ) * (Real.exp (β * (links : ℝ)) / lam0) *
            β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) ≤
          8 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
            ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        have h_mul_lam : 2 * (N : ℝ) * (Real.exp (β * (links : ℝ)) / lam0) *
              β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) ≤
            2 * (N : ℝ) * (Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
              ((K : ℝ) ^ (2 * N * N)) ^ (2 * links)) *
              β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) :=
          mul_le_mul_of_nonneg_right
            (mul_le_mul_of_nonneg_left h_lam_div (by positivity))
            (by positivity)
        have h_nonneg_tail : 0 ≤ (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
            ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
          positivity
        linarith
      have h_N_err : (N : ℝ) * err = 2 * ε_sq + 8 * (N : ℝ) *
          Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) * ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
            β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        dsimp only [err]
        exact mul_div_cancel₀ _ hN_pos.ne'
      linarith
    exact h_step1.trans (h_step2 ▸ h_step3)
  have hS_a : S.a = 1 := rfl
  have h_gap_sum : ∑ p : Fin N × Fin N, (⟪ψ p, S.T (ψ p)⟫_ℂ).re ≤
      Real.exp (-S.Δ) * (N : ℝ) := by
    have h_each : ∀ p : Fin N × Fin N,
        (⟪ψ p, S.T (ψ p)⟫_ℂ).re ≤ Real.exp (-S.Δ) * ‖ψ p‖ ^ 2 := fun p => by
      have hg := S.gap (ψ p) (hψ_orth p)
      rwa [hS_a, mul_one] at hg
    calc ∑ p : Fin N × Fin N, (⟪ψ p, S.T (ψ p)⟫_ℂ).re
        ≤ ∑ p : Fin N × Fin N, Real.exp (-S.Δ) * ‖ψ p‖ ^ 2 :=
          Finset.sum_le_sum fun p _ => h_each p
      _ = Real.exp (-S.Δ) * ∑ p : Fin N × Fin N, ‖ψ p‖ ^ 2 := by rw [← Finset.mul_sum]
      _ = Real.exp (-S.Δ) * (N : ℝ) := by rw [hψ_norm_sum]
  have h_mul_le : (1 - err) * (N : ℝ) ≤ Real.exp (-S.Δ) * (N : ℝ) := by linarith
  have h_le_exp : 1 - err ≤ Real.exp (-S.Δ) :=
    le_of_mul_le_mul_right h_mul_le hN_pos
  have h_log_le : Real.log (1 - err) ≤ Real.log (Real.exp (-S.Δ)) :=
    Real.log_le_log (by linarith) h_le_exp
  rw [Real.log_exp] at h_log_le
  linarith'''

old_sorry = "  sorry -- full assembly continues identically with Step 2 (Dirichlet form) & Step 3 (ε/δ split)"
target = "theorem fullRankCubic_gap_upper_bound"
assert src.count(target) == 1
assert src.count(old_sorry) == 1
src = src.replace(target, helpers + target, 1).replace(old_sorry, new_proof, 1)

for i, line in enumerate(src.splitlines(), 1):
    code_part = line.split('--')[0]
    if 'sorry' in code_part:
        raise AssertionError(f"Found sorry on line {i}: {line}")

print("Verified ZERO sorrys! Final line count:", len(src.splitlines()))
