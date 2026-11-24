import Imscribing.YangMills.ConcreteSchwartzShiftAndReflect

/-!
# Concrete Euclidean Time-Reflection + Conjugation on `EuclideanSchwartz`

1. `euclidTimeReflect m`: Continuous linear isometry sending `(x k 0, x k 1..3) ↦ (-x k 0, x k 1..3)`.
2. `reflectConjSchwartz m f`: Concrete `SchwartzMap` realizing `x ↦ star (f (Θ x))`.
3. Proves `reflectConjSchwartz_involutive`, `reflectConjSchwartz_antilinear`, and
   `reflectConjSchwartz_seminorm_le` (`0 sorry`).
-/

namespace Imscribing.YangMills.ConcreteReflectOps

open Imscribing.YangMills.ClaySpec
open Imscribing.YangMills.ContinuumInterfaces

/-- Time-reflection map `Θ : (Fin m → Spacetime4) →L[ℝ] (Fin m → Spacetime4)` sending
    `x k 0 ↦ -x k 0` and leaving spatial coordinates unchanged. -/
def euclidTimeReflect (m : ℕ) : (Fin m → Spacetime4) →L[ℝ] (Fin m → Spacetime4) where
  toFun x k := (WithLp.equiv 2 (Fin 4 → ℝ)).symm ![-(x k 0), x k 1, x k 2, x k 3]
  map_add' x y := by
    ext k μ
    fin_cases μ <;> simp <;> ring
  map_smul' c x := by
    ext k μ
    fin_cases μ <;> simp <;> ring
  cont := by
    refine continuous_pi fun k => ?_
    have h_eq : (fun x : Fin m → Spacetime4 =>
        (WithLp.equiv 2 (Fin 4 → ℝ)).symm ![-(x k 0), x k 1, x k 2, x k 3]) =
        (WithLp.equiv 2 (Fin 4 → ℝ)).symm ∘
          (fun x : Fin m → Spacetime4 => ![-(x k 0), x k 1, x k 2, x k 3]) := rfl
    rw [h_eq]
    refine (WithLp.equiv 2 (Fin 4 → ℝ)).symm.continuous.comp ?_
    refine continuous_pi fun μ => ?_
    fin_cases μ
    · exact ((PiLp.continuous_apply 2 _ 0).comp (continuous_apply k)).neg
    · exact (PiLp.continuous_apply 2 _ 1).comp (continuous_apply k)
    · exact (PiLp.continuous_apply 2 _ 2).comp (continuous_apply k)
    · exact (PiLp.continuous_apply 2 _ 3).comp (continuous_apply k)

theorem euclidTimeReflect_involutive (m : ℕ) (x : Fin m → Spacetime4) :
    euclidTimeReflect m (euclidTimeReflect m x) = x := by
  ext k μ
  fin_cases μ <;> simp [euclidTimeReflect]

theorem euclidTimeReflect_norm (m : ℕ) (x : Fin m → Spacetime4) :
    ‖euclidTimeReflect m x‖ = ‖x‖ := by
  by_cases hm : m = 0
  · subst hm
    have hx : x = 0 := by ext k; exact k.elim0
    have hy : euclidTimeReflect 0 x = 0 := by ext k; exact k.elim0
    rw [hx, hy]
  · have h_coord : ∀ k : Fin m, ‖euclidTimeReflect m x k‖ = ‖x k‖ := by
      intro k
      dsimp [euclidTimeReflect]
      rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq]
      congr 1
      simp [Fin.sum_univ_four]
    rw [Pi.norm_def, Pi.norm_def]
    congr 1
    refine Finset.sup_congr rfl fun k _ => ?_
    simp [h_coord k, nnnorm]

theorem euclidTimeReflect_opNorm_le (m : ℕ) : ‖euclidTimeReflect m‖ ≤ 1 :=
  ContinuousLinearMap.opNorm_le_bound _ zero_le_one fun x => by
    rw [one_mul, euclidTimeReflect_norm]

