import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

start_marker = "private lemma evalPosLat_norm_le"
end_marker = "private lemma latticeBorchers_integrable"

before, rest = text.split(start_marker, 1)
_, after = rest.split(end_marker, 1)

new_block = '''private noncomputable def evalPosLatBound (M : ℕ) [NeZero M] (a Z_ren : ℝ)
    (n : ℕ) (fn : PosSchwartzSubmodule n) : ℝ :=
  letI := Classical.propDecidable
  ‖(Z_ren ^ n * a ^ (4 * n) : ℂ)‖ *
    ∑ xs : Fin n → Lat4 (2 * M),
      if (∀ k : Fin n, ((xs k) 0).val < M) then
        ‖fn.1 (fun k => posHalfLatSite M a (xs k))‖ * (18 : ℝ) ^ n
      else 0

private lemma evalPosLat_norm_le (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ)
    (n : ℕ) (fn : PosSchwartzSubmodule n) (p : HalfVar N M) :
    ‖evalPosLat N M a Z_ren n fn p‖ ≤ evalPosLatBound M a Z_ren n fn := by
  unfold evalPosLat evalPosLatBound
  rw [norm_mul]
  refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
  refine le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun xs _ => ?_)
  split_ifs
  · rw [norm_mul, norm_prod]
    refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
    calc ∏ k : Fin n, ‖(spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ)‖
        ≤ ∏ _k : Fin n, (18 : ℝ) :=
          Finset.prod_le_prod (fun _ _ => norm_nonneg _) fun k _ => by
            rw [Complex.norm_real, Real.norm_of_nonneg (spatialPlaqDensity_bounds N (2 * M) p.1 _).1]
            exact (spatialPlaqDensity_bounds N (2 * M) p.1 _).2
      _ = (18 : ℝ) ^ n := by simp only [Finset.prod_const, Finset.card_fin]
  · simp only [norm_zero, le_refl]

private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :
    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by
  refine ⟨∑ n ∈ F.support, evalPosLatBound M a Z_ren n (F n),
    Finset.sum_nonneg fun n _ => ?_, fun p => ?_⟩
  · unfold evalPosLatBound
    exact mul_nonneg (norm_nonneg _) (Finset.sum_nonneg fun xs _ => by split_ifs <;> positivity)
  · unfold evalPosBorchers DFinsupp.sum
    exact le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun n _ => evalPosLat_norm_le N M a Z_ren n (F n) p)

'''

p.write_text(before + new_block + end_marker + after, encoding="utf-8")
print("Updated evalPosLatBound / evalPosBorchers_bounded cleanly.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)