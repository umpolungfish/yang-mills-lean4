import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# 1. Remove the shadowing letI := Classical.propDecidable in evalPosBorchers_bounded
text = text.replace(
    """set_option maxHeartbeats 800000 in
private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :
    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by
  classical
  letI := Classical.propDecidable""",
    """set_option maxHeartbeats 800000 in
private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :
    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by
  classical"""
)

# 2. Fix starRingEnd ℂ simplification in latticeBorchersForm_herm
text = text.replace(
    "rw [wilsonAction_glueConfig_symm N M β p q, star_mul, star_mul, star_star, Complex.conj_ofReal]",
    "rw [wilsonAction_glueConfig_symm N M β p q, map_mul, map_mul, Complex.conj_conj, Complex.conj_ofReal]"
)

p.write_text(text, encoding="utf-8")
print("Patched final 2 lines.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)