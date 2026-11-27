from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# 1. Fix the ZMod cast lemmas (lines 35-88)
text = text.replace(
"""      have hcast := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
      push_cast at hcast
      have h_zero : (2 * (M : ZMod (2 * M))) = 0 := by exact (CharP.cast_eq_zero (ZMod (2 * M)) (2 * M))
      rw [h_zero] at hcast
      linear_combination hcast""",
"""      have hcast := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
      rw [ZMod.natCast_self] at hcast
      push_cast at hcast
      rw [ZMod.natCast_zmod_val] at hcast
      exact hcast"""
)

text = text.replace(
"""      have hcast := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
      push_cast at hcast
      have h_zero : (2 * (M : ZMod (2 * M))) = 0 := by exact (CharP.cast_eq_zero (ZMod (2 * M)) (2 * M))
      rw [h_zero] at hcast
      exact hcast""",
"""      have hcast := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
      rw [ZMod.natCast_self] at hcast
      push_cast at hcast
      rw [ZMod.natCast_zmod_val] at hcast
      exact hcast"""
)

text = text.replace(
"""    have hz := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
    push_cast at hz
    have h_zero : (2 * (M : ZMod (2 * M))) = 0 := by exact (CharP.cast_eq_zero (ZMod (2 * M)) (2 * M))
    rw [h_zero] at hz
    linear_combination hz""",
"""    have hz := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
    rw [ZMod.natCast_self] at hz
    push_cast at hz
    rw [ZMod.natCast_zmod_val] at hz
    linear_combination hz"""
)

# 2. Fix Cauchy-Schwarz calc steps in CanonicalFiniteVolumeBorchers4D.lean
text = text.replace(
"""    have h_nn := latticeBorchersForm_nonneg N M a hβ Z_ren (u • F + v • G)
    change 0 ≤ (B (u • F + v • G) (u • F + v • G)).re at h_nn
    rw [h_add1, h_add2, h_add2, h_smul1, h_smul1, h_smul2, h_smul2, h_smul2, h_smul2,
      latticeBorchersForm_herm N M a hβ Z_ren F G] at h_nn""",
"""    have h_nn := latticeBorchersForm_nonneg N M a hβ Z_ren (u • F + v • G)
    rw [h_add1, h_add2, h_add2, h_smul1, h_smul1, h_smul2, h_smul2, h_smul2, h_smul2,
      latticeBorchersForm_herm N M a hβ Z_ren F G] at h_nn
    change 0 ≤ (star u * u * B F F + star u * v * B F G +
         star v * u * star (B F G) + star v * v * B G G).re at *"""
)

text = text.replace(
"""        calc ((r : ℂ) * star (B F G)) * ((r : ℂ) * B F G)""",
"""        calc (star (B F G) * (r : ℂ)) * ((r : ℂ) * B F G)"""
)

text = text.replace(
"""      have h2 : star ((r : ℂ) * B F G) * 1 * B F G = ((r * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by
        rw [star_mul, Complex.star_def, Complex.conj_ofReal, mul_one, mul_assoc, h_nsq_self]
        push_cast; rfl""",
"""      have h2 : star ((r : ℂ) * B F G) * 1 * B F G = ((r * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by
        rw [star_mul, Complex.star_def, Complex.conj_ofReal, mul_one]
        calc (star (B F G) * (r : ℂ)) * B F G = (r : ℂ) * (star (B F G) * B F G) := by ring
          _ = ((r * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by rw [h_nsq_self]; push_cast; rfl"""
)

p.write_text(text, encoding="utf-8")
print("Patched ZMod and Cauchy-Schwarz blocks.")

# Print the remaining context blocks needed for the final patch
lines = text.splitlines()
print("\n=== CanonicalFiniteVolumeBorchers4D.lean lines 255-278 ===")
for i in range(255, min(len(lines)+1, 279)):
    print(f"{i:4d}: {lines[i-1]}")

print("\n=== CanonicalFiniteVolumeBorchers4D.lean lines 315-395 ===")
for i in range(315, min(len(lines)+1, 396)):
    print(f"{i:4d}: {lines[i-1]}")

print("\n=== CanonicalFiniteVolumeBorchers4D.lean lines 465-505 ===")
for i in range(465, min(len(lines)+1, 506)):
    print(f"{i:4d}: {lines[i-1]}")

print("\n=== CanonicalFiniteVolumeBorchers4D.lean lines 555-645 ===")
for i in range(555, min(len(lines)+1, 646)):
    print(f"{i:4d}: {lines[i-1]}")