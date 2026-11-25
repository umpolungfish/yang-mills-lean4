import Imscribing.YangMills.OSHilbertCompletion

/-!
# Osterwalder–Schrader Pre-Hilbert Data → Quotient Inner Product Space & Completion Lift
-/

namespace Imscribing.YangMills.OSBorchers

open scoped InnerProductSpace
open Imscribing.YangMills.OSCompletion

/-- Pre-Hilbert Osterwalder–Schrader data on a `ℂ`-vector space `E`. -/
structure EuclideanPreData (E : Type*) [AddCommGroup E] [Module ℂ E] where
  B : E → E → ℂ
  B_add_left : ∀ x y z : E, B (x + y) z = B x z + B y z
  B_smul_left : ∀ (c : ℂ) (x y : E), B (c • x) y = star c * B x y
  B_add_right : ∀ x y z : E, B x (y + z) = B x y + B x z
  B_smul_right : ∀ (c : ℂ) (x y : E), B x (c • y) = c * B x y
  B_herm : ∀ x y : E, B y x = star (B x y)
  B_nonneg : ∀ x : E, 0 ≤ (B x x).re
  e₀ : E
  B_vac : B e₀ e₀ = 1
  θ : ℝ → E →ₗ[ℂ] E
  θ_vac : ∀ t : ℝ, 0 ≤ t → θ t e₀ = e₀
  θ_symm : ∀ t : ℝ, 0 ≤ t → ∀ x y : E, B x (θ t y) = B (θ t x) y
  θ_add : ∀ s t : ℝ, 0 ≤ s → 0 ≤ t → ∀ x : E, θ (s + t) x = θ s (θ t x)
  θ_poly : ∀ x : E, ∃ C r : ℝ, 0 < C ∧ 0 ≤ r ∧
    ∀ t ≥ 0, (B (θ t x) (θ t x)).re ≤ C ^ 2 * (1 + t) ^ (2 * r)
  Δ : ℝ
  Δ_pos : 0 < Δ
  θ_decay : ∀ t : ℝ, 0 ≤ t → ∀ x : E, B e₀ x = 0 →
    (B (θ t x) (θ t x)).re ≤ Real.exp (-2 * Δ * t) * (B x x).re

section QuotientSpace

variable {E : Type*} [AddCommGroup E] [Module ℂ E]

/-- Null-space kernel `N₀ = { x : E | Re B(x, x) = 0 }`. -/
def nullSubmodule (pre : EuclideanPreData E) : Submodule ℂ E :=
  sesquilinearNullSubmodule pre.B pre.B_add_left pre.B_smul_left
    pre.B_add_right pre.B_smul_right pre.B_herm pre.B_nonneg

private lemma B_eq_zero_of_left_mem (pre : EuclideanPreData E) {x : E}
    (hx : x ∈ nullSubmodule pre) (y : E) : pre.B x y = 0 := by
  have hcs := sesquilinear_cauchy_schwarz pre.B pre.B_add_left pre.B_smul_left
    pre.B_add_right pre.B_smul_right pre.B_herm pre.B_nonneg x y
  have hx0 : (pre.B x x).re = 0 := hx
  rw [hx0, zero_mul] at hcs
  exact norm_eq_zero.mp (by nlinarith [norm_nonneg (pre.B x y)])

private lemma B_eq_zero_of_right_mem (pre : EuclideanPreData E) (x : E) {y : E}
    (hy : y ∈ nullSubmodule pre) : pre.B x y = 0 := by
  rw [← star_zero, ← B_eq_zero_of_left_mem pre hy x, pre.B_herm]
  simp

private lemma B_quot_wd (pre : EuclideanPreData E) {x₁ x₂ y₁ y₂ : E}
    (hx : x₁ ≈ x₂) (hy : y₁ ≈ y₂) : pre.B x₁ y₁ = pre.B x₂ y₂ := by
  have hx_mem : x₁ - x₂ ∈ nullSubmodule pre := by
    rw [Submodule.quotientRel_def] at hx
    have hneg : -(x₁ - x₂) ∈ nullSubmodule pre := by simpa [neg_sub] using hx
    simpa using (nullSubmodule pre).neg_mem hneg
  have hy_mem : y₁ - y₂ ∈ nullSubmodule pre := by
    rw [Submodule.quotientRel_def] at hy
    have hneg : -(y₁ - y₂) ∈ nullSubmodule pre := by simpa [neg_sub] using hy
    simpa using (nullSubmodule pre).neg_mem hneg
  have h1 : pre.B x₁ y₁ - pre.B x₂ y₁ = 0 := by
    have hsub : x₁ = (x₁ - x₂) + x₂ := by abel
    conv_lhs => rw [hsub, pre.B_add_left, B_eq_zero_of_left_mem pre hx_mem y₁, zero_add]
    exact sub_self _
  have h2 : pre.B x₂ y₁ - pre.B x₂ y₂ = 0 := by
    have hsub : y₁ = (y₁ - y₂) + y₂ := by abel
    conv_lhs => rw [hsub, pre.B_add_right, B_eq_zero_of_right_mem pre x₂ hy_mem, zero_add]
    exact sub_self _
  exact sub_eq_zero.mp (by linear_combination h1 + h2)

