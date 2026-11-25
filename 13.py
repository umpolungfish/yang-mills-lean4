import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"Total lines in {p.name}: {len(lines)}")

print("\n=== Testing first 95 lines in isolation ===")
# Let's extract the header and the first 4 lemmas
test_code = "\n".join(lines[:95])
Path("test_first95.lean").write_text(test_code, encoding="utf-8")

res = subprocess.run(["lake", "env", "lean", "test_first95.lean"], capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode != 0:
    for err in res.stderr.splitlines()[:15]:
        print(" ", err)
else:
    print("First 95 lines compile cleanly!")
