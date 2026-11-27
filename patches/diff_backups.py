import difflib
from pathlib import Path

baks = sorted(Path("Imscribing/YangMills").glob("*.prepatch.bak"))

for bak in baks:
    orig = bak.with_suffix("")
    print(f"\n==========================================")
    print(f"Comparing: {orig.name} vs {bak.name}")
    print(f"==========================================")
    if orig.exists() and bak.exists():
        lines_orig = orig.read_text(encoding="utf-8").splitlines()
        lines_bak = bak.read_text(encoding="utf-8").splitlines()
        diff = list(difflib.unified_diff(lines_bak, lines_orig, fromfile=bak.name, tofile=orig.name, lineterm=""))
        if not diff:
            print("Files are identical.")
        else:
            print(f"Diff lines: {len(diff)}")
            for line in diff[:40]:  # print first 40 lines of diff
                print(line)
            if len(diff) > 40:
                print(f"... and {len(diff) - 40} more lines.")
    else:
        print("Missing file.")