"""Data tests (Module 04/07 layers) for the capstone dataset."""

from __future__ import annotations

from src.validate import run_checks


def test_all_contract_checks_pass_on_generated_data(data, config):
    checks = run_checks(data, config)
    failed = [c["name"] for c in checks if not c["ok"]]
    assert not failed, f"contract violations: {failed}"


def test_leakage_trap_exists_in_the_file(data):
    # The trap must be present — otherwise the guard proves nothing.
    assert "term_end_flag" in data.columns


def test_no_nulls_in_modelled_columns(data, config):
    cols = config["features"]["numeric"] + [config["features"]["target"]]
    assert data[cols].isna().sum().sum() == 0


def test_student_refs_are_unique_synthetic_ids(data):
    assert data["student_ref"].is_unique
    assert data["student_ref"].str.match(r"^S\d+$").all()
    # no real-person fields exist at all
    for column in ("name", "email", "national_id", "student_id"):
        assert column not in data.columns


def test_target_rate_is_plausible(data):
    rate = data["at_risk"].mean()
    assert 0.02 <= rate <= 0.60, f"implausible target rate {rate:.3f}"