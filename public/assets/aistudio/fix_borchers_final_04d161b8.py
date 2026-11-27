import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# 1. Fix m4 in glueConfig_action_measurable
text = text.replace(
    """    have m4 : Measurable (fun U : LinkConfig N (2 * M) => (U x ν)⁻¹) :=
      ((measurable_pi_apply _).comp (measurable_pi_apply _)).inv""",
    """    have m4' : Measurable (fun U : LinkConfig N (2 * M) => U x ν) :=
      (measurable_pi_apply ν).comp (measurable_pi_apply x)
    have m4 : Measurable (fun U : LinkConfig N (2 * M) => (U x ν)⁻¹) := m4'.inv"""
)

# 2. Fix ml3 and ml4 in evalPosBorchers_measurable
text = text.replace(
    """    have ml3 : Measurable (fun p : HalfVar N M => (p.1 (x + stepDir (2 * M) j.succ) i.succ)⁻¹) :=
      ((measurable_pi_apply i.succ).comp ((measurable_pi_apply (x + stepDir (2 * M) j.succ)).comp measurable_fst)).inv
    have ml4 : Measurable (fun p : HalfVar N M => (p.1 x j.succ)⁻¹) :=
      ((measurable_pi_apply j.succ).comp ((measurable_pi_apply x).comp measurable_fst)).inv""",
    """    have ml3' : Measurable (fun p : HalfVar N M => p.1 (x + stepDir (2 * M) j.succ) i.succ) :=
      (measurable_pi_apply i.succ).comp ((measurable_pi_apply (x + stepDir (2 * M) j.succ)).comp measurable_fst)
    have ml3 : Measurable (fun p : HalfVar N M => (p.1 (x + stepDir (2 * M) j.succ) i.succ)⁻¹) := ml3'.inv
    have ml4' : Measurable (fun p : HalfVar N M => p.1 x j.succ) :=
      (measurable_pi_apply j.succ).comp ((measurable_pi_apply x).comp measurable_fst)
    have ml4 : Measurable (fun p : HalfVar N M => (p.1 x j.succ)⁻¹) := ml4'.inv"""
)

# 3. Fix evalPosBorchers_smul Decidable instance inside h_eq
text = text.replace(
    """    have h_eq :
        (∑ xs : Fin n → Lat4 (2 * M),""",
    """    letI := Classical.propDecidable
    have h_eq :
        (∑ xs : Fin n → Lat4 (2 * M),"""
)

# 4. Fix evalPosBorchers_bounded whnf timeout
text = text.replace(
    """private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :
    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by
  classical""",
    """set_option maxHeartbeats 800000 in
private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :
    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by
  classical
  letI := Classical.propDecidable"""
)
text = text.replace(
    "  dsimp [evalPosBorchers, DFinsupp.sum, BF]",
    "  unfold evalPosBorchers; simp only [DFinsupp.sum, BF]"
)

# 5. Fix latticeBorchersForm_vac outer integral_ofReal
text = text.replace(
    """  simp_rw [h_in]
  rw [integral_ofReal]""",
    """  have h_in_fn : (fun p : HalfVar N M =>
      ∫ q : HalfVar N M, (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂(halfVarHaarMeasure N M)) =
      fun p : HalfVar N M =>
        ((∫ q : HalfVar N M, Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) ∂(halfVarHaarMeasure N M) : ℝ) : ℂ) :=
    funext h_in
  rw [h_in_fn]
  have h_out : (∫ p : HalfVar N M,
      ((∫ q : HalfVar N M, Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) ∂(halfVarHaarMeasure N M) : ℝ) : ℂ)
      ∂(halfVarHaarMeasure N M)) =
      ((∫ p : HalfVar N M,
        ∫ q : HalfVar N M, Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) ∂(halfVarHaarMeasure N M)
        ∂(halfVarHaarMeasure N M) : ℝ) : ℂ) :=
    integral_ofReal
  rw [h_out]"""
)

# 6. Fix simp_rw [h_in] in latticeBorchersForm_sesquilinear using funext h_in
text = text.replace(
    "    simp_rw [h_in]\n    rw [integral_add",
    "    rw [show (fun p => _) = _ from funext h_in]\n    rw [integral_add"
)
text = text.replace(
    "    simp_rw [h_in]\n    rw [integral_const_mul]",
    "    rw [show (fun p => _) = _ from funext h_in]\n    rw [integral_const_mul]"
)

# 7. Fix star_mul ordering in latticeBorchersForm_herm before congr 1
text = text.replace(
    "  rw [star_mul, Complex.star_def, map_inv₀, Complex.conj_ofReal]\n  congr 1",
    "  rw [star_mul, Complex.star_def, map_inv₀, Complex.conj_ofReal, mul_comm _ ((gluePartitionFn N M β : ℂ)⁻¹)]\n  congr 1"
)

# 8. Inspect lines around 769 if there's an extra line in Cauchy-Schwarz
lines = text.splitlines()
for i in range(max(0, len(lines) - 20), len(lines)):
    if "nlinarith" in lines[i] and i > 0 and "linarith" in lines[i-1]:
        pass

# Check line 750-775 just in case
print("=== Tail of CanonicalFiniteVolumeBorchers4D.lean ===")
for idx in range(max(1, len(lines) - 20), len(lines) + 1):
    print(f"{idx:4d}: {lines[idx-1]}")

p.write_text(text, encoding="utf-8")
print("\nPatched CanonicalFiniteVolumeBorchers4D.lean. Building...")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)