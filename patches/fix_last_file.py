import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/BalabanRGToClayMaster.lean")
text = p.read_text(encoding="utf-8")

# 1. Add missing import
if "import Imscribing.YangMills.CanonicalBalabanSubsequentialBridge" not in text:
    text = "import Imscribing.YangMills.CanonicalBalabanSubsequentialBridge\n" + text

# 2. Replace S_∞ identifier with S_inf
text = text.replace("S_∞", "S_inf")

p.write_text(text, encoding="utf-8")
print("Patched BalabanRGToClayMaster.lean.")

print("\n=== Running full lake build Imscribing.YangMills ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
print("Build return code:", res.returncode)