"""Read a filled-in tracker CSV and write a plain-text chronology sorted by date."""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_tracker import validate  # noqa: E402


def describe(row: dict) -> str:
    action = (row.get("action_taken") or "").strip()
    summary = (row.get("summary") or "").strip()
    text = action or summary
    issue_id = (row.get("issue_id") or "").strip()
    if issue_id:
        return f"{issue_id}: {text}" if text else issue_id
    return text


def build_chronology(path: str) -> tuple[list[str], list[str]]:
    """Return (chronology lines sorted by date, undated or unparseable report lines).

    A row contributes one line for its action_date and, if the row records one, a
    second line for its response_received date. response_due is a deadline rather
    than something that happened, so it is not an event.
    """
    dated: list[tuple[date, str]] = []
    undated: list[str] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            return [], []
        for line, row in enumerate(reader, start=2):
            issue_id = (row.get("issue_id") or "").strip() or f"row {line}"
            raw_date = (row.get("action_date") or "").strip()
            evidence = (row.get("evidence") or "").strip() or "no evidence recorded"
            desc = describe(row)

            if not raw_date:
                undated.append(f"{issue_id}: no action_date recorded ({desc})")
                continue
            try:
                parsed = date.fromisoformat(raw_date)
            except ValueError:
                undated.append(
                    f"{issue_id}: action_date {raw_date!r} could not be parsed ({desc})"
                )
                continue
            dated.append((parsed, f"{parsed.isoformat()} | {desc} | {evidence}"))

            raw_reply = (row.get("response_received") or "").strip()
            if not raw_reply:
                continue
            try:
                replied = date.fromisoformat(raw_reply)
            except ValueError:
                undated.append(
                    f"{issue_id}: response_received {raw_reply!r} could not be parsed"
                )
                continue
            reply_desc = f"{issue_id}: response received" if issue_id else "response received"
            dated.append((replied, f"{replied.isoformat()} | {reply_desc} | {evidence}"))

    dated.sort(key=lambda item: item[0])
    return [line for _, line in dated], undated


def render(lines: list[str], undated: list[str]) -> str:
    out: list[str] = []
    if lines:
        out.extend(lines)
    else:
        out.append("(no dated events)")
    if undated:
        out.append("")
        out.append("UNDATED OR UNPARSEABLE ROWS, not included above:")
        out.extend(undated)
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to your tracker CSV")
    args = parser.parse_args()

    try:
        problems = validate(args.path)
    except FileNotFoundError:
        print(f"no such file: {args.path}", file=sys.stderr)
        return 2

    if problems:
        print(f"{args.path}: cannot export, fix these problems first", file=sys.stderr)
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"\n{len(problems)} problem(s)", file=sys.stderr)
        return 1

    lines, undated = build_chronology(args.path)
    sys.stdout.write(render(lines, undated))
    return 0


if __name__ == "__main__":
    sys.exit(main())
