#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("Imscribing/YangMills")


def read_lines(rel: str) -> list[str]:
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


def write_lines(rel: str, lines: list[str]) -> None:
    (ROOT / rel).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[UPDATED] {ROOT / rel}")


def dump(rel: str, a: int, b: int) -> None:
    ls = read_lines(rel)
    print(f"=== {ROOT / rel}:{a}-{b} ===")
    for i in range(max(1, a), min(len(ls), b) + 1):
        print(f"{i:4d}: {ls[i - 1]}")


# 1. PoincareLieAlgebraAndNelson.lean: replace `ring` in both branches (lines 60 & 65)
ls = read_lines("PoincareLieAlgebraAndNelson.lean")
out = []
for i, l in enumerate(ls):
    if l.strip() == "ring" and i > 0 and ls[i - 1].strip() == "dsimp [K]":
        indent = l[: len(l) - len(l.lstrip())]
        # First branch uses h_JH, second branch uses h_JP
        if any("h_JH" in x for x in out[-10:]):
            out.append(f"{indent}rw [← smul_sub, h_JP ψ, smul_neg, neg_smul]")
        else:
            out.append(f"{indent}rw [← smul_sub, h_JH ψ]")
    else:
        out.append(l)
write_lines("PoincareLieAlgebraAndNelson.lean", out)

# 2. TransferMatrixToSemigroup.lean: fix lines 94-97 and line 203
ls = read_lines("TransferMatrixToSemigroup.lean")
out = []
for i, l in enumerate(ls):
    if "Commute.pow_self" in l:
        continue
    if l.strip() == "rw [hT_symm m, ih]":
        indent = l[: len(l) - len(l.lstrip())]
        out.append(l)
        out.append(f"{indent}congr 1")
        out.append(f"{indent}rw [← ContinuousLinearMap.mul_apply, ← pow_succ, pow_succ', ContinuousLinearMap.mul_apply]")
    elif "← ContinuousLinearMap.mul_apply, ← pow_succ', pow_succ" in l:
        indent = l[: len(l) - len(l.lstrip())]
        out.append(f"{indent}· rw [heq, pow_succ, ContinuousLinearMap.mul_apply, ← map_sub]")
    else:
        out.append(l)
write_lines("TransferMatrixToSemigroup.lean", out)

# 3. SemigroupGapBridge.lean: clean multi-line h_inner proof around line 113
ls = read_lines("SemigroupGapBridge.lean")
out = []
for l in ls:
    if "tendsto_iff_norm_sub_tendsto_zero" in l and "squeeze_zero" in l:
        out.append("      by")
        out.append("        rw [tendsto_iff_norm_sub_tendsto_zero]")
        out.append("        have h_le : ∀ t : ℝ, ‖⟪ψ, (t⁻¹ : ℂ) • (ψ - T t ψ)⟫_ℂ - ⟪ψ, Hψ⟫_ℂ‖ ≤")
        out.append("            ‖ψ‖ * ‖(t⁻¹ : ℂ) • (ψ - T t ψ) - Hψ‖ := fun t => by")
        out.append("          rw [← inner_sub_right]")
        out.append("          exact norm_inner_le_norm ψ _")
        out.append("        have h_mul : Filter.Tendsto (fun t : ℝ => ‖ψ‖ * ‖(t⁻¹ : ℂ) • (ψ - T t ψ) - Hψ‖)")
        out.append("            (𝓝[>] 0) (𝓝 (‖ψ‖ * 0)) :=")
        out.append("          (tendsto_const_nhds (x := ‖ψ‖)).mul (tendsto_iff_norm_sub_tendsto_zero.mp h_gen)")
        out.append("        rw [mul_zero] at h_mul")
        out.append("        exact squeeze_zero (fun _ => norm_nonneg _) h_le h_mul")
    else:
        out.append(l)
write_lines("SemigroupGapBridge.lean", out)

# 4. AsymptoticFreedomAndOSClosure.lean: fix line 57 and lines 116-117
dump("AsymptoticFreedomAndOSClosure.lean", 30, 58)
ls = read_lines("AsymptoticFreedomAndOSClosure.lean")
out = []
i = 0
while i < len(ls):
    l = ls[i]
    if "div_lt_one (by norm_num) (by positivity)" in l:
        indent = l[: len(l) - len(l.lstrip())]
        out.append(f"{indent}exact (div_lt_one (by positivity)).mpr (by have : (0 : ℝ) ≤ m := Nat.cast_nonneg m; linarith)")
        i += 1
    elif l.strip() == "simp [zero_pow hk]" and i + 1 < len(ls) and ls[i + 1].strip() == "simp [zero_pow hk]":
        out.append("    · subst hn")
        out.append("      simp [Subsingleton.elim (![] : Fin 0 → Spacetime4) 0, zero_pow hk]")
        i += 2
    else:
        out.append(l)
        i += 1
write_lines("AsymptoticFreedomAndOSClosure.lean", out)

# 5. IBPBoundaryToWightman.lean: fix line 152 positivity on C f
ls = read_lines("IBPBoundaryToWightman.lean")
out = []
for l in ls:
    if l.strip() == "have hFx_nn : 0 ≤ F x := by dsimp [F]; positivity":
        indent = l[: len(l) - len(l.lstrip())]
        out.append(f"{indent}have hCf_nn : 0 ≤ C f := by")
        out.append(f"{indent}  have h1 := le_trans (norm_nonneg (W_reg x (D_ibp f))) (h_half f x ⟨hx, le_trans hxy hy1⟩)")
        out.append(f"{indent}  exact nonneg_of_mul_nonneg_left h1 (Real.rpow_pos_of_pos hx _)")
        out.append(f"{indent}have hFx_nn : 0 ≤ F x := by")
        out.append(f"{indent}  dsimp [F]")
        out.append(f"{indent}  exact mul_nonneg (mul_nonneg (by norm_num) hCf_nn) (Real.sqrt_nonneg x)")
    else:
        out.append(l)
write_lines("IBPBoundaryToWightman.lean", out)