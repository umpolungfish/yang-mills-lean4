import subprocess
from pathlib import Path

print("=== 1. Git status ===")
res = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
print(res.stdout if res.stdout else "Clean working directory.")

print("\n=== 2. OSPoincareMasterDischarge.lean lines 1-45 ===")
p_os = Path("Imscribing/YangMills/OSPoincareMasterDischarge.lean")
if p_os.exists():
    lines = p_os.read_text(encoding="utf-8").splitlines()
    for i in range(1, min(len(lines) + 1, 46)):
        print(f"{i:4d}: {lines[i-1]}")

print("\n=== 3. OSPoincareMasterDischarge.lean lines 90-115 ===")
if p_os.exists():
    lines = p_os.read_text(encoding="utf-8").splitlines()
    for i in range(max(1, 90), min(len(lines) + 1, 115)):
        print(f"{i:4d}: {lines[i-1]}")

print("\n=== 4. Git log for both files ===")
subprocess.run(["git", "log", "-n", "2", "--oneline", "Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean", "Imscribing/YangMills/OSPoincareMasterDischarge.lean"])