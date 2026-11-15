"""Verify locked source integrity and mapping references; does not execute content."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def verify(root=ROOT):
    lock = json.loads((root / "sources.lock.json").read_text(encoding="utf-8"))
    errors = []
    source_paths = set()
    ids = set()
    for item in lock["legacy"] + lock["upstream"]["files"]:
        name = item.get("local_path", item.get("path"))
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append(f"Path escapes repository: {name}")
            continue
        if not path.is_file():
            errors.append(f"Missing source: {name}")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            errors.append(f"Hash mismatch: {name}")
        if "source_path" in item:
            source_paths.add(item["source_path"])
        else:
            # A narrow inventory check; deliberately not a YAML schema validator.
            for cid in re.findall(r"^\s*- id: ((?:LNX|WIN)-[A-Z]{2,4}-\d{3})\s*$", data.decode("utf-8"), re.M):
                ids.add(cid)
    mapped = set()
    for mapping in lock["mappings"]:
        cid = mapping["control_id"]
        if cid in mapped:
            errors.append(f"Duplicate mapping: {cid}")
        mapped.add(cid)
        if cid not in ids or not cid.startswith("LNX-"):
            errors.append(f"Unknown Linux control: {cid}")
        if not mapping["source_paths"] or not set(mapping["source_paths"]).issubset(source_paths):
            errors.append(f"Unpinned source for {cid}")
    if not any(p.endswith("/LICENSE") for p in (f["local_path"] for f in lock["upstream"]["files"])):
        errors.append("Missing upstream license")
    return errors


if __name__ == "__main__":
    try:
        errors = verify()
    except (OSError, ValueError, KeyError) as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print("OK: locked source hashes and filesystem mappings verified. Native OS behavior is not tested.")
