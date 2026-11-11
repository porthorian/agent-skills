def parse_region(value):
    region = value.strip().casefold()
    if not region:
        raise ValueError("region is required")
    return region
