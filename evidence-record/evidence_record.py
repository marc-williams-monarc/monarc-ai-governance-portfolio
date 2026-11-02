"""Evidence record: a small, dependency-free reference implementation.

What it does
- Fingerprints a file with SHA-256.
- Appends each fingerprint to an append-only JSON Lines log in which every
  entry carries the hash of the entry before it (a hash chain). Editing,
  deleting or reordering any earlier entry breaks every hash after it.
- Optionally asks an RFC 3161 timestamp authority (TSA) to countersign an
  entry, using the `openssl` command line tool if it is installed. The TSA's
  reply is stored next to the log so the time can be checked independently.
- Verifies the whole log, and checks a file against the fingerprint recorded
  for it.

What it is not
- Not a production system or a legal record. It shows the pattern: a record
  whose integrity and timing can be proved after the fact, without trusting the
  person who keeps it.

Usage
  python evidence_record.py add   LOG FILE [--note TEXT] [--tsa URL]
  python evidence_record.py verify LOG
  python evidence_record.py check LOG FILE
  python evidence_record.py show  LOG
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

GENESIS = "0" * 64
CHUNK = 1024 * 1024


def sha256_file(path: str | os.PathLike) -> str:
    """Return the SHA-256 hex digest of a file, read in chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def _canonical(obj: dict) -> bytes:
    """Stable JSON encoding so the same entry always hashes the same way."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def entry_hash(entry: dict) -> str:
    """Hash of an entry's content, excluding its own entry_hash field."""
    body = {k: v for k, v in entry.items() if k != "entry_hash"}
    return hashlib.sha256(_canonical(body)).hexdigest()


def read_log(log: str | os.PathLike) -> list[dict]:
    p = Path(log)
    if not p.exists():
        return []
    out = []
    with open(p, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"line {n} is not valid JSON: {e}") from e
    return out


def _utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def append(log: str | os.PathLike, file: str | os.PathLike, note: str = "", tsa_url: str | None = None,
           now: str | None = None) -> dict:
    """Fingerprint FILE and append a chained entry to LOG. Returns the entry."""
    entries = read_log(log)
    if entries:
        problems = verify_chain(entries)
        if problems:
            raise ValueError("refusing to append to a log that fails verification: " + "; ".join(problems))
    prev = entries[-1]["entry_hash"] if entries else GENESIS
    entry = {
        "seq": len(entries) + 1,
        "recorded_at": now or _utc_now(),
        "file_name": Path(file).name,
        "file_sha256": sha256_file(file),
        "note": note,
        "prev_hash": prev,
    }
    entry["entry_hash"] = entry_hash(entry)
    if tsa_url:
        entry_tsr = request_timestamp(entry["entry_hash"], tsa_url, Path(log).with_suffix(f".{entry['seq']}.tsr"))
        entry["tsa"] = {"url": tsa_url, "response_file": entry_tsr.name}
        # The timestamp reply is stored beside the log; adding its reference does not change entry_hash,
        # which is what the TSA countersigned.
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def verify_chain(entries: list[dict]) -> list[str]:
    """Return a list of problems; an empty list means the chain is intact."""
    problems = []
    prev = GENESIS
    for i, e in enumerate(entries, 1):
        if e.get("seq") != i:
            problems.append(f"entry {i}: sequence number is {e.get('seq')}, expected {i} (entry missing or reordered)")
        if e.get("prev_hash") != prev:
            problems.append(f"entry {i}: link to previous entry is broken")
        expected = entry_hash({k: v for k, v in e.items() if k != "tsa"})
        if e.get("entry_hash") != expected:
            problems.append(f"entry {i}: content does not match its hash (entry was edited)")
        prev = e.get("entry_hash", "")
    return problems


def check_file(entries: list[dict], file: str | os.PathLike) -> tuple[bool, str]:
    """Is this file's current content the one last recorded under its name?"""
    name = Path(file).name
    digest = sha256_file(file)
    recorded = [e for e in entries if e.get("file_name") == name]
    if not recorded:
        return False, f"{name} has no entry in the log"
    last = recorded[-1]
    if last["file_sha256"] == digest:
        return True, f"{name} matches entry {last['seq']} recorded {last['recorded_at']}"
    if any(e["file_sha256"] == digest for e in recorded):
        older = next(e for e in recorded if e["file_sha256"] == digest)
        return False, f"{name} matches an older version (entry {older['seq']}), not the latest (entry {last['seq']})"
    return False, f"{name} does not match any recorded version"


def request_timestamp(digest_hex: str, tsa_url: str, out_path: Path) -> Path:
    """Ask an RFC 3161 TSA to timestamp a SHA-256 digest. Requires the openssl CLI."""
    if not shutil.which("openssl"):
        raise RuntimeError("openssl is not installed; run without --tsa or install OpenSSL")
    with tempfile.TemporaryDirectory() as td:
        tsq = Path(td) / "req.tsq"
        subprocess.run(["openssl", "ts", "-query", "-digest", digest_hex, "-sha256", "-cert", "-out", str(tsq)],
                       check=True, capture_output=True)
        req = urllib.request.Request(tsa_url, data=tsq.read_bytes(),
                                     headers={"Content-Type": "application/timestamp-query"})
        with urllib.request.urlopen(req, timeout=30) as r:
            out_path.write_bytes(r.read())
    return out_path


def _cmd_add(a):
    e = append(a.log, a.file, a.note or "", a.tsa)
    print(f"entry {e['seq']} recorded: {e['file_name']} sha256={e['file_sha256'][:16]}… chain={e['entry_hash'][:16]}…")


def _cmd_verify(a):
    entries = read_log(a.log)
    problems = verify_chain(entries)
    if problems:
        print("FAILED"); [print(" -", p) for p in problems]; sys.exit(1)
    print(f"OK: {len(entries)} entries, chain intact")


def _cmd_check(a):
    ok, msg = check_file(read_log(a.log), a.file)
    print(("OK: " if ok else "NO MATCH: ") + msg); sys.exit(0 if ok else 1)


def _cmd_show(a):
    for e in read_log(a.log):
        print(f"{e['seq']:>3}  {e['recorded_at']}  {e['file_name']}  {e['file_sha256'][:16]}…  {e.get('note','')}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Append-only, hash-chained evidence record")
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("add"); x.add_argument("log"); x.add_argument("file"); x.add_argument("--note"); x.add_argument("--tsa"); x.set_defaults(fn=_cmd_add)
    x = s.add_parser("verify"); x.add_argument("log"); x.set_defaults(fn=_cmd_verify)
    x = s.add_parser("check"); x.add_argument("log"); x.add_argument("file"); x.set_defaults(fn=_cmd_check)
    x = s.add_parser("show"); x.add_argument("log"); x.set_defaults(fn=_cmd_show)
    a = p.parse_args(argv); a.fn(a)


if __name__ == "__main__":
    main()
