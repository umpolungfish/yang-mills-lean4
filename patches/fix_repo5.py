#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path("Imscribing/YangMills")


def read_lines(rel: str) -> list[str]:
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


def write_lines(rel: str, lines: list[str]) -> None:
    (ROOT / rel).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[UPDATED] {ROOT / rel}")


# 1. AsymptoticFreedomAndOSClosure.lean: remove the `![]` rewrite before `norm_zero`
ls = read_lines("AsymptoticFreedomAndOSClosure.lean")
ls = [
    l.replace(
        "show (![] : Fin 0 → Spacetime4) = 0 from Subsingleton.elim _ _, ",
        "",
    )
    for l in ls
]
write_lines("AsymptoticFreedomAndOSClosure.lean", ls)

# 2. IBPBoundaryToWightman.lean: fix lines 51 and 277
ls = read_lines("IBPBoundaryToWightman.lean")
out = []
for l in ls:
    if l.strip() == "simpa [F, F', h_eq] using hd.const_mul (A / (r + 1))":
        indent = l[: len(l) - len(l.lstrip())]
        out.append(f"{indent}convert hd.const_mul (A / (r + 1)) using 1")
        out.append(f"{indent}dsimp [F']")
        out.append(f"{indent}exact h_eq.symm")
    elif l.strip() == "exact Real.rpow_le_rpow_of_exponent_ge ht.1 ht.2 hexp_nonpos":
        indent = l[: len(l) - len(l.lstrip())]
        out.append(f"{indent}simpa using Real.rpow_le_rpow_of_exponent_ge ht.1 ht.2 hexp_nonpos")
    else:
        out.append(l)
write_lines("IBPBoundaryToWightman.lean", out)