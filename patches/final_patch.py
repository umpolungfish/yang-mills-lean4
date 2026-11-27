import subprocess
from pathlib import Path

# 1. Fix the final rfl in SemigroupToUnitaryGroupCFC.lean
cfc_path = Path("Imscribing/YangMills/SemigroupToUnitaryGroupCFC.lean")
cfc_text = cfc_path.read_text(encoding="utf-8")
cfc_text = cfc_text.replace("simp [h0, h1, h2]⟩", "simp [h0, h1, h2]; rfl⟩")
cfc_path.write_text(cfc_text, encoding="utf-8")
print("Updated SemigroupToUnitaryGroupCFC.lean.")

# 2. Cleanly patch CanonicalFiniteVolumeBorchers4D.lean
p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# 2a. Fix linear_combination -hz at lines 89 & 103
text = text.replace("    linear_combination hz", "    linear_combination -hz")

# 2b. Add a single canonical NeZero (2 * M) instance at the top of the file
inst_2m = "\nprivate instance instNeZeroTwoMul (M : ℕ) [NeZero M] : NeZero (2 * M) :=\n  ⟨Nat.mul_ne_zero two_ne_zero (NeZero.ne M)⟩\n"
if "instNeZeroTwoMul" not in text:
    text = text.replace(
        "private lemma fvb_gaugeGroup_coe_inv_star",
        inst_2m + "\nprivate lemma fvb_gaugeGroup_coe_inv_star"
    )

# Remove inline NeZero (2 * M) blocks that created competing Fintype instances & omega kernel errors
text = text.replace("    haveI : NeZero (2 * M) := ⟨by have := NeZero.pos M; omega⟩\n", "")
text = text.replace("  haveI : NeZero (2 * M) := ⟨by have := NeZero.pos M; omega⟩\n", "")

# 2c. Add [NeZero M] to posHalfLatSite
text = text.replace(
    "def posHalfLatSite (M : ℕ) (a : ℝ) (x : Lat4 (2 * M)) : ContinuumInterfaces.Spacetime4 :=",
    "def posHalfLatSite (M : ℕ) [NeZero M] (a : ℝ) (x : Lat4 (2 * M)) : ContinuumInterfaces.Spacetime4 :="
)

# 2d. Fix glueConfig_measurable with explicit projections
old_glue_meas = """  refine measurable_pi_iff.mpr fun x => measurable_pi_iff.mpr fun μ => ?_
  dsimp [glueConfig]
  split_ifs
  · exact ((measurable_pi_apply _).comp (measurable_pi_apply _)).comp measurable_fst
  · exact (((measurable_pi_apply _).comp measurable_snd).comp measurable_fst).inv.mul
      (((measurable_pi_apply _).comp measurable_snd).comp measurable_snd)
  · exact (((measurable_pi_apply _).comp measurable_snd).comp measurable_snd).inv.mul
      (((measurable_pi_apply _).comp measurable_snd).comp measurable_fst)
  · dsimp [linkReflect]
    split_ifs
    · exact (((measurable_pi_apply _).comp (measurable_pi_apply _)).comp measurable_fst).comp
        measurable_snd |>.inv
    · exact (((measurable_pi_apply _).comp (measurable_pi_apply _)).comp measurable_fst).comp
        measurable_snd"""

new_glue_meas = """  have mp1 : ∀ y ν, Measurable (fun pq : HalfVar N M × HalfVar N M => pq.1.1 y ν) :=
    fun y ν => (measurable_pi_apply ν).comp ((measurable_pi_apply y).comp (measurable_fst.comp measurable_fst))
  have mp2 : ∀ y ν, Measurable (fun pq : HalfVar N M × HalfVar N M => pq.2.1 y ν) :=
    fun y ν => (measurable_pi_apply ν).comp ((measurable_pi_apply y).comp (measurable_fst.comp measurable_snd))
  refine measurable_pi_iff.mpr fun x => measurable_pi_iff.mpr fun μ => ?_
  dsimp [glueConfig]
  split_ifs
  · exact mp1 x μ
  · exact (((measurable_pi_apply _).comp measurable_snd).comp measurable_fst).inv.mul
      (((measurable_pi_apply _).comp measurable_snd).comp measurable_snd)
  · exact (((measurable_pi_apply _).comp measurable_snd).comp measurable_snd).inv.mul
      (((measurable_pi_apply _).comp measurable_snd).comp measurable_fst)
  · dsimp [linkReflect]
    split_ifs
    · exact (mp2 _ _).inv
    · exact mp2 _ _"""

text = text.replace(old_glue_meas, new_glue_meas)

# 2e. Fix m3 in glueConfig_action_measurable
text = text.replace(
    """    have m3 : Measurable (fun U : LinkConfig N (2 * M) => (U (x + stepDir (2 * M) ν) μ)⁻¹) :=
      ((measurable_pi_apply _).comp (measurable_pi_apply _)).inv""",
    """    have m3' : Measurable (fun U : LinkConfig N (2 * M) => U (x + stepDir (2 * M) ν) μ) :=
      (measurable_pi_apply μ).comp (measurable_pi_apply (x + stepDir (2 * M) ν))
    have m3 : Measurable (fun U : LinkConfig N (2 * M) => (U (x + stepDir (2 * M) ν) μ)⁻¹) := m3'.inv"""
)

