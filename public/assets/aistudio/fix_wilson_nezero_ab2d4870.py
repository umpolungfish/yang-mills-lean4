#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path("Imscribing/YangMills")


def patch(rel: str, fn) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    new_txt = fn(txt)
    if new_txt != txt:
        p.write_text(new_txt, encoding="utf-8")
        print(f"[UPDATED] {p}")


def fix_wl(t: str) -> str:
    t = t.replace("def realTrace {N : ℕ}", "noncomputable def realTrace {N : ℕ}")
    t = t.replace(
        "noncomputable def wilsonAction (N L : ℕ) [NeZero N]",
        "noncomputable def wilsonAction (N L : ℕ) [NeZero N] [NeZero L]",
    )
    t = t.replace(
        "theorem wilsonAction_gaugeInvariant (N L : ℕ) [NeZero N]",
        "theorem wilsonAction_gaugeInvariant (N L : ℕ) [NeZero N] [NeZero L]",
    )
    t = t.replace(
        "2 ≤ N → Nonempty (ClayReduction.OSReconstructedInput N)",
        "2 ≤ N → Nonempty (ClayReduction.OSReconstructedInput.{0} N)",
    )
    return t


def add_nezero_L(t: str) -> str:
    # Add [NeZero L] anywhere [NeZero N] appears without [NeZero L]
    t = re.sub(r"\[NeZero N\](?!\s*\[NeZero L\])", "[NeZero N] [NeZero L]", t)
    return t


patch("WilsonLattice4D.lean", fix_wl)
for f in [
    "WilsonActionBounds4D.lean",
    "WilsonHaarCompactness4D.lean",
    "LatticeReflectionPositivity4D.lean",
    "WilsonFrobeniusAndSmeared4D.lean",
]:
    patch(f, add_nezero_L)