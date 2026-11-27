import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/AllDegreesSchwingerLimit.lean")
lines = p.read_text(encoding="utf-8").splitlines()
print("=== AllDegreesSchwingerLimit.lean lines 40-65 ===")
for i in range(40, min(len(lines)+1, 66)):
    print(f"{i:4d}: {lines[i-1]}")

text = "\n".join(lines) + "\n"
if "S_∞" in text:
    print("\nReplacing S_∞ -> S_inf...")
    text = text.replace("S_∞", "S_inf")
    p.write_text(text, encoding="utf-8")
    print("Patched. Building Imscribing.YangMills...")
    res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
    print("Build return code:", res.returncode)