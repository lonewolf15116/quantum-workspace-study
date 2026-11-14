#!/usr/bin/env python3
"""Reassemble split evidence ZIPs and verify all SHA-256 checksums.

Run from the repository root:
    python scripts/reassemble_evidence.py
"""
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
CHECKSUMS = ROOT / "SHA256SUMS"


def verify(path: Path, expected: str) -> bool:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    actual = h.hexdigest()
    print(f"{'PASS' if actual == expected else 'FAIL'} {path.relative_to(ROOT)} {actual}")
    return actual == expected


def main() -> int:
    ok = True
    for raw in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        expected, relpath = raw.split(maxsplit=1)
        output = ROOT / relpath
        if not output.exists():
            parts = sorted(EVIDENCE.glob(output.name + ".part[0-9][0-9]"))
            if not parts:
                print(f"MISSING {relpath}: no ZIP or numbered parts")
                ok = False
                continue
            with output.open("wb") as out:
                for part in parts:
                    with part.open("rb") as src:
                        for chunk in iter(lambda: src.read(1024 * 1024), b""):
                            out.write(chunk)
            print(f"REASSEMBLED {relpath} from {len(parts)} parts")
        if not verify(output, expected):
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