/-- Pre-Hilbert inner product core on `E ⧸ nullSubmodule pre`. -/
noncomputable def quotInnerCore (pre : EuclideanPreData E) :
    InnerProductSpace.Core ℂ (E ⧸ nullSubmodule pre) where
  inner x y := Quotient.liftOn₂ x y pre.B (fun _ _ _ _ hx hy => B_quot_wd pre hx hy)
  conj_symm x y := by
    induction x using Submodule.Quotient.induction_on
    induction y using Submodule.Quotient.induction_on
    exact (pre.B_herm _ _).symm
  nonneg_re x := by
    induction x using Submodule.Quotient.induction_on
    exact pre.B_nonneg _
  definite x hx := by
    induction x using Submodule.Quotient.induction_on with
    | _ F =>
      rw [Submodule.Quotient.mk_eq_zero]
      change (pre.B F F).re = 0
      change pre.B F F = 0 at hx
      rw [hx, Complex.zero_re]
  add_left x y z := by
    induction x using Submodule.Quotient.induction_on
    induction y using Submodule.Quotient.induction_on
    induction z using Submodule.Quotient.induction_on
    exact pre.B_add_left _ _ _
  smul_left x y r := by
    induction x using Submodule.Quotient.induction_on
    induction y using Submodule.Quotient.induction_on
    exact pre.B_smul_left _ _ _

