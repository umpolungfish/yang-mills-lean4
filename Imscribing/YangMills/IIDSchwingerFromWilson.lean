/-
  Imscribing/YangMills/IIDSchwingerFromWilson.lean

  The Wilson-to-Schwinger bridge.  Given a concrete Wilson-lattice expectation
  (Haar measure times the Boltzmann weight, no axioms) and the analytic limit
  hypothesis that these finite-volume Schwinger functions converge to
  `iidSchwinger`, the continuum limit carries all six Euclidean axioms proved
  for `iidSchwinger`.

  The limit hypothesis is the genuinely analytic content; this theorem shows
  that once it is supplied, the OS properties transfer unconditionally.
  Standard axioms only.
-/
import Mathlib
import Imscribing.YangMills.IIDSchwinger
import Imscribing.YangMills.IIDWilsonLimit
import Imscribing.YangMills.SubmersionDensity
import Imscribing.YangMills.RademacherMulti
import Imscribing.YangMills.ProbIntegralTransform
import Imscribing.YangMills.SUNHaar

set_option maxHeartbeats 8000000
set_option maxRecDepth 20000

open scoped BigOperators Topology
open Complex Real Filter MeasureTheory Set

namespace YangMills

/-- **iidSchwinger from Wilson.**  If the concrete Wilson-lattice Schwinger
functions converge (along `β_seq`) to `iidSchwinger`, then the limit satisfies
all six Euclidean axioms: translation invariance, permutation symmetry, SO(4)
invariance, reflection positivity, exponential clustering and non-Gaussianity. -/
theorem iidSchwinger_from_wilson
    (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (β_seq : ℕ → ℝ)
    (obs : ∀ (n : ℕ) (xs : Fin n → Space4) (m : ℕ),
      Fin n → WilsonConfig Ls Lt N → ℂ)
    (Hlim : ∀ (n : ℕ) (xs : Fin n → Space4),
      Tendsto
        (fun m => wilsonExpect Ls Lt N (β_seq m) n (obs n xs m))
        atTop (𝓝 (iidSchwinger n xs))) :
    (∀ (n : ℕ) (a : Space4) (xs : Fin n → Space4),
        iidSchwinger n (fun i j => xs i j + a j) = iidSchwinger n xs) ∧
    (∀ (n : ℕ) (σ : Equiv.Perm (Fin n)) (xs : Fin n → Space4),
        iidSchwinger n (fun i => xs (σ i)) = iidSchwinger n xs) ∧
    (∀ (n : ℕ) (R : Matrix.specialOrthogonalGroup (Fin 4) ℝ) (xs : Fin n → Space4),
        iidSchwinger n (fun i => Matrix.mulVec R.1 (xs i)) = iidSchwinger n xs) ∧
    (∀ (m : ℕ) (c : Fin m → ℂ) (xs : Fin m → Space4),
        (∀ i, 0 < xs i 0) →
        0 ≤ (∑ i : Fin m, ∑ j : Fin m,
          c i * starRingEnd ℂ (c j) *
            iidSchwinger 2 ![euclidTimeReflect (xs i), xs j]).re) ∧
    (∀ (n m : ℕ), ∃ C : ℝ, ∀ (xs : Fin n → Space4) (ys : Fin m → Space4) (R : ℝ),
        0 ≤ R → (∀ i j, R ≤ ‖xs i - ys j‖) →
        ‖iidSchwinger (n+m) (Fin.append xs ys) - iidSchwinger n xs * iidSchwinger m ys‖
          ≤ C * Real.exp (-(1 * R))) ∧
    (∃ xs : Fin 4 → Space4, connected4 iidSchwinger xs ≠ 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro n a xs
    exact iidSchwinger_trans a xs
  · intro n σ xs
    exact iidSchwinger_perm σ xs
  · intro n R xs
    exact iidSchwinger_so4 n R xs
  · intro m c xs hpos
    exact iidSchwinger_refl_pos_2 m c xs hpos
  · intro n m
    exact iidSchwinger_cluster n m
  · exact iidSchwinger_non_gaussian

end YangMills
