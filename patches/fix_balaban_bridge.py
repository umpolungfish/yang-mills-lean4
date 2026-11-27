import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/CanonicalBalabanSubsequentialBridge.lean")
text = p.read_text(encoding="utf-8")

replacements = [
    (
        "    (∀ y : Fin n → Spacetime4, f_π y = f (fun k => y (π k))) →",
        "    (∀ y : Fin n → ContinuumInterfaces.Spacetime4, f_π y = f (fun k => y (π k))) →",
    ),
    (
        "    ∃ (f g : SchwartzMap Spacetime4 ℂ),",
        "    ∃ (f g : SchwartzMap ContinuumInterfaces.Spacetime4 ℂ),",
    ),
    (
        """    (W : CanonicalSchwingerLimitWitness N L a β Z_ren)
    (E : CanonicalBalabanEstimates W) :""",
        """    (W : @CanonicalSchwingerLimitWitness N ⟨Nat.ne_of_gt (lt_of_lt_of_le Nat.zero_lt_two hN)⟩ L _ a β Z_ren)
    (E : @CanonicalBalabanEstimates N ⟨Nat.ne_of_gt (lt_of_lt_of_le Nat.zero_lt_two hN)⟩ L _ a β Z_ren W) :""",
    ),
]

for old, new in replacements:
    assert old in text, f"Pattern not found:\n{old}"
    text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")
print("Patched CanonicalBalabanSubsequentialBridge.lean.", flush=True)


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
    text = p.read_text(encoding="utf-8").replace(
        "    ∃ (f g : SchwartzMap ContinuumInterfaces.Spacetime4 ℂ),",
        "    ∃ (f g : SchwartzMap ClaySpec.Spacetime4 ℂ),",
        1,
    )
    p.write_text(text, encoding="utf-8")
    print("Switched line 116 to ClaySpec.Spacetime4.", flush=True)
    rc, out = check()

if out:
    print(out, flush=True)
print(f"lake env lean exit code: {rc}", flush=True)

if rc == 0 and "sorry" not in out:
    print("SUCCESS: CanonicalBalabanSubsequentialBridge.lean compiled with 0 errors and 0 sorries!", flush=True)
    print("\n=== Running lake build Imscribing.YangMills ===", flush=True)
    res_b = subprocess.run(["lake", "build", "Imscribing.YangMills"])
    print("Build return code:", res_b.returncode, flush=True)