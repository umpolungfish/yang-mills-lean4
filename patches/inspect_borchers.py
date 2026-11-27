import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
print(f"=== 1. Git status & log for {p} ===")
proc_log = subprocess.run(["git", "log", "-n", "3", "--oneline", str(p)], capture_output=True, text=True)
print(proc_log.stdout)

proc_diff = subprocess.run(["git", "diff", "--stat", str(p)], capture_output=True, text=True)
if proc_diff.stdout.strip():
    print("Uncommitted changes:")
    print(proc_diff.stdout)
else:
    print("File is clean in git working tree.")

print("\n=== 2. Where is CanonicalFiniteVolumeBorchers4D imported? ===")
proc_grep = subprocess.run(["git", "grep", "-n", "CanonicalFiniteVolumeBorchers4D"], capture_output=True, text=True)
print(proc_grep.stdout)

print("\n=== 3. Lines 290-325 of CanonicalFiniteVolumeBorchers4D.lean (around the sorries) ===")
if p.exists():
    lines = p.read_text(encoding="utf-8").splitlines()
    for i in range(max(1, 290), min(len(lines) + 1, 325)):
        print(f"{i:4d}: {lines[i-1]}")