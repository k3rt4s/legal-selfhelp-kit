"""Tests for the source-health checker, covering table parsing and result classification against fixtures."""
from __future__ import annotations

import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_sources  # noqa: E402
from check_sources import (  # noqa: E402
    ALLOWED_SCHEMES,
    MAX_RESPONSE_BYTES,
    default_fetch,
    FetchResult,
    SourceRow,
    classify,
    claim_match_fraction,
    discover_files,
    parse_reference_file,
    resolve_backref,
    run,
    state_for_file,
    strip_html,
    strip_url_trailing_punctuation,
)


def write(tmp_path: Path, name: str, text: str) -> Path:
    target = tmp_path / name
    target.write_text(text, encoding="utf-8")
    return target


FIXTURE = """# Verification: Testland (state_tl.md)

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| The filing fee for a small claims appeal is $100 | <https://courts.testland.gov/rules/appeal.pdf> | 2026-08-20 | Read directly |
| SUPERSEDED, this row should be skipped | <https://old.testland.gov/gone> | 2026-08-01 | replaced below |

## Flagged: sourced but resting on less than a primary or official publication

| Claim | Source | URL | Reason flagged |
| ----- | ------ | --- | --------------- |
| The bar's ethics hotline number is 555-0100 | Testland Bar FAQ | https://bar.testland.gov/faq | Secondary summary, not primary text |

## Gap list: looked for, not sourced, therefore not claimed

1. No confirmation found for the appeal deadline. See https://example.com/should-not-be-checked
   for what was searched.

## Cut from the pack

1. This claim was removed and has no table row.
"""

BAD_ROW_FIXTURE = """# Verification: Badland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| A claim with no reachable URL anywhere in the row | just a name, no link | 2026-08-20 | oops |
| | https://example.com/empty-claim | 2026-08-20 | claim cell is empty |
"""


def test_state_for_file_names() -> None:
    assert state_for_file(Path("references/verification_ak.md")) == "AK"
    assert state_for_file(Path("references/verification_national.md")) == "NATIONAL"
    assert state_for_file(Path("references/VERIFICATION.md")) == "INDEX"


