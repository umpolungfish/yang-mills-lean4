import re
import subprocess
from pathlib import Path

TARGET = Path("Imscribing/YangMills/AllDegreesSchwingerLimit.lean")
DIAG_RE = re.compile(r"^(?:.*/)?AllDegreesSchwingerLimit\.lean:(\d+):(\d+): (error|warning): (.*)$")


def run_lean():
    res = subprocess.run(["lake", "env", "lean", str(TARGET)], capture_output=True, text=True)
    out = (res.stdout + "\n" + res.stderr).strip()
    diags = []
    cur = None
    for line in out.splitlines():
        m = DIAG_RE.match(line)
        if m:
            if cur:
                diags.append(cur)
            cur = {
                "line": int(m.group(1)),
                "col": int(m.group(2)),
                "kind": m.group(3),
                "msg": m.group(4),
                "full": [line],
            }
        elif cur is not None:
            cur["full"].append(line)
    if cur:
        diags.append(cur)
    return res.returncode, out, diags


def parse_two_args(text, start_idx):
    n = len(text)
    args = []
    pos = start_idx
    for _ in range(2):
        while pos < n and text[pos] in " \t":
            pos += 1
        if pos >= n or text[pos] in (",", ")", "]", "}", ";", "\n"):
            break
        arg_start = pos
        if text[pos] in "([{":
            open_ch = text[pos]
            close_ch = {"(": ")", "[": "]", "{": "}"}[open_ch]
            depth = 1
            pos += 1
            while pos < n and depth > 0:
                if text[pos] == open_ch:
                    depth += 1
                elif text[pos] == close_ch:
                    depth -= 1
                pos += 1
            args.append((arg_start, pos, text[arg_start:pos]))
        else:
            while pos < n and not text[pos].isspace() and text[pos] not in (",", ")", "]", "}", ";"):
                pos += 1
            args.append((arg_start, pos, text[arg_start:pos]))
    return args


def strip_redundant_tactic_at(lines, line_no, col_no):
    idx_line = line_no - 1
    if idx_line < 0 or idx_line >= len(lines):
        return lines, False
    s = lines[idx_line]
    search_upto = min(len(s), col_no + 2)
    semi_pos = -1
    i = 0
    while i < search_upto:
        if s[i] == ";":
            if i > 0 and s[i - 1] == "<":
                i += 1
                continue
            semi_pos = i
        i += 1
    if semi_pos != -1 and s[semi_pos + 1:col_no].strip() == "":
        depth = 0
        pos = semi_pos + 1
        while pos < len(s):
            ch = s[pos]
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif ch == "," and depth == 0:
                break
            pos += 1
        new_lines = list(lines)
        new_lines[idx_line] = s[:semi_pos].rstrip() + s[pos:]
        return new_lines, True

    if s[:col_no].strip() == "":
        stripped = s.strip()
        if (
            stripped
            and not stripped.startswith(("·", "case ", "by", "have ", "let ", "obtain ", "theorem ", "lemma ", "def ", "end "))
            and not any(c in stripped for c in ")]}")
        ):
            new_lines = list(lines)
            del new_lines[idx_line]
            return new_lines, True
    return lines, False


def try_candidate(new_text, check_fn):
    old_text = TARGET.read_text(encoding="utf-8")
    TARGET.write_text(new_text, encoding="utf-8")
    rc, out, diags = run_lean()
    if check_fn(rc, diags, new_text):
        return True, rc, out, diags
    TARGET.write_text(old_text, encoding="utf-8")
    return False, rc, out, diags


