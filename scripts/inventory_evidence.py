#!/usr/bin/env python3
"""Read-only inventory of archived evidence. Never extracts or mutates original ZIPs."""
from pathlib import Path
import json
import zipfile
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SUMS = ROOT / "SHA256SUMS"

def main():
    records = []
    ok = True
    for line in SUMS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, name = line.split(maxsplit=1)
        path = ROOT / name
        if not path.exists():
            print(f"MISSING: {name}", file=sys.stderr)
            return 1
        actual = hashlib.file_digest(path.open("rb"), "sha256").hexdigest()
        passed = actual == expected
        ok &= passed
        if not passed:
            print(f"HASH FAIL: {name}", file=sys.stderr)
            continue
        try:
            with zipfile.ZipFile(path) as z:
                entries = [{"path": f.filename, "size": f.file_size, "compressed_size": f.compress_size}
                           for f in z.infolist() if not f.is_dir()]
                invalid = z.testzip()
        except (zipfile.BadZipFile, OSError) as e:
            print(f"ZIP FAIL: {name}: {e}", file=sys.stderr)
            ok = False
            continue
        if invalid:
            print(f"CRC FAIL: {name}: {invalid}", file=sys.stderr)
            ok = False
        records.append({"archive": name, "sha256": actual,
                        "sha256_match": passed, "zip_crc_valid": invalid is None,
                        "files": entries})
    out = ROOT / "evidence_inventory.json"
    out.write_text(json.dumps({"archives": records}, indent=2) + "\n", encoding="utf-8")
    for archive in records:
        print(f"ARCHIVE {archive['archive']} ({len(archive['files'])} files, hash and CRC checked)")
        for f in archive["files"]:
            print(f"  {f['size']:>10}  {f['path']}")
    print("INVENTORY " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
