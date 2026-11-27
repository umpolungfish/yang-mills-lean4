import re
import subprocess
from pathlib import Path

# --- Helper 1: Inspect Poincare4 & integral_prod_right ---
clay_spec = Path("Imscribing/YangMills/ClaySpec.lean")
poincare_fields = ""
if clay_spec.exists():
    cs_text = clay_spec.read_text(encoding="utf-8")
    m = re.search(r"structure Poincare4.*?(?=\n(?:def|theorem|structure|lemma|abbrev|end))", cs_text, re.S)
    if m:
        print("=== Poincare4 in ClaySpec.lean ===")
        print(m.group(0))
    m2 = re.search(r"(?:def|abbrev) poincareTimeTrans.*?(?=\n(?:def|theorem|structure|lemma|abbrev|end|\n\n))", cs_text, re.S)
    if m2:
        print("=== poincareTimeTrans in ClaySpec.lean ===")
        print(m2.group(0))

prod_lean = Path(".lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean")
if prod_lean.exists():
    for i, l in enumerate(prod_lean.read_text(encoding="utf-8").splitlines(), 1):
        if "integral_prod_right" in l and re.match(r"^(?:theorem|lemma)\s+", l):
            print(f"Prod.lean:{i}: {l}")

# --- Helper 2: Patch CanonicalFiniteVolumeBorchers4D.lean ---
p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")

# Add fvb_gaugeGroup_coe_inv_star right after open statements
inv_star_lemma = '''
private lemma fvb_gaugeGroup_coe_inv_star {N : ℕ} (A : GaugeGroup N) :
    ((A⁻¹ : GaugeGroup N) : Matrix (Fin N) (Fin N) ℂ) = star (A : Matrix (Fin N) (Fin N) ℂ) := by
  have h1 : (A : Matrix (Fin N) (Fin N) ℂ) * ((A⁻¹ : GaugeGroup N) : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    congrArg Subtype.val (mul_inv_cancel A)
  have h2 : star (A : Matrix (Fin N) (Fin N) ℂ) * (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff'.mp A.2.1
  calc ((A⁻¹ : GaugeGroup N) : Matrix (Fin N) (Fin N) ℂ)
      = (star (A : Matrix (Fin N) (Fin N) ℂ) * (A : Matrix (Fin N) (Fin N) ℂ)) *
          ((A⁻¹ : GaugeGroup N) : Matrix (Fin N) (Fin N) ℂ) := by rw [h2, Matrix.one_mul]
    _ = star (A : Matrix (Fin N) (Fin N) ℂ) *
          ((A : Matrix (Fin N) (Fin N) ℂ) * ((A⁻¹ : GaugeGroup N) : Matrix (Fin N) (Fin N) ℂ)) := by
          rw [Matrix.mul_assoc]
    _ = star (A : Matrix (Fin N) (Fin N) ℂ) := by rw [h1, Matrix.mul_one]
'''

if "fvb_gaugeGroup_coe_inv_star" not in text:
    text = text.replace(
        "private lemma reflectSite_sub_step0_cutMid",
        inv_star_lemma + "\nprivate lemma reflectSite_sub_step0_cutMid"
    )

# Inject SecondCountableTopology and ContinuousInv before MeasurableMul₂
old_inst_block = """  haveI : BorelSpace (GaugeGroup N) := ⟨rfl⟩
  haveI : MeasurableMul₂ (GaugeGroup N) := ContinuousMul.measurableMul₂
  haveI : MeasurableInv (GaugeGroup N) := ContinuousInv.measurableInv"""

