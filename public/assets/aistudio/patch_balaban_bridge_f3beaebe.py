import re
import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalBalabanSubsequentialBridge.lean")
text = p.read_text(encoding="utf-8")

# 1. Replace S_∞ -> S_inf
if "S_∞" in text:
    text = text.replace("S_∞", "S_inf")
    print("Replaced S_∞ -> S_inf", flush=True)

# 2. Disambiguate Spacetime4 on line 42
lines = text.splitlines()
assert len(lines) >= 42, f"Expected >= 42 lines, got {len(lines)}"
line42_orig = lines[41]
lines[41] = re.sub(r"(?<!\.)\bSpacetime4\b", "ContinuumInterfaces.Spacetime4", line42_orig)
p.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Updated line 42 -> {lines[41].strip()}", flush=True)


def check():
    res = subprocess.run(
        ["lake", "env", "lean", str(p)],
        capture_output=True,
        text=True,
        timeout=90,
    )
    out = (res.stdout + "\n" + res.stderr).strip()
    return res.returncode, out


rc, out = check()
if rc != 0 and ("ClaySpec.Spacetime4" in out and "type mismatch" in out):
    lines[41] = re.sub(r"(?<!\.)\bSpacetime4\b", "ClaySpec.Spacetime4", line42_orig)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Switched line 42 -> {lines[41].strip()}", flush=True)
    rc, out = check()

if out:
    print(out, flush=True)
print(f"lake env lean exit code: {rc}", flush=True)

if rc != 0 or "sorry" in out:
    print("\n=== CanonicalBalabanSubsequentialBridge.lean ===", flush=True)
    for i, l in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        print(f"{i:4d}: {l}")
else:
    print("SUCCESS: CanonicalBalabanSubsequentialBridge.lean compiled with 0 errors and 0 sorries!", flush=True)
    print("\n=== Running lake build Imscribing.YangMills ===", flush=True)
    res_b = subprocess.run(["lake", "build", "Imscribing.YangMills"])
    print("Build return code:", res_b.returncode, flush=True)