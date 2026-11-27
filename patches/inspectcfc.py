from pathlib import Path

p = Path("Imscribing/YangMills/SemigroupToUnitaryGroupCFC.lean.prepatch.bak")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"Total lines: {len(lines)}")

# Print in chunks of 50 lines
for i, line in enumerate(lines[35:], 36):
    print(f"{i:4d}: {line}")