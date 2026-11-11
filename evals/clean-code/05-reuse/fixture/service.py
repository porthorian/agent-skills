from normalization import parse_region


def create_job(region):
    return {"region": parse_region(region), "preview": False}


def preview_job(region):
    normalized = region.strip().casefold()
    if not normalized:
        raise ValueError("region is required")
    return {"region": normalized, "preview": True}
