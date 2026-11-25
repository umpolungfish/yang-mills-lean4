import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv
import Mathlib.Analysis.InnerProductSpace.PiL2
import Imscribing.YangMills.BorchersContinuumReconstruction
import Imscribing.YangMills.OSHilbertCompletion

noncomputable section

namespace Imscribing.YangMills.OSCanonicalSemigroupContinuity

open Imscribing.YangMills.BorchersReconstruction
open Imscribing.YangMills.OSCompletion

/-- Shift of a Schwartz function is Lipschitz in the Schwartz seminorms. -/
theorem shiftSchwartz_seminorm_lipschitz {n : ℕ} (f : EuclideanSchwartz n) (t s : ℝ)
    (k m : ℕ) :
    |SchwartzMap.seminorm ℂ k m (shiftPos t f) - SchwartzMap.seminorm ℂ k m (shiftPos s f)| ≤
      |t - s| * SchwartzMap.seminorm ℂ (k + 1) m f := by
  -- Use Mean Value Theorem on the shift parameter
  by_cases ht : t = s
  · simp [ht]
  · have h_diff : Differentiable ℝ (fun τ => SchwartzMap.seminorm ℂ k m (shiftPos τ f)) := by
      refine Differentiable.comp ?_ (differentiable_const _).add differentiable_id
      sorry
    have h_deriv_bound : ∀ τ : ℝ, 
        |deriv (fun τ => SchwartzMap.seminorm ℂ k m (shiftPos τ f)) τ| ≤
          SchwartzMap.seminorm ℂ (k + 1) m f := by
      intro τ
      sorry
    -- Apply MVT
    sorry

/-- The OS semigroup satisfies T(0) = 1. -/
theorem osSemigroup_zero_eq_id (T : ℝ → OSHilbert N →L[ℂ] OSHilbert N)
    (hT : OSAnalyticCore N T) : T 0 = 1 := by
  sorry

/-- Strong right-continuity of the OS semigroup at 0. -/
theorem osSemigroup_strong_right_continuous_at_zero (T : ℝ → OSHilbert N →L[ℂ] OSHilbert N)
    (hT : OSAnalyticCore N T) :
    ∀ ψ : OSHilbert N, Filter.Tendsto (fun t => T t ψ) (𝓝[>] 0) (𝓝 ψ) := by
  sorry

/-- The OS semigroup can be extended to a strongly continuous contraction semigroup
    on the completion Hilbert space. -/
theorem osSemigroup_extend_to_completion (T : ℝ → OSHilbert N →L[ℂ] OSHilbert N)
    (hT : OSAnalyticCore N T) :
    ∃ (T_ext : ℝ → (UniformSpace.Completion (OSHilbert N)) →L[ℂ] 
        (UniformSpace.Completion (OSHilbert N))),
      T_ext 0 = 1 ∧
      (∀ t : ℝ, 0 ≤ t → ∀ ψ : UniformSpace.Completion (OSHilbert N), 
        ‖T_ext t ψ‖ ≤ ‖ψ‖) ∧
      (∀ ψ : OSHilbert N, ∀ t : ℝ, 0 ≤ t → 
        T_ext t (UniformSpace.Completion.ofComplete (ψ : OSHilbert N)) = 
        UniformSpace.Completion.ofComplete (T t ψ)) := by
  sorry

end Imscribing.YangMills.OSCanonicalSemigroupContinuity
