def list_membership_baseline(candidates, allowed):
    return [v for v in candidates if v in allowed]


def set_membership_optimized(candidates, allowed):
    allowed_set = set(allowed)
    return [v for v in candidates if v in allowed_set]


def duplicate_check_baseline(values):
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                return True
    return False


def duplicate_check_optimized(values):
    seen = set()
    for value in values:
        if value in seen:
            return True
        seen.add(value)
    return False


def make_inputs(size):
    if size < 1:
        raise ValueError("size must be positive")
    return list(range(size)), list(range(0, size, 3))
