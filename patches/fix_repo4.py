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


# 1. TransferMatrixToSemigroup.lean: cleanly replace lines 114-127 (`h_lhs` and `h_rhs`)
ls = read_lines("TransferMatrixToSemigroup.lean")
start_idx = next(i for i, l in enumerate(ls) if "have h_lhs :" in l)
end_idx = next(i for i, l in enumerate(ls) if i > start_idx and "have h_eq :" in l)
new_block = [
    "    have h_lhs : Filter.Tendsto (fun m : ℕ => ⟪x, ((T_lat m) ^ Nat.floor (t / a m)) y⟫_ℂ)",
    "        Filter.atTop (𝓝 ⟪x, T t y⟫_ℂ) := by",
    "      rw [tendsto_iff_norm_sub_tendsto_zero]",
    "      have h_le : ∀ m : ℕ, ‖⟪x, ((T_lat m) ^ Nat.floor (t / a m)) y⟫_ℂ - ⟪x, T t y⟫_ℂ‖ ≤",
    "          ‖x‖ * ‖((T_lat m) ^ Nat.floor (t / a m)) y - T t y‖ := fun m => by",
    "        rw [← inner_sub_right]",
    "        exact norm_inner_le_norm x _",
    "      have h_mul : Filter.Tendsto (fun m : ℕ => ‖x‖ * ‖((T_lat m) ^ Nat.floor (t / a m)) y - T t y‖)",
    "          Filter.atTop (𝓝 (‖x‖ * 0)) :=",
    "        (tendsto_const_nhds (x := ‖x‖)).mul (tendsto_iff_norm_sub_tendsto_zero.mp hy)",
    "      rw [mul_zero] at h_mul",
    "      exact squeeze_zero (fun _ => norm_nonneg _) h_le h_mul",
    "    have h_rhs : Filter.Tendsto (fun m : ℕ => ⟪((T_lat m) ^ Nat.floor (t / a m)) x, y⟫_ℂ)",
    "        Filter.atTop (𝓝 ⟪T t x, y⟫_ℂ) := by",
    "      rw [tendsto_iff_norm_sub_tendsto_zero]",
    "      have h_le : ∀ m : ℕ, ‖⟪((T_lat m) ^ Nat.floor (t / a m)) x, y⟫_ℂ - ⟪T t x, y⟫_ℂ‖ ≤",
    "          ‖((T_lat m) ^ Nat.floor (t / a m)) x - T t x‖ * ‖y‖ := fun m => by",
    "        rw [← inner_sub_left]",
    "        exact norm_inner_le_norm _ y",
    "      have h_mul : Filter.Tendsto (fun m : ℕ => ‖((T_lat m) ^ Nat.floor (t / a m)) x - T t x‖ * ‖y‖)",
    "          Filter.atTop (𝓝 (0 * ‖y‖)) :=",
    "        (tendsto_iff_norm_sub_tendsto_zero.mp hx).mul (tendsto_const_nhds (x := ‖y‖))",
    "      rw [zero_mul] at h_mul",
    "      exact squeeze_zero (fun _ => norm_nonneg _) h_le h_mul",
]
ls = ls[:start_idx] + new_block + ls[end_idx:]
write_lines("TransferMatrixToSemigroup.lean", ls)

# 2. AsymptoticFreedomAndOSClosure.lean: replace looping simp on line 117
ls = read_lines("AsymptoticFreedomAndOSClosure.lean")
out = []
for l in ls:
    if "Subsingleton.elim (![] : Fin 0 → Spacetime4) 0" in l:
        out.append("      rw [show (![] : Fin 0 → Spacetime4) = 0 from Subsingleton.elim _ _, norm_zero, zero_pow hk, zero_mul]")
        out.append("      exact zero_le_one")
    else:
        out.append(l)
write_lines("AsymptoticFreedomAndOSClosure.lean", out)

# 3. IBPBoundaryToWightman.lean: fix line 138 and dump lines 40-58 & 265-282
ls = read_lines("IBPBoundaryToWightman.lean")
out = []
for l in ls:
    if "simpa [F', h_eq] using hd.const_mul (2 * C f)" in l:
        indent = l[: len(l) - len(l.lstrip())]
        out.append(f"{indent}convert hd.const_mul (2 * C f) using 1")
        out.append(f"{indent}dsimp [F']")
        out.append(f"{indent}exact h_eq.symm")
    else:
        out.append(l)
write_lines("IBPBoundaryToWightman.lean", out)
dump("IBPBoundaryToWightman.lean", 40, 58)
dump("IBPBoundaryToWightman.lean", 265, 282)