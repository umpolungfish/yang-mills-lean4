#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path("Imscribing/YangMills")


def read_lines(rel: str) -> list[str]:
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


def write_lines(rel: str, lines: list[str]) -> None:
    (ROOT / rel).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[UPDATED] {ROOT / rel}")


def dump(rel: str, a: int, b: int) -> None:
    p = ROOT / rel
    if not p.exists():
        print(f"[MISSING] {p}")
        return
    ls = p.read_text(encoding="utf-8").splitlines()
    print(f"=== {p}:{a}-{b} ===")
    for i in range(max(1, a), min(len(ls), b) + 1):
        print(f"{i:4d}: {ls[i - 1]}")


# 1. TransferMatrixToSemigroup.lean (lines 93, 115-122, 194)
p_tms = ROOT / "TransferMatrixToSemigroup.lean"
if p_tms.exists():
    ls = read_lines("TransferMatrixToSemigroup.lean")
    # Fix line 93 (0-idx 92): append Commute.pow_self simp if not present
    if len(ls) >= 93 and "Commute.pow_self" not in ls[92]:
        indent = ls[92][: len(ls[92]) - len(ls[92].lstrip())]
        ls[92] = ls[92] + f"\n{indent}simp only [← ContinuousLinearMap.mul_apply, (Commute.pow_self (T_lat m) k).eq]"
    # Fix broken h_rhs block around lines 116-123
    txt = "\n".join(ls) + "\n"
    txt_new, n = re.subn(
        r"([ \t]*)have h_rhs\b[\s\S]*?(?=\n\1(?:exact|rw|simpa|have h_eq|show|calc)\b)",
        r"""\1have h_rhs : Filter.Tendsto (fun m => ⟪(T_lat m ^ ⌊t / a m⌋₊) x, y⟫_ℂ)
\1    Filter.atTop (𝓝 ⟪(T t) x, y⟫_ℂ) := by
\1  rw [tendsto_iff_norm_sub_tendsto_zero]
\1  refine squeeze_zero (fun _ => norm_nonneg _)
\1    (fun m => by rw [← inner_sub_left]; exact norm_inner_le_norm _ y) ?_
\1  convert (tendsto_iff_norm_sub_tendsto_zero.mp hx).mul_const ‖y‖
\1  simp""",
        txt,
        count=1,
    )
    if n == 0:
        print("[WARN] TransferMatrixToSemigroup.lean: h_rhs block did not match; dumping lines 108-128")
        dump("TransferMatrixToSemigroup.lean", 108, 128)
    # Fix line 194 right before `exact hpow_contr m (ks + kt)`
    txt_new, n2 = re.subn(
        r"(?m)^([ \t]*)rw \[[^\n]+\]\s*\n([ \t]*exact hpow_contr m \(ks \+ kt\) \(\(T_lat m\) x - x\))",
        r"\1rw [heq, pow_succ, ContinuousLinearMap.mul_apply, ← map_sub]\n\2",
        txt_new,
    )
    if n2 == 0:
        print("[WARN] TransferMatrixToSemigroup.lean: line 194 did not match; dumping lines 188-200")
        dump("TransferMatrixToSemigroup.lean", 188, 200)
    p_tms.write_text(txt_new, encoding="utf-8")
    print("[UPDATED] TransferMatrixToSemigroup.lean")

# 2. SemigroupGapBridge.lean (line 113)
p_sgb = ROOT / "SemigroupGapBridge.lean"
if p_sgb.exists():
    ls = read_lines("SemigroupGapBridge.lean")
    if len(ls) >= 113 and "tendsto_const_nhds.inner" in ls[112]:
        m = re.search(r"tendsto_const_nhds\.inner\s+([^\s\)\]]+)", ls[112])
        if m:
            arg = m.group(1)
            repl = (
                "(by rw [tendsto_iff_norm_sub_tendsto_zero]; "
                "refine squeeze_zero (fun _ => norm_nonneg _) "
                "(fun m => by rw [← inner_sub_right]; exact norm_inner_le_norm _ _) ?_; "
                f"convert (tendsto_iff_norm_sub_tendsto_zero.mp {arg}).const_mul _; simp)"
            )
            ls[112] = re.sub(r"\(?tendsto_const_nhds\.inner\s+" + re.escape(arg) + r"\)?", repl, ls[112])
            write_lines("SemigroupGapBridge.lean", ls)
        else:
            dump("SemigroupGapBridge.lean", 105, 122)
    else:
        dump("SemigroupGapBridge.lean", 105, 122)

