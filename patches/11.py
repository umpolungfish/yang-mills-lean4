from pathlib import Path
import re

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
lines = p.read_text(encoding="utf-8").splitlines()

print(f"=== All 'sorry' occurrences in {p.name} ===")
for i, line in enumerate(lines, 1):
    if "sorry" in line:
        print(f"Line {i:4d}: {line}")
        # print context
        for j in range(max(1, i - 2), min(len(lines) + 1, i + 3)):
            if j != i:
                print(f"     {j:4d}: {lines[j-1]}")
