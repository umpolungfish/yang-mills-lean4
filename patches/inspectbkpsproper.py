import difflib
from pathlib import Path

baks = sorted(Path("Imscribing/YangMills").glob("*.prepatch.bak"))

for bak in baks:
    orig_str = str(bak).replace(".prepatch.bak", "")
    orig = Path(orig_str)
    print(f"\n==========================================")
    print(f"Comparing: {orig.name} vs {bak.name}")
    print(f"==========================================")
    if orig.exists() and bak.exists():
        lines_orig = orig.read_text(encoding="utf-8").splitlines()
        lines_bak = bak.read_text(encoding="utf-8").splitlines()
        diff = list(difflib.unified_diff(lines_bak, lines_orig, fromfile=bak.name, tofile=orig.name, lineterm=""))
        if not diff:
            print("Files are 100% identical.")
        else:
            print(f"Diff lines: {len(diff)}")
            for line in diff[:35]:
                print(line)
            if len(diff) > 35:
                print(f"... and {len(diff) - 35} more lines.")
    else:
        print(f"Target file {orig} does not exist.")