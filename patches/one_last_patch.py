import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# 1. Fix evalPosBorchers_smul (line 385)
old_smul_2 = """    rw [Finset.mul_sum]
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

new_smul_2 = """    rw [Finset.mul_sum, ← mul_assoc, Finset.mul_sum]
    refine Finset.sum_congr rfl fun xs _ => ?_
    by_cases h_cond : (∀ k : Fin n, ((xs k) 0).val < M)
    · simp only [h_cond, ↓reduceIte]; ring
    · simp only [h_cond, ↓reduceIte, mul_zero]"""

text = text.replace(old_smul_2, new_smul_2)

# 2. Fix evalPosBorchers_bounded (line 473)
old_bd = """  unfold evalPosBorchers DFinsupp.sum
  dsimp only [BF]
  refine le_trans (norm_sum_le _ _) (Finset.sum_le_sum fun n _ => ?_)"""

new_bd = """  change ‖∑ n ∈ F.support, evalPosLat N M a Z_ren n (F n) p‖ ≤
    ∑ n ∈ F.support, ‖(Z_ren ^ n * a ^ (4 * n) : ℂ)‖ *
      ∑ xs : Fin n → Lat4 (2 * M),
        if (∀ k : Fin n, ((xs k) 0).val < M) then
          ‖(F n).1 (fun k => posHalfLatSite M a (xs k))‖ * (18 : ℝ) ^ n
        else 0
  refine le_trans (norm_sum_le F.support _) (Finset.sum_le_sum fun n _ => ?_)"""

text = text.replace(old_bd, new_bd)

# 3. Fix beta-reduction before integral_conj in latticeBorchersForm_herm (line 731)
text = text.replace(
    "  refine integral_congr_ae (Filter.Eventually.of_forall fun p => ?_)\n  rw [← integral_conj]",
    "  refine integral_congr_ae (Filter.Eventually.of_forall fun p => ?_)\n  dsimp only\n  rw [← integral_conj]"
)

# 4. Fix redundant '; ring' after field_simp [hFG2.ne'] (line 791:42)
text = text.replace(
    "dsimp [r]; field_simp [hFG2.ne']; ring",
    "dsimp [r]; field_simp [hFG2.ne']"
)

p.write_text(text, encoding="utf-8")
print("Patched CanonicalFiniteVolumeBorchers4D.lean.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)