import argparse
import json
import sys
from pathlib import Path
from green_analyzer.analyzer import analyze_file, findings_as_dicts


def main():
    parser = argparse.ArgumentParser(description="Analyze Python source for selected efficiency heuristics.")
    parser.add_argument("file")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        rows = findings_as_dicts(analyze_file(args.file))
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if not rows:
        print("No findings from configured rules.")
    for f in rows:
        print(f"[{f['severity'].upper()}] {f['rule_id']} line {f['line']}: {f['message']}")
        print(f"  Why: {f['explanation']}\n  Try: {f['suggestion']}")
    if args.json_output:
        out = Path(args.json_output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"JSON written to {out}")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
