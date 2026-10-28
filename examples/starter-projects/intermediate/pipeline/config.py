"""Configuration loading with validation — the intermediate starter's
first lesson: a config you did not validate is just an undocumented
crash waiting to happen.

    config = load_config()                 # config.yaml next to this package
    config = load_config(path)             # or an explicit path
"""

from __future__ import annotations

import pathlib
from typing import Any

import yaml

DEFAULT_PATH = pathlib.Path(__file__).resolve().parent.parent / "config.yaml"


class ConfigError(ValueError):
    """The configuration is invalid — name the key and the reason."""


REQUIRED_KEYS = ("seed", "rows", "test_size", "threshold", "output_dir")


def load_config(path: pathlib.Path = DEFAULT_PATH) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"missing config file: {path}")
    with path.open(encoding="utf-8") as fh:
        config = yaml.safe_load(fh)
    if not isinstance(config, dict):
        raise ConfigError(f"{path.name} must contain a YAML mapping")
    validate(config, source=path.name)
    return config


def validate(config: dict[str, Any], source: str = "config") -> None:
    """Fail loudly on bad values. Every message names the offending key."""
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ConfigError(f"{source}: missing required key '{key}'")

    if not isinstance(config["seed"], int):
        raise ConfigError(f"{source}: seed must be an integer")
    if not isinstance(config["rows"], int) or config["rows"] < 100:
        raise ConfigError(f"{source}: rows must be an integer >= 100")
    if not 0.0 < float(config["test_size"]) < 1.0:
        raise ConfigError(f"{source}: test_size must be between 0 and 1 "
                          f"(got {config['test_size']!r})")
    if not 0.0 <= float(config["threshold"]) <= 1.0:
        raise ConfigError(f"{source}: threshold must be in [0, 1] "
                          f"(got {config['threshold']!r})")
    if not isinstance(config["output_dir"], str) or not config["output_dir"]:
        raise ConfigError(f"{source}: output_dir must be a non-empty string")
