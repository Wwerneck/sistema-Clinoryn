from contextvars import ContextVar

current_request = ContextVar("audit_request", default=None)
