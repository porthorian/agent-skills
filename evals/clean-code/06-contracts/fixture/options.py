def parse_limit(value):
    """Default to 100; accept integers >= 1. None and '' select the default."""
    if value is None or value == "":
        return 100
    parsed = int(value)
    if parsed < 1:
        raise ValueError("limit must be positive")
    return parsed


def parse_retries(value):
    """Default to 0; accept integers >= 0. None and '' select the default."""
    if value is None or value == "":
        return 0
    parsed = int(value)
    if parsed < 0:
        raise ValueError("retries must not be negative")
    return parsed
