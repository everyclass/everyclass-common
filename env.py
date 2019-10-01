import os

from typing import Optional


def get_env() -> Optional[str]:
    return os.environ.get("MODE")


def is_production() -> bool:
    return get_env() == "PRODUCTION"


def is_staging() -> bool:
    return get_env() == "STAGING"


def is_testing() -> bool:
    return get_env() == "TESTING"
