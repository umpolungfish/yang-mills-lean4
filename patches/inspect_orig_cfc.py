from pathlib import Path

p = Path("Imscribing/YangMills/SemigroupToUnitaryGroupCFC.lean.prepatch.bak")
if p.exists():
    print(p.read_text(encoding="utf-8"))