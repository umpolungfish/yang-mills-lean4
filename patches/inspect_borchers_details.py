from pathlib import Path

print("=== 1. Inspecting apply_fixes.py around line 343 ===")
p_fix = Path("apply_fixes.py")
if p_fix.exists():
    lines = p_fix.read_text(encoding="utf-8").splitlines()
    for i in range(max(1, 335), min(len(lines) + 1, 390)):
        print(f"{i:4d}: {lines[i-1]}")

print("\n=== 2. Lines 1 to 100 of CanonicalFiniteVolumeBorchers4D.lean ===")
p_borch = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
if p_borch.exists():
    lines = p_borch.read_text(encoding="utf-8").splitlines()
    for i in range(1, min(len(lines) + 1, 105)):
        print(f"{i:4d}: {lines[i-1]}")

print("\n=== 3. Lines 270 to 300 of CanonicalFiniteVolumeBorchers4D.lean ===")
if p_borch.exists():
    lines = p_borch.read_text(encoding="utf-8").splitlines()
    for i in range(max(1, 270), min(len(lines) + 1, 305)):
        print(f"{i:4d}: {lines[i-1]}")