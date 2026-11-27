#!/usr/bin/env python3
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
src = path.read_text(encoding="utf-8")

anchor = "/-- **Explicit Spectral-Gap Upper Bound & Convergence to `0` (`0 sorry`):**"
assert src.count(anchor) == 1

helpers = """private lemma frobeniusNormSq_su_eq {N : ℕ}
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq (A : Matrix (Fin N) (Fin N) ℂ) = (N : ℝ) := by
  rw [frobeniusNormSq_trace]
  have hA : (A : Matrix (Fin N) (Fin N) ℂ) * star (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    (Unitary.mem_iff.mp A.2.1).2
  rw [hA]
  simp [Matrix.trace]

private lemma frobeniusNormSq_sub_rev {N : ℕ} (M₁ M₂ : Matrix (Fin N) (Fin N) ℂ) :
    frobeniusNormSq (M₁ - M₂) = frobeniusNormSq (M₂ - M₁) := by
  unfold frobeniusNormSq
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  rw [Matrix.sub_apply, Matrix.sub_apply, norm_sub_rev]

private lemma frobeniusNormSq_su_sub_le {N : ℕ}
    (A B : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - (B : Matrix (Fin N) (Fin N) ℂ)) ≤
      4 * (N : ℝ) := by
  rw [← frobeniusNormSq_sub_self_su A B]
  have hneg : frobeniusNormSq (-((1 : Matrix (Fin N) (Fin N) ℂ))) = (N : ℝ) := by
    unfold frobeniusNormSq
    simp [Matrix.one_apply]
  have hle := frobeniusNormSq_add_le
    ((A * B⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) (-1)
  rw [← sub_eq_add_neg] at hle
  calc frobeniusNormSq (((A * B⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ) - 1)
      ≤ 2 * frobeniusNormSq ((A * B⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ) + 2 * frobeniusNormSq (-(1 : Matrix (Fin N) (Fin N) ℂ)) := hle
    _ = 2 * (N : ℝ) + 2 * (N : ℝ) := by rw [frobeniusNormSq_su_eq, hneg]
    _ = 4 * (N : ℝ) := by ring

private lemma frobeniusNormSq_plaq4_le {N : ℕ}
    (A B C D : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq (((A * (B * (C⁻¹ * (D⁻¹ * 1))) : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ) - 1) ≤
      4 * (frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) +
        frobeniusNormSq ((B : Matrix (Fin N) (Fin N) ℂ) - 1) +
        frobeniusNormSq ((C : Matrix (Fin N) (Fin N) ℂ) - 1) +
        frobeniusNormSq ((D : Matrix (Fin N) (Fin N) ℂ) - 1)) := by
  have heq : A * (B * (C⁻¹ * (D⁻¹ * 1))) = (A * B) * (C⁻¹ * D⁻¹) := by group
  rw [heq]
  have h1 := frobeniusNormSq_su_mul_sub_one (A * B) (C⁻¹ * D⁻¹)
  have h2 := frobeniusNormSq_su_mul_sub_one A B
  have h3 := frobeniusNormSq_su_mul_sub_one C⁻¹ D⁻¹
  rw [frobeniusNormSq_su_inv_sub_one, frobeniusNormSq_su_inv_sub_one] at h3
  linarith

private lemma frobeniusNormSq_su_sub_one_eq {N : ℕ}
    (A : Matrix.specialUnitaryGroup (Fin N) ℂ) :
    frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) =
      2 * ((N : ℝ) - (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re) := by
  rw [frobeniusNormSq_trace]
  have hA : (A : Matrix (Fin N) (Fin N) ℂ) * star (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    (Unitary.mem_iff.mp A.2.1).2
  have hmul : ((A : Matrix (Fin N) (Fin N) ℂ) - 1) *
      star ((A : Matrix (Fin N) (Fin N) ℂ) - 1) =
      2 • (1 : Matrix (Fin N) (Fin N) ℂ) - (A : Matrix (Fin N) (Fin N) ℂ) -
        star (A : Matrix (Fin N) (Fin N) ℂ) := by
    rw [star_sub, star_one, Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_sub,
      Matrix.one_mul, Matrix.mul_one, hA, two_smul]
    abel
  rw [hmul]
  simp only [Matrix.trace, Matrix.diag_apply, Complex.re_sum, Matrix.sub_apply,
    Matrix.smul_apply, Matrix.one_apply_eq, Matrix.star_apply, Complex.sub_re,
    Complex.smul_re, smul_eq_mul, Complex.one_re, Complex.star_def, Complex.conj_re]
  rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul]
  ring

private lemma cubicLink_card (L : ℕ) [NeZero L] :
    Fintype.card (cubicTorus3 L).Link = 3 * L ^ 3 := by
  change Fintype.card ((Fin L × Fin L × Fin L) × Fin 3) = 3 * L ^ 3
  simp [Fintype.card_prod, Fintype.card_fin]
  ring

private lemma cubicPlaquettes_length (L : ℕ) [NeZero L] :
    (cubicPlaquettes L).length = 3 * L ^ 3 := by
  unfold cubicPlaquettes
  have h_flat : ∀ (xs : List (Fin L × Fin L × Fin L))
      (g : Fin L × Fin L × Fin L → List (LatticePlaquette (cubicTorus3 L))),
      (∀ x, (g x).length = 3) → (xs.flatMap g).length = 3 * xs.length := by
    intro xs g hg
    induction xs with
    | nil => simp
    | cons x xs ih => simp [List.flatMap_cons, hg x, ih]; ring
  rw [h_flat _ _ (fun _ => rfl), Finset.length_toList, Finset.card_univ]
  simp [Fintype.card_prod, Fintype.card_fin]
  ring

private lemma wilsonPlaquetteTerm_nonneg {L : SpatialLattice} {N : ℕ} (hN : 1 ≤ N)
    (p : LatticePlaquette L)
    (U : GaugeField L (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    0 ≤ wilsonPlaquetteTerm p U := by
  unfold wilsonPlaquetteTerm
  have hN_pos : (0 : ℝ) < N := Nat.cast_pos.mpr hN
  have htr := (abs_le.mp (abs_re_trace_su_le (pathHolonomy U p.loop))).2
  have hdiv : (1 / (N : ℝ)) * (Matrix.trace ((pathHolonomy U p.loop :
      Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ)).re ≤ 1 := by
    rw [one_div, ← div_eq_inv_mul, div_le_one hN_pos]
    exact htr
  linarith

private lemma wilsonAction_nonneg_of_nonneg {L : SpatialLattice} {N : ℕ} (hN : 1 ≤ N)
    {β : ℝ} (hβ : 0 ≤ β) (plaquettes : List (LatticePlaquette L))
    (U : GaugeField L (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    0 ≤ wilsonAction β plaquettes U := by
  unfold wilsonAction
  refine mul_nonneg hβ ?_
  induction plaquettes with
  | nil => simp
  | cons p ps ih =>
    simp only [List.map_cons, List.sum_cons]
    exact add_nonneg (wilsonPlaquetteTerm_nonneg hN p U) ih

private lemma wilsonAction_ball_le (L N : ℕ) [NeZero L] (hN : 1 ≤ N)
    {β : ℝ} (hβ : 0 < β)
    (U : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ))
    (hU : ∀ e, frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 1 / β) :
    wilsonAction β (cubicPlaquettes L) U ≤ 24 * (L : ℝ) ^ 3 / (N : ℝ) := by
  have hN_pos : (0 : ℝ) < N := Nat.cast_pos.mpr hN
  have h_term : ∀ p ∈ cubicPlaquettes L, wilsonPlaquetteTerm p U ≤ 8 / ((N : ℝ) * β) := by
    intro p hp
    unfold cubicPlaquettes at hp
    simp only [List.mem_flatMap, Finset.mem_toList, Finset.mem_univ, true_and,
      List.mem_cons, List.not_mem_nil, or_false] at hp
    have h_frob : frobeniusNormSq (((pathHolonomy U p.loop :
        Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 16 / β := by
      rcases hp with ⟨x, rfl | rfl | rfl⟩ <;>
        dsimp [cubicPlaquette, pathHolonomy] <;>
        have hle := frobeniusNormSq_plaq4_le _ _ _ _ <;>
        linarith [hU (x, _), hU (cubicShift L _ x, _)]
    have h_eq : wilsonPlaquetteTerm p U =
        frobeniusNormSq (((pathHolonomy U p.loop :
          Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) - 1) /
          (2 * (N : ℝ)) := by
      unfold wilsonPlaquetteTerm
      rw [frobeniusNormSq_su_sub_one_eq]
      field_simp [hN_pos.ne']
    rw [h_eq]
    calc _ ≤ (16 / β) / (2 * (N : ℝ)) :=
          div_le_div_of_nonneg_right h_frob (by positivity)
      _ = 8 / ((N : ℝ) * β) := by field_simp [hN_pos.ne', hβ.ne']; ring
  have h_list_sum_le : ∀ (l : List (LatticePlaquette (cubicTorus3 L)))
      (f : LatticePlaquette (cubicTorus3 L) → ℝ) (C : ℝ),
      (∀ x ∈ l, f x ≤ C) → (l.map f).sum ≤ (l.length : ℝ) * C := by
    intro l f C hle
    induction l with
    | nil => simp
    | cons x xs ih =>
      simp only [List.map_cons, List.sum_cons, List.length_cons, Nat.cast_add, Nat.cast_one]
      have hx := hle x (by simp)
      have hxs := ih (fun y hy => hle y (by simp [hy]))
      linarith
  unfold wilsonAction
  calc β * ((cubicPlaquettes L).map (fun p => wilsonPlaquetteTerm p U)).sum
      ≤ β * (((cubicPlaquettes L).length : ℝ) * (8 / ((N : ℝ) * β))) :=
        mul_le_mul_of_nonneg_left (h_list_sum_le _ _ _ h_term) hβ.le
    _ = 24 * (L : ℝ) ^ 3 / (N : ℝ) := by
        rw [cubicPlaquettes_length]
        push_cast
        field_simp [hN_pos.ne', hβ.ne']
        ring

private lemma cubicLinkKineticKernel_ball_ge (L N : ℕ) [NeZero L] (hN : 1 ≤ N)
    {β : ℝ} (hβ : 0 < β)
    (U W : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ))
    (hU : ∀ e, frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 1 / β)
    (hW : ∀ e, frobeniusNormSq ((W e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 1 / β) :
    Real.exp ((3 * (L : ℝ) ^ 3) * (β / 2) - 3 * (L : ℝ) ^ 3 / (N : ℝ)) ≤
      cubicLinkKineticKernel L N β U W := by
  have hN_pos : (0 : ℝ) < N := Nat.cast_pos.mpr hN
  have h_fac : ∀ e : (cubicTorus3 L).Link,
      Real.exp (β / 2 - 1 / (N : ℝ)) ≤
        Real.exp ((β / (2 * (N : ℝ))) *
          (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re) := by
    intro e
    apply Real.exp_le_exp.mpr
    have h_tr : (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ))).re =
        (N : ℝ) - (1 / 2 : ℝ) * frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) := by
      have h1 := frobeniusNormSq_su_sub_one_eq (U e * (W e)⁻¹)
      rw [frobeniusNormSq_sub_self_su] at h1
      linarith
    have h_diff : frobeniusNormSq
        ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) ≤ 4 / β := by
      have hsub : (U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ) =
          ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) +
            (1 - (W e : Matrix (Fin N) (Fin N) ℂ)) := by abel
      rw [hsub]
      have hadd := frobeniusNormSq_add_le
        ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) (1 - (W e : Matrix (Fin N) (Fin N) ℂ))
      rw [frobeniusNormSq_sub_rev 1 (W e : Matrix (Fin N) (Fin N) ℂ)] at hadd
      linarith [hU e, hW e]
    rw [h_tr]
    have heq : β / 2 - 1 / (N : ℝ) = (β / (2 * (N : ℝ))) * ((N : ℝ) - (1 / 2 : ℝ) * (4 / β)) := by
      field_simp [hN_pos.ne', hβ.ne']
      ring
    rw [heq]
    exact mul_le_mul_of_nonneg_left (by linarith) (by positivity)
  unfold cubicLinkKineticKernel
  calc Real.exp ((3 * (L : ℝ) ^ 3) * (β / 2) - 3 * (L : ℝ) ^ 3 / (N : ℝ))
      = Real.exp (((Fintype.card (cubicTorus3 L).Link : ℕ) : ℝ) * (β / 2 - 1 / (N : ℝ))) := by
          rw [cubicLink_card]; push_cast; ring_nf
    _ = (Real.exp (β / 2 - 1 / (N : ℝ))) ^ Fintype.card (cubicTorus3 L).Link := by
          rw [Real.exp_nat_mul]
    _ = ∏ _e : (cubicTorus3 L).Link, Real.exp (β / 2 - 1 / (N : ℝ)) := by
          simp [Finset.prod_const, Finset.card_univ]
    _ ≤ ∏ e : (cubicTorus3 L).Link, _ :=
          Finset.prod_le_prod (fun _ _ => (Real.exp_pos _).le) (fun e _ => h_fac e)

private lemma cubicLinkKineticKernel_mul_le (L N : ℕ) [NeZero L] (hN : 1 ≤ N)
    {β : ℝ} (hβ : 0 ≤ β)
    (U U' W : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) :
    cubicLinkKineticKernel L N β U W * cubicLinkKineticKernel L N β U' W ≤
      Real.exp ((3 * (L : ℝ) ^ 3) * β - (β / (8 * (N : ℝ))) *
        ∑ e : (cubicTorus3 L).Link, frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))) := by
  have hN_pos : (0 : ℝ) < N := Nat.cast_pos.mpr hN
  unfold cubicLinkKineticKernel
  rw [← Finset.prod_mul_distrib]
  have h_fac : ∀ e : (cubicTorus3 L).Link,
      Real.exp ((β / (2 * (N : ℝ))) *
          (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re) *
        Real.exp ((β / (2 * (N : ℝ))) *
          (Matrix.trace (((U' e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re) ≤
        Real.exp (β - (β / (8 * (N : ℝ))) * frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))) := by
    intro e
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    have htr1 : (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ))).re =
        (N : ℝ) - (1 / 2 : ℝ) * frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) := by
      have h1 := frobeniusNormSq_su_sub_one_eq (U e * (W e)⁻¹)
      rw [frobeniusNormSq_sub_self_su] at h1
      linarith
    have htr2 : (Matrix.trace (((U' e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ))).re =
        (N : ℝ) - (1 / 2 : ℝ) * frobeniusNormSq
          ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) := by
      have h1 := frobeniusNormSq_su_sub_one_eq (U' e * (W e)⁻¹)
      rw [frobeniusNormSq_sub_self_su] at h1
      linarith
    have htri : frobeniusNormSq
        ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)) ≤
        2 * frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) +
        2 * frobeniusNormSq
          ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) := by
      have hsub : (U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ) =
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) +
            ((W e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)) := by abel
      rw [hsub]
      have hadd := frobeniusNormSq_add_le
        ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))
        ((W e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))
      rwa [frobeniusNormSq_sub_rev (W e : Matrix (Fin N) (Fin N) ℂ)
        (U' e : Matrix (Fin N) (Fin N) ℂ)] at hadd
    rw [htr1, htr2]
    have heq1 : (β / (2 * (N : ℝ))) * ((N : ℝ) - (1 / 2 : ℝ) * frobeniusNormSq
        ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) +
      (β / (2 * (N : ℝ))) * ((N : ℝ) - (1 / 2 : ℝ) * frobeniusNormSq
        ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) =
      β - (β / (4 * (N : ℝ))) * (frobeniusNormSq
        ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) +
        frobeniusNormSq
        ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) := by
      field_simp [hN_pos.ne']; ring
    rw [heq1]
    have hmul : (β / (8 * (N : ℝ))) * frobeniusNormSq
        ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)) ≤
        (β / (4 * (N : ℝ))) * (frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ)) +
          frobeniusNormSq
          ((U' e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ))) := by
      have heq2 : (β / (8 * (N : ℝ))) * frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)) =
          (β / (4 * (N : ℝ))) * ((1 / 2 : ℝ) * frobeniusNormSq
            ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))) := by
        ring
      rw [heq2]
      exact mul_le_mul_of_nonneg_left (by linarith) (by positivity)
    linarith
  calc ∏ e : (cubicTorus3 L).Link, _
      ≤ ∏ e : (cubicTorus3 L).Link, Real.exp (β - (β / (8 * (N : ℝ))) * frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ))) :=
        Finset.prod_le_prod (fun _ _ => by positivity) (fun e _ => h_fac e)
    _ = Real.exp (∑ e : (cubicTorus3 L).Link, (β - (β / (8 * (N : ℝ))) * frobeniusNormSq
          ((U e : Matrix (Fin N) (Fin N) ℂ) - (U' e : Matrix (Fin N) (Fin N) ℂ)))) :=
        (Real.exp_sum Finset.univ _).symm
    _ = _ := by
        congr 1
        rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, cubicLink_card,
          nsmul_eq_mul, ← Finset.mul_sum]
        push_cast; ring

"""

src = src.replace(anchor, helpers + anchor, 1)
path.write_text(src, encoding="utf-8")
print("Patched Patch 1/3 successfully.")