/-- **OS Completion Theorem on `E ⧸ nullSubmodule pre`.** -/
theorem os_borchers_to_completion (pre : EuclideanPreData E) :
    let core := quotInnerCore pre
    letI : NormedAddCommGroup (E ⧸ nullSubmodule pre) := core.toNormedAddCommGroup
    letI : InnerProductSpace ℂ (E ⧸ nullSubmodule pre) := InnerProductSpace.ofCore core
    let H := UniformSpace.Completion (E ⧸ nullSubmodule pre)
    let Ω : H := ((Submodule.Quotient.mk pre.e₀ : E ⧸ nullSubmodule pre) : H)
    ∃ T : ℝ → H →L[ℂ] H,
      ‖Ω‖ = 1 ∧
      (∀ t : ℝ, 0 ≤ t → T t Ω = Ω) ∧
      (∀ t : ℝ, 0 ≤ t → ∀ x y : H, ⟪x, T t y⟫_ℂ = ⟪T t x, y⟫_ℂ) ∧
      (∀ s t : ℝ, 0 ≤ s → 0 ≤ t → ∀ x : H, T (s + t) x = T s (T t x)) ∧
      (∀ t : ℝ, 0 ≤ t → ∀ x : H, ‖T t x‖ ≤ ‖x‖) ∧
      (∀ t : ℝ, 0 ≤ t → ∀ φ : H, ⟪Ω, φ⟫_ℂ = 0 →
        ‖T t φ‖ ≤ Real.exp (-pre.Δ * t) * ‖φ‖) := by
  intro core
  letI : NormedAddCommGroup (E ⧸ nullSubmodule pre) := core.toNormedAddCommGroup
  letI : InnerProductSpace ℂ (E ⧸ nullSubmodule pre) := InnerProductSpace.ofCore core
  set H₀ := E ⧸ nullSubmodule pre
  set Ω₀ : H₀ := Submodule.Quotient.mk pre.e₀
  have hΩ₀ : ‖Ω₀‖ = 1 := by
    have hsq : ‖Ω₀‖ ^ 2 = 1 := by
      have h1 : (⟪Ω₀, Ω₀⟫_ℂ).re = ‖Ω₀‖ ^ 2 := by
        rw [inner_self_eq_norm_sq_to_K]; norm_cast
      rw [← h1]
      change (pre.B pre.e₀ pre.e₀).re = 1
      rw [pre.B_vac, Complex.one_re]
    nlinarith [norm_nonneg Ω₀]
  have h_null_θ : ∀ t : ℝ, 0 ≤ t → ∀ {x : E},
      x ∈ nullSubmodule pre → pre.θ t x ∈ nullSubmodule pre := by
    intro t ht x hx
    change (pre.B (pre.θ t x) (pre.θ t x)).re = 0
    rw [pre.θ_symm t ht (pre.θ t x) x]
    have hcs := sesquilinear_cauchy_schwarz pre.B pre.B_add_left pre.B_smul_left
      pre.B_add_right pre.B_smul_right pre.B_herm pre.B_nonneg
      (pre.θ t (pre.θ t x)) x
    have hx0 : (pre.B x x).re = 0 := hx
    rw [hx0, mul_zero] at hcs
    have h0 : pre.B (pre.θ t (pre.θ t x)) x = 0 :=
      norm_eq_zero.mp (by nlinarith [norm_nonneg (pre.B (pre.θ t (pre.θ t x)) x)])
    rw [h0, Complex.zero_re]
  let T₀ : ℝ → H₀ →ₗ[ℂ] H₀ := fun t =>
    if ht : 0 ≤ t then
      (nullSubmodule pre).liftQ ((Submodule.mkQ (nullSubmodule pre)).comp (pre.θ t))
        (fun x hx => by
          simp only [LinearMap.mem_ker, LinearMap.comp_apply, Submodule.mkQ_apply,
            Submodule.Quotient.mk_eq_zero]
          exact h_null_θ t ht hx)
    else LinearMap.id
  have hT₀_mk : ∀ t : ℝ, 0 ≤ t → ∀ x : E,
      T₀ t (Submodule.Quotient.mk x) = Submodule.Quotient.mk (pre.θ t x) := by
    intro t ht x
    dsimp [T₀]
    rw [dif_pos ht]
    rfl
  have hT₀_vac : ∀ t : ℝ, 0 ≤ t → T₀ t Ω₀ = Ω₀ := by
    intro t ht
    rw [hT₀_mk t ht pre.e₀, pre.θ_vac t ht]
  have hT₀_symm : ∀ t : ℝ, 0 ≤ t → ∀ x y : H₀, ⟪x, T₀ t y⟫_ℂ = ⟪T₀ t x, y⟫_ℂ := by
    intro t ht x y
    induction x using Submodule.Quotient.induction_on
    induction y using Submodule.Quotient.induction_on
    rw [hT₀_mk t ht _, hT₀_mk t ht _]
    exact pre.θ_symm t ht _ _
  have hT₀_add : ∀ s t : ℝ, 0 ≤ s → 0 ≤ t → ∀ x : H₀, T₀ (s + t) x = T₀ s (T₀ t x) := by
    intro s t hs ht x
    induction x using Submodule.Quotient.induction_on
    rw [hT₀_mk (s + t) (add_nonneg hs ht) _, hT₀_mk t ht _, hT₀_mk s hs _, pre.θ_add s t hs ht _]
  have hT₀_poly : ∀ x : H₀, ∃ C r : ℝ, 0 < C ∧ 0 ≤ r ∧ ∀ t ≥ 0, ‖T₀ t x‖ ≤ C * (1 + t) ^ r := by
    intro x
    induction x using Submodule.Quotient.induction_on with
    | _ F =>
      obtain ⟨C, r, hC, hr, hpoly⟩ := pre.θ_poly F
      refine ⟨C, r, hC, hr, fun t ht => ?_⟩
      have hsq : ‖T₀ t (Submodule.Quotient.mk F)‖ ^ 2 ≤ (C * (1 + t) ^ r) ^ 2 := by
        have h1 : (⟪T₀ t (Submodule.Quotient.mk F), T₀ t (Submodule.Quotient.mk F)⟫_ℂ).re =
            ‖T₀ t (Submodule.Quotient.mk F)‖ ^ 2 := by
          rw [inner_self_eq_norm_sq_to_K]; norm_cast
        rw [← h1, hT₀_mk t ht F]
        have h2 : (C * (1 + t) ^ r) ^ 2 = C ^ 2 * (1 + t) ^ (2 * r) := by
          rw [mul_pow, ← Real.rpow_natCast ((1 + t) ^ r) 2, ← Real.rpow_mul (by linarith)]
          congr 2; ring
        rw [h2]
        exact hpoly t ht
      have h_rhs_nn : 0 ≤ C * (1 + t) ^ r := mul_nonneg hC.le (Real.rpow_nonneg (by linarith) r)
      nlinarith [norm_nonneg (T₀ t (Submodule.Quotient.mk F))]
  have hT₀_decay : ∀ t : ℝ, 0 ≤ t → ∀ φ : H₀, ⟪Ω₀, φ⟫_ℂ = 0 →
      ‖T₀ t φ‖ ≤ Real.exp (-pre.Δ * t) * ‖φ‖ := by
    intro t ht φ hφ
    induction φ using Submodule.Quotient.induction_on with
    | _ F =>
      have h_orth : pre.B pre.e₀ F = 0 := hφ
      have hdec := pre.θ_decay t ht F h_orth
      have hsq : ‖T₀ t (Submodule.Quotient.mk F)‖ ^ 2 ≤
          (Real.exp (-pre.Δ * t) * ‖(Submodule.Quotient.mk F : H₀)‖) ^ 2 := by
        have h1 : (⟪T₀ t (Submodule.Quotient.mk F), T₀ t (Submodule.Quotient.mk F)⟫_ℂ).re =
            ‖T₀ t (Submodule.Quotient.mk F)‖ ^ 2 := by
          rw [inner_self_eq_norm_sq_to_K]; norm_cast
        have h2 : (⟪(Submodule.Quotient.mk F : H₀), Submodule.Quotient.mk F⟫_ℂ).re =
            ‖(Submodule.Quotient.mk F : H₀)‖ ^ 2 := by
          rw [inner_self_eq_norm_sq_to_K]; norm_cast
        rw [← h1, hT₀_mk t ht F, mul_pow, ← h2]
        have hexp : Real.exp (-pre.Δ * t) ^ 2 = Real.exp (-2 * pre.Δ * t) := by
          rw [sq, ← Real.exp_add]
          congr 1; ring
        rw [hexp]
        exact hdec
      have h_rhs_nn : 0 ≤ Real.exp (-pre.Δ * t) * ‖(Submodule.Quotient.mk F : H₀)‖ :=
        mul_nonneg (Real.exp_pos _).le (norm_nonneg _)
      nlinarith [norm_nonneg (T₀ t (Submodule.Quotient.mk F))]
  exact os_completion_semigroup_bridge Ω₀ hΩ₀ T₀ hT₀_vac hT₀_symm hT₀_add hT₀_poly pre.Δ hT₀_decay

