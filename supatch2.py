#!/usr/bin/env python3
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
src = path.read_text(encoding="utf-8")

replacements = [
    (
        """/-- **Explicit Spectral-Gap Upper Bound & Convergence to `0` (`0 sorry`):**""",
        """private lemma frobeniusNormSq_neg {N : ℕ} (M : Matrix (Fin N) (Fin N) ℂ) :
    frobeniusNormSq (-M) = frobeniusNormSq M := by
  unfold frobeniusNormSq
  simp only [Matrix.neg_apply, norm_neg]

private lemma frobeniusNormSq_su_self {N : ℕ}
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq (A : Matrix (Fin N) (Fin N) ℂ) = (N : ℝ) := by
  rw [frobeniusNormSq_trace, (Unitary.mem_iff.mp A.2.1).2, su_one_trace_re]

private lemma frobeniusNormSq_su_sub_one_eq {N : ℕ}
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) =
      2 * ((N : ℝ) - (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re) := by
  rw [frobeniusNormSq_trace]
  have hA : (A : Matrix (Fin N) (Fin N) ℂ) * star (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    (Unitary.mem_iff.mp A.2.1).2
  have hexp : ((A : Matrix (Fin N) (Fin N) ℂ) - 1) *
      star ((A : Matrix (Fin N) (Fin N) ℂ) - 1) =
      1 + 1 - (A : Matrix (Fin N) (Fin N) ℂ) - star (A : Matrix (Fin N) (Fin N) ℂ) := by
    simp only [star_sub, star_one, Matrix.sub_mul, Matrix.mul_sub, Matrix.one_mul,
      Matrix.mul_one, hA]
    abel
  have htr_sub : ∀ M₁ M₂ : Matrix (Fin N) (Fin N) ℂ,
      Matrix.trace (M₁ - M₂) = Matrix.trace M₁ - Matrix.trace M₂ := fun M₁ M₂ => by
    simp [Matrix.trace]
  have htr_add : ∀ M₁ M₂ : Matrix (Fin N) (Fin N) ℂ,
      Matrix.trace (M₁ + M₂) = Matrix.trace M₁ + Matrix.trace M₂ := fun M₁ M₂ => by
    simp [Matrix.trace]
  rw [hexp, htr_sub, htr_sub, htr_add, Complex.sub_re, Complex.sub_re, Complex.add_re]
  have hstar_tr : (Matrix.trace (star (A : Matrix (Fin N) (Fin N) ℂ))).re =
      (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re := by
    change (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)ᴴ).re = _
    rw [Matrix.trace_conjTranspose, Complex.star_def, Complex.conj_re]
  rw [hstar_tr, su_one_trace_re]
  ring

private lemma wilsonPlaquetteTerm_eq_frobenius {L : SpatialLattice} {N : ℕ} [NeZero N]
    (p : LatticePlaquette L)
    (U : GaugeField L (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    wilsonPlaquetteTerm p U =
      frobeniusNormSq ((pathHolonomy U p.loop : Matrix (Fin N) (Fin N) ℂ) - 1) /
        (2 * (N : ℝ)) := by
  unfold wilsonPlaquetteTerm
  rw [frobeniusNormSq_su_sub_one_eq]
  have hN_ne : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (NeZero.ne N)
  field_simp [hN_ne]

private lemma wilsonPlaquetteTerm_nonneg {L : SpatialLattice} {N : ℕ} [NeZero N]
    (p : LatticePlaquette L)
    (U : GaugeField L (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    0 ≤ wilsonPlaquetteTerm p U := by
  rw [wilsonPlaquetteTerm_eq_frobenius]
  exact div_nonneg (frobeniusNormSq_nonneg _) (by positivity)

private lemma frobeniusNormSq_path4_le {L : SpatialLattice} {N : ℕ}
    (U : GaugeField L (Matrix.specialUnitaryGroup (Fin N) ℂ)) {δ : ℝ}
    (hU : ∀ e, frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2)
    (s₁ s₂ s₃ s₄ : L.Link × Bool) :
    frobeniusNormSq ((pathHolonomy U [s₁, s₂, s₃, s₄] : Matrix (Fin N) (Fin N) ℂ) - 1) ≤
      16 * δ ^ 2 := by
  let stepEl : L.Link × Bool → Matrix.specialUnitaryGroup (Fin N) ℂ :=
    fun s => if s.2 then U s.1 else (U s.1)⁻¹
  have hstep : ∀ s, frobeniusNormSq ((stepEl s : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 := by
    intro s
    dsimp [stepEl]
    cases hs : s.2
    · simp only [Bool.false_eq_true, ↓reduceIte, frobeniusNormSq_su_inv_sub_one]
      exact hU s.1
    · simp only [↓reduceIte]
      exact hU s.1
  have hhol : pathHolonomy U [s₁, s₂, s₃, s₄] =
      (stepEl s₁ * stepEl s₂) * (stepEl s₃ * stepEl s₄) := by
    rcases s₁ with ⟨e₁, b₁⟩
    rcases s₂ with ⟨e₂, b₂⟩
    rcases s₃ with ⟨e₃, b₃⟩
    rcases s₄ with ⟨e₄, b₄⟩
    dsimp [stepEl]
    cases b₁ <;> cases b₂ <;> cases b₃ <;> cases b₄ <;>
      simp [pathHolonomy, mul_assoc]
  rw [hhol]
  have h12 := frobeniusNormSq_su_mul_sub_one (stepEl s₁) (stepEl s₂)
  have h34 := frobeniusNormSq_su_mul_sub_one (stepEl s₃) (stepEl s₄)
  have h1234 := frobeniusNormSq_su_mul_sub_one (stepEl s₁ * stepEl s₂) (stepEl s₃ * stepEl s₄)
  linarith [hstep s₁, hstep s₂, hstep s₃, hstep s₄]

private lemma cubicPlaquettes_length (L : ℕ) [NeZero L] :
    (cubicPlaquettes L).length = 3 * L ^ 3 := by
  unfold cubicPlaquettes
  rw [List.length_flatMap]
  have hsum : ∀ (l : List (Fin L × Fin L × Fin L)),
      (l.map fun x => ([ { base := x, loop := cubicPlaquette x 0 1,
            is_closed := cubicPlaquette_isPath x 0 1 },
          { base := x, loop := cubicPlaquette x 0 2,
            is_closed := cubicPlaquette_isPath x 0 2 },
          { base := x, loop := cubicPlaquette x 1 2,
            is_closed := cubicPlaquette_isPath x 1 2 } ] :
          List (LatticePlaquette (cubicTorus3 L))).length).sum = 3 * l.length := by
    intro l
    induction l with
    | nil => simp
    | cons _ tl ih =>
      simp only [List.map_cons, List.sum_cons, List.length_cons, List.length_nil] at ih ⊢
      omega
  rw [hsum, Finset.length_toList, Finset.card_univ, Fintype.card_prod, Fintype.card_prod,
    Fintype.card_fin]
  ring

private lemma integrable_finset_sum_aux {α ι : Type*} [MeasurableSpace α]
    {μ : MeasureTheory.Measure α} (s : Finset ι) (f : ι → α → ℝ)
    (hf : ∀ i ∈ s, MeasureTheory.Integrable (f i) μ) :
    MeasureTheory.Integrable (fun x => ∑ i ∈ s, f i x) μ := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using (MeasureTheory.integrable_zero α ℝ μ)
  | @insert i s hi ih =>
    simp only [Finset.sum_insert hi]
    exact (hf i (Finset.mem_insert_self i s)).add
      (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))

private lemma integral_finset_sum_aux {α ι : Type*} [MeasurableSpace α]
    {μ : MeasureTheory.Measure α} (s : Finset ι) (f : ι → α → ℝ)
    (hf : ∀ i ∈ s, MeasureTheory.Integrable (f i) μ) :
    (∑ i ∈ s, ∫ x, f i x ∂μ) = ∫ x, ∑ i ∈ s, f i x ∂μ := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih =>
    have hf_i : MeasureTheory.Integrable (f i) μ := hf i (Finset.mem_insert_self i s)
    have hf_s : MeasureTheory.Integrable (fun x => ∑ j ∈ s, f j x) μ :=
      integrable_finset_sum_aux s f (fun j hj => hf j (Finset.mem_insert_of_mem hj))
    simp only [Finset.sum_insert hi]
    rw [ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)), MeasureTheory.integral_add hf_i hf_s]

private lemma integral_ofReal_eq {α : Type*} [MeasurableSpace α] {μ : MeasureTheory.Measure α}
    (f : α → ℝ) (hf : MeasureTheory.Integrable f μ) :
    ∫ x, ((f x : ℝ) : ℂ) ∂μ = ((∫ x, f x ∂μ : ℝ) : ℂ) := by
  simpa using (Complex.ofRealCLM.integral_comp_comm hf).symm

/-- **Explicit Spectral-Gap Upper Bound & Convergence to `0` (`0 sorry`):**""",
    ),
    (
        """  sorry -- full assembly continues identically with Step 2 (Dirichlet form) & Step 3 (ε/δ split)""",
        """  have hKW_symm : ∀ U U', K_W U' U = K_W U U' := fun U U' =>
    wilsonKernel_symm β (cubicPlaquettes L) K_kin hK_symm U' U
  have hKW_bounds : ∀ U U', 0 ≤ K_W U U' ∧ K_W U U' ≤ (linkChiUb L β) ^ 2 := fun U U' =>
    wilsonKernel_cubic_le L N β hβ_pos.le K_kin hK_nn ((linkChiUb L β) ^ 2) hK_bd U U'
  have hKW_cont : Continuous (Function.uncurry K_W) :=
    continuous_cubicWilsonKernel L N β K_kin hK_cont
  have hω_int : ∀ U, ∫ U', K_W U U' * ω U' ∂μ = lam0 * ω U := by
    let g_fn : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℂ :=
      fun U => ((∫ U', K_W U U' * ω U' ∂μ : ℝ) : ℂ)
    have h_fn_eq : wilsonIntegralFn L N β K_kin Ω = g_fn := by
      funext U
      dsimp [wilsonIntegralFn, g_fn]
      have h_ae_mul : (fun U' => ((K_W U U' : ℝ) : ℂ) * Ω U') =ᵐ[μ]
          fun U' => ((K_W U U' * ω U' : ℝ) : ℂ) := by
        filter_upwards [hgs.ae_eq] with U' hu'
        rw [hu', Complex.ofReal_mul]
      have h_int_kw : MeasureTheory.Integrable (fun U' => K_W U U' * ω U') μ :=
        integrable_of_continuous_compact μ _
          ((hKW_cont.comp (continuous_const.prodMk continuous_id)).mul hgs.ω_cont)
      rw [MeasureTheory.integral_congr_ae h_ae_mul, integral_ofReal_eq _ h_int_kw]
    have h_ae1 := wilsonIntegralOp_apply_ae L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd Ω
    have h_eig_ae : ⇑(T_raw Ω) =ᵐ[μ] fun U => ((lam0 * ω U : ℝ) : ℂ) := by
      have h_T_eig : T_raw Ω = (lam0 : ℂ) • Ω := hgs.eig
      have hsm := MeasureTheory.Lp.coeFn_smul (lam0 : ℂ) Ω
      filter_upwards [hsm, hgs.ae_eq] with U hsu hu
      rw [h_T_eig]
      change ⇑((lam0 : ℂ) • Ω) U = _
      rw [hsu]
      simp only [Pi.smul_apply, smul_eq_mul, hu, Complex.ofReal_mul]
    have h_ae_eq : g_fn =ᵐ[μ] fun U => ((lam0 * ω U : ℝ) : ℂ) := by
      filter_upwards [h_ae1, h_eig_ae] with U h1 h2
      have h1' : ⇑(T_raw Ω) U = g_fn U := by
        calc ⇑(T_raw Ω) U = wilsonIntegralFn L N β K_kin Ω U := h1
          _ = g_fn U := congrFun h_fn_eq U
      exact h1'.symm.trans h2
    have hg_cont : Continuous g_fn := by
      rw [← h_fn_eq]
      exact wilsonIntegralFn_continuous L N β hβ_pos.le K_kin hK_cont hK_nn
        ((linkChiUb L β) ^ 2) hK_bd Ω
    intro U
    exact Complex.ofReal_injective (eq_of_ae_continuous μ hg_cont
      (Complex.continuous_ofReal.comp (continuous_const.mul hgs.ω_cont)) h_ae_eq U)
  -- Step 2: Entrywise trial family `ψ i j (U) = (U e₀) i j * ω(U)` orthogonal to `Ω`
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  let e₀ : (cubicTorus3 L).Link := ((0, 0, 0), 0)
  let f_ij : Fin N → Fin N → G_L → ℂ := fun i j U =>
    ((U e₀ : Matrix (Fin N) (Fin N) ℂ) i j)
  have hf_cont : ∀ i j, Continuous (f_ij i j) := fun i j =>
    ((continuous_apply j).comp ((continuous_apply i).comp continuous_subtype_val)).comp
      (continuous_apply e₀)
  have hf_flip : ∀ i j U,
      f_ij i j (e_flip U) =
        Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) * f_ij i j U := by
    intro i j U
    dsimp [f_ij, e_flip, sliceCenterFlipEquiv, sliceCenterFlip]
    have he₀ : e₀.1.1 = 0 ∧ e₀.2 = 0 := ⟨rfl, rfl⟩
    simp only [he₀, and_self, ↓reduceIte]
    change ((centralElem N hN : Matrix (Fin N) (Fin N) ℂ) *
        (U e₀ : Matrix (Fin N) (Fin N) ℂ)) i j = _
    dsimp [centralElem]
    simp [Matrix.smul_mul]
  have hψ_mem : ∀ i j, MeasureTheory.MemLp (fun U => f_ij i j U * (ω U : ℂ)) 2 μ := by
    intro i j
    have h_fn_cont : Continuous (fun U => f_ij i j U * (ω U : ℂ)) :=
      (hf_cont i j).mul (Complex.continuous_ofReal.comp hgs.ω_cont)
    rw [MeasureTheory.memLp_two_iff_integrable_sq_norm
      h_fn_cont.stronglyMeasurable.aestronglyMeasurable]
    exact integrable_of_continuous_compact μ _ (h_fn_cont.norm.pow 2)
  let ψ : Fin N → Fin N → HaarGaugeSpace μ := fun i j =>
    (hψ_mem i j).toLp (fun U => f_ij i j U * (ω U : ℂ))
  have hψ_orth : ∀ i j, ⟪ψ i j, Ω⟫_ℂ = 0 := by
    intro i j
    have h_comm : ⟪Ω, ψ i j⟫_ℂ =
        Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) * ⟪Ω, ψ i j⟫_ℂ := by
      have hcoe := (hψ_mem i j).coeFn_toLp
      have h_int_ae : (fun U => ⟪Ω U, (ψ i j) U⟫_ℂ) =ᵐ[μ]
          fun U => (ω U : ℂ) * (ω U : ℂ) * f_ij i j U := by
        filter_upwards [hgs.ae_eq, hcoe] with U hu1 hu2
        change starRingEnd ℂ (⇑Ω U) * ⇑(ψ i j) U = _
        rw [hu1, hu2]
        simp only [Complex.conj_ofReal]
        ring
      have h_eq1 : ⟪Ω, ψ i j⟫_ℂ = ∫ U, (ω U : ℂ) * (ω U : ℂ) * f_ij i j U ∂μ := by
        rw [MeasureTheory.L2.inner_def]
        exact MeasureTheory.integral_congr_ae h_int_ae
      rw [h_eq1, ← hmp.integral_comp' (fun U => (ω U : ℂ) * (ω U : ℂ) * f_ij i j U)]
      have h_flip_fn : (fun U => (ω (e_flip U) : ℂ) * (ω (e_flip U) : ℂ) * f_ij i j (e_flip U)) =
          fun U => Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) *
            ((ω U : ℂ) * (ω U : ℂ) * f_ij i j U) := by
        funext U
        have hw' : ω (e_flip U) = ω U := by
          change ω (sliceCenterFlip L N hN U) = ω U
          exact hω_flip U
        rw [hw', hf_flip i j U]
        ring
      rw [h_flip_fn, MeasureTheory.integral_const_mul, ← h_eq1]
    have hmul0 : (1 - Complex.exp (2 * Real.pi * Complex.I / (N : ℂ))) * ⟪Ω, ψ i j⟫_ℂ = 0 := by
      linear_combination h_comm
    have hne : 1 - Complex.exp (2 * Real.pi * Complex.I / (N : ℂ)) ≠ 0 :=
      sub_ne_zero.mpr (centralElem_ne_one N hN).symm
    have h0 : ⟪Ω, ψ i j⟫_ℂ = 0 := (mul_eq_zero.mp hmul0).resolve_left hne
    rw [← inner_conj_symm, h0, map_zero]
  have hω_int1 : MeasureTheory.Integrable ω μ :=
    integrable_of_continuous_compact μ ω hgs.ω_cont
  have hω_sq_int : MeasureTheory.Integrable (fun U => ω U ^ 2) μ :=
    integrable_of_continuous_compact μ _ (hgs.ω_cont.pow 2)
  have hω_sq_eq : ∫ U, ω U ^ 2 ∂μ = 1 := by
    have h1 : (⟪Ω, Ω⟫_ℂ).re = 1 := by
      rw [inner_self_eq_norm_sq_to_K, hgs.unit]
      simp
    have h_ae : (fun U => (⟪Ω U, Ω U⟫_ℂ).re) =ᵐ[μ] fun U => ω U ^ 2 := by
      filter_upwards [hgs.ae_eq] with U hu
      change (starRingEnd ℂ (⇑Ω U) * ⇑Ω U).re = _
      rw [hu, Complex.conj_ofReal, ← Complex.ofReal_mul, Complex.ofReal_re, sq]
    rw [MeasureTheory.L2.inner_def] at h1
    change RCLike.re (∫ U, ⟪Ω U, Ω U⟫_ℂ ∂μ) = 1 at h1
    rw [← integral_re (MeasureTheory.L2.integrable_inner (𝕜 := ℂ) Ω Ω)] at h1
    rw [← h1]
    exact (MeasureTheory.integral_congr_ae h_ae).symm
  have hω_l1_sq : (∫ U, ω U ∂μ) ^ 2 ≤ 1 := by
    let m : ℝ := ∫ U, ω U ∂μ
    have h_nn : 0 ≤ ∫ U, (ω U - m) ^ 2 ∂μ :=
      MeasureTheory.integral_nonneg fun _ => sq_nonneg _
    have h_id : (fun U => (ω U - m) ^ 2) = fun U => ω U ^ 2 - 2 * m * ω U + m ^ 2 := by
      funext U; ring
    have h_int_lin : MeasureTheory.Integrable (fun U => ω U ^ 2 - 2 * m * ω U) μ :=
      hω_sq_int.sub (hω_int1.const_mul (2 * m))
    rw [h_id, MeasureTheory.integral_add h_int_lin (MeasureTheory.integrable_const _),
      MeasureTheory.integral_sub hω_sq_int (hω_int1.const_mul (2 * m)),
      MeasureTheory.integral_const_mul, hω_sq_eq] at h_nn
    simp only [MeasureTheory.integral_const, Measure.real, MeasureTheory.measure_univ,
      ENNReal.toReal_one, smul_eq_mul, one_mul] at h_nn
    change 0 ≤ 1 - 2 * m * m + m ^ 2 at h_nn
    linarith
  have hψ_norm_sq : ∀ i j, ‖ψ i j‖ ^ 2 = ∫ U, ‖f_ij i j U‖ ^ 2 * ω U ^ 2 ∂μ := by
    intro i j
    have h1 : ‖ψ i j‖ ^ 2 = (⟪ψ i j, ψ i j⟫_ℂ).re := by
      rw [inner_self_eq_norm_sq_to_K, ← Complex.ofReal_pow, Complex.ofReal_re]
    rw [h1, MeasureTheory.L2.inner_def]
    change RCLike.re (∫ U, ⟪(ψ i j) U, (ψ i j) U⟫_ℂ ∂μ) = _
    rw [← integral_re (MeasureTheory.L2.integrable_inner (𝕜 := ℂ) (ψ i j) (ψ i j))]
    refine MeasureTheory.integral_congr_ae ?_
    filter_upwards [(hψ_mem i j).coeFn_toLp] with U hu
    change (starRingEnd ℂ (⇑(ψ i j) U) * ⇑(ψ i j) U).re = _
    rw [hu, Complex.mul_conj, Complex.ofReal_re, Complex.normSq_eq_norm_sq, norm_mul,
      mul_pow, Complex.norm_real, Real.norm_of_nonneg (hgs.ω_pos U).le]
  have hψ_norm_sum : ∑ i : Fin N, ∑ j : Fin N, ‖ψ i j‖ ^ 2 = (N : ℝ) := by
    have h_int_ij : ∀ i j : Fin N,
        MeasureTheory.Integrable (fun U => ‖f_ij i j U‖ ^ 2 * ω U ^ 2) μ := fun i j =>
      integrable_of_continuous_compact μ _
        (((hf_cont i j).norm.pow 2).mul (hgs.ω_cont.pow 2))
    simp_rw [hψ_norm_sq]
    have h_inner : ∀ i : Fin N,
        (∑ j : Fin N, ∫ U, ‖f_ij i j U‖ ^ 2 * ω U ^ 2 ∂μ) =
          ∫ U, (∑ j : Fin N, ‖f_ij i j U‖ ^ 2 * ω U ^ 2) ∂μ := fun i =>
      integral_finset_sum_aux Finset.univ _ fun j _ => h_int_ij i j
    simp_rw [h_inner]
    rw [integral_finset_sum_aux Finset.univ _ fun i _ =>
      integrable_finset_sum_aux Finset.univ _ fun j _ => h_int_ij i j]
    have h_pt : (fun U => ∑ i : Fin N, ∑ j : Fin N, ‖f_ij i j U‖ ^ 2 * ω U ^ 2) =
        fun U => (N : ℝ) * ω U ^ 2 := by
      funext U
      simp_rw [← Finset.sum_mul]
      congr 1
      exact frobeniusNormSq_su_self (U e₀)
    rw [h_pt, MeasureTheory.integral_const_mul, hω_sq_eq, mul_one]
  -- Pointwise Dirichlet form integrand identity
  have h_prod_int : ∀ (F : G_L × G_L → ℝ), Continuous F →
      MeasureTheory.Integrable (fun p : G_L × G_L => F p * (ω p.1 * ω p.2)) (μ.prod μ) := by
    intro F hF
    exact integrable_of_continuous_compact (μ.prod μ) _
      (hF.mul ((hgs.ω_cont.comp continuous_fst).mul (hgs.ω_cont.comp continuous_snd)))
  have h_T_re : ∀ i j,
      (⟪ψ i j, T_raw (ψ i j)⟫_ℂ).re =
        ∫ U, ∫ U', K_W U U' * ω U * ω U' *
          (starRingEnd ℂ (f_ij i j U) * f_ij i j U').re ∂μ ∂μ := by
    intro i j
    have h_ae_T := wilsonIntegralOp_apply_ae L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd (ψ i j)
    have hcoe := (hψ_mem i j).coeFn_toLp
    rw [MeasureTheory.L2.inner_def]
    change RCLike.re (∫ U, ⟪(ψ i j) U, (T_raw (ψ i j)) U⟫_ℂ ∂μ) = _
    rw [← integral_re (MeasureTheory.L2.integrable_inner (𝕜 := ℂ) (ψ i j) (T_raw (ψ i j)))]
    refine MeasureTheory.integral_congr_ae ?_
    filter_upwards [hcoe, h_ae_T] with U hu hT
    change (starRingEnd ℂ (⇑(ψ i j) U) * ⇑(T_raw (ψ i j)) U).re = _
    rw [hu, hT]
    dsimp [wilsonIntegralFn]
    have h_int_U' := wilsonKernel_mul_integrable L N β hβ_pos.le K_kin hK_cont hK_nn
      ((linkChiUb L β) ^ 2) hK_bd (ψ i j) U
    have h_int_swap : (fun U' => ((K_W U U' : ℝ) : ℂ) * ⇑(ψ i j) U') =ᵐ[μ]
        fun U' => ((K_W U U' : ℝ) : ℂ) * (f_ij i j U' * (ω U' : ℂ)) := by
      filter_upwards [hcoe] with U' hu'
      rw [hu']
    have h_int_U'' : MeasureTheory.Integrable
        (fun U' => ((K_W U U' : ℝ) : ℂ) * (f_ij i j U' * (ω U' : ℂ))) μ :=
      h_int_U'.congr h_int_swap
    rw [MeasureTheory.integral_congr_ae h_int_swap, ← MeasureTheory.integral_const_mul,
      ← integral_re (h_int_U''.const_mul _)]
    refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U' => ?_)
    change (starRingEnd ℂ (f_ij i j U * (ω U : ℂ)) *
        (((K_W U U' : ℝ) : ℂ) * (f_ij i j U' * (ω U' : ℂ)))).re = _
    have h_eq_c : starRingEnd ℂ (f_ij i j U * (ω U : ℂ)) *
          (((K_W U U' : ℝ) : ℂ) * (f_ij i j U' * (ω U' : ℂ))) =
        ((K_W U U' * ω U * ω U' : ℝ) : ℂ) * (starRingEnd ℂ (f_ij i j U) * f_ij i j U') := by
      simp only [map_mul, Complex.conj_ofReal, Complex.ofReal_mul]
      ring
    rw [h_eq_c, Complex.re_ofReal_mul]
  have h_dirichlet :
      ∑ i : Fin N, ∑ j : Fin N, (‖ψ i j‖ ^ 2 - (⟪ψ i j, S.T (ψ i j)⟫_ℂ).re) =
        (1 / (2 * lam0)) *
          ∫ U, ∫ U', K_W U U' * ω U * ω U' *
            frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
              (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ∂μ ∂μ := by
    have h_term : ∀ i j,
        2 * (lam0 * ‖ψ i j‖ ^ 2 - (⟪ψ i j, T_raw (ψ i j)⟫_ℂ).re) =
          ∫ U, ∫ U', K_W U U' * ω U * ω U' * ‖f_ij i j U - f_ij i j U'‖ ^ 2 ∂μ ∂μ := by
      intro i j
      let G1 : G_L → G_L → ℝ := fun U U' =>
        K_W U U' * ω U * ω U' * ‖f_ij i j U‖ ^ 2
      let G2 : G_L → G_L → ℝ := fun U U' =>
        K_W U U' * ω U * ω U' * ‖f_ij i j U'‖ ^ 2
      let G12 : G_L → G_L → ℝ := fun U U' =>
        K_W U U' * ω U * ω U' * (starRingEnd ℂ (f_ij i j U) * f_ij i j U').re
      have hG1_int : MeasureTheory.Integrable (Function.uncurry G1) (μ.prod μ) := by
        have h_eq : Function.uncurry G1 =
            fun p : G_L × G_L => (K_W p.1 p.2 * ‖f_ij i j p.1‖ ^ 2) * (ω p.1 * ω p.2) := by
          funext p; dsimp [G1]; ring
        rw [h_eq]
        exact h_prod_int _ (hKW_cont.mul (((hf_cont i j).comp continuous_fst).norm.pow 2))
      have hG2_int : MeasureTheory.Integrable (Function.uncurry G2) (μ.prod μ) := by
        have h_eq : Function.uncurry G2 =
            fun p : G_L × G_L => (K_W p.1 p.2 * ‖f_ij i j p.2‖ ^ 2) * (ω p.1 * ω p.2) := by
          funext p; dsimp [G2]; ring
        rw [h_eq]
        exact h_prod_int _ (hKW_cont.mul (((hf_cont i j).comp continuous_snd).norm.pow 2))
      have hG12_int : MeasureTheory.Integrable (Function.uncurry G12) (μ.prod μ) := by
        have h_re_cont : Continuous (fun p : G_L × G_L =>
            (starRingEnd ℂ (f_ij i j p.1) * f_ij i j p.2).re) :=
          Complex.continuous_re.comp
            ((Complex.continuous_conj.comp ((hf_cont i j).comp continuous_fst)).mul
              ((hf_cont i j).comp continuous_snd))
        have h_eq : Function.uncurry G12 =
            fun p : G_L × G_L =>
              (K_W p.1 p.2 * (starRingEnd ℂ (f_ij i j p.1) * f_ij i j p.2).re) *
                (ω p.1 * ω p.2) := by
          funext p; dsimp [G12]; ring
        rw [h_eq]
        exact h_prod_int _ (hKW_cont.mul h_re_cont)
      have h_int1 : ∫ U, ∫ U', G1 U U' ∂μ ∂μ = lam0 * ‖ψ i j‖ ^ 2 := by
        have h_in : ∀ U, ∫ U', G1 U U' ∂μ = lam0 * (‖f_ij i j U‖ ^ 2 * ω U ^ 2) := by
          intro U
          have h_eq : (fun U' => G1 U U') =
              fun U' => (K_W U U' * ω U') * (ω U * ‖f_ij i j U‖ ^ 2) := by
            funext U'; dsimp [G1]; ring
          rw [h_eq, MeasureTheory.integral_mul_const, hω_int U]
          ring
        simp_rw [h_in]
        rw [MeasureTheory.integral_const_mul, hψ_norm_sq i j]
      have h_int2 : ∫ U, ∫ U', G2 U U' ∂μ ∂μ = lam0 * ‖ψ i j‖ ^ 2 := by
        rw [MeasureTheory.integral_integral_swap hG2_int]
        have h_swap : (fun U' => ∫ U, G2 U U' ∂μ) = fun U' => ∫ U, G1 U' U ∂μ := by
          funext U'
          congr 1; funext U
          dsimp [G1, G2]
          rw [hKW_symm U U']
          ring
        rw [h_swap]
        exact h_int1
      have h_sub_inner : ∀ U,
          (∫ U', G1 U U' ∂μ) + (∫ U', G2 U U' ∂μ) - 2 * (∫ U', G12 U U' ∂μ) =
            ∫ U', K_W U U' * ω U * ω U' * ‖f_ij i j U - f_ij i j U'‖ ^ 2 ∂μ := by
        intro U
        have hi1 : MeasureTheory.Integrable (G1 U) μ :=
          integrable_of_continuous_compact μ _
            (((hKW_cont.comp (continuous_const.prodMk continuous_id)).mul
              continuous_const).mul (hgs.ω_cont.mul continuous_const))
        have hi2 : MeasureTheory.Integrable (G2 U) μ :=
          integrable_of_continuous_compact μ _
            ((((hKW_cont.comp (continuous_const.prodMk continuous_id)).mul
              (continuous_const.mul hgs.ω_cont))).mul
              ((hf_cont i j).norm.pow 2))
        have hi12 : MeasureTheory.Integrable (G12 U) μ :=
          integrable_of_continuous_compact μ _
            ((((hKW_cont.comp (continuous_const.prodMk continuous_id)).mul
              (continuous_const.mul hgs.ω_cont))).mul
              (Complex.continuous_re.comp (continuous_const.mul (hf_cont i j))))
        rw [← MeasureTheory.integral_add hi1 hi2, ← MeasureTheory.integral_const_mul 2,
          ← MeasureTheory.integral_sub (hi1.add hi2) (hi12.const_mul 2)]
        congr 1; funext U'
        have h_c_sq : ‖f_ij i j U‖ ^ 2 + ‖f_ij i j U'‖ ^ 2 -
            2 * (starRingEnd ℂ (f_ij i j U) * f_ij i j U').re =
            ‖f_ij i j U - f_ij i j U'‖ ^ 2 := by
          rw [← Complex.normSq_eq_norm_sq, ← Complex.normSq_eq_norm_sq,
            ← Complex.normSq_eq_norm_sq, Complex.normSq_apply, Complex.normSq_apply,
            Complex.normSq_apply]
          simp only [Complex.sub_re, Complex.sub_im, Complex.mul_re, Complex.conj_re,
            Complex.conj_im]
          ring
        rw [← h_c_sq]
        dsimp [G1, G2, G12]
        ring
      have h_lin :
          2 * (lam0 * ‖ψ i j‖ ^ 2 - (⟪ψ i j, T_raw (ψ i j)⟫_ℂ).re) =
            (∫ U, ∫ U', G1 U U' ∂μ ∂μ) + (∫ U, ∫ U', G2 U U' ∂μ ∂μ) -
              2 * (∫ U, ∫ U', G12 U U' ∂μ ∂μ) := by
        rw [h_int1, h_int2, h_T_re i j]; ring
      rw [h_lin]
      have ho1 := hG1_int.integral_prod_left
      have ho2 := hG2_int.integral_prod_left
      have ho12 := hG12_int.integral_prod_left
      rw [← MeasureTheory.integral_add ho1 ho2, ← MeasureTheory.integral_const_mul 2,
        ← MeasureTheory.integral_sub (ho1.add ho2) (ho12.const_mul 2)]
      congr 1; funext U
      exact h_sub_inner U
    have h_each : ∀ i j,
        ‖ψ i j‖ ^ 2 - (⟪ψ i j, S.T (ψ i j)⟫_ℂ).re =
          (1 / (2 * lam0)) *
            ∫ U, ∫ U', K_W U U' * ω U * ω U' * ‖f_ij i j U - f_ij i j U'‖ ^ 2 ∂μ ∂μ := by
      intro i j
      have hST_re : (⟪ψ i j, S.T (ψ i j)⟫_ℂ).re =
          lam0⁻¹ * (⟪ψ i j, T_raw (ψ i j)⟫_ℂ).re := by
        rw [hS_T, ContinuousLinearMap.smul_apply, inner_smul_right, Complex.re_ofReal_mul]
      rw [hST_re, ← h_term i j]
      field_simp [hlam0_pos.ne']
    simp_rw [h_each, ← Finset.mul_sum]
    congr 1
    let D_ij : Fin N → Fin N → G_L → G_L → ℝ := fun i j U U' =>
      K_W U U' * ω U * ω U' * ‖f_ij i j U - f_ij i j U'‖ ^ 2
    have hD_prod_int : ∀ i j : Fin N,
        MeasureTheory.Integrable (Function.uncurry (D_ij i j)) (μ.prod μ) := by
      intro i j
      have h_eq : Function.uncurry (D_ij i j) =
          fun p : G_L × G_L =>
            (K_W p.1 p.2 * ‖f_ij i j p.1 - f_ij i j p.2‖ ^ 2) * (ω p.1 * ω p.2) := by
        funext p; dsimp [D_ij]; ring
      rw [h_eq]
      exact h_prod_int _ (hKW_cont.mul ((((hf_cont i j).comp continuous_fst).sub
        ((hf_cont i j).comp continuous_snd)).norm.pow 2))
    have hD_inner_int : ∀ (U : G_L) (i j : Fin N),
        MeasureTheory.Integrable (D_ij i j U) μ := fun U i j =>
      integrable_of_continuous_compact μ _
        ((((hKW_cont.comp (continuous_const.prodMk continuous_id)).mul
          (continuous_const.mul hgs.ω_cont))).mul
          ((continuous_const.sub (hf_cont i j)).norm.pow 2))
    have h_sum_inner : ∀ (U : G_L) (i : Fin N),
        (∑ j : Fin N, ∫ U', D_ij i j U U' ∂μ) = ∫ U', ∑ j : Fin N, D_ij i j U U' ∂μ :=
      fun U i => integral_finset_sum_aux Finset.univ _ fun j _ => hD_inner_int U i j
    have h_sum_outer_j : ∀ i : Fin N,
        (∑ j : Fin N, ∫ U, ∫ U', D_ij i j U U' ∂μ ∂μ) =
          ∫ U, ∑ j : Fin N, ∫ U', D_ij i j U U' ∂μ ∂μ := fun i =>
      integral_finset_sum_aux Finset.univ _ fun j _ => (hD_prod_int i j).integral_prod_left
    simp_rw [h_sum_outer_j, h_sum_inner]
    rw [integral_finset_sum_aux Finset.univ _ fun i _ =>
      integrable_finset_sum_aux Finset.univ _ fun j _ => (hD_prod_int i j).integral_prod_left]
    congr 1; funext U
    rw [integral_finset_sum_aux Finset.univ _ fun i _ =>
      integrable_finset_sum_aux Finset.univ _ fun j _ => hD_inner_int U i j]
    congr 1; funext U'
    dsimp [D_ij]
    simp_rw [← Finset.sum_mul]
    congr 1
    unfold frobeniusNormSq
    rfl
  -- Step 3: ε / δ split and lower bound on lam0
  have hcard_links : Fintype.card (cubicTorus3 L).Link = links := by
    dsimp [cubicTorus3, links]
    simp [Fintype.card_prod, Fintype.card_fin]
    ring
  have hχ_eq_frob : ∀ U W,
      χ U W = Real.exp ((β / 2) * (links : ℝ) -
        (β / (4 * (N : ℝ))) * ∑ e : (cubicTorus3 L).Link,
          frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
            (W e : Matrix (Fin N) (Fin N) ℂ))) := by
    intro U W
    dsimp [χ, cubicLinkKineticKernel]
    rw [← Real.exp_sum]
    congr 1
    have h_each : ∀ e : (cubicTorus3 L).Link,
        (β / (2 * (N : ℝ))) *
          (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re =
          β / 2 - (β / (4 * (N : ℝ))) *
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
              (W e : Matrix (Fin N) (Fin N) ℂ)) := by
      intro e
      have hfrob := frobeniusNormSq_su_sub_one_eq (U e * (W e)⁻¹)
      rw [frobeniusNormSq_sub_self_su (U e) (W e)] at hfrob
      have htr : (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re =
          (N : ℝ) - frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
            (W e : Matrix (Fin N) (Fin N) ℂ)) / 2 := by
        linarith
      rw [htr]
      field_simp [hN_pos.ne']
      ring
    simp_rw [h_each, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
      hcard_links, nsmul_eq_mul, ← Finset.mul_sum]
    ring
  -- Ball B_δ around the identity and lower bound on lam0
  let δ : ℝ := 1 / Real.sqrt β
  have hδ_pos : 0 < δ := by positivity
  let B_link : Set (Matrix.specialUnitaryGroup (Fin N) ℂ) :=
    { A | frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 }
  let B : Set G_L := Set.pi Set.univ (fun _ => B_link)
  have hB_link_cont : Continuous (fun A : Matrix.specialUnitaryGroup (Fin N) ℂ =>
      frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1)) := by
    unfold frobeniusNormSq
    refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
    simp only [Matrix.sub_apply]
    exact (continuous_norm.comp (((continuous_apply j).comp
      ((continuous_apply i).comp continuous_subtype_val)).sub continuous_const)).pow 2
  have hB_meas : MeasurableSet B := by
    have h_eq : B = ⋂ e : (cubicTorus3 L).Link,
        { U : G_L | frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 } := by
      ext U; simp [B, B_link]
    rw [h_eq]
    exact MeasurableSet.iInter fun e =>
      measurableSet_Iic.preimage (hB_link_cont.measurable.comp (measurable_pi_apply e))
  have hμB_eq : μ.real B = ((suHaar N B_link).toReal) ^ links := by
    change (μ B).toReal = _
    dsimp [μ, B]
    erw [MeasureTheory.Measure.pi_pi (fun _ => suHaar N) _]
    simp [Finset.prod_const, Finset.card_univ, hcard_links, ENNReal.toReal_pow]
  have hμB_lb : ((1 : ℝ) / (K : ℝ) ^ (2 * N * N)) ^ links ≤ μ.real B := by
    rw [hμB_eq]
    have hball := suHaar_ball_ge N hδ_pos
    exact pow_le_pow_left₀ (by positivity) hball links
  have hK_pos : (0 : ℝ) < (K : ℝ) := by dsimp [K]; positivity
  have hμB_pos : 0 < μ.real B :=
    lt_of_lt_of_le (pow_pos (by positivity) links) hμB_lb
  have hS_W_ball : ∀ U ∈ B, wilsonAction β (cubicPlaquettes L) U ≤ 24 * (L : ℝ) ^ 3 / (N : ℝ) := by
    intro U hU
    have hU' : ∀ e, frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 := fun e =>
      hU e (Set.mem_univ e)
    have h_plaq_le : ∀ p ∈ cubicPlaquettes L, wilsonPlaquetteTerm p U ≤ 8 / ((N : ℝ) * β) := by
      intro p hp
      rw [wilsonPlaquetteTerm_eq_frobenius]
      unfold cubicPlaquettes at hp
      simp only [List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and,
        List.mem_cons, List.not_mem_nil, or_false] at hp
      have hf16 : frobeniusNormSq ((pathHolonomy U p.loop : Matrix (Fin N) (Fin N) ℂ) - 1) ≤
          16 * δ ^ 2 := by
        rcases hp with ⟨x, rfl | rfl | rfl⟩ <;>
          exact frobeniusNormSq_path4_le U hU' _ _ _ _
      have hδ2 : δ ^ 2 = 1 / β := by
        dsimp [δ]; rw [div_pow, one_pow, Real.sq_sqrt hβ_pos.le]
      rw [hδ2] at hf16
      calc frobeniusNormSq ((pathHolonomy U p.loop : Matrix (Fin N) (Fin N) ℂ) - 1) /
            (2 * (N : ℝ))
          ≤ (16 * (1 / β)) / (2 * (N : ℝ)) :=
            div_le_div_of_nonneg_right hf16 (by positivity)
        _ = 8 / ((N : ℝ) * β) := by
            field_simp [hN_pos.ne', hβ_pos.ne']; ring
    unfold wilsonAction
    have hsum_le : ((cubicPlaquettes L).map (fun p => wilsonPlaquetteTerm p U)).sum ≤
        ((cubicPlaquettes L).length : ℝ) * (8 / ((N : ℝ) * β)) := by
      have h_gen : ∀ (ps : List (LatticePlaquette (cubicTorus3 L))),
          (∀ p ∈ ps, wilsonPlaquetteTerm p U ≤ 8 / ((N : ℝ) * β)) →
          (ps.map (fun p => wilsonPlaquetteTerm p U)).sum ≤
            (ps.length : ℝ) * (8 / ((N : ℝ) * β)) := by
        intro ps hps
        induction ps with
        | nil => simp
        | cons p ps ih =>
          simp only [List.map_cons, List.sum_cons, List.length_cons, Nat.cast_add, Nat.cast_one]
          have hp0 := hps p (by simp)
          have ih0 := ih (fun q hq => hps q (by simp [hq]))
          linarith
      exact h_gen _ h_plaq_le
    rw [cubicPlaquettes_length L] at hsum_le
    calc β * ((cubicPlaquettes L).map (fun p => wilsonPlaquetteTerm p U)).sum
        ≤ β * (((3 * L ^ 3 : ℕ) : ℝ) * (8 / ((N : ℝ) * β))) :=
          mul_le_mul_of_nonneg_left hsum_le hβ_pos.le
      _ = 24 * (L : ℝ) ^ 3 / (N : ℝ) := by
          push_cast; field_simp [hN_pos.ne', hβ_pos.ne']; ring
  have hχ_ball : ∀ U ∈ B, ∀ W ∈ B,
      Real.exp ((β / 2) * (links : ℝ) - 3 * (L : ℝ) ^ 3 / (N : ℝ)) ≤ χ U W := by
    intro U hU W hW
    rw [hχ_eq_frob U W]
    apply Real.exp_le_exp.mpr
    have h_each : ∀ e : (cubicTorus3 L).Link,
        frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
          (W e : Matrix (Fin N) (Fin N) ℂ)) ≤ 4 / β := by
      intro e
      have hU_e : frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 1 / β := by
        simpa [δ, div_pow, one_pow, Real.sq_sqrt hβ_pos.le] using hU e (Set.mem_univ e)
      have hW_e : frobeniusNormSq (1 - (W e : Matrix (Fin N) (Fin N) ℂ)) ≤ 1 / β := by
        have hW' : frobeniusNormSq ((W e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 1 / β := by
          simpa [δ, div_pow, one_pow, Real.sq_sqrt hβ_pos.le] using hW e (Set.mem_univ e)
        rwa [show 1 - (W e : Matrix (Fin N) (Fin N) ℂ) =
            -((W e : Matrix (Fin N) (Fin N) ℂ) - 1) by abel, frobeniusNormSq_neg]
      have hadd := frobeniusNormSq_add_le
        ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) (1 - (W e : Matrix (Fin N) (Fin N) ℂ))
      rw [show ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) +
          (1 - (W e : Matrix (Fin N) (Fin N) ℂ)) =
          (U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ) by abel] at hadd
      linarith
    have h_sum : ∑ e : (cubicTorus3 L).Link,
        frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
          (W e : Matrix (Fin N) (Fin N) ℂ)) ≤ (links : ℝ) * (4 / β) := by
      calc ∑ e : (cubicTorus3 L).Link, _
          ≤ ∑ _e : (cubicTorus3 L).Link, (4 / β) :=
            Finset.sum_le_sum fun e _ => h_each e
        _ = (links : ℝ) * (4 / β) := by
            simp [Finset.sum_const, Finset.card_univ, hcard_links]
    have h_mul := mul_le_mul_of_nonneg_left h_sum (by positivity : 0 ≤ β / (4 * (N : ℝ)))
    have h_simp : (β / (4 * (N : ℝ))) * ((links : ℝ) * (4 / β)) =
        3 * (L : ℝ) ^ 3 / (N : ℝ) := by
      dsimp [links]; push_cast; field_simp [hN_pos.ne', hβ_pos.ne']; ring
    linarith
  have hKW_ball : ∀ U ∈ B, ∀ U' ∈ B,
      μ.real B * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) ≤ K_W U U' := by
    intro U hU U' hU'
    dsimp [K_W, wilsonKernel, K_kin, wilsonGramKernel]
    have hS1 := hS_W_ball U hU
    have hS2 := hS_W_ball U' hU'
    have h_act : Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) ≤
        Real.exp (-(1 / 2 : ℝ) * (wilsonAction β (cubicPlaquettes L) U +
          wilsonAction β (cubicPlaquettes L) U')) := by
      apply Real.exp_le_exp.mpr
      linarith
    have h_int_χ : MeasureTheory.Integrable (fun W => χ U W * χ U' W) μ :=
      integrable_of_continuous_compact μ _
        ((hχ_cont.comp (continuous_const.prodMk continuous_id)).mul
          (hχ_cont.comp (continuous_const.prodMk continuous_id)))
    let c₀ : ℝ := Real.exp ((β / 2) * (links : ℝ) - 3 * (L : ℝ) ^ 3 / (N : ℝ))
    have h_ind_int : MeasureTheory.Integrable (Set.indicator B (fun _ => c₀ ^ 2)) μ :=
      (MeasureTheory.integrable_const (c₀ ^ 2)).indicator hB_meas
    have h_ind_le : ∀ W, Set.indicator B (fun _ => c₀ ^ 2) W ≤ χ U W * χ U' W := by
      intro W
      by_cases hW : W ∈ B
      · rw [Set.indicator_of_mem hW, sq]
        exact mul_le_mul (hχ_ball U hU W hW) (hχ_ball U' hU' W hW)
          (Real.exp_pos _).le (hχ_nn U W)
      · rw [Set.indicator_of_notMem hW]
        exact mul_nonneg (hχ_nn U W) (hχ_nn U' W)
    have hK_kin_lb : μ.real B * c₀ ^ 2 ≤ ∫ W, χ U W * χ U' W ∂μ := by
      calc μ.real B * c₀ ^ 2
          = ∫ W, Set.indicator B (fun _ => c₀ ^ 2) W ∂μ := by
              rw [MeasureTheory.integral_indicator hB_meas, MeasureTheory.setIntegral_const,
                smul_eq_mul]
        _ ≤ ∫ W, χ U W * χ U' W ∂μ :=
            MeasureTheory.integral_mono h_ind_int h_int_χ h_ind_le
    have h_exp_prod : Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) * c₀ ^ 2 =
        Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) := by
      dsimp [c₀]
      rw [← Real.exp_nat_mul, ← Real.exp_add]
      congr 1
      push_cast
      ring
    calc μ.real B * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ))
        = Real.exp (-(24 * (L : ℝ) ^ 3 / (N : ℝ))) * (μ.real B * c₀ ^ 2) := by
            rw [← h_exp_prod]; ring
      _ ≤ Real.exp (-(1 / 2 : ℝ) * (wilsonAction β (cubicPlaquettes L) U +
            wilsonAction β (cubicPlaquettes L) U')) * ∫ W, χ U W * χ U' W ∂μ :=
          mul_le_mul h_act hK_kin_lb (by positivity) (Real.exp_pos _).le
  have hlam0_lb :
      (μ.real B) ^ 2 * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) ≤ lam0 := by
    let val : ℝ := 1 / Real.sqrt (μ.real B)
    have hφ_mem : MeasureTheory.MemLp (Set.indicator B (fun _ => (val : ℂ))) 2 μ := by
      refine memLp_two_of_measurable_bound μ _
        (measurable_const.indicator hB_meas) (|val|) (abs_nonneg _) fun U => ?_
      by_cases hU : U ∈ B
      · simp [Set.indicator_of_mem hU]
      · simp [Set.indicator_of_notMem hU]
    let φ : HaarGaugeSpace μ := hφ_mem.toLp (Set.indicator B (fun _ => (val : ℂ)))
    have hφ_norm : ‖φ‖ = 1 := by
      have hsq : ‖φ‖ ^ 2 = 1 := by
        have h1 : ‖φ‖ ^ 2 = (⟪φ, φ⟫_ℂ).re := by
          rw [inner_self_eq_norm_sq_to_K, ← Complex.ofReal_pow, Complex.ofReal_re]
        rw [h1, MeasureTheory.L2.inner_def]
        change RCLike.re (∫ U, ⟪φ U, φ U⟫_ℂ ∂μ) = 1
        rw [← integral_re (MeasureTheory.L2.integrable_inner (𝕜 := ℂ) φ φ)]
        have h_ae : (fun U => (⟪φ U, φ U⟫_ℂ).re) =ᵐ[μ]
            Set.indicator B (fun _ => val ^ 2) := by
          filter_upwards [hφ_mem.coeFn_toLp] with U hu
          change (starRingEnd ℂ (⇑φ U) * ⇑φ U).re = _
          rw [hu]
          by_cases hU : U ∈ B
          · simp [Set.indicator_of_mem hU, Complex.mul_conj, Complex.ofReal_re,
              Complex.normSq_eq_norm_sq]
          · simp [Set.indicator_of_notMem hU]
        rw [MeasureTheory.integral_congr_ae h_ae, MeasureTheory.integral_indicator hB_meas,
          MeasureTheory.setIntegral_const, smul_eq_mul]
        dsimp [val]
        rw [div_pow, one_pow, Real.sq_sqrt hμB_pos.le]
        field_simp [hμB_pos.ne']
      nlinarith [norm_nonneg φ]
    have h_le_norm : (⟪φ, T_raw φ⟫_ℂ).re ≤ lam0 := by
      calc (⟪φ, T_raw φ⟫_ℂ).re ≤ ‖⟪φ, T_raw φ⟫_ℂ‖ :=
            (le_abs_self _).trans (Complex.abs_re_le_norm _)
        _ ≤ ‖φ‖ * ‖T_raw φ‖ := norm_inner_le_norm _ _
        _ ≤ ‖φ‖ * (lam0 * ‖φ‖) :=
            mul_le_mul_of_nonneg_left (T_raw.le_opNorm φ) (norm_nonneg _)
        _ = lam0 := by rw [hφ_norm, mul_one, mul_one]
    have h_inner_eq : (⟪φ, T_raw φ⟫_ℂ).re =
        val ^ 2 * ∫ U, Set.indicator B (fun U =>
          ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ) U ∂μ := by
      have h_ae_T := wilsonIntegralOp_apply_ae L N β hβ_pos.le K_kin hK_cont hK_nn
        ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd φ
      have hcoe := hφ_mem.coeFn_toLp
      rw [MeasureTheory.L2.inner_def]
      change RCLike.re (∫ U, ⟪φ U, (T_raw φ) U⟫_ℂ ∂μ) = _
      rw [← integral_re (MeasureTheory.L2.integrable_inner (𝕜 := ℂ) φ (T_raw φ))]
      have h_outer : (fun U => (⟪φ U, (T_raw φ) U⟫_ℂ).re) =ᵐ[μ]
          fun U => val ^ 2 * Set.indicator B (fun U =>
            ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ) U := by
        filter_upwards [hcoe, h_ae_T] with U hu hT
        change (starRingEnd ℂ (⇑φ U) * ⇑(T_raw φ) U).re = _
        rw [hu, hT]
        by_cases hU : U ∈ B
        · rw [Set.indicator_of_mem hU, Set.indicator_of_mem hU]
          dsimp [wilsonIntegralFn]
          have h_ae_in : (fun U' => ((K_W U U' : ℝ) : ℂ) * ⇑φ U') =ᵐ[μ]
              fun U' => ((Set.indicator B (fun U' => val * K_W U U') U' : ℝ) : ℂ) := by
            filter_upwards [hcoe] with U' hu'
            rw [hu']
            by_cases hU' : U' ∈ B
            · simp [Set.indicator_of_mem hU']; ring
            · simp [Set.indicator_of_notMem hU']
          have h_ind_kw : MeasureTheory.Integrable
              (Set.indicator B (fun U' => val * K_W U U')) μ :=
            ((integrable_of_continuous_compact μ _
              (hKW_cont.comp (continuous_const.prodMk continuous_id))).const_mul val).indicator
              hB_meas
          rw [MeasureTheory.integral_congr_ae h_ae_in, integral_ofReal_eq _ h_ind_kw]
          simp only [Complex.conj_ofReal, Complex.re_ofReal_mul]
          have h_ind_eq : (fun U' => Set.indicator B (fun U' => val * K_W U U') U') =
              fun U' => val * Set.indicator B (fun U' => K_W U U') U' := by
            funext U'
            by_cases hU' : U' ∈ B <;> simp [hU']
          rw [h_ind_eq, MeasureTheory.integral_const_mul]
          ring
        · simp [Set.indicator_of_notMem hU]
      rw [MeasureTheory.integral_congr_ae h_outer, MeasureTheory.integral_const_mul]
    have h_dbl_lb :
        (μ.real B) ^ 2 * (μ.real B * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ))) ≤
          ∫ U, Set.indicator B (fun U =>
            ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ) U ∂μ := by
      let c₁ : ℝ := μ.real B * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ))
      have h_in_lb : ∀ U ∈ B, μ.real B * c₁ ≤
          ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ := by
        intro U hU
        have h_int_k : MeasureTheory.Integrable (Set.indicator B (fun U' => K_W U U')) μ :=
          (integrable_of_continuous_compact μ _
            (hKW_cont.comp (continuous_const.prodMk continuous_id))).indicator hB_meas
        have h_int_c : MeasureTheory.Integrable (Set.indicator B (fun _ => c₁)) μ :=
          (MeasureTheory.integrable_const c₁).indicator hB_meas
        calc μ.real B * c₁
            = ∫ U', Set.indicator B (fun _ => c₁) U' ∂μ := by
                rw [MeasureTheory.integral_indicator hB_meas, MeasureTheory.setIntegral_const,
                  smul_eq_mul]
          _ ≤ ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ := by
              refine MeasureTheory.integral_mono h_int_c h_int_k fun U' => ?_
              by_cases hU' : U' ∈ B
              · rw [Set.indicator_of_mem hU', Set.indicator_of_mem hU']
                exact hKW_ball U hU U' hU'
              · rw [Set.indicator_of_notMem hU', Set.indicator_of_notMem hU']
      have h_out_int_c : MeasureTheory.Integrable (Set.indicator B (fun _ => μ.real B * c₁)) μ :=
        (MeasureTheory.integrable_const _).indicator hB_meas
      have h_cont_fn : Continuous (fun U => ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ) := by
        refine MeasureTheory.continuous_of_dominated ?_ ?_
          (MeasureTheory.integrable_const ((linkChiUb L β) ^ 2)) ?_
        · intro U
          exact ((integrable_of_continuous_compact μ _
            (hKW_cont.comp (continuous_const.prodMk continuous_id))).indicator
              hB_meas).aestronglyMeasurable
        · intro U
          refine Filter.Eventually.of_forall fun U' => ?_
          by_cases hU' : U' ∈ B
          · rw [Set.indicator_of_mem hU', Real.norm_of_nonneg (hKW_bounds U U').1]
            exact (hKW_bounds U U').2
          · rw [Set.indicator_of_notMem hU', norm_zero]; positivity
        · refine Filter.Eventually.of_forall fun U' => ?_
          by_cases hU' : U' ∈ B
          · simp only [Set.indicator_of_mem hU']
            exact hKW_cont.comp (continuous_id.prodMk continuous_const)
          · simp only [Set.indicator_of_notMem hU']; exact continuous_const
      have h_out_int_k : MeasureTheory.Integrable (Set.indicator B (fun U =>
          ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ)) μ :=
        (integrable_of_continuous_compact μ _ h_cont_fn).indicator hB_meas
      calc (μ.real B) ^ 2 * c₁
          = μ.real B * (μ.real B * c₁) := by ring
        _ = ∫ U, Set.indicator B (fun _ => μ.real B * c₁) U ∂μ := by
            rw [MeasureTheory.integral_indicator hB_meas, MeasureTheory.setIntegral_const,
              smul_eq_mul]
        _ ≤ ∫ U, Set.indicator B (fun U =>
              ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ) U ∂μ := by
            refine MeasureTheory.integral_mono h_out_int_c h_out_int_k fun U => ?_
            by_cases hU : U ∈ B
            · rw [Set.indicator_of_mem hU, Set.indicator_of_mem hU]
              exact h_in_lb U hU
            · rw [Set.indicator_of_notMem hU, Set.indicator_of_notMem hU]
    have h_val_sq : val ^ 2 = (μ.real B)⁻¹ := by
      dsimp [val]; rw [div_pow, one_pow, Real.sq_sqrt hμB_pos.le, one_div]
    calc (μ.real B) ^ 2 * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ))
        = (μ.real B)⁻¹ * ((μ.real B) ^ 2 *
            (μ.real B * Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)))) := by
          field_simp [hμB_pos.ne']
      _ ≤ val ^ 2 * ∫ U, Set.indicator B (fun U =>
            ∫ U', Set.indicator B (fun U' => K_W U U') U' ∂μ) U ∂μ := by
          rw [h_val_sq]
          exact mul_le_mul_of_nonneg_left h_dbl_lb (inv_nonneg.mpr hμB_pos.le)
      _ = (⟪φ, T_raw φ⟫_ℂ).re := h_inner_eq.symm
      _ ≤ lam0 := h_le_norm
  have hlam0_inv_ub :
      lam0⁻¹ ≤ ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
        Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ) - β * (links : ℝ)) := by
    have h_lb1 : ((1 : ℝ) / ((K : ℝ) ^ (2 * N * N))) ^ (2 * links) *
        Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) ≤ lam0 := by
      have h_pow : ((1 : ℝ) / ((K : ℝ) ^ (2 * N * N))) ^ (2 * links) ≤ (μ.real B) ^ 2 := by
        rw [mul_comm 2 links, pow_mul]
        exact pow_le_pow_left₀ (by positivity) hμB_lb 2
      exact (mul_le_mul_of_nonneg_right h_pow (Real.exp_pos _).le).trans hlam0_lb
    have h_pos_lb : 0 < ((1 : ℝ) / ((K : ℝ) ^ (2 * N * N))) ^ (2 * links) *
        Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)) := by positivity
    calc lam0⁻¹
        ≤ (((1 : ℝ) / ((K : ℝ) ^ (2 * N * N))) ^ (2 * links) *
            Real.exp (β * (links : ℝ) - 30 * (L : ℝ) ^ 3 / (N : ℝ)))⁻¹ :=
          inv_anti₀ h_pos_lb h_lb1
      _ = ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
          Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ) - β * (links : ℝ)) := by
          rw [mul_inv, ← Real.exp_neg, one_div, inv_pow, inv_inv, neg_sub]
  -- Split the Dirichlet integral at jump threshold `2 * ε_sq`
  let jump : G_L → G_L → ℝ := fun U U' =>
    ∑ e : (cubicTorus3 L).Link,
      frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
        (U' e : Matrix (Fin N) (Fin N) ℂ))
  have h_KW_jump : ∀ U U',
      K_W U U' ≤ Real.exp (β * (links : ℝ) - (β / (8 * (N : ℝ))) * jump U U') := by
    intro U U'
    have hS_nn : 0 ≤ wilsonAction β (cubicPlaquettes L) U +
        wilsonAction β (cubicPlaquettes L) U' := by
      have h_act_nn : ∀ X, 0 ≤ wilsonAction β (cubicPlaquettes L) X := by
        intro X
        unfold wilsonAction
        refine mul_nonneg hβ_pos.le ?_
        have h_list : ∀ ps : List (LatticePlaquette (cubicTorus3 L)),
            0 ≤ (ps.map (fun p => wilsonPlaquetteTerm p X)).sum := by
          intro ps
          induction ps with
          | nil => simp
          | cons p ps ih =>
            simp only [List.map_cons, List.sum_cons]
            exact add_nonneg (wilsonPlaquetteTerm_nonneg p X) ih
        exact h_list _
      exact add_nonneg (h_act_nn U) (h_act_nn U')
    have h_act_le : Real.exp (-(1 / 2 : ℝ) * (wilsonAction β (cubicPlaquettes L) U +
        wilsonAction β (cubicPlaquettes L) U')) ≤ 1 := by
      rw [Real.exp_le_one_iff]; linarith
    have hχ_prod : ∀ W, χ U W * χ U' W ≤
        Real.exp (β * (links : ℝ) - (β / (8 * (N : ℝ))) * jump U U') := by
      intro W
      rw [hχ_eq_frob U W, hχ_eq_frob U' W, ← Real.exp_add]
      apply Real.exp_le_exp.mpr
      have h_tri : jump U U' ≤
          2 * (∑ e : (cubicTorus3 L).Link,
            frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) -
              (W e : Matrix (Fin N) (Fin N) ℂ))) +
          2 * (∑ e : (cubicTorus3 L).Link,
            frobeniusNormSq ((U' e : Matrix (Fin N) (Fin N) ℂ