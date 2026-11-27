import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

old_branch = """  by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
  · simp [h_cond, norm_mul, norm_prod]
    refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
    calc ∏ k : Fin n, ‖(spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ)‖
        ≤ ∏ _k : Fin n, (18 : ℝ) :=
          Finset.prod_le_prod (fun _ _ => norm_nonneg _) fun k _ => by
            rw [Complex.norm_real, Real.norm_of_nonneg (spatialPlaqDensity_bounds N (2 * M) p.1 _).1]
            exact (spatialPlaqDensity_bounds N (2 * M) p.1 _).2
      _ = (18 : ℝ) ^ n := by simp [Finset.prod_const]
  · simp [h_cond]"""

new_branch = """  split_ifs
  · rw [norm_mul, norm_prod]
    refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
    calc ∏ k : Fin n, ‖(spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ)‖
        ≤ ∏ _k : Fin n, (18 : ℝ) :=
          Finset.prod_le_prod (fun _ _ => norm_nonneg _) fun k _ => by
            rw [Complex.norm_real, Real.norm_of_nonneg (spatialPlaqDensity_bounds N (2 * M) p.1 _).1]
            exact (spatialPlaqDensity_bounds N (2 * M) p.1 _).2
      _ = (18 : ℝ) ^ n := by simp only [Finset.prod_const, Finset.card_fin]
  · simp only [norm_zero, le_refl]"""

text = text.replace(old_branch, new_branch)

text = text.replace(
    "(Finset.sum_nonneg fun xs _ => by by_cases h : (∀ k : Fin n, ((xs k) 0).val < M) <;> simp [h]; positivity)",
    "(Finset.sum_nonneg fun xs _ => by split_ifs <;> positivity)"
)

p.write_text(text, encoding="utf-8")
print("Applied micro-fix.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)