new_inst_block = """  haveI : BorelSpace (GaugeGroup N) := ⟨rfl⟩
  haveI : SecondCountableTopology (Matrix (Fin N) (Fin N) ℂ) :=
    inferInstanceAs (SecondCountableTopology (Fin N → Fin N → ℂ))
  haveI : SecondCountableTopology (GaugeGroup N) :=
    Topology.IsInducing.secondCountableTopology
      (⟨rfl⟩ : Topology.IsInducing (Subtype.val : GaugeGroup N → Matrix (Fin N) (Fin N) ℂ))
  haveI : ContinuousInv (GaugeGroup N) :=
    ⟨continuous_induced_rng.mpr (by
      simpa only [Function.comp_def, fvb_gaugeGroup_coe_inv_star] using
        continuous_star.comp continuous_subtype_val)⟩
  haveI : MeasurableMul₂ (GaugeGroup N) := ContinuousMul.measurableMul₂
  haveI : MeasurableInv (GaugeGroup N) := ContinuousInv.measurableInv"""

text = text.replace(old_inst_block, new_inst_block)

# Fix integral_prod_right' at line 269
text = text.replace(
    "(h_meas.integral_prod_right').aestronglyMeasurable",
    "h_meas.stronglyMeasurable.integral_prod_right.aestronglyMeasurable"
)

# Add [NeZero M] to evalPosLat and all downstream lemmas
text = text.replace(
    "noncomputable def evalPosLat (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) :\n    ∀ n : ℕ, PosSchwartzSubmodule n → HalfVar N M → ℂ :=\n  fun n fn p =>\n    letI := Classical.propDecidable",
    "noncomputable def evalPosLat (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) :\n    ∀ n : ℕ, PosSchwartzSubmodule n → HalfVar N M → ℂ :=\n  fun n fn p =>\n    letI := Classical.propDecidable\n    haveI : NeZero (2 * M) := ⟨by have := NeZero.pos M; omega⟩"
)

for fn_name in [
    "theorem evalPosLat_vac (N M : ℕ) [NeZero N]",
    "noncomputable def evalPosBorchers (N M : ℕ) [NeZero N]",
    "theorem evalPosBorchers_vac (N M : ℕ) [NeZero N]",
    "theorem evalPosBorchers_add (N M : ℕ) [NeZero N]",
    "theorem evalPosBorchers_smul (N M : ℕ) [NeZero N]",
    "private lemma evalPosBorchers_measurable (N M : ℕ) [NeZero N]",
    "private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N]",
]:
    text = text.replace(fn_name, fn_name + " [NeZero M]")

# Add NeZero (2 * M) inside evalPosBorchers_bounded
text = text.replace(
    "private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :\n    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by\n  classical",
    "private lemma evalPosBorchers_bounded (N M : ℕ) [NeZero N] [NeZero M] (a Z_ren : ℝ) (F : BorchersPos) :\n    ∃ BF : ℝ, 0 ≤ BF ∧ ∀ p : HalfVar N M, ‖evalPosBorchers N M a Z_ren F p‖ ≤ BF := by\n  classical\n  haveI : NeZero (2 * M) := ⟨by have := NeZero.pos M; omega⟩"
)

# Add NeZero (2 * M) inside evalPosBorchers_smul and evalPosBorchers_measurable
text = text.replace(
    "    have h_eq :\n        (∑ xs : Fin n → Lat4 (2 * M),",
    "    haveI : NeZero (2 * M) := ⟨by have := NeZero.pos M; omega⟩\n    have h_eq :\n        (∑ xs : Fin n → Lat4 (2 * M),"
)

# Fix DFinsupp renames
text = text.replace("DFinsupp.sum_add_index'", "DFinsupp.sum_add_index")
text = text.replace("DFinsupp.support_smul\n", "DFinsupp.support_smul c F\n")

# Fix conj_ofReal on inv in latticeBorchersForm_herm
text = text.replace(
    "rw [star_mul, Complex.star_def, Complex.conj_ofReal]",
    "rw [star_mul, Complex.star_def, map_inv₀, Complex.conj_ofReal]"
)

# Fix redundant rfl in Cauchy-Schwarz h3
text = text.replace(
    "rw [star_one, one_mul, mul_assoc, mul_comm (B F G), h_nsq_self]\n        push_cast; rfl",
    "rw [star_one, one_mul, mul_assoc, mul_comm (B F G), h_nsq_self]\n        push_cast"
)

p.write_text(text, encoding="utf-8")
print("\nCanonicalFiniteVolumeBorchers4D.lean patched.")