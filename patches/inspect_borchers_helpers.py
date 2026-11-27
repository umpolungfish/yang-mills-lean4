from pathlib import Path

print("=== 1. CanonicalLatticeBorchers4D.lean around line 46 ===")
p_clb = Path("Imscribing/YangMills/CanonicalLatticeBorchers4D.lean")
if p_clb.exists():
    lines = p_clb.read_text(encoding="utf-8").splitlines()
    for i in range(40, min(len(lines) + 1, 75)):
        print(f"{i:4d}: {lines[i-1]}")

print("\n=== 2. BorchersContinuumReconstruction.lean lines 20 to 45 ===")
p_bcr = Path("Imscribing/YangMills/BorchersContinuumReconstruction.lean")
if p_bcr.exists():
    lines = p_bcr.read_text(encoding="utf-8").splitlines()
    for i in range(20, min(len(lines) + 1, 45)):
        print(f"{i:4d}: {lines[i-1]}")