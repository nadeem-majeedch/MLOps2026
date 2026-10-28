"""Tests for the monitoring and orchestration helpers (Modules 13-14).

These are unit tests: fast, offline, no model training required.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from monitoring.decision import ACTIONS
from monitoring.drift import psi, verdict_for
from monitoring.log_predictions import broken_rule, churn_rule


def test_psi_of_identical_distributions_is_near_zero():
    rng = np.random.default_rng(0)
    sample = rng.normal(50, 10, 2000)
    assert psi(sample, sample) == 0.0


def test_psi_grows_with_a_real_shift():
    rng = np.random.default_rng(0)
    reference = rng.normal(50, 10, 2000)
    shifted = rng.normal(70, 10, 2000)
    assert psi(reference, shifted) > 0.20


def test_psi_is_never_negative():
    rng = np.random.default_rng(1)
    a = rng.normal(0, 1, 500)
    b = rng.normal(0.5, 1, 500)
    assert psi(a, b) >= 0.0


def test_verdict_thresholds_follow_the_documented_rule():
    assert verdict_for(0.05, 0.5) == "stable"
    assert verdict_for(0.15, 0.5) == "moderate"
    assert verdict_for(0.30, 0.5) == "strong"
    assert verdict_for(0.05, 0.001) == "moderate"   # tiny p-value still alerts


def test_decision_matrix_covers_all_four_cases():
    assert ACTIONS[(False, False)] == "KEEP"
    assert ACTIONS[(True, False)] == "MONITOR"          # drift != proof
    assert ACTIONS[(False, True)] == "INVESTIGATE"
    assert ACTIONS[(True, True)] == "RETRAIN CANDIDATE"


def test_same_rule_gives_same_labels_for_same_features():
    df = pd.DataFrame(
        {
            "monthly_charges": [70.0, 40.0],
            "support_tickets": [2, 0],
            "tenure_months": [12, 40],
            "contract_type": ["monthly", "two_year"],
        }
    )
    first = churn_rule(df)
    second = churn_rule(df)
    assert np.array_equal(first, second)


def test_broken_rule_disagrees_with_the_original_rule_somewhere():
    rng = np.random.default_rng(3)
    df = pd.DataFrame(
        {
            "monthly_charges": rng.normal(65, 20, 300).round(2),
            "support_tickets": rng.poisson(1.2, 300),
            "tenure_months": rng.integers(1, 72, 300),
            "contract_type": rng.choice(["monthly", "one_year", "two_year"], 300),
        }
    )
    assert not np.array_equal(churn_rule(df), broken_rule(df, rng))