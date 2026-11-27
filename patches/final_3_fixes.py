import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# 1. Line 387: evalPosBorchers_smul
text = text.replace(
    """    by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
    · simp only [h_cond, ↓reduceIte]; ring
    · simp only [h_cond, ↓reduceIte, mul_zero]""",
    """    by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
    · simp [h_cond]; ring
    · simp [h_cond]"""
)

# 2. Line 459: evalPosBorchers_bounded
old_bd2 = """  change ‖∑ n ∈ F.support, evalPosLat N M a Z_ren n (F n) p‖ ≤
    ∑ n ∈ F.support, ‖(Z_ren ^ n * a ^ (4 * n) : ℂ)‖ *
      ∑ xs : Fin n → Lat4 (2 * M),
        if (∀ k : Fin n, ((xs k) 0).val < M) then
          ‖(F n).1 (fun k => posHalfLatSite M a (xs k))‖ * (18 : ℝ) ^ n
        else 0
  refine le_trans (norm_sum_le F.support _) (Finset.sum_le_sum fun n _ => ?_)"""

new_bd2 = """  unfold evalPosBorchers DFinsupp.sum
  dsimp only [BF]
  refine le_trans (norm_sum_le F.support (fun n => evalPosLat N M a Z_ren n (F n) p))
    (Finset.sum_le_sum fun n _ => ?_)"""

text = text.replace(old_bd2, new_bd2)

text = text.replace(
    """  by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
  · simp only [h_cond, ↓reduceIte]
    rw [norm_mul, norm_prod]""",
    """  by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
  · simp only [h_cond, ↓reduceIte]
    rw [norm_mul, norm_prod]"""
)

# Make sure both sides of if reduce cleanly under h_cond regardless of Decidable instance
text = text.replace(
    """  · simp only [h_cond, ↓reduceIte]
    rw [norm_mul, norm_prod]
    refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
    calc ∏ k : Fin n, ‖(spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ)‖
        ≤ ∏ _k : Fin n, (18 : ℝ) :=
          Finset.prod_le_prod (fun _ _ => norm_nonneg _) fun k _ => by
            rw [Complex.norm_real, Real.norm_of_nonneg (spatialPlaqDensity_bounds N (2 * M) p.1 _).1]
            exact (spatialPlaqDensity_bounds N (2 * M) p.1 _).2
      _ = (18 : ℝ) ^ n := by simp [Finset.prod_const]
  · simp only [h_cond, ↓reduceIte, norm_zero, le_refl]""",
    """  · simp [h_cond]
    rw [norm_mul, norm_prod]
    refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
    calc ∏ k : Fin n, ‖(spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ)‖
        ≤ ∏ _k : Fin n, (18 : ℝ) :=
          Finset.prod_le_prod (fun _ _ => norm_nonneg _) fun k _ => by
            rw [Complex.norm_real, Real.norm_of_nonneg (spatialPlaqDensity_bounds N (2 * M) p.1 _).1]
            exact (spatialPlaqDensity_bounds N (2 * M) p.1 _).2
      _ = (18 : ℝ) ^ n := by simp [Finset.prod_const]
  · simp [h_cond]"""
)

# 3. Line 726: beta-reduce before wilsonAction_glueConfig_symm
text = text.replace(
    "  refine integral_congr_ae (Filter.Eventually.of_forall fun q => ?_)\n  rw [wilsonAction_glueConfig_symm",
    "  refine integral_congr_ae (Filter.Eventually.of_forall fun q => ?_)\n  dsimp only\n  rw [wilsonAction_glueConfig_symm"
)

p.write_text(text, encoding="utf-8")
print("Patched the final 3 tactics.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)