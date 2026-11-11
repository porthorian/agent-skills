def display_label(value):
    """Trim surrounding whitespace while preserving the displayed case."""
    return value.strip()


def lookup_key(value):
    """Trim whitespace and produce a case-insensitive lookup key."""
    return value.strip().casefold()