# 3. CenteredLatticeTranslation4D.lean (lines 57, 68)
p_clt = ROOT / "CenteredLatticeTranslation4D.lean"
if p_clt.exists():
    txt = p_clt.read_text(encoding="utf-8")
    txt_new = re.sub(
        r"have hq0 : q = 0 := by[\s\S]*?(?=\n[ \t]*(?:linarith|rw \[hq0|subst hq0))",
        """have h1 := abs_le.mp h_abs_ij
  have h2 := abs_lt.mp hi
  have h3 := abs_lt.mp hj
  have hdiv : 2 * ((L : ℤ) / 4) + (L : ℤ) / 2 ≤ L := by omega
  have hq0 : q = 0 := by
    by_contra hne
    rcases lt_or_gt_of_ne hne with hlt | hgt
    · have : q ≤ -1 := by omega
      nlinarith
    · have : 1 ≤ q := by omega
      nlinarith""",
        txt,
        count=1,
    )
    # Also ensure hx/hy around line 63-68 use < (L : ℤ) / 4 if currently ≤
    ls = txt_new.splitlines()
    for idx in range(max(0, 58), min(len(ls), 70)):
        if "centeredCoord L (x" in ls[idx] or "centeredCoord L (y" in ls[idx]:
            ls[idx] = ls[idx].replace("≤ (L : ℤ) / 4", "< (L : ℤ) / 4")
    write_lines("CenteredLatticeTranslation4D.lean", ls)

# 4. AsymptoticFreedomAndOSClosure.lean (lines 41, 57, 79, 111, 116)
p_af = ROOT / "AsymptoticFreedomAndOSClosure.lean"
if p_af.exists():
    ls = read_lines("AsymptoticFreedomAndOSClosure.lean")
    for ln in [41, 79]:
        if len(ls) >= ln and "⟨" in ls[ln - 1] and "eventually_atTop" not in ls[ln - 1]:
            ls[ln - 1] = ls[ln - 1].replace("⟨", "Filter.eventually_atTop.mpr ⟨", 1)
    if len(ls) >= 57 and "div_lt_one" in ls[56]:
        ls[56] = re.sub(r"div_lt_one\s+_\s+\(by positivity\)", "(div_lt_one (by positivity)).mpr", ls[56])
    if len(ls) >= 111 and "opNorm_le_bound" in ls[110]:
        ls[110] = re.sub(r"ContinuousMultilinearMap\.opNorm_le_bound\s+_\s+zero_le_one",
                         "ContinuousMultilinearMap.opNorm_le_bound zero_le_one", ls[110])
    if len(ls) >= 116:
        indent = ls[115][: len(ls[115]) - len(ls[115].lstrip())]
        if "Subsingleton.elim" not in ls[115]:
            ls[115] = f"{indent}rw [show ![] = 0 from Subsingleton.elim _ _, norm_zero, zero_pow hk]; norm_num"
    write_lines("AsymptoticFreedomAndOSClosure.lean", ls)

# 5. LatticeRiemannSchwartzBound4D.lean (lines 25, 47)
p_lrs = ROOT / "LatticeRiemannSchwartzBound4D.lean"
if p_lrs.exists():
    ls = read_lines("LatticeRiemannSchwartzBound4D.lean")
    if len(ls) >= 25:
        ls[24] = re.sub(r"div_le_self\s+ha\.le\s+\(by [^\n]+$",
                        "div_le_self ha.le (le_add_of_nonneg_right (sq_nonneg _))", ls[24])
    if len(ls) >= 47 and ";" in ls[46]:
        ls[46] = ls[46].rsplit(";", 1)[0]
    write_lines("LatticeRiemannSchwartzBound4D.lean", ls)

# 6. IBPBoundaryToWightman.lean (lines 51, 94, 198, 242, 268)
p_ibp = ROOT / "IBPBoundaryToWightman.lean"
if p_ibp.exists():
    ls = read_lines("IBPBoundaryToWightman.lean")
    if len(ls) >= 51 and "HasDerivAt.const_mul (A / (r + 1)) hd" in ls[50]:
        indent = ls[50][: len(ls[50]) - len(ls[50].lstrip())]
        ls[50] = f"{indent}convert HasDerivAt.const_mul (A / (r + 1)) hd using 1\n{indent}rw [← mul_assoc, div_mul_cancel₀ _ (by linarith)]"
    if len(ls) >= 94 and "h_base" in ls[93] and "simpa" not in ls[93]:
        ls[93] = ls[93].replace("h_base", "(by simpa using h_base)")
    if len(ls) >= 198 and "add_le_add_left" in ls[197]:
        ls[197] = re.sub(r"add_le_add_left\s+h1\s+[^\s,\)]+", "add_le_add le_rfl h1", ls[197])
    if len(ls) >= 242 and ";" in ls[241]:
        ls[241] = ls[241].rsplit(";", 1)[0]
    if len(ls) >= 268 and "Real.rpow_le_rpow_of_exponent_ge" in ls[267]:
        ls[267] = ls[267].replace(
            "Real.rpow_le_rpow_of_exponent_ge ht.left ht.right hexp_nonpos",
            "(by simpa using Real.rpow_le_rpow_of_exponent_ge ht.left ht.right hexp_nonpos)",
        )
    write_lines("IBPBoundaryToWightman.lean", ls)

# 7. Dump remaining unseen lines for any follow-up
dump("PoincareLieAlgebraAndNelson.lean", 55, 72)
dump("ClayStatement.lean", 120, 132)
dump("IBPBoundaryToWightman.lean", 130, 160)
dump("IBPBoundaryToWightman.lean", 295, 315)
dump("LatticeOSReflectionPositivity4D.lean", 1, 25)
dump("WilsonHaarCompactness4D.lean", 1, 25)