import os

from flask import current_app


def plugin_available(plugin_name: str) -> bool:
    """
    check if a plugin (Sentry, apm, logstash) is available in the current environment.
    :return True if available else False
    """
    mode = os.environ.get("MODE", None)
    if mode:
        return mode.lower() in current_app.config[f"{plugin_name.upper()}_AVAILABLE_IN"]
    else:
        raise EnvironmentError("MODE not in environment variables")
