"""Registry tests — stage / promote / rollback / verify, isolated to tmp.

    python -m pytest -q

The whole point: release bookkeeping is tested *without* touching the
real `versions/` folder, so a failed test never corrupts your registry.
"""

from __future__ import annotations

import json
import pathlib

import joblib
import pytest

import registry as R
import train as T


@pytest.fixture()
def isolated(tmp_path: pathlib.Path, monkeypatch) -> pathlib.Path:
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    monkeypatch.setattr(R, "ARTIFACTS", artifacts)
    monkeypatch.setattr(R, "VERSIONS", tmp_path / "versions")
    monkeypatch.setattr(R, "STATE", tmp_path / "registry.json")

    model, info = T.train(T.generate(rows=300))
    joblib.dump(model, artifacts / "model.joblib")
    (artifacts / "model_info.json").write_text(json.dumps(info),
                                               encoding="utf-8")
    return tmp_path


def test_stage_creates_version_with_recorded_hash(isolated):
    vid = R.stage("first")
    assert vid == "v001"
    assert (isolated / "versions" / "v001" / "model.joblib").exists()
    state = R.load_state()
    assert state["versions"]["v001"]["status"] == "staged"
    assert len(state["versions"]["v001"]["sha256"]) == 64


def test_promote_and_rollback_move_current(isolated):
    v1 = R.stage("one")
    R.promote(v1)
    assert R.load_state()["current"] == v1

    v2 = R.stage("two")
    R.promote(v2)
    state = R.load_state()
    assert state["current"] == v2 and state["previous"] == v1
    assert state["versions"][v1]["status"] == "superseded"

    R.rollback()
    state = R.load_state()
    assert state["current"] == v1 and state["previous"] == v2
    # the audit trail records the mechanism: rollback is implemented as a
    # promote to the previous version, plus an explicit rollback entry
    actions = [h["action"] for h in state["history"]]
    assert actions[-1] == "rollback"
    assert state["history"][-1]["to"] == v1
    assert state["history"][-1]["from"] == v2


def test_verify_detects_a_tampered_model(isolated):
    vid = R.stage("watch me")
    assert R.verify() == 0                       # bytes match the record

    (isolated / "versions" / vid / "model.joblib").write_bytes(b"corrupted!")
    assert R.verify() == 1                       # mismatch is a failure


def test_promote_unknown_version_fails_loudly(isolated):
    with pytest.raises(SystemExit):
        R.promote("v999")


def test_rollback_without_history_fails_loudly(isolated):
    with pytest.raises(SystemExit):
        R.rollback()
