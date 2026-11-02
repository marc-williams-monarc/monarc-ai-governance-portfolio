# Evidence record

A small working demo of a record whose **integrity and timing can be proved after the fact**, without having to trust whoever keeps it.

It is a reference implementation of the evidentiary record pattern I designed for Monarc's AI decision assessments. It uses only the Python standard library, plus the `openssl` command for the optional timestamp step.

## How it works

1. **Fingerprint.** Each file is hashed with SHA-256. Change one byte and the fingerprint changes.
2. **Append-only, hash-chained log.** Each log entry records the file's fingerprint and the hash of the entry before it. Edit, delete or reorder any earlier entry and every later link breaks, so tampering shows.
3. **Independent timestamp (optional).** With `--tsa`, the entry's hash is sent to an RFC 3161 timestamp authority. The authority's signed reply is kept beside the log, so the time an entry existed can be checked against a third party rather than the keeper's clock.
4. **Verification.** `verify` re-walks the chain. `check` says whether a file is the latest recorded version, an older one, or not recorded at all.

## Try it

```bash
python evidence_record.py add    evidence.jsonl report.pdf --note "Report issued at debrief"
python evidence_record.py verify evidence.jsonl
python evidence_record.py check  evidence.jsonl report.pdf
# with an independent timestamp (FreeTSA is one public RFC 3161 service):
python evidence_record.py add    evidence.jsonl report.pdf --tsa https://freetsa.org/tsr
```

## Tests

```bash
python -m pytest -q
```

The ten tests cover:
- an intact chain;
- a known SHA-256 value;
- an edited entry;
- a deleted entry;
- reordered entries;
- a forged entry that was re-hashed (the next link still breaks);
- a changed file;
- an unchanged file;
- an older version of a file;
- refusal to append to a log that has been tampered with.

## Limits

This is a demonstration of the pattern, not a production evidence system:
- Whoever controls the log can still delete the whole file. Anchoring entries with a third-party timestamp, or storing copies with someone else, is what guards against that.
- Hash chaining shows that tampering happened. It does not stop tampering.
- A timestamp proves when a hash existed. It says nothing about whether the content is true.
