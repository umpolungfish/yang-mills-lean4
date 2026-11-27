import subprocess
from pathlib import Path

print("=== 1. Searching for SecondCountableTopology GaugeGroup across the repo ===")
proc = subprocess.run(["git", "grep", "-n", "SecondCountableTopology.*GaugeGroup"], capture_output=True, text=True)
print(proc.stdout if proc.stdout else "None found via regex; checking GaugeGroup instances:")
proc2 = subprocess.run(["git", "grep", "-n", "instance.*GaugeGroup"], capture_output=True, text=True)
for line in proc2.stdout.splitlines()[:15]:
    print(" ", line)

print("\n=== 2. Checking PosSchwartzSubmodule definition & Spacetime4 ===")
proc3 = subprocess.run(["git", "grep", "-n", "PosSchwartzSubmodule"], capture_output=True, text=True)
for line in proc3.stdout.splitlines()[:10]:
    print(" ", line)

print("\n=== 3. Lines 185-225 of CanonicalFiniteVolumeBorchers4D.lean ===")
p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
if p.exists():
    lines = p.read_text(encoding="utf-8").splitlines()
    for i in range(185, min(len(lines) + 1, 230)):
        print(f"{i:4d}: {lines[i-1]}")