/-- Strict variance on `E` descends to ‖⟪Ω, x⟫‖ < ‖x‖ in `Completion (E ⧸ N₀)`. -/
theorem strict_variance_in_completion (pre : EuclideanPreData E) {x : E}
    (hx : ‖pre.B pre.e₀ x‖ ^ 2 < (pre.B x x).re) :
    let core := quotInnerCore pre
    letI : NormedAddCommGroup (E ⧸ nullSubmodule pre) := core.toNormedAddCommGroup
    letI : InnerProductSpace ℂ (E ⧸ nullSubmodule pre) := InnerProductSpace.ofCore core
    let H := UniformSpace.Completion (E ⧸ nullSubmodule pre)
    let Ω : H := ((Submodule.Quotient.mk pre.e₀ : E ⧸ nullSubmodule pre) : H)
    ‖⟪Ω, ((Submodule.Quotient.mk x : E ⧸ nullSubmodule pre) : H)⟫_ℂ‖ <
      ‖((Submodule.Quotient.mk x : E ⧸ nullSubmodule pre) : H)‖ := by
  intro core
  letI : NormedAddCommGroup (E ⧸ nullSubmodule pre) := core.toNormedAddCommGroup
  letI : InnerProductSpace ℂ (E ⧸ nullSubmodule pre) := InnerProductSpace.ofCore core
  set H₀ := E ⧸ nullSubmodule pre
  have h_in : ⟪((Submodule.Quotient.mk pre.e₀ : H₀) : UniformSpace.Completion H₀),
      ((Submodule.Quotient.mk x : H₀) : UniformSpace.Completion H₀)⟫_ℂ = pre.B pre.e₀ x := by
    rw [UniformSpace.Completion.inner_coe]
    rfl
  have h_norm_sq : ‖((Submodule.Quotient.mk x : H₀) : UniformSpace.Completion H₀)‖ ^ 2 =
      (pre.B x x).re := by
    rw [UniformSpace.Completion.norm_coe]
    have h1 : (⟪(Submodule.Quotient.mk x : H₀), Submodule.Quotient.mk x⟫_ℂ).re =
        ‖(Submodule.Quotient.mk x : H₀)‖ ^ 2 := by
      rw [inner_self_eq_norm_sq_to_K]; norm_cast
    rw [← h1]
    rfl
  have h_sq_lt :
      ‖⟪((Submodule.Quotient.mk pre.e₀ : H₀) : UniformSpace.Completion H₀),
          ((Submodule.Quotient.mk x : H₀) : UniformSpace.Completion H₀)⟫_ℂ‖ ^ 2 <
        ‖((Submodule.Quotient.mk x : H₀) : UniformSpace.Completion H₀)‖ ^ 2 := by
    rw [h_in, h_norm_sq]
    exact hx
  nlinarith [norm_nonneg ⟪((Submodule.Quotient.mk pre.e₀ : H₀) : UniformSpace.Completion H₀),
      ((Submodule.Quotient.mk x : H₀) : UniformSpace.Completion H₀)⟫_ℂ,
    norm_nonneg ((Submodule.Quotient.mk x : H₀) : UniformSpace.Completion H₀)]

end QuotientSpace

end Imscribing.YangMills.OSBorchers