import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

start_marker = "set_option maxHeartbeats 800000 in\nprivate lemma evalPosBorchers_bounded"
end_marker = "private lemma latticeBorchers_integrable"

if start_marker not in text or end_marker not in text:
    raise RuntimeError("Could not find evalPosBorchers_bounded markers.")

before, rest = text.split(start_marker, 1)
_, after = rest.split(end_marker, 1)

new_bounded_block = '''private lemma evalPosLat_norm_le (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ)
    (n : ℕ) (fn : PosSchwartzSubmodule n) (p : HalfVar N M) :
    ‖evalPosLat N M a Z_ren n fn p‖ ≤
      ‖(Z_ren ^ n * a ^ (4 * n) : ℂ)‖ *
        ∑ xs : Fin n → Lat4 (2 * M),
          letI := Classical.propDecidable
          if (∀ k : Fin n, ((xs k) 0).val < M) then
            ‖fn.1 (fun k => posHalfLatSite M a (xs k))‖ * (18 : ℝ) ^ n
          else 0 := by
  unfold evalPosLat
  rw [norm_mul]
  refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
  refine le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun xs _ => ?_)
  by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
  · simp [h_cond, norm_mul, norm_prod]
    refine mul_le_mul_of_nonneg_left ?_ (norm_nonneg _)
    calc ∏ k : Fin n, ‖(spatialPlaqDensity N (2 * M) p.1 (xs k) : ℂ)‖
        ≤ ∏ _k : Fin n, (18 : ℝ) :=
          Finset.prod_le_prod (fun _ _ => norm_nonneg _) fun k _ => by
            rw [Complex.norm_real, Real.norm_of_nonneg (spatialPlaqDensity_bounds N (2 * M) p.1 _).1]
            exact (spatialPlaqDensity_bounds N (2 * M) p.1 _).2
      _ = (18 : ℝ) ^ n := by simp [Finset.prod_const]
  · simp [h_cond]

private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :
    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by
  let term : ℕ → ℝ := fun n =>
    ‖(Z_ren ^ n * a ^ (4 * n) : ℂ)‖ *
      ∑ xs : Fin n → Lat4 (2 * M),
        letI := Classical.propDecidable
        if (∀ k : Fin n, ((xs k) 0).val < M) then
          ‖(F n).1 (fun k => posHalfLatSite M a (xs k))‖ * (18 : ℝ) ^ n
        else 0
  refine ⟨∑ n ∈ F.support, term n, Finset.sum_nonneg fun n _ => mul_nonneg (norm_nonneg _)
    (Finset.sum_nonneg fun xs _ => by by_cases h : (∀ k : Fin n, ((xs k) 0).val < M) <;> simp [h]; positivity), fun p => ?_⟩
  unfold evalPosBorchers DFinsupp.sum
  exact le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun n _ => evalPosLat_norm_le N M a Z_ren n (F n) p)

'''

p.write_text(before + new_bounded_block + end_marker + after, encoding="utf-8")
print("Updated evalPosBorchers_bounded cleanly.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)