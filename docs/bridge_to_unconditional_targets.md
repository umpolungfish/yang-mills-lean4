# Bridge to Unconditional — formal targets

The nine properties required to discharge the §46 unconditional mass-gap claim,
given as Lean formal statements. These are the targets; the task is to prove
them from the corpus's finite-volume lemmas and pass them to the infinite-volume
limit.

```lean
import Mathlib
open scoped BigOperators

variable {ι : Type*} [Fintype ι]

abbrev Config (n : ℕ) := Fin n → EuclideanSpace ℝ (Fin 4)

-- 1. SO(4) rotation invariance
def SO4RotationInvariance (S : (n : ℕ) → Config n → ℝ) : Prop :=
  ∀ (n : ℕ) (R : Matrix (Fin 4) (Fin 4) ℝ),
    R ∈ Matrix.orthogonalGroup (Fin 4) ℝ → R.det = 1 →
    ∀ x : Config n, S n (R • x) = S n x

-- 2. Translation invariance
def TranslationInvariance (S : (n : ℕ) → Config n → ℝ) : Prop :=
  ∀ (n : ℕ) (a : EuclideanSpace ℝ (Fin 4)) (x : Config n),
    S n (fun i => x i + a) = S n x

-- 3. Cluster property with exponential decay
def ClusterProperty (S : (n : ℕ) → Config n → ℝ) (Δ : ℝ) : Prop :=
  ∀ n m : ℕ, ∃ C : ℝ, 0 < C ∧
    ∀ (x : Config n) (y : Config m) (R : ℝ), 0 ≤ R →
      (∀ i j, R ≤ dist (x i) (y j)) →
      |S (n + m) (Fin.append x y) - S n x * S m y| ≤ C * Real.exp (-Δ * R)

-- 4. Osterwalder–Schrader reflection positivity
opaque Theta : ∀ {n : ℕ}, Config n → Config n
def OSReflectionPositivity (S : (n : ℕ) → Config n → ℝ) : Prop :=
  ∀ (k : ℕ) (n : Fin k → ℕ) (x : ∀ i, Config (n i)) (c : Fin k → ℂ),
    0 ≤ Complex.re (∑ i, ∑ j,
      c i * starRingEnd ℂ (c j) *
        (S (n i + n j) (Fin.append (Theta (x i)) (x j)) : ℂ))

-- 5. Nonvanishing connected four-point function
def NonvanishingConnectedFourPoint (Sconn : Config 4 → ℝ) : Prop :=
  ∃ x : Config 4, Sconn x ≠ 0

-- 6. Nontriviality of Schwinger functions
def NontrivialitySchwinger (S : (n : ℕ) → Config n → ℝ) : Prop :=
  ∀ n : ℕ, 1 ≤ n → ∃ x : Config n, S n x ≠ 0

-- 7. Hermitian symmetry of the reflection-positivity kernel
def reflectionKernel (S : (n : ℕ) → Config n → ℝ) {n m : ℕ}
    (x : Config n) (y : Config m) : ℂ :=
  S (n + m) (Fin.append (Theta x) y)
def KernelHermitian (S : (n : ℕ) → Config n → ℝ) : Prop :=
  ∀ (n m : ℕ) (x : Config n) (y : Config m),
    reflectionKernel S x y = starRingEnd ℂ (reflectionKernel S y x)

-- 8. Lattice–continuum limit convergence
opaque Slatt : ℝ → (n : ℕ) → Config n → ℝ
opaque Sinf : (n : ℕ) → Config n → ℝ
def LatticeContinuumLimit : Prop :=
  ∀ n : ℕ, ∀ ε : ℝ, 0 < ε → ∃ M : ℝ, ∀ β : ℝ, M ≤ β →
    ∀ x : Config n, |Slatt β n x - Sinf n x| < ε

-- 9. Vacuum cyclicity and the physical Hilbert space
variable
  (Hphys : Type*) [NormedAddCommGroup Hphys] [InnerProductSpace ℂ Hphys] [CompleteSpace Hphys]
  (U : ∀ g : Unit, Hphys →L[ℂ] Hphys)
  (phi : ∀ n : ℕ, Config n → Hphys →L[ℂ] Hphys)
  (Omega : Hphys)
def VacuumCyclicity : Prop :=
  Closure (Submodule.span ℂ
    { v : Hphys | ∃ (g : Unit) (n : ℕ) (x : Config n),
        v = U g (phi n x Omega) }) = ⊤
```
