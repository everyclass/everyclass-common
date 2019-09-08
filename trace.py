import os

from ddtrace import patch_all, tracer


def patch():
    """设置 datadog tracer，需要保证环境内有 DD_AGENT_HOST、DD_TRACE_AGENT_PORT 环境变量"""
    patch_all()
    if os.environ.get("DD_AGENT_HOST", None) and os.environ.get("DD_TRACE_AGENT_PORT", None):
        tracer.configure(hostname=os.environ['DD_AGENT_HOST'],
                         port=os.environ['DD_TRACE_AGENT_PORT'])
    else:
        print("WARNING: or DD_TRACE_AGENT_PORT not set, ignore configuring datadog tracer.")
