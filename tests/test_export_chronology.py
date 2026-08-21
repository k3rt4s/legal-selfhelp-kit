"""Tests for the chronology exporter, covering ordering, missing dates, and rejection paths."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from export_chronology import build_chronology, render  # noqa: E402

HEADER = (
    "issue_id,bucket,summary,evidence,rule_touchpoint,forum,status,"
    "action_taken,action_date,sent_method,response_due,response_received,"
    "amount_disputed,notes"
)
ROW_1 = "I-01,money,Rate not in agreement,inv.pdf,Rule 1.5(b),demand,asked,Itemized bill request sent,2026-04-10,mail,2026-04-24,,1200.00,"
ROW_2 = "I-02,communication,Lawyer stopped responding,email_thread.pdf,Rule 1.4(a),demand,asked,Status request sent,2026-02-01,email,2026-02-15,,,"
ROW_REPLIED = "I-03,money,Unearned advance,receipt.pdf,Rule 1.16(d),demand,asked,Refund request sent,2026-03-01,mail,2026-03-15,2026-03-12,900.00,"
ROW_BAD_REPLY = "I-04,money,Unearned advance,receipt.pdf,Rule 1.16(d),demand,asked,Refund request sent,2026-03-01,mail,2026-03-15,March 12,900.00,"


def write(tmp_path: Path, *rows: str) -> str:
    target = tmp_path / "tracker.csv"
    target.write_text("\n".join((HEADER, *rows)) + "\n", encoding="utf-8")
    return str(target)


def test_good_tracker_produces_one_sorted_line_per_row(tmp_path: Path) -> None:
    lines, undated = build_chronology(write(tmp_path, ROW_1, ROW_2))
    assert undated == []
    assert lines == [
        "2026-02-01 | I-02: Status request sent | email_thread.pdf",
        "2026-04-10 | I-01: Itemized bill request sent | inv.pdf",
    ]


def test_response_received_becomes_a_second_event(tmp_path: Path) -> None:
    lines, undated = build_chronology(write(tmp_path, ROW_REPLIED))
    assert undated == []
    assert lines == [
        "2026-03-01 | I-03: Refund request sent | receipt.pdf",
        "2026-03-12 | I-03: response received | receipt.pdf",
    ]


def test_response_due_is_not_an_event(tmp_path: Path) -> None:
    lines, _ = build_chronology(write(tmp_path, ROW_REPLIED))
    assert not any("2026-03-15" in line for line in lines)


def test_unparseable_response_date_is_reported_not_dropped(tmp_path: Path) -> None:
    lines, undated = build_chronology(write(tmp_path, ROW_BAD_REPLY))
    assert len(lines) == 1
    assert len(undated) == 1
    assert "response_received" in undated[0]
    assert "I-04" in undated[0]


def test_empty_tracker_has_no_dated_events(tmp_path: Path) -> None:
    lines, undated = build_chronology(write(tmp_path))
    assert lines == []
    assert undated == []
    assert render(lines, undated) == "(no dated events)\n"


def test_out_of_order_rows_are_sorted_by_date(tmp_path: Path) -> None:
    lines, _ = build_chronology(write(tmp_path, ROW_1, ROW_2))
    dates = [line.split(" | ", 1)[0] for line in lines]
    assert dates == sorted(dates)


def test_missing_date_is_reported_and_not_dropped(tmp_path: Path) -> None:
    row = ROW_1.replace(",2026-04-10,", ",,", 1)
    lines, undated = build_chronology(write(tmp_path, row))
    assert lines == []
    assert len(undated) == 1
    assert "I-01" in undated[0]
    assert "no action_date recorded" in undated[0]


def test_unparseable_date_is_reported_and_not_dropped(tmp_path: Path) -> None:
    row = ROW_1.replace(",2026-04-10,", ",2026-02-31,", 1)
    lines, undated = build_chronology(write(tmp_path, row))
    assert lines == []
    assert len(undated) == 1
    assert "could not be parsed" in undated[0]


def test_render_labels_the_trailing_undated_section(tmp_path: Path) -> None:
    row = ROW_1.replace(",2026-04-10,", ",,", 1)
    lines, undated = build_chronology(write(tmp_path, row))
    text = render(lines, undated)
    assert "UNDATED OR UNPARSEABLE ROWS" in text
    assert "I-01" in text


def test_main_refuses_a_malformed_tracker(tmp_path: Path, capsys) -> None:
    from export_chronology import main

    target = tmp_path / "tracker.csv"
    target.write_text("issue_id,bucket\nI-01,money\n", encoding="utf-8")
    old_argv = sys.argv
    sys.argv = ["export_chronology.py", str(target)]
    try:
        exit_code = main()
    finally:
        sys.argv = old_argv
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "cannot export" in captured.err
    assert "missing columns" in captured.err


def test_main_exports_a_good_tracker(tmp_path: Path, capsys) -> None:
    from export_chronology import main

    target = Path(write(tmp_path, ROW_1))
    old_argv = sys.argv
    sys.argv = ["export_chronology.py", str(target)]
    try:
        exit_code = main()
    finally:
        sys.argv = old_argv
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "2026-04-10 | I-01: Itemized bill request sent | inv.pdf" in captured.out
