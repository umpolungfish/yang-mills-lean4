import os
from pathlib import Path
import re

print("=== 1. Locating target path for SemigroupToUnitaryGroupCFC.lean ===")
repo_root = Path(".")
matches = list(repo_root.glob("**/SemigroupToUnitaryGroupCFC.lean"))
if matches:
    print(f"Found existing file: {matches[0]}")
    target_path = matches[0]
else:
    candidates = [
        Path("Imscribing/YangMills/SemigroupToUnitaryGroupCFC.lean"),
        Path("YangMills/SemigroupToUnitaryGroupCFC.lean"),
        Path("SemigroupToUnitaryGroupCFC.lean"),
    ]
    target_path = None
    for cand in candidates:
        if cand.parent.exists():
            target_path = cand
            break
    if not target_path:
        target_path = candidates[0]
    print(f"Target path determined: {target_path}")

print("\n=== 2. Inspecting exact CFC lemma names in local Mathlib ===")
mathlib = Path(".lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra")
if mathlib.exists():
    for p in [
        mathlib / "ContinuousFunctionalCalculus" / "Basic.lean",
        mathlib / "ContinuousFunctionalCalculus" / "Unital.lean",
        mathlib / "Spectrum.lean",
    ]:
        if p.exists():
            print(f"\n--- {p.name} ---")
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if re.match(r"^(?:theorem|lemma)\s+", line) and any(
                    k in line for k in ("cfc_one", "cfc_mul", "cfc_star", "cfc_const", "spectrum_subset_reals", "subset_reals")
                ):
                    print(f"  {i:4d}: {line}")