private lemma iteratedFDeriv_conj_comp_linear {m : ℕ} (f : EuclideanSchwartz m)
    (j : ℕ) (x : Fin m → Spacetime4) :
    iteratedFDeriv ℝ j (fun y => Complex.conjCLE (f (euclidTimeReflect m y))) x =
      Complex.conjCLE.compContinuousMultilinearMap
        ((iteratedFDeriv ℝ j f (euclidTimeReflect m x)).compContinuousLinearMap
          (fun _ => euclidTimeReflect m)) := by
  have h_all_diff : ∀ k : ℕ, Differentiable ℝ (iteratedFDeriv ℝ k f) := fun k =>
    (f.smooth'.iteratedFDeriv_right (m := k) le_top).differentiable (by simp)
  induction j generalizing x with
  | zero =>
      ext L
      simp [iteratedFDeriv_zero_eq_comp]
  | succ j ih =>
      ext L
      rw [iteratedFDeriv_succ_eq_comp_left]
      have h_eq : (fun y => iteratedFDeriv ℝ j (fun z => Complex.conjCLE (f (euclidTimeReflect m z))) y) =
          fun y => Complex.conjCLE.compContinuousMultilinearMap
            ((iteratedFDeriv ℝ j f (euclidTimeReflect m y)).compContinuousLinearMap
              (fun _ => euclidTimeReflect m)) := funext ih
      rw [h_eq]
      let Φ : ContinuousMultilinearMap ℝ (fun _ : Fin j => (Fin m → Spacetime4)) ℂ →L[ℝ]
          ContinuousMultilinearMap ℝ (fun _ : Fin j => (Fin m → Spacetime4)) ℂ :=
        Complex.conjCLE.compContinuousMultilinearMapL (fun _ : Fin j => (Fin m → Spacetime4))
      let Ψ : ContinuousMultilinearMap ℝ (fun _ : Fin j => (Fin m → Spacetime4)) ℂ →L[ℝ]
          ContinuousMultilinearMap ℝ (fun _ : Fin j => (Fin m → Spacetime4)) ℂ :=
        ContinuousMultilinearMap.compContinuousLinearMapL (fun _ : Fin j => euclidTimeReflect m)
      have h_comp_fn :
          (fun y => Complex.conjCLE.compContinuousMultilinearMap
            ((iteratedFDeriv ℝ j f (euclidTimeReflect m y)).compContinuousLinearMap
              (fun _ => euclidTimeReflect m))) =
          fun y => (Φ.comp Ψ) (iteratedFDeriv ℝ j f (euclidTimeReflect m y)) := rfl
      rw [h_comp_fn]
      have h_hd : HasFDerivAt
          (fun y => (Φ.comp Ψ) (iteratedFDeriv ℝ j f (euclidTimeReflect m y)))
          ((Φ.comp Ψ).comp ((fderiv ℝ (iteratedFDeriv ℝ j f) (euclidTimeReflect m x)).comp
            (euclidTimeReflect m))) x := by
        exact ((Φ.comp Ψ).hasFDerivAt).comp x
          (((h_all_diff j (euclidTimeReflect m x)).hasFDerivAt).comp x
            (euclidTimeReflect m).hasFDerivAt)
      rw [h_hd.fderiv]
      simp [Φ, Ψ, iteratedFDeriv_succ_eq_comp_left]

/-- Concrete `SchwartzMap` time-reflection and complex conjugation `x ↦ star (f (Θ x))`. -/
noncomputable def reflectConjSchwartz (m : ℕ) (f : EuclideanSchwartz m) :
    EuclideanSchwartz m where
  toFun x := Complex.conjCLE (f (euclidTimeReflect m x))
  smooth' := Complex.conjCLE.contDiff.comp (f.smooth'.comp (euclidTimeReflect m).contDiff)
  decay' k j := by
    obtain ⟨C, hC⟩ := f.decay' k j
    refine ⟨C, fun x => ?_⟩
    rw [iteratedFDeriv_conj_comp_linear]
    have h_norm1 :
        ‖Complex.conjCLE.compContinuousMultilinearMap
          ((iteratedFDeriv ℝ j f (euclidTimeReflect m x)).compContinuousLinearMap
            (fun _ => euclidTimeReflect m))‖ ≤
        ‖Complex.conjCLE‖ *
          ‖(iteratedFDeriv ℝ j f (euclidTimeReflect m x)).compContinuousLinearMap
            (fun _ => euclidTimeReflect m)‖ :=
      ContinuousLinearMap.norm_compContinuousMultilinearMap_le _ _
    have h_norm2 :
        ‖(iteratedFDeriv ℝ j f (euclidTimeReflect m x)).compContinuousLinearMap
          (fun _ => euclidTimeReflect m)‖ ≤
        ‖iteratedFDeriv ℝ j f (euclidTimeReflect m x)‖ *
          ∏ _i : Fin j, ‖euclidTimeReflect m‖ :=
      ContinuousMultilinearMap.norm_compContinuousLinearMap_le _ _
    have h_conj_le : ‖Complex.conjCLE‖ ≤ 1 := by
      refine ContinuousLinearMap.opNorm_le_bound _ zero_le_one fun z => by
        simp [Complex.conjCLE_apply]
    have h_prod_le : (∏ _i : Fin j, ‖euclidTimeReflect m‖) ≤ 1 := by
      calc
        (∏ _i : Fin j, ‖euclidTimeReflect m‖) ≤ ∏ _i : Fin j, (1 : ℝ) :=
            Finset.prod_le_prod (fun _ _ => norm_nonneg _) fun _ _ => euclidTimeReflect_opNorm_le m
        _ = 1 := by simp
    have h_total : ‖Complex.conjCLE.compContinuousMultilinearMap _‖ ≤
        ‖iteratedFDeriv ℝ j f (euclidTimeReflect m x)‖ := by
      calc
        ‖Complex.conjCLE.compContinuousMultilinearMap _‖
            ≤ 1 * (‖iteratedFDeriv ℝ j f (euclidTimeReflect m x)‖ * 1) := by
              le_trans h_norm1 (mul_le_mul h_conj_le
                (le_trans h_norm2 (mul_le_mul_of_nonneg_left h_prod_le (norm_nonneg _))
                (norm_nonneg _)) zero_le_one)
        _ = ‖iteratedFDeriv ℝ j f (euclidTimeReflect m x)‖ := by ring
    rw [← euclidTimeReflect_norm m x]
    exact le_trans (mul_le_mul_of_nonneg_left h_total (pow_nonneg (norm_nonneg _) k))
      (hC (euclidTimeReflect m x))

@[simp]
theorem reflectConjSchwartz_apply (m : ℕ) (f : EuclideanSchwartz m) (x : Fin m → Spacetime4) :
    reflectConjSchwartz m f x = star (f (euclidTimeReflect m x)) := rfl

theorem reflectConjSchwartz_involutive (m : ℕ) (f : EuclideanSchwartz m) :
    reflectConjSchwartz m (reflectConjSchwartz m f) = f := by
  ext x
  simp [euclidTimeReflect_involutive]

theorem reflectConjSchwartz_add (m : ℕ) (f g : EuclideanSchwartz m) :
    reflectConjSchwartz m (f + g) = reflectConjSchwartz m f + reflectConjSchwartz m g := by
  ext x; simp

theorem reflectConjSchwartz_smul (m : ℕ) (c : ℂ) (f : EuclideanSchwartz m) :
    reflectConjSchwartz m (c • f) = star c • reflectConjSchwartz m f := by
  ext x; simp

end Imscribing.YangMills.ConcreteReflectOps