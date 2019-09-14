import os


def get_env() -> str:
    return os.environ.get("MODE")


def is_production() -> bool:
    return get_env() == "PRODUCTION"


def is_staging() -> bool:
    return get_env() == "STAGING"


def is_testing() -> bool:
    return get_env() == "TESTING"
