"""Example source for the analyzer; findings are heuristic."""
def find_common_items(records, blocked_items):
    common = []
    for record in records:
        for item in record:
            if item in blocked_items:
                common.append(item)
    return common
