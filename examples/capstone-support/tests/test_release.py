"""Release governance tests (Modules 09 + 15): gates, acks, rollback.

State paths are monkeypatched into a temp directory so tests never touch the
real release.json / releases/ on disk.
"""

from __future__ import annotations

import argparse

import pytest

import release


@pytest.fixture()
def isolated(tmp_path, monkeypatch):
    """Point the release tool at a scratch state file and release folder."""
    monkeypatch.setattr(release, "STATE", tmp_path / "release.json")
    monkeypatch.setattr(release, "REL", tmp_path / "releases")
    return tmp_path


def _record(**overrides) -> dict:
    base = {
        "id": "r001", "at": "2026-10-26T00:00:00+00:00", "note": "test",
        "by": "test", "gate": {"passed": True},
        "fairness_within_target": True, "fairness_gap": 0.0,
        "roc_auc": 0.7662, "threshold": 0.25,
        "data_sha256": "x", "model_sha256": "y",
    }
    base.update(overrides)
    return base


def _state_with(record: dict) -> dict:
    return {"releases": {record["id"]: record}, "current": None,
            "previous": None, "history": []}


def test_promotion_requires_a_passed_gate(isolated, monkeypatch):
    state = _state_with(_record(gate={"passed": False}))
    monkeypatch.setattr(release, "load", lambda: state)
    monkeypatch.setattr(release, "save", lambda s: None)
    args = argparse.Namespace(release="r001", ack="", by="t")
    with pytest.raises(SystemExit, match="never passed its quality gate"):
        release.cmd_promote(args)


def test_over_target_fairness_needs_an_explicit_ack(isolated, monkeypatch):
    state = _state_with(_record(fairness_within_target=False, fairness_gap=0.1318))
    monkeypatch.setattr(release, "load", lambda: state)
    monkeypatch.setattr(release, "save", lambda s: None)
    with pytest.raises(SystemExit, match="OVER-TARGET fairness gap"):
        release.cmd_promote(argparse.Namespace(release="r001", ack="", by="t"))


def test_ack_allows_promotion_and_is_recorded(isolated, monkeypatch):
    state = _state_with(_record(fairness_within_target=False, fairness_gap=0.1318))
    monkeypatch.setattr(release, "load", lambda: state)
    monkeypatch.setattr(release, "save", lambda s: None)

    args = argparse.Namespace(release="r001",
                              ack="documented in risk register, mitigations agreed",
                              by="reviewer")
    assert release.cmd_promote(args) == 0
    assert state["current"] == "r001"
    entry = state["history"][-1]
    assert entry["action"] == "promote" and entry["ack"].startswith("documented")


def test_rollback_restores_the_previous_release(isolated, monkeypatch):
    state = _state_with(_record())
    state["current"], state["previous"] = "r002", "r001"
    monkeypatch.setattr(release, "load", lambda: state)
    monkeypatch.setattr(release, "save", lambda s: None)

    assert release.cmd_rollback(argparse.Namespace()) == 0
    assert state["current"] == "r001" and state["previous"] == "r002"
    assert state["history"][-1]["action"] == "rollback"


def test_rollback_without_history_refuses(monkeypatch):
    monkeypatch.setattr(release, "load",
                        lambda: {"releases": {}, "current": "r001",
                                 "previous": None, "history": []})
    with pytest.raises(SystemExit, match="nothing to roll back"):
        release.cmd_rollback(argparse.Namespace())