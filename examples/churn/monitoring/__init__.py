"""Prediction monitoring (Module 14): log -> detect drift -> measure
performance -> decide (with a human in the loop).

    python -m monitoring.log_predictions --scenario baseline --labels
    python -m monitoring.drift --snapshot
    python -m monitoring.log_predictions --scenario shift
    python -m monitoring.drift
    python -m monitoring.log_predictions --scenario degrade --labels
    python -m monitoring.performance
    python -m monitoring.decision

Everything runs offline on synthetic data. The stages are deliberately
separate because they answer four *different* questions:

  drift        "does the input distribution still look like training?"
  performance  "given labels, is the model still accurate?"
  decision     "given both, should a human retrain, wait, or investigate?"

Drift alone is never proof of a bad model — that is the module's core lesson.
"""