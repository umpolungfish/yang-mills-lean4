#!/usr/bin/env python3
"""Patch kernel-failing `decide` / `trivial` / `simp +decide` in LatticeExteriorCutoff4D.lean."""

import difflib
import pathlib
import re
import sys

TARGET = pathlib.Path("Imscribing/YangMills/LatticeExteriorCutoff4D.lean")
TARGET_LINE = 29

TOP_DECL_RE = re.compile(
    r"^(?:@\[.*?\]\s*)*(?:private\s+|protected\s+|noncomputable\s+|unsafe\s+|partial\s+)*"
    r"(?:theorem|lemma|def|abbrev|instance|example|structure|inductive|class)\b"
)

SAFE_DECIDE = (
    "(first | exact decide_eq_true (by first | rfl | simp) "
    "| simp only [decide_eq_true_eq]; rfl | decide +kernel | rfl)"
)
SAFE_TRIVIAL = (
    "(first | exact True.intro | rfl | assumption "
    "| exact decide_eq_true (by first | rfl | simp) | decide +kernel)"
)


def patch_range(lines: list[str], start: int, end: int) -> tuple[int, list[str]]:
    total = 0
    out: list[str] = []
    for line in lines[start:end]:
        code, sep, comment = line.partition("--")
        new_code, n1 = re.subn(
            r"(?<![\w.])decide(?!\s*\+|\s*\(|_|\w|,|\])",
            SAFE_DECIDE,
            code,
        )
        new_code, n2 = re.subn(
            r"\b(simp(?:_all)?)\s+\+decide\b",
            r"\1 [decide_eq_true_eq]",
            new_code,
        )
        new_code, n3 = re.subn(
            r"(?<![\w.])trivial(?!_|\w)",
            SAFE_TRIVIAL,
            new_code,
        )
        total += n1 + n2 + n3
        out.append(new_code + sep + comment)
    return total, out


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    idx = min(TARGET_LINE - 1, len(lines) - 1)

    start = idx
    while start > 0 and not TOP_DECL_RE.match(lines[start]):
        start -= 1

    end = idx + 1
    while end < len(lines):
        if TOP_DECL_RE.match(lines[end]) or lines[end].startswith("end "):
            break
        end += 1

    total, new_block = patch_range(lines, start, end)
    if total == 0:
        # Fallback: scan lines 1..80 if line 29 is inside a section/macro/nested block
        scan_end = min(len(lines), 80)
        total, new_block = patch_range(lines, 0, scan_end)
        start, end = 0, scan_end

    if total == 0:
        print(f"No matching tactic in {TARGET} lines 1..{min(len(lines), 80)}:", file=sys.stderr)
        for lineno, l in enumerate(lines[: min(len(lines), 80)], start=1):
            print(f"{lineno:5d}: {l}", end="", file=sys.stderr)
        return 2

    new_lines = lines[:start] + new_block + lines[end:]
    new_text = "".join(new_lines)

    backup = TARGET.with_suffix(TARGET.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")
    TARGET.write_text(new_text, encoding="utf-8")

    sys.stdout.writelines(
        difflib.unified_diff(lines, new_lines, fromfile=f"a/{TARGET}", tofile=f"b/{TARGET}")
    )
    print(f"\n[PATCHED] {TARGET} ({total} replacements; backup: {backup})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())