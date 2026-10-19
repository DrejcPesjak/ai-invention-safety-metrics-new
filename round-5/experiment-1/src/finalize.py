#!/usr/bin/env python3
"""Run the standalone verifier and stamp its result into method_out.json.

Kept out of analysis.py deliberately: verify.py must be able to run against a
method_out.json it did not itself produce, so the stamping is a separate step
that happens AFTER both exist.  The stamp records the exit code and the full
per-entry table, so a reader of method_out.json alone can see what was checked.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    r = subprocess.run([sys.executable, str(HERE / "verify.py")],
                       capture_output=True, text=True, cwd=str(HERE))
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    entries = []
    import re as _re
    for ln in lines:
        if " PASS" not in ln and " FAIL" not in ln:
            continue
        status = "PASS" if " PASS" in ln else "FAIL"
        key = ln.split(status)[0].strip()
        detail = ln.split(status, 1)[1].strip()
        # skip the trailing "60/60 PASS" summary line and the rule separators;
        # counting the summary as an entry inflates the block by one
        if not key or key.startswith("-") or _re.fullmatch(r"\d+/\d+", key):
            continue
        entries.append({"entry": key, "status": status, "detail": detail})
    block = {
        "verifier": "verify.py (standalone; imports nothing from the pipeline)",
        "exit_code": r.returncode,
        "n_entries": len(entries),
        "n_pass": sum(1 for e in entries if e["status"] == "PASS"),
        "n_fail": sum(1 for e in entries if e["status"] == "FAIL"),
        "all_pass": bool(r.returncode == 0),
        "entries": entries,
        "stderr_tail": r.stderr[-800:] if r.stderr else "",
    }
    p = HERE / "method_out.json"
    obj = json.loads(p.read_text())
    obj["metadata"]["assertion_block"] = block
    p.write_text(json.dumps(obj, indent=1))
    (HERE / "results" / "verify_table.json").write_text(json.dumps(block, indent=1))
    print(f"assertion_block stamped: {block['n_pass']}/{block['n_entries']} PASS, "
          f"exit={block['exit_code']}")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
