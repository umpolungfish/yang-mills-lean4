/-
  Imscribing/YangMills/IIDSchwingerFromWilson.lean

  The Wilson-to-Schwinger bridge.  Given a concrete Wilson-lattice expectation
  (Haar measure times the Boltzmann weight, no axioms) and the analytic limit
  hypothesis that these finite-volume Schwinger functions converge to
  `iidSchwinger`, the continuum limit object built from the Wilson expectations
  carries all six Euclidean axioms proved for `iidSchwinger`.

  The limit hypothesis is used essentially: the limit Schwinger function is
  defined as the `lim` of the Wilson expectations, and the hypothesis identifies
  that limit with `iidSchwinger` by uniqueness of limits.  Two different
  observation families that both converge therefore produce the same limit —
  a glut of equivalent derivations of the same continuum object.

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

/-- The continuum Schwinger function obtained as the limit of concrete Wilson
lattice expectations.  This is the object the analytic hypothesis is about. -/
noncomputable def wilsonLimitSchwinger
    (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (β_seq : ℕ → ℝ)
    (obs : ∀ (n : ℕ) (xs : Fin n → Space4) (m : ℕ),
      Fin n → WilsonConfig Ls Lt N → ℂ) :
    (n : ℕ) → (Fin n → Space4) → ℂ :=
  fun n xs => lim (Filter.map (fun m =>
    wilsonExpect Ls Lt N (β_seq m) n (obs n xs m)) Filter.atTop)

/-- The limit hypothesis identifies the Wilson limit object with `iidSchwinger`. -/
lemma wilsonLimitSchwinger_eq_iid
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
    wilsonLimitSchwinger Ls Lt N β_seq obs = iidSchwinger := by
  funext n xs
  unfold wilsonLimitSchwinger
  exact lim_eq (Hlim n xs)

/-- A glut of equivalent derivations: any two observation families whose Wilson
expectations converge to `iidSchwinger` determine the same continuum limit. -/
theorem wilson_limit_glut
    (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (β_seq : ℕ → ℝ)
    (obs obs' : ∀ (n : ℕ) (xs : Fin n → Space4) (m : ℕ),
      Fin n → WilsonConfig Ls Lt N → ℂ)
    (Hlim : ∀ (n : ℕ) (xs : Fin n → Space4),
      Tendsto (fun m => wilsonExpect Ls Lt N (β_seq m) n (obs n xs m))
        atTop (𝓝 (iidSchwinger n xs)))
    (Hlim' : ∀ (n : ℕ) (xs : Fin n → Space4),
      Tendsto (fun m => wilsonExpect Ls Lt N (β_seq m) n (obs' n xs m))
        atTop (𝓝 (iidSchwinger n xs))) :
    wilsonLimitSchwinger Ls Lt N β_seq obs =
      wilsonLimitSchwinger Ls Lt N β_seq obs' := by
  rw [wilsonLimitSchwinger_eq_iid Ls Lt N β_seq obs Hlim,
      wilsonLimitSchwinger_eq_iid Ls Lt N β_seq obs' Hlim']

/-- **iidSchwinger from Wilson.**  If the concrete Wilson-lattice Schwinger
functions converge (along `β_seq`) to `iidSchwinger`, then the resulting Wilson
limit Schwinger function satisfies all six Euclidean axioms. -/
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
    let S := wilsonLimitSchwinger Ls Lt N β_seq obs
    (∀ (n : ℕ) (a : Space4) (xs : Fin n → Space4),
        S n (fun i j => xs i j + a j) = S n xs) ∧
    (∀ (n : ℕ) (σ : Equiv.Perm (Fin n)) (xs : Fin n → Space4),
        S n (fun i => xs (σ i)) = S n xs) ∧
    (∀ (n : ℕ) (R : Matrix.specialOrthogonalGroup (Fin 4) ℝ) (xs : Fin n → Space4),
        S n (fun i => Matrix.mulVec R.1 (xs i)) = S n xs) ∧
    (∀ (m : ℕ) (c : Fin m → ℂ) (xs : Fin m → Space4),
        (∀ i, 0 < xs i 0) →
        0 ≤ (∑ i : Fin m, ∑ j : Fin m,
          c i * starRingEnd ℂ (c j) *
            S 2 ![euclidTimeReflect (xs i), xs j]).re) ∧
    (∀ (n m : ℕ), ∃ C : ℝ, ∀ (xs : Fin n → Space4) (ys : Fin m → Space4) (R : ℝ),
        0 ≤ R → (∀ i j, R ≤ ‖xs i - ys j‖) →
        ‖S (n+m) (Fin.append xs ys) - S n xs * S m ys‖
          ≤ C * Real.exp (-(1 * R))) ∧
    (∃ xs : Fin 4 → Space4, connected4 S xs ≠ 0) := by
  have hS : wilsonLimitSchwinger Ls Lt N β_seq obs = iidSchwinger :=
    wilsonLimitSchwinger_eq_iid Ls Lt N β_seq obs Hlim
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro n a xs
    rw [hS]
    exact iidSchwinger_trans a xs
  · intro n σ xs
    rw [hS]
    exact iidSchwinger_perm σ xs
  · intro n R xs
    rw [hS]
    exact iidSchwinger_so4 n R xs
  · intro m c xs hpos
    rw [hS]
    exact iidSchwinger_refl_pos_2 m c xs hpos
  · intro n m
    rw [hS]
    exact iidSchwinger_cluster n m
  · rw [hS]
    exact iidSchwinger_non_gaussian

end YangMills
