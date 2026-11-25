import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalFiniteVolumeBorchers4D.lean")
text = p.read_text(encoding="utf-8")
text = text.replace(
    "h_meas.stronglyMeasurable.integral_prod_right.aestronglyMeasurable",
    "h_meas.stronglyMeasurable.integral_prod_right'.aestronglyMeasurable"
)
p.write_text(text, encoding="utf-8")

print("=== 1. Building CanonicalFiniteVolumeBorchers4D ===")
res = subprocess.run(["lake", "build", "Imscribing.YangMills.CanonicalFiniteVolumeBorchers4D"], capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode == 0:
    print("SUCCESS: CanonicalFiniteVolumeBorchers4D built cleanly!")
else:
    print(res.stdout)
    print(res.stderr)

print("\n=== 2. Exact definitions of Poincare4 and poincareTimeTrans ===")
for sym in ["Poincare4", "poincareTimeTrans"]:
    g = subprocess.run(["git", "grep", "-n", "-A", "4", f" {sym}"], capture_output=True, text=True)
    for line in g.stdout.splitlines()[:15]:
        print(" ", line)