"""Validate a tracker CSV against the kit schema and report every problem found."""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date

COLUMNS = [
    "issue_id", "bucket", "summary", "evidence", "rule_touchpoint", "forum",
    "status", "action_taken", "action_date", "sent_method", "response_due",
    "response_received", "amount_disputed", "notes",
]
REQUIRED = {"issue_id", "bucket", "summary", "status"}
BUCKETS = {"money", "communication", "property", "conduct"}
STATUSES = {"open", "asked", "escalated", "resolved", "dropped"}
ID_RE = re.compile(r"^I-\d{2,}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_FIELDS = ("action_date", "response_due", "response_received")


def check_date(value: str) -> str | None:
    if not DATE_RE.match(value):
        return "not YYYY-MM-DD"
    try:
        date.fromisoformat(value)
    except ValueError:
        return "not a real calendar date"
    return None


def validate(path: str) -> list[str]:
    problems: list[str] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            return [f"{path}: file is empty"]
        missing = [c for c in COLUMNS if c not in reader.fieldnames]
        if missing:
            problems.append(f"header: missing columns {', '.join(missing)}")
        extra = [c for c in reader.fieldnames if c not in COLUMNS]
        if extra:
            problems.append(f"header: unexpected columns {', '.join(extra)}")

        seen_ids: set[str] = set()
        for line, row in enumerate(reader, start=2):
            surplus = row.get(None)
            if surplus:
                problems.append(
                    f"row {line}: {len(surplus)} value(s) past the last column, "
                    "usually an unquoted comma; quote the cell or remove the comma"
                )

            for field in REQUIRED:
                if not (row.get(field) or "").strip():
                    problems.append(f"row {line}: {field} is required")

            issue_id = (row.get("issue_id") or "").strip()
            if issue_id:
                if not ID_RE.match(issue_id):
                    problems.append(f"row {line}: issue_id {issue_id!r} is not I-NN")
                elif issue_id in seen_ids:
                    problems.append(f"row {line}: issue_id {issue_id} is duplicated")
                else:
                    seen_ids.add(issue_id)

            bucket = (row.get("bucket") or "").strip()
            if bucket and bucket not in BUCKETS:
                problems.append(f"row {line}: bucket {bucket!r} not in {sorted(BUCKETS)}")

            status = (row.get("status") or "").strip()
            if status and status not in STATUSES:
                problems.append(f"row {line}: status {status!r} not in {sorted(STATUSES)}")

            for field in DATE_FIELDS:
                value = (row.get(field) or "").strip()
                if value:
                    bad = check_date(value)
                    if bad:
                        problems.append(f"row {line}: {field} {value!r} {bad}")

            amount = (row.get("amount_disputed") or "").strip()
            if amount:
                cleaned = amount.replace(",", "")
                try:
                    float(cleaned)
                except ValueError:
                    problems.append(
                        f"row {line}: amount_disputed {amount!r} is not a plain number"
                    )
                if any(sym in amount for sym in "$£€"):
                    problems.append(
                        f"row {line}: amount_disputed {amount!r} should have no currency symbol"
                    )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to your tracker CSV")
    args = parser.parse_args()

    try:
        problems = validate(args.path)
    except FileNotFoundError:
        print(f"no such file: {args.path}", file=sys.stderr)
        return 2

    if not problems:
        print(f"{args.path}: ok")
        return 0
    for problem in problems:
        print(problem)
    print(f"\n{len(problems)} problem(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
