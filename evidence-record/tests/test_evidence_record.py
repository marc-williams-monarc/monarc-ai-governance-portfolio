import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import evidence_record as er  # noqa: E402


@pytest.fixture
def setup(tmp_path):
    log = tmp_path / "evidence.jsonl"
    files = []
    for i, text in enumerate(["report v1", "minutes", "policy"], 1):
        f = tmp_path / f"doc{i}.txt"
        f.write_text(text)
        files.append(f)
    for i, f in enumerate(files):
        er.append(log, f, note=f"n{i}", now=f"2026-10-26T15:0{i}:00Z")
    return log, files


def rewrite(log, entries):
    log.write_text("".join(json.dumps(e) + "\n" for e in entries))


def test_intact_chain_verifies(setup):
    log, _ = setup
    assert er.verify_chain(er.read_log(log)) == []


def test_hash_matches_known_value(tmp_path):
    f = tmp_path / "x.txt"; f.write_bytes(b"abc")
    assert er.sha256_file(f) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_edited_entry_is_detected(setup):
    log, _ = setup
    e = er.read_log(log); e[1]["note"] = "changed later"; rewrite(log, e)
    assert any("edited" in p for p in er.verify_chain(er.read_log(log)))


def test_deleted_entry_is_detected(setup):
    log, _ = setup
    e = er.read_log(log); del e[1]; rewrite(log, e)
    probs = er.verify_chain(er.read_log(log))
    assert any("missing or reordered" in p for p in probs) and any("broken" in p for p in probs)


def test_reordered_entries_are_detected(setup):
    log, _ = setup
    e = er.read_log(log); e[0], e[1] = e[1], e[0]; rewrite(log, e)
    assert er.verify_chain(er.read_log(log))


def test_rehashing_one_entry_still_breaks_the_next_link(setup):
    log, _ = setup
    e = er.read_log(log); e[0]["note"] = "forged"; e[0]["entry_hash"] = er.entry_hash(e[0]); rewrite(log, e)
    assert any("entry 2: link" in p for p in er.verify_chain(er.read_log(log)))


def test_changed_file_does_not_match(setup):
    log, files = setup
    files[0].write_text("report v1, quietly edited")
    ok, msg = er.check_file(er.read_log(log), files[0])
    assert not ok and "does not match" in msg


def test_unchanged_file_matches(setup):
    log, files = setup
    ok, _ = er.check_file(er.read_log(log), files[2])
    assert ok


def test_older_version_is_reported(setup, tmp_path):
    log, files = setup
    files[0].write_text("report v2"); er.append(log, files[0], note="v2")
    files[0].write_text("report v1")
    ok, msg = er.check_file(er.read_log(log), files[0])
    assert not ok and "older version" in msg


def test_refuses_to_append_to_tampered_log(setup, tmp_path):
    log, files = setup
    e = er.read_log(log); e[2]["file_sha256"] = "0" * 64; rewrite(log, e)
    with pytest.raises(ValueError):
        er.append(log, files[0])
