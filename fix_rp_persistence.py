import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/ContinuumRPAndClusterPersistence.lean")
text = p.read_text(encoding="utf-8")

# 1. Line 65: ge_of_tendsto
text = text.replace(
    "exact le_of_tendsto h1 (Filter.Eventually.of_forall fun m => h_rp_m m F)",
    "exact ge_of_tendsto h1 (Filter.Eventually.of_forall fun m => h_rp_m m F)"
)

# 2. Lines 98 & 118: simp only instead of extra rw
text = text.replace(
    """      rw [hs, h_add_l, h_add_r, h_add_r, h_smul_l, h_smul_r, h_smul_r, h_smul_l, h_smul_r]
      simp only [star_neg]
      ring""",
    """      rw [hs]
      simp only [h_add_l, h_add_r, h_smul_l, h_smul_r, star_neg]
      ring"""
)

# 3. Lines 138 & 160: simpa only [Function.comp_apply, sub_zero, add_zero]
text = text.replace(
    "      simpa using (Complex.continuous_re.tendsto _).comp hC",
    "      simpa only [Function.comp_apply, sub_zero, add_zero] using (Complex.continuous_re.tendsto _).comp hC"
)
text = text.replace(
    "        simpa using (Complex.continuous_re.tendsto _).comp hC",
    "        simpa only [Function.comp_apply, sub_zero, add_zero] using (Complex.continuous_re.tendsto _).comp hC"
)

# 4. Line 161: close h_rhs_tend and unindent le_of_tendsto_of_tendsto
text = text.replace(
    """        simpa only [Function.comp_apply, sub_zero, add_zero] using (Complex.continuous_re.tendsto _).comp hC
      exact le_of_tendsto_of_tendsto h_lhs_tend h_rhs_tend (Filter.Eventually.of_forall h_ineq_m)""",
    """        simpa only [Function.comp_apply, sub_zero, add_zero] using (Complex.continuous_re.tendsto _).comp hC
      exact tendsto_const_nhds.mul h_G_tend
    exact le_of_tendsto_of_tendsto h_lhs_tend h_rhs_tend (Filter.Eventually.of_forall h_ineq_m)"""
)

p.write_text(text, encoding="utf-8")
print("Patched ContinuumRPAndClusterPersistence.lean.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)