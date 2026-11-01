import argparse
import json
from pathlib import Path
from examples.workloads import (list_membership_baseline, set_membership_optimized,
    duplicate_check_baseline, duplicate_check_optimized, make_inputs)
from green_analyzer.benchmark import compare_functions


def run_suite(size=1500, repeats=5):
    candidates, allowed = make_inputs(size)
    a = compare_functions(list_membership_baseline, set_membership_optimized,
        (candidates, allowed), repeats, "List vs set membership")
    b = compare_functions(duplicate_check_baseline, duplicate_check_optimized,
        (list(range(size)),), repeats, "Nested-loop vs set duplicate check")
    return [a, b]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--size", type=int, default=1500)
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--output", default="reports/benchmark_results.json")
    a = p.parse_args()
    if a.size < 1 or a.repeats < 1:
        p.error("--size and --repeats must be positive")
    results = run_suite(a.size, a.repeats)
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"size": a.size, "repeats": a.repeats, "results": results}, indent=2), encoding="utf-8")
    for r in results:
        print(f"\n{r['workload']}: equivalent={r['outputs_equivalent']}")
        if r["outputs_equivalent"]:
            print(f"  baseline median: {r['baseline']['median_seconds']:.6f} s")
            print(f"  optimized median: {r['optimized']['median_seconds']:.6f} s")
            print(f"  speedup: {r['speedup']:.2f}x")
            print(f"  peak Python allocations: {r['baseline']['median_peak_bytes']:.0f} -> {r['optimized']['median_peak_bytes']:.0f} bytes")
        else:
            print(r.get("error"))
    print(f"\nSaved results to {out}")
    print("Runtime and tracemalloc are proxies, not direct electricity measurements.")


if __name__ == "__main__":
    main()