def main():
    orig_text = TARGET.read_text(encoding="utf-8")
    Path("/tmp/AllDegreesSchwingerLimit.lean.bak").write_text(orig_text, encoding="utf-8")

    if "S_∞" in orig_text:
        TARGET.write_text(orig_text.replace("S_∞", "S_inf"), encoding="utf-8")

    rc, out, diags = run_lean()
    print(f"Initial diagnostics: {len(diags)} (rc={rc})")

    # 1. Disambiguate Spacetime4
    ambig_lines = sorted(set(
        d["line"] for d in diags
        if d["kind"] == "error" and "ambiguous" in d["msg"] and "Spacetime4" in "\n".join(d["full"])
    ))
    for ln in ambig_lines:
        lines = TARGET.read_text(encoding="utf-8").splitlines()
        line_str = lines[ln - 1]
        prev_errs = len([d for d in diags if d["kind"] == "error"])
        for qual in ["ContinuumInterfaces.Spacetime4", "ClaySpec.Spacetime4"]:
            cand_line = re.sub(r"(?<!\.)\bSpacetime4\b", qual, line_str)
            if cand_line == line_str:
                continue
            cand_lines = list(lines)
            cand_lines[ln - 1] = cand_line
            ok, rc, out, new_diags = try_candidate(
                "\n".join(cand_lines) + "\n",
                lambda r, ds, nt, ln=ln, pe=prev_errs: (
                    not any(d["line"] == ln and d["kind"] == "error" for d in ds)
                    and len([d for d in ds if d["kind"] == "error"]) <= pe
                ),
            )
            if ok:
                print(f"Line {ln}: disambiguated Spacetime4 -> {qual}")
                diags = new_diags
                break

    # 2. Fix add_le_add_right argument-order mismatch
    rc, out, diags = run_lean()
    cur_lines = TARGET.read_text(encoding="utf-8").splitlines()
    add_lines = sorted(set(
        d["line"] for d in diags
        if d["kind"] == "error" and 1 <= d["line"] <= len(cur_lines) and "add_le_add_right" in cur_lines[d["line"] - 1]
    ))
    for ln in add_lines:
        text_cur = TARGET.read_text(encoding="utf-8")
        lines = text_cur.splitlines()
        line_start_offset = sum(len(l) + 1 for l in lines[:ln - 1])
        rel_idx = lines[ln - 1].find("add_le_add_right")
        if rel_idx == -1:
            continue
        abs_start = line_start_offset + rel_idx
        after_name = abs_start + len("add_le_add_right")
        args = parse_two_args(text_cur, after_name)
        span_end = args[-1][1] if args else after_name

        candidates = []
        if len(args) == 2:
            a1, a2 = args[0][2], args[1][2]
            candidates.extend([
                f"(add_le_add {a1} le_rfl)",
                f"(add_le_add le_rfl {a1})",
                f"(add_le_add_right {a2} {a1})",
                f"(add_le_add {a2} le_rfl)",
                f"(add_le_add le_rfl {a2})",
                "(add_le_add (norm_add_le _ _) le_rfl)",
                "(add_le_add le_rfl (norm_add_le _ _))",
            ])
        elif len(args) == 1:
            a1 = args[0][2]
            candidates.extend([
                f"(add_le_add {a1} le_rfl)",
                f"(add_le_add le_rfl {a1})",
                "(add_le_add (norm_add_le _ _) le_rfl)",
                "(add_le_add le_rfl (norm_add_le _ _))",
            ])
        else:
            candidates.extend([
                "(add_le_add (norm_add_le _ _) le_rfl)",
                "(add_le_add le_rfl (norm_add_le _ _))",
            ])

        prev_errs = len([d for d in diags if d["kind"] == "error"])
        for rep in candidates:
            new_text = text_cur[:abs_start] + rep + text_cur[span_end:]
            ok, rc, out, new_diags = try_candidate(
                new_text,
                lambda r, ds, nt, ln=ln, pe=prev_errs: (
                    not any(d["line"] == ln and d["kind"] == "error" for d in ds)
                    and len([d for d in ds if d["kind"] == "error"]) <= pe
                ),
            )
            if ok:
                print(f"Line {ln}: replaced add_le_add_right -> {rep}")
                diags = new_diags
                break

    # 3. Strip redundant 'No goals to be solved' tactics bottom-up
    for _ in range(10):
        rc, out, diags = run_lean()
        no_goals = [d for d in diags if d["kind"] == "error" and "No goals to be solved" in d["msg"]]
        if not no_goals:
            break
        changed = False
        for d in sorted(no_goals, key=lambda x: (x["line"], x["col"]), reverse=True):
            lines = TARGET.read_text(encoding="utf-8").splitlines()
            new_lines, ok_strip = strip_redundant_tactic_at(lines, d["line"], d["col"])
            if ok_strip:
                prev_errs = len([x for x in diags if x["kind"] == "error"])
                ok, rc2, out2, new_diags = try_candidate(
                    "\n".join(new_lines) + "\n",
                    lambda r, ds, nt, ln=d["line"], pe=prev_errs, nlines=len(new_lines): (
                        not any(x["line"] == ln and "No goals to be solved" in x["msg"] for x in ds)
                        and not any(x["line"] > nlines and x["kind"] == "error" for x in ds)
                        and len([x for x in ds if x["kind"] == "error"]) <= pe
                    ),
                )
                if ok:
                    print(f"Line {d['line']}: stripped redundant tactic causing 'No goals to be solved'")
                    changed = True
                    break
        if not changed:
            break

    # 4. Handle isDefEq / heartbeat timeout options
    rc, out, diags = run_lean()

    def has_hb(ds):
        return any(
            any(k in "\n".join(x["full"]).lower() for k in ("heartbeat", "timeout"))
            for x in ds if x["kind"] == "error"
        )

    if has_hb(diags):
        text_cur = TARGET.read_text(encoding="utf-8")
        if "set_option maxHeartbeats" not in text_cur:
            m = re.search(r"^(namespace\s+[^\n]+)\n", text_cur, re.M)
            prev_errs = len([x for x in diags if x["kind"] == "error"])
            for opt_block in [
                "set_option maxHeartbeats 800000\n",
                "set_option maxSynthPendingDepth 1\nset_option maxHeartbeats 800000\n",
                "set_option maxSynthPendingDepth 1\nset_option maxHeartbeats 1600000\n",
            ]:
                if m:
                    new_text = text_cur[:m.end()] + "\n" + opt_block + text_cur[m.end():]
                else:
                    new_text = opt_block + text_cur
                ok, rc2, out2, new_diags = try_candidate(
                    new_text,
                    lambda r, ds, nt, pe=prev_errs: (
                        not has_hb(ds) and len([x for x in ds if x["kind"] == "error"]) <= pe
                    ),
                )
                if ok:
                    print(f"Applied options: {opt_block.strip()}")
                    break

    # 5. Verify and run full lake build
    rc, out, diags = run_lean()
    has_sorry = "uses 'sorry'" in out or "sorryAx" in out
    err_count = len([d for d in diags if d["kind"] == "error"])
    print(f"\n=== AllDegreesSchwingerLimit.lean check: rc={rc}, errors={err_count}, sorry={has_sorry} ===")
    if rc != 0 or has_sorry:
        print("--- Diagnostics ---")
        print(out)
        lines = TARGET.read_text(encoding="utf-8").splitlines()
        start_ln = 1 if len(lines) <= 240 else 45
        print(f"\n--- AllDegreesSchwingerLimit.lean lines {start_ln}..{len(lines)} ---")
        for i in range(start_ln, len(lines) + 1):
            print(f"{i:4d}: {lines[i - 1]}")
        return

    print("SUCCESS: AllDegreesSchwingerLimit.lean compiled cleanly with 0 errors and 0 sorries!")
    print("\n=== Running lake build Imscribing.YangMills ===")
    res = subprocess.run(["lake", "build", "Imscribing.YangMills"])
    print("Build return code:", res.returncode)


if __name__ == "__main__":
    main()