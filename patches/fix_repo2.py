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


# 1. PoincareLieAlgebraAndNelson.lean: remove no-op `simp only [LinearMap.smul_apply, smul_eq_mul]` before `ring`
ls = read_lines("PoincareLieAlgebraAndNelson.lean")
ls = [l for l in ls if l.strip() != "simp only [LinearMap.smul_apply, smul_eq_mul]"]
write_lines("PoincareLieAlgebraAndNelson.lean", ls)

# 2. ClayStatement.lean: remove `.{0, 0}` on HasYangMillsUVScaling
ls = read_lines("ClayStatement.lean")
ls = [l.replace("HasYangMillsUVScaling.{0, 0}", "HasYangMillsUVScaling") for l in ls]
write_lines("ClayStatement.lean", ls)

# 3. CenteredLatticeTranslation4D.lean: extend `≤` -> `<` to lines 65-78
ls = read_lines("CenteredLatticeTranslation4D.lean")
for idx in range(60, min(len(ls), 80)):
    if "centeredCoord L" in ls[idx] or "hx" in ls[idx] or "hy" in ls[idx]:
        ls[idx] = ls[idx].replace("≤ (L : ℤ) / 4", "< (L : ℤ) / 4")
write_lines("CenteredLatticeTranslation4D.lean", ls)

# 4. IBPBoundaryToWightman.lean: fix line 137 and strip trailing prose after `end Imscribing.YangMills.OSIBPBoundary`
ls = read_lines("IBPBoundaryToWightman.lean")
out = []
for l in ls:
    if "(by simpa [F', h_eq] using hd.const_mul (2 * C f)).congr_of_eventuallyEq h_sqrt_eq.symm" in l:
        indent = l[: len(l) - len(l.lstrip())]
        out.append(f"{indent}have hd' : HasDerivAt (fun u : ℝ => 2 * C f * u ^ (1 / 2 : ℝ)) (F' t) t := by")
        out.append(f"{indent}  simpa [F', h_eq] using hd.const_mul (2 * C f)")
        out.append(f"{indent}exact hd'.congr_of_eventuallyEq h_sqrt_eq.symm")
    else:
        out.append(l)
    if l.strip() == "end Imscribing.YangMills.OSIBPBoundary":
        break
write_lines("IBPBoundaryToWightman.lean", out)

# 5. AsymptoticFreedomAndOSClosure.lean: fix line 57 and line 116
ls = read_lines("AsymptoticFreedomAndOSClosure.lean")
if len(ls) >= 57:
    ls[56] = re.sub(r"div_lt_one\s+\S+\s+\(by positivity\)", "(div_lt_one (by positivity)).mpr", ls[56])
if len(ls) >= 117 and "Subsingleton.elim" in ls[115]:
    indent = ls[115][: len(ls[115]) - len(ls[115].lstrip())]
    ls[115] = f"{indent}simp [zero_pow hk]"
write_lines("AsymptoticFreedomAndOSClosure.lean", ls)

# 6. Dump exact slices for remaining items
dump("TransferMatrixToSemigroup.lean", 85, 130)
dump("TransferMatrixToSemigroup.lean", 198, 218)
dump("SemigroupGapBridge.lean", 105, 122)
dump("AsymptoticFreedomAndOSClosure.lean", 50, 62)
dump("AsymptoticFreedomAndOSClosure.lean", 105, 122)
dump("IBPBoundaryToWightman.lean", 115, 160)