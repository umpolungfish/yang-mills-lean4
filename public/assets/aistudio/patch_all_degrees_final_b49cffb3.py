import subprocess
from pathlib import Path

p = Path("Imscribing/YangMills/AllDegreesSchwingerLimit.lean")
text = p.read_text(encoding="utf-8")

replacements = [
    (
        "        (∀ y : Fin n → Spacetime4, f_π y = f (fun k => y (π k))) →",
        "        (∀ y : Fin n → ContinuumInterfaces.Spacetime4, f_π y = f (fun k => y (π k))) →",
    ),
    (
        """    gcongr
    · exact hZ m
    · exact Finset.sum_nonneg fun j _ => mul_nonneg (Nat.cast_nonneg _) (apply_nonneg _ _)""",
        """    gcongr
    exact hZ m""",
    ),
    (
        """      dsimp [p]; gcongr
      · exact hZ (φ m)
      · exact Finset.sum_nonneg fun j _ => mul_nonneg (Nat.cast_nonneg _) (apply_nonneg _ _)""",
        """      dsimp [p]; gcongr
      exact hZ (φ m)""",
    ),
    (
        "          le_trans (norm_add_le _ _) ((add_le_add (norm_add_le _ _) le_rfl))",
        "          le_trans (norm_add_le _ _) (add_le_add (norm_add_le _ _) le_rfl)",
    ),
    (
        """    dsimp [p]; gcongr
    · exact hZ (φ m)
    · exact Finset.sum_nonneg fun j _ => mul_nonneg (Nat.cast_nonneg _) (apply_nonneg _ _)""",
        """    dsimp [p]; gcongr
    exact hZ (φ m)""",
    ),
    (
        """  · exact continuum_schwinger_perm_symm N n (fun m => L (φ m)) (fun m => a (φ m))
      (fun m => β (φ m)) (fun m => Z_ren (φ m))
      (fun _ => inferInstance) (fun m => wilsonHaarLinkMeasure N (L (φ m)))
      (S_inf n) (h_spec n) π f f_π hf""",
        """  · letI := borel (GaugeGroup N)
    have h_lim_n := h_spec n
    dsimp only [canonicalSmearedPlaqSchwinger] at h_lim_n
    exact continuum_schwinger_perm_symm N n (fun m => L (φ m)) (fun m => a (φ m))
      (fun m => β (φ m)) (fun m => Z_ren (φ m))
      (fun _ => inferInstance) (fun m => wilsonHaarLinkMeasure N (L (φ m)))
      (S_inf n) h_lim_n π f f_π hf""",
    ),
]

for old, new in replacements:
    assert old in text, f"Pattern not found:\n{old}"
    text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")
print("Patched AllDegreesSchwingerLimit.lean cleanly.", flush=True)

print("=== Checking AllDegreesSchwingerLimit.lean (timeout 90s) ===", flush=True)
try:
    res = subprocess.run(
        ["lake", "env", "lean", str(p)],
        capture_output=True,
        text=True,
        timeout=90,
    )
except subprocess.TimeoutExpired:
    print("Timed out at 90s during lake env lean.", flush=True)
    raise SystemExit(1)

out = (res.stdout + "\n" + res.stderr).strip()
if out:
    print(out, flush=True)
print(f"lake env lean exit code: {res.returncode}", flush=True)

if res.returncode == 0 and "sorry" not in out:
    print("\n=== Building Imscribing.YangMills ===", flush=True)
    res_build = subprocess.run(["lake", "build", "Imscribing.YangMills"])
    print("Build return code:", res_build.returncode, flush=True)