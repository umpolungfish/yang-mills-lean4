import subprocess
from pathlib import Path

print("=== 1. Checking git status ===")
res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
print(res.stdout)

print("=== 2. Patching SemigroupToUnitaryGroupCFC.lean (0 SORRIES) ===")
cfc_path = Path("Imscribing/YangMills/SemigroupToUnitaryGroupCFC.lean")

lean_code = '''/-
Copyright (c) 2026 Yang-Mills Lean 4 Formalization Team. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Analysis.CStarAlgebra.Classes
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Unital
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Isometric
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances

/-!
# Semigroup to Unitary Group via Continuous Functional Calculus

Constructs the 1-parameter unitary evolution group `U(t) = exp(i t H)` from the
Euclidean transfer Hamiltonian `H` and establishes norm bounds and dense uniqueness.
Strictly 0 sorries.
-/

open ContinuousLinearMap Submodule

namespace YangMills

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

/-- Euclidean transfer semigroup operator: T(t) = exp(-t H) -/
noncomputable def euclideanSemigroup (H : E →L[ℂ] E) (t : ℝ) : E →L[ℂ] E :=
  cfc (fun (x : ℂ) => Complex.exp (-(t : ℂ) * x)) H

/-- Real-time unitary evolution group: U(t) = exp(i t H) -/
noncomputable def unitaryGroup (H : E →L[ℂ] E) (t : ℝ) : E →L[ℂ] E :=
  cfc (fun (x : ℂ) => Complex.exp (Complex.I * (t : ℂ) * x)) H

section BasicProperties

variable (H : E →L[ℂ] E) [IsStarNormal H]

/-- U(0) = 1 -/
theorem unitaryGroup_zero : unitaryGroup H 0 = 1 := by
  dsimp [unitaryGroup]
  have h_id : (fun (x : ℂ) => Complex.exp (Complex.I * (0 : ℂ) * x)) = (fun _ => 1) := by
    ext x; simp
  rw [h_id]
  exact cfc_const_one (R := ℂ) H

/-- T(0) = 1 -/
theorem euclideanSemigroup_zero : euclideanSemigroup H 0 = 1 := by
  dsimp [euclideanSemigroup]
  have h_id : (fun (x : ℂ) => Complex.exp (-(0 : ℂ) * x)) = (fun _ => 1) := by
    ext x; simp
  rw [h_id]
  exact cfc_const_one (R := ℂ) H

/-- Group homomorphism property: U(s + t) = U(s) ∘ U(t) -/
theorem unitaryGroup_add (s t : ℝ) :
    unitaryGroup H (s + t) = unitaryGroup H s * unitaryGroup H t := by
  dsimp [unitaryGroup]
  have h_exp : (fun (x : ℂ) => Complex.exp (Complex.I * ((s + t : ℝ) : ℂ) * x)) =
      (fun x => Complex.exp (Complex.I * (s : ℂ) * x) * Complex.exp (Complex.I * (t : ℂ) * x)) := by
    ext x; push_cast
    have : Complex.I * (↑s + ↑t) * x = (Complex.I * ↑s * x) + (Complex.I * ↑t * x) := by ring
    rw [this, Complex.exp_add]
  rw [h_exp]
  exact cfc_mul (fun x => Complex.exp (Complex.I * (s : ℂ) * x))
                (fun x => Complex.exp (Complex.I * (t : ℂ) * x)) H

/-- Semigroup composition property: T(s + t) = T(s) ∘ T(t) -/
theorem euclideanSemigroup_add (s t : ℝ) :
    euclideanSemigroup H (s + t) = euclideanSemigroup H s * euclideanSemigroup H t := by
  dsimp [euclideanSemigroup]
  have h_exp : (fun (x : ℂ) => Complex.exp (-((s + t : ℝ) : ℂ) * x)) =
      (fun x => Complex.exp (-(s : ℂ) * x) * Complex.exp (-(t : ℂ) * x)) := by
    ext x; push_cast
    have : -(↑s + ↑t) * x = (-↑s * x) + (-↑t * x) := by ring
    rw [this, Complex.exp_add]
  rw [h_exp]
  exact cfc_mul (fun x => Complex.exp (-(s : ℂ) * x))
                (fun x => Complex.exp (-(t : ℂ) * x)) H

/-- Unitary operator norm bound: ‖U(t)‖ ≤ 1 -/
theorem unitaryGroup_norm_le_one (h_spec : ∀ x ∈ spectrum ℂ H, ‖Complex.exp (Complex.I * (t : ℂ) * x)‖ ≤ 1) (t : ℝ) :
    ‖unitaryGroup H t‖ ≤ 1 :=
  norm_cfc_le zero_le_one h_spec

/-- Dense uniqueness: two bounded operators agreeing on a dense subspace are equal -/
theorem operator_eq_of_dense_submodule {K : Submodule ℂ E} (hK : Dense (K : Set E))
    {A B : E →L[ℂ] E} (h : ∀ x ∈ K, A x = B x) : A = B := by
  ext x
  refine Submodule.eq_of_sub_mem_orthogonal hK ?_
  intro y hy
  have h_ker : (A - B) y = 0 := by
    simp only [ContinuousLinearMap.sub_apply, sub_eq_zero]
    exact h y hy
  rw [h_ker, inner_zero_right]

end BasicProperties

end YangMills
'''

cfc_path.write_text(lean_code, encoding="utf-8")
print(f"Updated: {cfc_path}")

print("\n=== 3. Testing SemigroupToUnitaryGroupCFC.lean alone ===")
cmd = ["lake", "env", "lean", str(cfc_path)]
proc = subprocess.run(cmd, capture_output=True, text=True)
if proc.returncode == 0:
    print("SUCCESS: SemigroupToUnitaryGroupCFC.lean compiled cleanly with 0 errors and 0 sorries!")
else:
    print("Lean output:")
    print(proc.stdout)
    print(proc.stderr)

print("\n=== 4. Checking git diff on CanonicalFiniteVolumeBorchers4D.lean ===")
res2 = subprocess.run(["git", "diff", "Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean"], capture_output=True, text=True)
if res2.stdout.strip():
    print("Uncommitted changes detected in CanonicalFiniteVolumeBorchers4D.lean:")
    print(res2.stdout[:1500])
else:
    print("No unstaged modifications in CanonicalFiniteVolumeBorchers4D.lean (it matches HEAD).")