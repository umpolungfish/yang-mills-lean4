#!/usr/bin/env python3
from pathlib import Path

p = Path("Imscribing/YangMills/OSContractivityAndGenerator.lean")
txt = p.read_text(encoding="utf-8")

# 1. Add Pow.Real import
if "Mathlib.Analysis.SpecialFunctions.Pow.Real" not in txt:
    txt = txt.replace(
        "import Mathlib.Analysis.SpecialFunctions.Log.Basic",
        "import Mathlib.Analysis.SpecialFunctions.Log.Basic\nimport Mathlib.Analysis.SpecialFunctions.Pow.Real",
    )

# 2. Line 35: RCLike.re_le_norm -> Complex.re_le_norm
txt = txt.replace("RCLike.re_le_norm _", "Complex.re_le_norm _")

# 3. Lines 244 & 255: close map_add' and map_smul' with tendsto_nhds_unique
txt = txt.replace(
    "      rw [heq]\n      exact hx.add hy\n  map_smul' c x := by",
    "      rw [heq]\n      exact hx.add hy\n    exact tendsto_nhds_unique hxy (by simpa [Submodule.coe_add] using hsum)\n  map_smul' c x := by",
)
txt = txt.replace(
    "      rw [heq]\n      exact hx.const_smul c\n\ntheorem semigroupGenerator_tendsto",
    "      rw [heq]\n      exact hx.const_smul c\n    exact tendsto_nhds_unique hcx (by simpa [Submodule.coe_smul] using hsm)\n\ntheorem semigroupGenerator_tendsto",
)

# 4. Lines 288-306: replace innerSL / continuous_id.inner / hstar cleanly
old_symm = """  have h_lhs : Filter.Tendsto
      (fun t : ℝ => ⟪(ψ : H), (t⁻¹ : ℂ) • ((φ : H) - T t φ)⟫_ℂ)
      (𝓝[>] 0) (𝓝 ⟪(ψ : H), semigroupGenerator T φ⟫_ℂ) :=
    ((innerSL ℂ (ψ : H)).continuous.tendsto _).comp (semigroupGenerator_tendsto T φ)
  have h_rhs : Filter.Tendsto
      (fun t : ℝ => ⟪(t⁻¹ : ℂ) • ((ψ : H) - T t ψ), (φ : H)⟫_ℂ)
      (𝓝[>] 0) (𝓝 ⟪semigroupGenerator T ψ, (φ : H)⟫_ℂ) := by
    have hcont : Continuous (fun x : H => ⟪x, (φ : H)⟫_ℂ) := continuous_id.inner continuous_const
    exact (hcont.tendsto _).comp (semigroupGenerator_tendsto T ψ)
  have h_eq : ∀ᶠ t : ℝ in 𝓝[>] 0,
      ⟪(ψ : H), (t⁻¹ : ℂ) • ((φ : H) - T t φ)⟫_ℂ =
        ⟪(t⁻¹ : ℂ) • ((ψ : H) - T t ψ), (φ : H)⟫_ℂ := by
    filter_upwards [self_mem_nhdsWithin] with t (ht : 0 < t)
    rw [inner_smul_right, inner_smul_left, inner_sub_right, inner_sub_left]
    have hstar : star (t⁻¹ : ℂ) = (t⁻¹ : ℂ) := by
      change star (t⁻¹ : ℂ) = (t⁻¹ : ℂ)
      exact Complex.conj_ofReal _
    rw [hstar, h_symm t ht.le (ψ : H) (φ : H)]"""

new_symm = """  have h_lhs : Filter.Tendsto
      (fun t : ℝ => ⟪(ψ : H), (t⁻¹ : ℂ) • ((φ : H) - T t φ)⟫_ℂ)
      (𝓝[>] 0) (𝓝 ⟪(ψ : H), semigroupGenerator T φ⟫_ℂ) := by
    rw [tendsto_iff_norm_sub_tendsto_zero]
    have h_le : ∀ t : ℝ,
        ‖⟪(ψ : H), (t⁻¹ : ℂ) • ((φ : H) - T t φ)⟫_ℂ - ⟪(ψ : H), semigroupGenerator T φ⟫_ℂ‖ ≤
          ‖(ψ : H)‖ * ‖(t⁻¹ : ℂ) • ((φ : H) - T t φ) - semigroupGenerator T φ‖ := fun t => by
      rw [← inner_sub_right]
      exact norm_inner_le_norm (ψ : H) _
    have h_mul : Filter.Tendsto
        (fun t : ℝ => ‖(ψ : H)‖ * ‖(t⁻¹ : ℂ) • ((φ : H) - T t φ) - semigroupGenerator T φ‖)
        (𝓝[>] 0) (𝓝 (‖(ψ : H)‖ * 0)) :=
      (tendsto_const_nhds (x := ‖(ψ : H)‖)).mul
        (tendsto_iff_norm_sub_tendsto_zero.mp (semigroupGenerator_tendsto T φ))
    rw [mul_zero] at h_mul
    exact squeeze_zero (fun _ => norm_nonneg _) h_le h_mul
  have h_rhs : Filter.Tendsto
      (fun t : ℝ => ⟪(t⁻¹ : ℂ) • ((ψ : H) - T t ψ), (φ : H)⟫_ℂ)
      (𝓝[>] 0) (𝓝 ⟪semigroupGenerator T ψ, (φ : H)⟫_ℂ) := by
    rw [tendsto_iff_norm_sub_tendsto_zero]
    have h_le : ∀ t : ℝ,
        ‖⟪(t⁻¹ : ℂ) • ((ψ : H) - T t ψ), (φ : H)⟫_ℂ - ⟪semigroupGenerator T ψ, (φ : H)⟫_ℂ‖ ≤
          ‖(t⁻¹ : ℂ) • ((ψ : H) - T t ψ) - semigroupGenerator T ψ‖ * ‖(φ : H)‖ := fun t => by
      rw [← inner_sub_left]
      exact norm_inner_le_norm _ (φ : H)
    have h_mul : Filter.Tendsto
        (fun t : ℝ => ‖(t⁻¹ : ℂ) • ((ψ : H) - T t ψ) - semigroupGenerator T ψ‖ * ‖(φ : H)‖)
        (𝓝[>] 0) (𝓝 (0 * ‖(φ : H)‖)) :=
      (tendsto_iff_norm_sub_tendsto_zero.mp (semigroupGenerator_tendsto T ψ)).mul
        (tendsto_const_nhds (x := ‖(φ : H)‖))
    rw [zero_mul] at h_mul
    exact squeeze_zero (fun _ => norm_nonneg _) h_le h_mul
  have h_eq : ∀ᶠ t : ℝ in 𝓝[>] 0,
      ⟪(ψ : H), (t⁻¹ : ℂ) • ((φ : H) - T t φ)⟫_ℂ =
        ⟪(t⁻¹ : ℂ) • ((ψ : H) - T t ψ), (φ : H)⟫_ℂ := by
    filter_upwards [self_mem_nhdsWithin] with t (ht : 0 < t)
    rw [inner_smul_right, inner_smul_left, inner_sub_right, inner_sub_left]
    have hstar : (starRingEnd ℂ) (t⁻¹ : ℂ) = (t⁻¹ : ℂ) := by
      rw [← Complex.ofReal_inv]
      exact Complex.conj_ofReal _
    rw [hstar, h_symm t ht.le (ψ : H) (φ : H)]"""

assert old_symm in txt, "old_symm not found"
txt = txt.replace(old_symm, new_symm)

p.write_text(txt, encoding="utf-8")
print("[UPDATED]", p)