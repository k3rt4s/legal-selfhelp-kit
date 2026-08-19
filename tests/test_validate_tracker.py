"""Tests for the tracker validator, covering a clean file and each rejection path."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_tracker import validate  # noqa: E402

HEADER = (
    "issue_id,bucket,summary,evidence,rpc_touchpoint,forum,status,"
    "action_taken,action_date,sent_method,response_due,response_received,"
    "amount_disputed,notes"
)
GOOD_ROW = "I-01,money,Rate not in agreement,inv.pdf,RPC 1.5(b),demand,asked,Letter sent,2026-04-10,mail,2026-04-24,,1200.00,"


def write(tmp_path: Path, *rows: str) -> str:
    target = tmp_path / "tracker.csv"
    target.write_text("\n".join((HEADER, *rows)) + "\n", encoding="utf-8")
    return str(target)


def test_clean_file_has_no_problems(tmp_path: Path) -> None:
    assert validate(write(tmp_path, GOOD_ROW)) == []


def test_shipped_template_is_valid() -> None:
    template = Path(__file__).resolve().parents[1] / "tracker" / "tracker_template.csv"
    assert validate(str(template)) == []


def test_bad_issue_id_is_reported(tmp_path: Path) -> None:
    row = GOOD_ROW.replace("I-01", "1", 1)
    problems = validate(write(tmp_path, row))
    assert any("is not I-NN" in p for p in problems)


def test_duplicate_issue_id_is_reported(tmp_path: Path) -> None:
    problems = validate(write(tmp_path, GOOD_ROW, GOOD_ROW))
    assert any("duplicated" in p for p in problems)


def test_unknown_bucket_is_reported(tmp_path: Path) -> None:
    row = GOOD_ROW.replace(",money,", ",feelings,", 1)
    problems = validate(write(tmp_path, row))
    assert any("bucket" in p for p in problems)


def test_unknown_status_is_reported(tmp_path: Path) -> None:
    row = GOOD_ROW.replace(",asked,", ",thinking,", 1)
    problems = validate(write(tmp_path, row))
    assert any("status" in p for p in problems)


def test_bad_date_format_is_reported(tmp_path: Path) -> None:
    row = GOOD_ROW.replace("2026-04-10", "04/10/2026", 1)
    problems = validate(write(tmp_path, row))
    assert any("not YYYY-MM-DD" in p for p in problems)


def test_impossible_date_is_reported(tmp_path: Path) -> None:
    row = GOOD_ROW.replace("2026-04-10", "2026-02-31", 1)
    problems = validate(write(tmp_path, row))
    assert any("not a real calendar date" in p for p in problems)


def test_currency_symbol_is_reported(tmp_path: Path) -> None:
    row = GOOD_ROW.replace(",1200.00,", ",$1200.00,", 1)
    problems = validate(write(tmp_path, row))
    assert any("currency symbol" in p for p in problems)


def test_missing_required_field_is_reported(tmp_path: Path) -> None:
    row = GOOD_ROW.replace("Rate not in agreement", "", 1)
    problems = validate(write(tmp_path, row))
    assert any("summary is required" in p for p in problems)


@pytest.mark.parametrize("missing", ["issue_id", "bucket", "status"])
def test_each_required_column_is_enforced(tmp_path: Path, missing: str) -> None:
    index = HEADER.split(",").index(missing)
    parts = GOOD_ROW.split(",")
    parts[index] = ""
    problems = validate(write(tmp_path, ",".join(parts)))
    assert any(f"{missing} is required" in p for p in problems)