def test_parse_reference_file_extracts_table_rows(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_tl.md", FIXTURE)
    rows, problems = parse_reference_file(path)

    urls = [r.url for r in rows]
    assert "https://courts.testland.gov/rules/appeal.pdf" in urls
    assert "https://bar.testland.gov/faq" in urls
    assert len(rows) == 2
    assert problems == []


def test_superseded_row_is_skipped(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_tl.md", FIXTURE)
    rows, _ = parse_reference_file(path)
    assert not any("old.testland.gov" in r.url for r in rows)


def test_gap_list_urls_are_not_extracted(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_tl.md", FIXTURE)
    rows, _ = parse_reference_file(path)
    assert not any("example.com/should-not-be-checked" in r.url for r in rows)


def test_state_is_attached_to_each_row(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_tl.md", FIXTURE)
    rows, _ = parse_reference_file(path)
    assert all(r.state == "TL" for r in rows)


def test_unparseable_rows_are_reported_not_dropped(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_bl.md", BAD_ROW_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert rows == []
    assert len(problems) == 2
    reasons = {p.reason for p in problems}
    assert "no URL found in row" in reasons
    assert "empty Claim cell" in reasons


SPLIT_TABLE_FIXTURE = """# Verification: Splitland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| The first claim, inside the table | <https://courts.splitland.gov/one> | 2026-08-20 | Read directly |

| The second claim, cut off from its table by the blank line above | <https://courts.splitland.gov/two> | 2026-08-20 | Orphaned |
| The third claim, also orphaned | <https://courts.splitland.gov/three> | 2026-08-20 | Orphaned |

## Index of files, not a citation table

| State | File | Rows |
| ----- | ---- | ---- |
| Splitland | verification_sl.md | 3 |
"""


def test_rows_cut_off_from_their_table_are_reported_not_guessed(tmp_path: Path) -> None:
    """A blank line inside a table leaves the rows below it with no header; they must surface as unparseable, not be skipped or mapped to the wrong columns."""
    path = write(tmp_path, "verification_sl.md", SPLIT_TABLE_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert [r.url for r in rows] == ["https://courts.splitland.gov/one"]
    assert [p.row_number for p in problems] == [9, 10]
    assert all("no header row above it" in p.reason for p in problems)
    # A well-formed table that is not a citation table is still passed over silently.
    assert not any("Splitland" in p.raw for p in problems)


SAME_URL_FIXTURE = """# Verification: Sameland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| First claim from the statute | https://legis.sameland.gov/statute.pdf | 2026-08-20 | Read directly |
| Second claim from the same statute section | Same URL as above | 2026-08-20 | Read directly |
"""


def test_same_url_as_above_carries_forward(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_sl.md", SAME_URL_FIXTURE)
    rows, problems = parse_reference_file(path)
    urls = [r.url for r in rows]
    assert urls == [
        "https://legis.sameland.gov/statute.pdf",
        "https://legis.sameland.gov/statute.pdf",
    ]
    assert problems == []


BACKREF_FIXTURE = """# Verification: Backrefland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| Colo. RPC 1.15 is split into several subparts | Colo. RPC 1.15 PDF, <https://www.coloradosupremecourt.com/Search/rpcSearch.asp> | 2026-08-20 | Table of contents read directly |
| Rule 1.5(a) lists eight reasonableness factors | Same full RPC text as above | 2026-08-20 | Same fetch |
| Rule 1.16 requires notice on termination | Same Colo. RPC 1.5 PDF as above | 2026-08-20 | Same fetch; full section text read |
"""

NO_PRIOR_URL_FIXTURE = """# Verification: Noprior

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| A claim whose source is a dangling backreference | Same URL as above | 2026-08-20 | nothing came before this row |
"""

PLAIN_CITATION_FIXTURE = """# Verification: Plaincite

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| No Wyoming rule specifically labeled this way was found | No Wyoming rule specifically labeled "nonrefundable fee" was found in the Rules of Professional Conduct | 2026-08-20 | negative finding, no source to check |
"""

GA_URL_COLUMN_FIXTURE = """# Verification status for state_ga.md

## Confirmed against a primary or official source

| Claim | Source | URL | Note |
| ----- | ------ | --- | ---- |
| A Georgia Rule of Professional Conduct requires written fee agreements in contingency matters | State Bar of Georgia, Georgia Rules of Professional Conduct, Rule 1.5(c) | https://www.gabar.org/barrules/handbookdetail.cfm?handbook=1 | Confirmed against the handbook page directly |
"""


def test_backreference_resolves_and_records_inheritance(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_bk.md", BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert len(rows) == 3
    first, second, third = rows
    assert first.inherited_from is None
    assert second.url == first.url
    assert second.inherited_from == first.row_number
    assert third.url == first.url
    assert third.inherited_from == second.row_number


def test_backreference_with_no_prior_url_is_unparseable(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_np.md", NO_PRIOR_URL_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert rows == []
    assert len(problems) == 1
    assert "backreference" in problems[0].reason


def test_plain_citation_with_no_url_stays_unparseable(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_pc.md", PLAIN_CITATION_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert rows == []
    assert len(problems) == 1
    assert problems[0].reason == "no URL found in row"


def test_carried_url_resets_at_file_boundary(tmp_path: Path) -> None:
    first_path = write(tmp_path, "verification_bk.md", BACKREF_FIXTURE)
    second_path = write(tmp_path, "verification_np.md", NO_PRIOR_URL_FIXTURE)
    parse_reference_file(first_path)
    rows, problems = parse_reference_file(second_path)
    assert rows == []
    assert len(problems) == 1
    assert "backreference" in problems[0].reason


def test_ga_style_separate_url_column_is_parsed(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_ga.md", GA_URL_COLUMN_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert len(rows) == 1
    assert rows[0].url == "https://www.gabar.org/barrules/handbookdetail.cfm?handbook=1"


WIDER_SHAPES_FIXTURE = """# Verification: Widerland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| Rule 7(g) governs the base case | Maine Bar Rule 7(g) PDF, <https://www.mebaroverseers.org/rule7.pdf> | 2026-08-20 | Read directly |
| Rule 7(g) also covers a second point | Maine Bar Rule 7(g), same PDF | 2026-08-20 | Same fetch |
| Section 799 covers a related figure | stat799.pdf (above) | 2026-08-20 | Same fetch |
| The RPC text covers a third point | RPC PDF above | 2026-08-20 | Same fetch |
"""

NO_SOURCE_NOTE_FIXTURE = """# Verification: Nosourceland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| No ethics opinion on file retention was located | wyomingbar.org search attempted for ethics opinions on file retention | 2026-08-20 | negative finding |
"""


def test_backreference_rule_number_first_shape_resolves(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_wd.md", WIDER_SHAPES_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert len(rows) == 4
    base = rows[0]
    assert rows[1].url == base.url
    assert rows[1].inherited_from == base.row_number


def test_backreference_parenthesized_above_shape_resolves(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_wd.md", WIDER_SHAPES_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    stat799_row = rows[2]
    assert stat799_row.url == rows[0].url
    assert stat799_row.inherited_from == rows[1].row_number


def test_backreference_trailing_bare_above_shape_resolves(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_wd.md", WIDER_SHAPES_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    rpc_row = rows[3]
    assert rpc_row.url == rows[0].url
    assert rpc_row.inherited_from == rows[2].row_number


def test_bare_extension_is_not_enough_for_descriptor_match() -> None:
    history = [
        (5, "Fee Rules PDF", ["https://courts.example.gov/rules/fee-rules.pdf"]),
        (6, "Complaint overview", ["https://courts.example.gov/help/complaints.html"]),
    ]

    url, row_number, reason = resolve_backref("Same PDF source", "", history)

    assert reason == ""
    assert url == "https://courts.example.gov/help/complaints.html"
    assert row_number == 6


def test_digit_bearing_descriptor_keeps_its_digits() -> None:
    history = [
        (5, "Chapter 24 rules", ["https://courts.example.gov/rules/chapter24.pdf"]),
        (6, "Chapter 25 rules", ["https://courts.example.gov/rules/chapter25.pdf"]),
    ]

    url, row_number, reason = resolve_backref("Same chapter24 source", "", history)

    assert reason == ""
    assert url == "https://courts.example.gov/rules/chapter24.pdf"
    assert row_number == 5


def test_host_backreference_matches_only_host_boundary() -> None:
    history = [
        (5, "Impostor host", ["https://notnjleg.gov.example/statutes/chapter.pdf"]),
        (6, "Real host", ["https://pub.njleg.gov/statutes/chapter.pdf"]),
    ]

    url, row_number, reason = resolve_backref("Same njleg.gov source", "", history)

    assert reason == ""
    assert url == "https://pub.njleg.gov/statutes/chapter.pdf"
    assert row_number == 6


def test_host_backreference_rejects_substring_impostor() -> None:
    history = [
        (5, "Impostor host", ["https://notnjleg.gov.example/statutes/chapter.pdf"]),
    ]

    url, row_number, reason = resolve_backref("Same njleg.gov source", "", history)

    assert url is None
    assert row_number is None
    assert "njleg.gov" in reason


def test_host_backreference_matches_wayback_original_host() -> None:
    archived = "https://web.archive.org/web/20200101000000/https://www.mass.gov/rules/rule-15"
    history = [
        (5, "Archived rule", [archived]),
    ]

    url, row_number, reason = resolve_backref("Same mass.gov Rule 1.5 wayback snapshot as above", "", history)

    assert reason == ""
    assert url == archived
    assert row_number == 5


def test_above_with_named_short_filename_resolves_to_that_file() -> None:
    history = [
        (10, "Practice Book rules", ["https://www.jud.ct.gov/Publications/PracticeBook/PB.pdf"]),
        (
            19,
            "CBA Program Rules of Procedure",
            ["https://www.ctbar.org/docs/lawyer-client-fee-dispute-rules.pdf"],
        ),
        (20, "CBA Program jurisdiction", ["https://www.ctbar.org/docs/lawyer-client-fee-dispute-rules.pdf"]),
    ]

    url, row_number, reason = resolve_backref("PB.pdf (above), Sec. 2-32(a)(2)(A)", "", history)

    assert reason == ""
    assert url == "https://www.jud.ct.gov/Publications/PracticeBook/PB.pdf"
    assert row_number == 10


def test_named_numeric_filename_ignores_punctuation_difference() -> None:
    history = [
        (16, "Court order", ["https://courts.testland.gov/orders/200905.pdf"]),
        (18, "An unrelated statute", ["https://legislature.testland.gov/statutes/376.460"]),
    ]

    url, row_number, reason = resolve_backref("Same order, 2009-05.pdf", "", history)

    assert reason == ""
    assert url == "https://courts.testland.gov/orders/200905.pdf"
    assert row_number == 16


def test_genuine_no_source_note_stays_unparseable(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_ns.md", NO_SOURCE_NOTE_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert rows == []
    assert len(problems) == 1
    assert problems[0].reason == "no URL found in row"


def test_discover_files_includes_verification_and_top_level(tmp_path: Path) -> None:
    write(tmp_path, "verification_ak.md", FIXTURE)
    write(tmp_path, "verification_national.md", FIXTURE)
    write(tmp_path, "VERIFICATION.md", "# index\n")
    write(tmp_path, "state_ak.md", "# not a verification file\n")

    files = discover_files(tmp_path)
    names = {f.name for f in files}
    assert names == {"verification_ak.md", "verification_national.md", "VERIFICATION.md"}


def make_row(claim: str = "the filing fee is $100", url: str = "https://example.gov/x") -> SourceRow:
    return SourceRow(
        file="verification_tl.md", state="TL", section="Confirmed",
        claim=claim, source_cell=url, url=url, retrieved="2026-08-20", row_number=5,
    )


def result(status, body="", content_type="text/html", final_url=None, error=None, redirected=False):
    return FetchResult(
        requested_url="https://example.gov/x",
        final_url=final_url or "https://example.gov/x",
        status=status, content_type=content_type, body=body, error=error, redirected=redirected,
    )


def test_ok_when_claim_words_present() -> None:
    row = make_row(claim="the small claims appeal filing fee is one hundred dollars")
    outcome = classify(row, result(200, body="<html><body>The filing fee for a small claims appeal is $100.</body></html>"))
    assert outcome.bucket == "OK"


def test_no_claim_text_on_real_error_page_with_200(tmp_path: Path) -> None:
    # courts.wa.gov trap: HTTP 200 with a short, unrelated HTML error body.
    row = make_row(claim="the small claims appeal filing fee is one hundred dollars")
    body = "<html><head><title>Error</title></head><body>Page not found</body></html>"
    outcome = classify(row, result(200, body=body))
    assert outcome.bucket == "NO_CLAIM_TEXT"


def test_findlaw_404_page_is_no_claim_text_not_ok() -> None:
    row = make_row(claim="the statute of limitations for legal malpractice is three years")
    body = "<html><body>" + ("404 Error: Page not found. " * 500) + "</body></html>"
    outcome = classify(row, result(200, body=body))
    assert outcome.bucket == "NO_CLAIM_TEXT"


def test_client_rendered_shell_is_flagged_distinctly() -> None:
    row = make_row(claim="the small claims appeal filing fee is one hundred dollars")
    nav = "<div class='nav-item' data-x='y'><span class='ico'></span></div>" * 400
    body = f"<html><body>{nav}</body></html>"
    outcome = classify(row, result(200, body=body))
    assert outcome.bucket == "LIKELY_CLIENT_RENDERED"


def test_courtlistener_202_empty_body_is_blocked_not_broken() -> None:
    row = make_row()
    outcome = classify(row, result(202, body=""))
    assert outcome.bucket == "BLOCKED"


def test_head_style_zero_byte_200_is_not_ok() -> None:
    row = make_row(claim="the filing fee for a small claims appeal is one hundred dollars")
    outcome = classify(row, result(200, body=""))
    assert outcome.bucket in {"NO_CLAIM_TEXT", "LIKELY_CLIENT_RENDERED"}


def test_pdf_is_pdf_unchecked_not_ok() -> None:
    row = make_row()
    outcome = classify(row, result(200, body="%PDF-1.4 binary junk", content_type="application/pdf"))
    assert outcome.bucket == "PDF_UNCHECKED"


def test_redirect_is_reported_with_final_url() -> None:
    row = make_row(url="https://leg.mt.gov/old-page", claim="the fee arbitration rule text")
    r = result(
        200, body="<html><body>fee arbitration rule text</body></html>",
        final_url="https://mca.legmt.gov/old-page", redirected=True,
    )
    outcome = classify(row, r)
    assert outcome.bucket == "REDIRECTED"
    assert "mca.legmt.gov" in outcome.detail


def test_http_error_status_is_not_reported_as_verification() -> None:
    row = make_row()
    outcome = classify(row, result(404, body="not found"))
    assert outcome.bucket == "HTTP_ERROR"
    assert "404" in outcome.detail


def test_unreachable_on_fetch_error() -> None:
    row = make_row()
    r = FetchResult(requested_url=row.url, final_url=row.url, status=None, content_type="", body="", error="timed out")
    outcome = classify(row, r)
    assert outcome.bucket == "UNREACHABLE"


def test_claim_match_survives_curly_quotes_and_tags() -> None:
    claim = 'the lawyer must give a written "fee agreement"'
    page = "<p>The lawyer must give a written &#8220;fee agreement&#8221; before starting work.</p>"
    fraction = claim_match_fraction(claim, page_text=strip_html(page))
    assert fraction is not None and fraction >= 0.5


def test_claim_match_fails_on_unrelated_text() -> None:
    claim = "the small claims appeal filing fee is one hundred dollars in this state"
    fraction = claim_match_fraction(claim, "completely unrelated content about a different topic entirely")
    assert fraction is not None and fraction < 0.5


def test_run_uses_injected_fetch_and_never_touches_the_network(tmp_path: Path) -> None:
    write(tmp_path, "verification_tl.md", FIXTURE)
    calls: list[str] = []

    def fake_fetch(url: str) -> FetchResult:
        calls.append(url)
        return result(200, body=f"<html><body>{url} some content the claim will not match</body></html>")

    outcomes, problems = run(tmp_path, fetch=fake_fetch, delay=0)
    assert len(calls) == len(outcomes) == 2
    assert problems == []


def test_run_respects_limit_and_state(tmp_path: Path) -> None:
    write(tmp_path, "verification_tl.md", FIXTURE)
    write(tmp_path, "verification_national.md", FIXTURE)

    def fake_fetch(url: str) -> FetchResult:
        return result(200, body="content")

    outcomes, _ = run(tmp_path, fetch=fake_fetch, state="tl", delay=0)
    assert all(o.row.state == "TL" for o in outcomes)

    outcomes_limited, _ = run(tmp_path, fetch=fake_fetch, limit=1, delay=0)
    assert len(outcomes_limited) == 1


def test_default_fetch_refuses_a_non_http_scheme() -> None:
    """A URL that is not http or https is reported as refused, never opened."""
    for url in ("file:///etc/passwd", "ftp://example.invalid/x", "gopher://example.invalid"):
        result = default_fetch(url)
        assert result.status is None
        assert "refused" in result.error
        assert result.body == ""


def test_allowed_schemes_are_only_http_and_https() -> None:
    """The scheme allowlist stays an allowlist; widening it should be a deliberate edit."""
    assert set(ALLOWED_SCHEMES) == {"http", "https"}


def test_response_size_is_capped() -> None:
    """The fetcher caps how much of a response it will read into memory."""
    assert 0 < MAX_RESPONSE_BYTES <= 50_000_000


INTERLEAVED_BACKREF_FIXTURE = """# Verification: Interleaveland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| The disciplinary chapter exists | Chapter 9 court rules, <https://courts.testland.gov/chapter9.pdf> | 2026-08-20 | Read directly |
| The grievance commission is reached at this address | Grievance Commission homepage, <https://grievance.testland.org/> | 2026-08-20 | Read directly |
| Rule 9.112 sets the investigation deadline | Same Chapter 9 source, Rule 9.112(A) | 2026-08-20 | Read directly |
| Rule 9.130 sets the appeal deadline | Same Chapter 9 source, Rule 9.130 | 2026-08-20 | Read directly |
"""

NAMED_HOST_BACKREF_FIXTURE = """# Verification: Hostland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| The fund publishes its coverage limits | <https://bar.testland.org/plf.html> and <https://fund.testland.org/who-we-are.html> | 2026-08-20 | Both read directly |
| An unrelated statute sets the limitation period | <https://legislature.testland.gov/statutes/12.html> | 2026-08-20 | Read directly |
| Coverage is capped per claim | fund.testland.org/who-we-are.html (above) | 2026-08-20 | Read directly |
"""

MISSING_HOST_BACKREF_FIXTURE = """# Verification: Missingland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| An unrelated statute sets the limitation period | <https://legislature.testland.gov/statutes/12.html> | 2026-08-20 | Read directly |
| Coverage is capped per claim | fund.testland.org/who-we-are.html (above) | 2026-08-20 | Read directly |
"""

ADJACENT_BACKREF_FIXTURE = """# Verification: Adjacentland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| The fund covers dishonest conduct | <https://courts.testland.gov/Attorneys/Lawyers-Fund> | 2026-08-20 | Read directly |
| Rule 241 defines dishonest conduct | <https://courts.testland.gov/Rules/Rule-241> | 2026-08-20 | Read directly |
| Rule 241 caps the payout | same as above; also the Lawyers' Fund program page | 2026-08-20 | Read directly |
"""


DESCRIPTOR_ABOVE_BACKREF_FIXTURE = """# Verification: Descriptorabove

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| Program rules require written consent | Fee Arbitration Program Rules PDF, <https://bar.testland.gov/fee-arbitration/program-rules.pdf> | 2026-08-20 | Read directly |
| Unrelated statute sets a filing deadline | <https://courts.testland.gov/statutes/deadline.html> | 2026-08-20 | Read directly |
| Program rules allow remote hearings | Fee Arbitration Program Rules PDF, same URL as above | 2026-08-20 | Read directly |
"""


INHERITED_DESCRIPTOR_FIXTURE = """# Verification: Inheriteddescriptor

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| Court rules are published in the practice book | <https://courts.testland.gov/PB.pdf> | 2026-08-20 | Read directly |
| The bar publishes fee dispute rules | CBA Rules of Procedure PDF, <https://bar.testland.gov/fee-dispute-rules.pdf> | 2026-08-20 | Read directly |
| Cost shifting comes from the court rule, not the bar rules | PB.pdf (above), absence checked against CBA Rules of Procedure PDF (above) | 2026-08-20 | Read directly |
| Program rules contain no dollar floor | CBA Rules of Procedure PDF (above), Section IV | 2026-08-20 | Read directly |
"""


INFERENCE_ABOVE_FIXTURE = """# Verification: Inferland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| Inferland Code 78B-2-307 has a four-year catch-all period | <https://legislature.inferland.gov/78B-2-307.pdf> | 2026-08-20 | Read directly |
| The court rule page is unrelated | <https://courts.inferland.gov/rules/view.php?rule=3-0> | 2026-08-20 | Read directly |

## Flagged

| Claim | Source | Reason flagged |
| ----- | ------ | -------------- |
| The catch-all period applies in the absence of a dedicated statute | Inferland Code 78B-2-307(4) itself (Confirmed table above), reasoned by elimination rather than stated directly | The pack states this as an inference, not a settled rule |
"""


NOTE_ONLY_INFERENCE_ABOVE_FIXTURE = """# Verification: Noteinferland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| Noteinferland Code 657-7 has a tort period | <https://legislature.noteinferland.gov/657-7.html> | 2026-08-20 | Read directly |
| The disciplinary rules are hosted by the court | <https://courts.noteinferland.gov/rules> | 2026-08-20 | Read directly |

## Flagged

| Claim | Source | Reason flagged |
| ----- | ------ | -------------- |
| The tort statute may apply to malpractice | Code sections 657-1 and 657-7 (Confirmed table above) | This is reasoned by elimination rather than stated directly |
"""


def test_backreference_skips_an_interleaved_unrelated_source(tmp_path: Path) -> None:
    """A row naming "Same Chapter 9 source" means Chapter 9, not the homepage row between them."""
    path = write(tmp_path, "verification_il.md", INTERLEAVED_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    chapter9, homepage = rows[0], rows[1]
    for row in rows[2:]:
        assert row.url == chapter9.url
        assert row.inherited_from != homepage.row_number


def test_backreference_naming_a_host_finds_it_on_an_earlier_row(tmp_path: Path) -> None:
    """A row naming a host resolves to that host, even when it is the second URL on the earlier row."""
    path = write(tmp_path, "verification_hl.md", NAMED_HOST_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[-1].url == "https://fund.testland.org/who-we-are.html"
    assert rows[-1].inherited_from == rows[0].row_number


def test_backreference_naming_an_uncited_host_is_unparseable(tmp_path: Path) -> None:
    """Naming a host no earlier row carries is reported, never resolved to whatever came last."""
    path = write(tmp_path, "verification_ml.md", MISSING_HOST_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert len(rows) == 1
    assert len(problems) == 1
    assert "fund.testland.org" in problems[0].reason


def test_above_means_the_nearest_source_not_a_word_match(tmp_path: Path) -> None:
    """"same as above" is adjacency; a trailing mention of another page must not pull the row off it."""
    path = write(tmp_path, "verification_ad.md", ADJACENT_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[-1].url == "https://courts.testland.gov/Rules/Rule-241"
    assert rows[-1].inherited_from == rows[1].row_number


def test_above_with_descriptor_resolves_before_adjacency(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_da.md", DESCRIPTOR_ABOVE_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[-1].url == rows[0].url
    assert rows[-1].inherited_from == rows[0].row_number


def test_inherited_backreference_text_does_not_become_a_descriptor_anchor(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_id.md", INHERITED_DESCRIPTOR_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[2].url == "https://courts.testland.gov/PB.pdf"
    assert rows[3].url == "https://bar.testland.gov/fee-dispute-rules.pdf"
    assert rows[3].inherited_from == rows[1].row_number


def test_reasoned_by_elimination_confirmed_above_is_not_a_source_backreference(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_if.md", INFERENCE_ABOVE_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert [row.url for row in rows] == [
        "https://legislature.inferland.gov/78B-2-307.pdf",
        "https://courts.inferland.gov/rules/view.php?rule=3-0",
    ]
    assert len(problems) == 1
    assert problems[0].reason == "no URL found in row"


def test_single_confirmed_above_can_fall_back_to_adjacency() -> None:
    history = [
        (52, "Title 1 PDF", ["https://legislature.testland.gov/title01.pdf"]),
    ]

    url, row_number, reason = resolve_backref("W.S. 1-3-107 itself, Confirmed above", "", history)

    assert reason == ""
    assert url == "https://legislature.testland.gov/title01.pdf"
    assert row_number == 52


def test_note_only_reasoned_by_elimination_confirmed_above_is_not_a_backreference(tmp_path: Path) -> None:
    path = write(tmp_path, "verification_ni.md", NOTE_ONLY_INFERENCE_ABOVE_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert [row.url for row in rows] == [
        "https://legislature.noteinferland.gov/657-7.html",
        "https://courts.noteinferland.gov/rules",
    ]
    assert len(problems) == 1
    assert problems[0].reason == "no URL found in row"


def test_same_url_as_above_with_later_descriptor_does_not_short_circuit() -> None:
    history = [
        (10, "Named Rules PDF", ["https://bar.testland.gov/named-rules.pdf"]),
        (11, "Unrelated source", ["https://courts.testland.gov/unrelated.html"]),
    ]

    url, row_number, reason = resolve_backref("Same URL as above, Named Rules PDF", "", history)

    assert reason == ""
    assert url == "https://bar.testland.gov/named-rules.pdf"
    assert row_number == 10


def test_index_url_above_uses_nearest_index_row() -> None:
    history = [
        (55, "Section 3-501.5 fees", ["https://courts.testland.gov/article-5/section-3-5015-fees"]),
        (56, "Article 5 index", ["https://courts.testland.gov/chapter-3-attorneys-and-practice-law"]),
    ]

    url, row_number, reason = resolve_backref("Same Article 5 index URL as the two rows above", "", history)

    assert reason == ""
    assert url == "https://courts.testland.gov/chapter-3-attorneys-and-practice-law"
    assert row_number == 56


def test_plural_sources_above_is_not_resolved_to_one_url() -> None:
    history = [
        (31, "Polk County page", ["https://bar.testland.gov/polk"]),
        (34, "Polk County PDF", ["https://bar.testland.gov/polk-rules.pdf"]),
    ]

    url, row_number, reason = resolve_backref("Polk County Bar Association pages and PDFs cited above", "", history)

    assert url is None
    assert row_number is None
    assert "multiple sources above" in reason


def test_same_url_plus_second_source_is_not_resolved_to_one_url() -> None:
    history = [
        (56, "Rules page", ["https://courts.testland.gov/rules"]),
        (58, "Same URL", ["https://courts.testland.gov/rules"]),
    ]

    url, row_number, reason = resolve_backref("Same URL, plus Testland Chapter 73 text", "", history)

    assert url is None
    assert row_number is None
    assert "multiple sources above" in reason


def test_all_confirmed_above_multiple_sources_is_not_resolved_to_one_url() -> None:
    history = [
        (49, "Appellate rules", ["https://courts.testland.gov/wrap.pdf"]),
        (50, "Filing fee statute", ["https://legislature.testland.gov/title05.pdf"]),
    ]

    url, row_number, reason = resolve_backref("W.S. 5-3-205 and WRAP Rule 2.09(a), all Confirmed above", "", history)

    assert url is None
    assert row_number is None
    assert "multiple sources above" in reason


def test_confirmed_table_multi_sections_is_not_resolved_to_one_url() -> None:
    history = [
        (61, "Section 657-1", ["https://legislature.testland.gov/657-1.html"]),
        (62, "Section 657-7", ["https://legislature.testland.gov/657-7.html"]),
    ]

    url, row_number, reason = resolve_backref("HRS chapter 657, sections 657-1 and 657-7 (Confirmed table above)", "", history)

    assert url is None
    assert row_number is None
    assert "multiple sources above" in reason


SECTION_NUMBER_BACKREF_FIXTURE = """# Verification: Numberland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| An appeal is reviewed on the record | Testland Rev. Stat. section 25-2733, <https://legislature.testland.gov/statutes.php?statute=25-2733>, its own official annotations | 2026-08-20 | Read directly |
| Professional negligence has a two-year period | Testland Rev. Stat. section 25-222, <https://legislature.testland.gov/statutes.php?statute=25-222> | 2026-08-20 | Read directly |
| The ten-year repose period is constitutional | Same section 25-222 page, official annotations | 2026-08-20 | Read directly |
"""

PATH_SUBSTRING_BACKREF_FIXTURE = """# Verification: Substringland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| Rule 1.0(a) defines a firm | Testland Rules of Professional Conduct, Rule 1.0(a), <https://courts.testland.gov/siteassets/rules-of-professional-conduct/testland-rules-of-professional-conduct.pdf> | 2026-08-20 | Read directly |
| Rule 1.19 bars an arbitration clause covering a future dispute | Same rules PDF, Rule 1.19 full text | 2026-08-20 | Read directly |
| The court adopted Rule 1.19 effective 2022 | Testland Supreme Court order, ADM File No. 2021-07, <https://courts.testland.gov/adopted-orders/2021-07_formor_addmrpc1.19.pdf> | 2026-08-20 | Read directly |
| Rule 1.19's comment lists the informed-consent items | Same rules PDF, Rule 1.19 comment | 2026-08-20 | Read directly |
"""


def test_a_section_number_resolves_when_the_row_has_no_other_descriptor(tmp_path: Path) -> None:
    """"Same section 25-222 page" is the 25-222 row, not whichever section was cited last."""
    path = write(tmp_path, "verification_nl.md", SECTION_NUMBER_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[-1].url.endswith("statute=25-222")
    assert rows[-1].inherited_from == rows[1].row_number


def test_a_rule_number_is_not_matched_inside_a_url_path_word(tmp_path: Path) -> None:
    """A row citing Rule 1.19 means the rules book, not an order whose filename ends addmrpc1.19."""
    path = write(tmp_path, "verification_sl.md", PATH_SUBSTRING_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[-1].url == rows[0].url
    assert rows[-1].inherited_from == rows[1].row_number


LOCATOR_BACKREF_FIXTURE = """# Verification: Locatorland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| The bar publishes an ethics opinion on fees | <https://bar.testland.org/ethics/opinion-376>, Comment on fee splitting | 2026-08-20 | Read directly |
| Scope Comment [4] disclaims enlarging existing law | <https://bar.testland.org/rules-of-professional-conduct/scope> | 2026-08-20 | Read directly |
| Scope Comment [3]: a violation "is a basis for invoking the disciplinary process" | Same page, Comment [3] | 2026-08-20 | Read directly |
"""


def test_a_locator_word_does_not_name_a_source(tmp_path: Path) -> None:
    """"Same page, Comment [3]" is the page above; comment locates a passage, it names nothing."""
    path = write(tmp_path, "verification_ll.md", LOCATOR_BACKREF_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[-1].url == rows[-2].url
    assert rows[-1].inherited_from == rows[-2].row_number


# Tests for URL punctuation stripping: the extractor must handle backticks and trailing punctuation.
URL_PUNCTUATION_FIXTURE = """# Verification: Punctuationland

## Confirmed against a primary or official source

| Claim | Source | Retrieved | Note |
| ----- | ------ | --------- | ---- |
| The first claim in backticks | `https://courts.punctuationland.gov/rules.pdf` | 2026-08-20 | Backtick-wrapped URL |
| The second claim with backtick and comma | `https://courts.punctuationland.gov/statutes.zip`, a directory | 2026-08-20 | Backtick-wrapped with trailing comma |
| The third claim with period | https://courts.punctuationland.gov/notice.pdf. | 2026-08-20 | Plain URL with trailing period |
| The fourth claim plain | https://courts.punctuationland.gov/index.html | 2026-08-20 | Plain URL no punctuation |
"""


def test_url_wrapped_in_backticks_extracts_bare_url(tmp_path: Path) -> None:
    """A URL wrapped in backticks should extract without the backticks."""
    path = write(tmp_path, "verification_pl.md", URL_PUNCTUATION_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[0].url == "https://courts.punctuationland.gov/rules.pdf"


def test_url_with_backtick_and_trailing_comma_extracts_bare_url(tmp_path: Path) -> None:
    """A URL in backticks followed by a comma should extract without both."""
    path = write(tmp_path, "verification_pl.md", URL_PUNCTUATION_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[1].url == "https://courts.punctuationland.gov/statutes.zip"


def test_url_with_trailing_period_extracts_bare_url(tmp_path: Path) -> None:
    """A URL with a trailing period should extract without it."""
    path = write(tmp_path, "verification_pl.md", URL_PUNCTUATION_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[2].url == "https://courts.punctuationland.gov/notice.pdf"


def test_plain_url_extracts_unchanged(tmp_path: Path) -> None:
    """A plain URL with no trailing punctuation should extract unchanged."""
    path = write(tmp_path, "verification_pl.md", URL_PUNCTUATION_FIXTURE)
    rows, problems = parse_reference_file(path)
    assert problems == []
    assert rows[3].url == "https://courts.punctuationland.gov/index.html"


def test_strip_url_trailing_punctuation_removes_all_trailing_chars(tmp_path: Path) -> None:
    """strip_url_trailing_punctuation removes all trailing punctuation and delimiters."""
    assert strip_url_trailing_punctuation("https://example.com`") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com,") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com;") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com.") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com)") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com]") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com}") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com'") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com`,.;)]}'") == "https://example.com"
    assert strip_url_trailing_punctuation("https://example.com/path") == "https://example.com/path"


# ---------------------------------------------------------------------------
# curl fallback (A2): a TLS reset on Python's OpenSSL stack retries once
# through curl.exe rather than being reported UNREACHABLE.
# ---------------------------------------------------------------------------


def _make_curl_stdout(url: str, status: int, body: bytes, content_type: str = "text/html") -> bytes:
    meta = f"\n__CURL_STATUS__:{status}\n__CURL_URL__:{url}\n__CURL_TYPE__:{content_type}\n"
    return body + meta.encode("utf-8")


def test_default_fetch_falls_back_to_curl_on_tls_reset(monkeypatch: pytest.MonkeyPatch) -> None:
    """A urllib URLError (TLS reset) retries once through curl and the result records the transport."""
    url = "https://www.jud.ct.gov/"

    def raising_open(self, request, timeout=None):
        raise urllib.error.URLError("[SSL: TLSV1_ALERT_INTERNAL_ERROR] record layer failure")

    monkeypatch.setattr(urllib.request.OpenerDirector, "open", raising_open)
    monkeypatch.setattr(check_sources, "_locate_curl", lambda: "curl")

    stdout = _make_curl_stdout(url, 200, b"<html><body>hello from curl</body></html>")
    fake_proc = subprocess.CompletedProcess(args=["curl"], returncode=0, stdout=stdout, stderr=b"")
    monkeypatch.setattr(check_sources, "_invoke_curl", lambda curl_path, u, timeout: fake_proc)

    result = default_fetch(url)

    assert result.error is None
    assert result.status == 200
    assert result.transport == "curl"
    assert "hello from curl" in result.body

    outcome = classify(make_row(url=url), result)
    assert outcome.bucket != "UNREACHABLE"
    assert outcome.transport == "curl"


def test_default_fetch_does_not_retry_http_error_through_curl(monkeypatch: pytest.MonkeyPatch) -> None:
    """An HTTPError is a real answer from the server; it must never trigger the curl fallback."""
    import email.message
    import io

    url = "https://example.gov/missing"

    def raising_open(self, request, timeout=None):
        raise urllib.error.HTTPError(url, 404, "Not Found", email.message.Message(), io.BytesIO(b"nope"))

    monkeypatch.setattr(urllib.request.OpenerDirector, "open", raising_open)

    def must_not_be_called(*args, **kwargs):
        raise AssertionError("curl must not be invoked for an HTTPError")

    monkeypatch.setattr(check_sources, "_locate_curl", must_not_be_called)
    monkeypatch.setattr(check_sources, "_invoke_curl", must_not_be_called)

    result = default_fetch(url)

    assert result.status == 404
    assert result.transport == "urllib"


def test_default_fetch_refuses_scheme_without_invoking_curl(monkeypatch: pytest.MonkeyPatch) -> None:
    """A refused/disallowed scheme never invokes curl, it is rejected before any fetch attempt."""

    def must_not_be_called(*args, **kwargs):
        raise AssertionError("curl must not be invoked for a refused scheme")

    monkeypatch.setattr(check_sources, "_locate_curl", must_not_be_called)

    result = default_fetch("ftp://example.invalid/x")

    assert result.status is None
    assert "refused" in result.error
    assert result.transport == "urllib"


def test_default_fetch_degrades_gracefully_when_curl_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """When curl.exe is not on PATH, the urllib result is kept and the error string says why."""

    def raising_open(self, request, timeout=None):
        raise urllib.error.URLError("[SSL] record layer failure")

    monkeypatch.setattr(urllib.request.OpenerDirector, "open", raising_open)
    monkeypatch.setattr(check_sources, "_locate_curl", lambda: None)

    result = default_fetch("https://www.jud.ct.gov/")

    assert result.status is None
    assert result.transport == "urllib"
    assert "record layer failure" in result.error
    assert "curl" in result.error.lower()

    outcome = classify(make_row(url="https://www.jud.ct.gov/"), result)
    assert outcome.bucket == "UNREACHABLE"
