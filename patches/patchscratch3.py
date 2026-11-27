with open('input_file_1.txt', 'r', encoding='utf-8', errors='replace') as f:
    raw = f.read()
src = raw[raw.index('\n') + 1:]

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

patch_exec = patch_code.replace('src = path.read_text(encoding="utf-8")', '# keep src').replace('path.write_text(src, encoding="utf-8")', '# skip write')
exec(patch_exec)
print("Final check passed: sorry count =", len([l for l in src.splitlines() if 'sorry' in l and not l.strip().startswith('/--')]))
