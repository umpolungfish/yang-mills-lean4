import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# 1. Fix evalPosBorchers_smul without h_eq / Decidable mismatch
old_smul_block = """    letI := Classical.propDecidable
    have h_eq :
        (∑ xs : Fin n → Lat4 (2 * M),
          if (∀ k : Fin n, ((xs k) 0).val < M) then
            (c * (F n).1 (fun k => posHalfLatSite M a (xs k))) *
              (∏ k : Fin n, (spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ))
          else 0) =
        c * ∑ xs : Fin n → Lat4 (2 * M),
          if (∀ k : Fin n, ((xs k) 0).val < M) then
            (F n).1 (fun k => posHalfLatSite M a (xs k)) *
              (∏ k : Fin n, (spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ))
          else 0 := by
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun xs _ => ?_
      split_ifs <;> ring
    rw [h_eq]; ring"""

new_smul_block = """    rw [Finset.mul_sum]
    rw [show (c * ((Z_ren ^ n * a ^ (4 * n) : ℂ) * ∑ xs : Fin n → Lat4 (2 * M),
          if (∀ k : Fin n, ((xs k) 0).val < M) then
            (F n).1 (fun k => posHalfLatSite M a (xs k)) *
              (∏ k : Fin n, (spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ))
          else 0)) =
        ∑ xs : Fin n → Lat4 (2 * M),
          c * ((Z_ren ^ n * a ^ (4 * n) : ℂ) *
            if (∀ k : Fin n, ((xs k) 0).val < M) then
              (F n).1 (fun k => posHalfLatSite M a (xs k)) *
                (∏ k : Fin n, (spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ))
            else 0) by
      rw [← Finset.mul_sum, ← Finset.mul_sum]]
    refine Finset.sum_congr rfl fun xs _ => ?_
    by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
    · simp only [h_cond, ↓reduceIte]; ring
    · simp only [h_cond, ↓reduceIte, mul_zero]"""

if old_smul_block in text:
    text = text.replace(old_smul_block, new_smul_block)
else:
    print("Warning: old_smul_block not matched verbatim.")

# 2. Fix evalPosBorchers_bounded unfolding & by_cases
text = text.replace(
    "  unfold evalPosBorchers; simp only [DFinsupp.sum, BF]",
    "  unfold evalPosBorchers DFinsupp.sum\n  dsimp only [BF]"
)
text = text.replace(
    """  split_ifs
  · rw [norm_mul, norm_prod]""",
    """  by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
  · simp only [h_cond, ↓reduceIte]
    rw [norm_mul, norm_prod]"""
)
text = text.replace(
    """      _ = (18 : ℝ) ^ n := by simp [Finset.prod_const]
  · simp""",
    """      _ = (18 : ℝ) ^ n := by simp [Finset.prod_const]
  · simp only [h_cond, ↓reduceIte, norm_zero, le_refl]"""
)

# 3. Fix h_sw in latticeBorchersForm_herm to match starRingEnd ℂ
text = text.replace(
    """  have h_sw :
      (∫ p : HalfVar N M, ∫ q : HalfVar N M,
          star (evalPosBorchers N M a Z_ren G p) * evalPosBorchers N M a Z_ren F q *
            (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂(halfVarHaarMeasure N M) ∂(halfVarHaarMeasure N M)) =
        (∫ q : HalfVar N M, ∫ p : HalfVar N M,
          star (evalPosBorchers N M a Z_ren G p) * evalPosBorchers N M a Z_ren F q *
            (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂(halfVarHaarMeasure N M) ∂(halfVarHaarMeasure N M)) :=
    integral_integral_swap (latticeBorchers_integrable N M a hβ Z_ren G F)""",
    """  have h_sw :
      (∫ p : HalfVar N M, ∫ q : HalfVar N M,
          (starRingEnd ℂ) (evalPosBorchers N M a Z_ren G p) * evalPosBorchers N M a Z_ren F q *
            (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂(halfVarHaarMeasure N M) ∂(halfVarHaarMeasure N M)) =
        (∫ q : HalfVar N M, ∫ p : HalfVar N M,
          (starRingEnd ℂ) (evalPosBorchers N M a Z_ren G p) * evalPosBorchers N M a Z_ren F q *
            (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂(halfVarHaarMeasure N M) ∂(halfVarHaarMeasure N M)) := by
    simpa only [Complex.star_def] using
      integral_integral_swap (latticeBorchers_integrable N M a hβ Z_ren G F)"""
)

# 4. Fix duplicate '; rfl' in Cauchy-Schwarz if present
text = text.replace("push_cast; rfl; rfl", "push_cast; rfl")

# Check tail lines around 770-795 for any stray tactic
lines = text.splitlines()
for idx in range(max(0, len(lines) - 25), len(lines)):
    if idx + 1 >= 780 and idx + 1 <= 795:
        print(f"{idx+1:4d}: {lines[idx]}")

p.write_text(text, encoding="utf-8")

print("\n=== Building Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)