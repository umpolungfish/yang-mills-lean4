import subprocess
from pathlib import Path

print("=== 1. Patching SemigroupToUnitaryGroupCFC.lean with correct namespace ===")
cfc_path = Path("Imscribing/YangMills/SemigroupToUnitaryGroupCFC.lean")
lean_cfc = '''/-
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
Strictly 0 sorries.
-/

open ContinuousLinearMap

namespace Imscribing.YangMills.SemigroupCFC

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

/-- Euclidean transfer semigroup operator: T(t) = exp(-t H) -/
noncomputable def euclideanSemigroup (H : E →L[ℂ] E) (t : ℝ) : E →L[ℂ] E :=
  cfc (fun (x : ℂ) => Complex.exp (-(t : ℂ) * x)) H

/-- Real-time unitary evolution group: U(t) = exp(i t H) -/
noncomputable def unitaryGroup (H : E →L[ℂ] E) (t : ℝ) : E →L[ℂ] E :=
  cfc (fun (x : ℂ) => Complex.exp (Complex.I * (t : ℂ) * x)) H

section BasicProperties

variable (H : E →L[ℂ] E) [IsStarNormal H]

theorem unitaryGroup_zero : unitaryGroup H 0 = 1 := by
  dsimp [unitaryGroup]
  have h_id : (fun (x : ℂ) => Complex.exp (Complex.I * (0 : ℂ) * x)) = (fun _ => 1) := by
    ext x; simp
  rw [h_id]
  exact cfc_const_one (R := ℂ) H

theorem euclideanSemigroup_zero : euclideanSemigroup H 0 = 1 := by
  dsimp [euclideanSemigroup]
  have h_id : (fun (x : ℂ) => Complex.exp (-(0 : ℂ) * x)) = (fun _ => 1) := by
    ext x; simp
  rw [h_id]
  exact cfc_const_one (R := ℂ) H

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

theorem unitaryGroup_norm_le_one (t : ℝ) (h_spec : ∀ x ∈ spectrum ℂ H, ‖Complex.exp (Complex.I * (t : ℂ) * x)‖ ≤ 1) :
    ‖unitaryGroup H t‖ ≤ 1 :=
  norm_cfc_le zero_le_one h_spec

theorem operator_eq_of_dense {s : Set E} (hs : Dense s)
    {A B : E →L[ℂ] E} (h : ∀ x ∈ s, A x = B x) : A = B :=
  ContinuousLinearMap.ext fun x =>
    congr_fun (Continuous.ext_on hs A.continuous B.continuous h) x

theorem operator_eq_of_dense_submodule {K : Submodule ℂ E} (hK : Dense (K : Set E))
    {A B : E →L[ℂ] E} (h : ∀ x ∈ K, A x = B x) : A = B :=
  operator_eq_of_dense hK fun x hx => h x hx

end BasicProperties

end Imscribing.YangMills.SemigroupCFC
'''
cfc_path.write_text(lean_cfc, encoding="utf-8")
print("SemigroupToUnitaryGroupCFC.lean patched.")

print("\n=== 2. Patching OSPoincareMasterDischarge.lean imports ===")
os_path = Path("Imscribing/YangMills/OSPoincareMasterDischarge.lean")
os_text = os_path.read_text(encoding="utf-8")
if "import Imscribing.YangMills.SpatialISO3UnitariesOnOS" not in os_text:
    os_text = "import Imscribing.YangMills.SpatialISO3UnitariesOnOS\n" + os_text
    os_path.write_text(os_text, encoding="utf-8")
    print("OSPoincareMasterDischarge.lean import added.")
else:
    print("OSPoincareMasterDischarge.lean import already present.")

print("\n=== 3. Patching CanonicalFiniteVolumeBorchers4D.lean ===")
borch_path = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
borch_text = borch_path.read_text(encoding="utf-8")

# Fix 1: Replace .isLt on ZMod with ZMod.val_lt
borch_text = borch_text.replace("(x 0).isLt", "ZMod.val_lt (x 0)")

# Fix 2: Disambiguate Spacetime4
borch_text = borch_text.replace(
    "def posHalfLatSite (M : ℕ) (a : ℝ) (x : Lat4 (2 * M)) : Spacetime4 :=",
    "def posHalfLatSite (M : ℕ) (a : ℝ) (x : Lat4 (2 * M)) : ContinuumInterfaces.Spacetime4 :="
)

# Fix 3: Add [NeZero M] to evalPosLat if missing
borch_text = borch_text.replace(
    "noncomputable def evalPosLat (N M : ℕ) [NeZero N] (a Z_ren : ℝ) :",
    "noncomputable def evalPosLat (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) :"
)

# Fix 4: Fix ZMod.natCast rewrites in the first 4 lemmas
old_rw1 = "rw [ZMod.natCast_zmod_val, ZMod.natCast_self] at hcast"
new_rw1 = "have h_zero : (2 * (M : ZMod (2 * M))) = 0 := by exact (CharP.cast_eq_zero (ZMod (2 * M)) (2 * M))\n      rw [h_zero] at hcast"
borch_text = borch_text.replace(old_rw1, new_rw1)

old_rw2 = "rw [ZMod.natCast_zmod_val, ZMod.natCast_self] at hz"
new_rw2 = "have h_zero : (2 * (M : ZMod (2 * M))) = 0 := by exact (CharP.cast_eq_zero (ZMod (2 * M)) (2 * M))\n    rw [h_zero] at hz"
borch_text = borch_text.replace(old_rw2, new_rw2)

borch_path.write_text(borch_text, encoding="utf-8")
print("CanonicalFiniteVolumeBorchers4D.lean patched.")

print("\n=== 4. Running lake build ===")
cmd = ["lake", "build", "Imscribing.YangMills"]
proc = subprocess.run(cmd)
print("Lake return code:", proc.returncode)