# 2f. Fix evalPosBorchers_add
text = text.replace(
    "simp only [AddSubmonoidClass.coe_add, SchwartzMap.add_apply, add_mul]",
    "simp only [Submodule.coe_add, SchwartzMap.add_apply, add_mul]"
)

# 2g. Fix evalPosBorchers_smul notMem_support
text = text.replace(
    """  · intro n _ hn
    have hn0 : (c • F) n = 0 := DFinsupp.not_mem_support_iff.mp hn
    simp [hn0, evalPosLat]""",
    """  · intro n _ hn
    have hn0 : c • F n = 0 := by
      by_contra h_ne
      exact hn (DFinsupp.mem_support_iff.mpr (by simpa [DFinsupp.coe_smul, Pi.smul_apply] using h_ne))
    rcases smul_eq_zero.mp hn0 with hc | hFn
    · simp [hc, evalPosLat]
    · simp [hFn, evalPosLat]"""
)

# 2h. Fix evalPosBorchers_measurable ml1..ml4 with explicit indices
old_ml = """    have ml1 : Measurable (fun p : HalfVar N M => p.1 x i.succ) :=
      ((measurable_pi_apply _).comp (measurable_pi_apply _)).comp measurable_fst
    have ml2 : Measurable (fun p : HalfVar N M => p.1 (x + stepDir (2 * M) i.succ) j.succ) :=
      ((measurable_pi_apply _).comp (measurable_pi_apply _)).comp measurable_fst
    have ml3 : Measurable (fun p : HalfVar N M => (p.1 (x + stepDir (2 * M) j.succ) i.succ)⁻¹) :=
      (((measurable_pi_apply _).comp (measurable_pi_apply _)).comp measurable_fst).inv
    have ml4 : Measurable (fun p : HalfVar N M => (p.1 x j.succ)⁻¹) :=
      (((measurable_pi_apply _).comp (measurable_pi_apply _)).comp measurable_fst).inv"""

new_ml = """    have ml1 : Measurable (fun p : HalfVar N M => p.1 x i.succ) :=
      (measurable_pi_apply i.succ).comp ((measurable_pi_apply x).comp measurable_fst)
    have ml2 : Measurable (fun p : HalfVar N M => p.1 (x + stepDir (2 * M) i.succ) j.succ) :=
      (measurable_pi_apply j.succ).comp ((measurable_pi_apply (x + stepDir (2 * M) i.succ)).comp measurable_fst)
    have ml3 : Measurable (fun p : HalfVar N M => (p.1 (x + stepDir (2 * M) j.succ) i.succ)⁻¹) :=
      ((measurable_pi_apply i.succ).comp ((measurable_pi_apply (x + stepDir (2 * M) j.succ)).comp measurable_fst)).inv
    have ml4 : Measurable (fun p : HalfVar N M => (p.1 x j.succ)⁻¹) :=
      ((measurable_pi_apply j.succ).comp ((measurable_pi_apply x).comp measurable_fst)).inv"""

text = text.replace(old_ml, new_ml)

# 2i. Fix integral_integral_swap in latticeBorchersForm_herm
text = text.replace(
    "  rw [integral_integral_swap (latticeBorchers_integrable N M a hβ Z_ren G F)]",
    """  have h_sw :
      (∫ p : HalfVar N M, ∫ q : HalfVar N M,
          star (evalPosBorchers N M a Z_ren G p) * evalPosBorchers N M a Z_ren F q *
            (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂(halfVarHaarMeasure N M) ∂(halfVarHaarMeasure N M)) =
        (∫ q : HalfVar N M, ∫ p : HalfVar N M,
          star (evalPosBorchers N M a Z_ren G p) * evalPosBorchers N M a Z_ren F q *
            (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂(halfVarHaarMeasure N M) ∂(halfVarHaarMeasure N M)) :=
    integral_integral_swap (latticeBorchers_integrable N M a hβ Z_ren G F)
  rw [h_sw]"""
)

# 2j. Fix Cauchy-Schwarz accidental map_inv₀ and simp only
text = text.replace(
    """    rw [h_add1, h_add2, h_add2, h_smul1, h_smul1, h_smul2, h_smul2, h_smul2, h_smul2,
      latticeBorchersForm_herm N M a hβ Z_ren F G] at h_nn""",
    """    simp only [h_add1, h_add2, h_smul1, h_smul2,
      latticeBorchersForm_herm N M a hβ Z_ren F G] at h_nn"""
)

# Remove accidental map_inv₀ in Cauchy-Schwarz (keep it only in latticeBorchersForm_herm)
cs_marker = "theorem latticeBorchersForm_cauchy_schwarz"
if cs_marker in text:
    before_cs, after_cs = text.split(cs_marker, 1)
    after_cs = after_cs.replace("rw [star_mul, Complex.star_def, map_inv₀, Complex.conj_ofReal]", "rw [star_mul, Complex.star_def, Complex.conj_ofReal]")
    after_cs = after_cs.replace("rw [star_one, one_mul, mul_assoc, mul_comm (B F G), h_nsq_self]\n        push_cast", "rw [star_one, one_mul, mul_assoc, mul_comm (B F G), h_nsq_self]\n        push_cast; rfl")
    text = before_cs + cs_marker + after_cs

p.write_text(text, encoding="utf-8")
print("Updated CanonicalFiniteVolumeBorchers4D.lean.")

print("\n=== 3. Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)