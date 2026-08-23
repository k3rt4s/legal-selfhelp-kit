"""Structural checks over every state pack and its verification file, enforced as a repository gate."""
from __future__ import annotations

import io
import re
from pathlib import Path
from typing import Optional

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = REPO_ROOT / "references"
TEMPLATE_PATH = REFERENCES / "state_template.md"
VERIFICATION_INDEX_PATH = REFERENCES / "VERIFICATION.md"
README_PATH = REPO_ROOT / "README.md"

URL_RE = re.compile(r"https?://[^\s<>\[\]\"'`)]+")
HEADING_RE = re.compile(r"^## (.+)$", re.MULTILINE)
NUMBERED_HEADING_RE = re.compile(r"^## (\d+)\.\s")


def _read(path: Path) -> str:
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def _state_codes() -> list[str]:
    codes = []
    for path in REFERENCES.glob("state_*.md"):
        if path.name == "state_template.md":
            continue
        codes.append(path.stem[len("state_"):])
    return sorted(codes)


STATE_CODES = _state_codes()


def _template_required_section_numbers() -> list[str]:
    """Return the numbered section headings ("### N. Title") the template defines, in order."""
    text = _read(TEMPLATE_PATH)
    return re.findall(r"^### (\d+)\. .+$", text, re.MULTILINE)


TEMPLATE_SECTION_NUMBERS = _template_required_section_numbers()


def _has_ellipsis(candidate: str) -> bool:
    return "..." in candidate or "…" in candidate


def _is_complete_url(candidate: str) -> bool:
    """A URL counts as complete when it has a scheme, a host, and a path beyond a bare "/"."""
    if _has_ellipsis(candidate):
        return False
    match = re.match(r"https?://([^/\s]+)(/[^\s<>\[\]\"'`)]*)?", candidate)
    if not match:
        return False
    path = match.group(2)
    return bool(path and path != "/")


def _heading_line_indexes(lines: list[str]) -> list[int]:
    return [i for i, line in enumerate(lines) if line.startswith("## ")]


def _section_block(text: str, number: int) -> Optional[str]:
    """Return the text of numbered section "## N. ..." through (not including) the next "## " heading."""
    lines = text.splitlines()
    heading_idxs = _heading_line_indexes(lines)
    start = next((i for i in heading_idxs if NUMBERED_HEADING_RE.match(lines[i]) and lines[i].split(".", 1)[0] == f"## {number}"), None)
    if start is None:
        return None
    later = [i for i in heading_idxs if i > start]
    end = later[0] if later else len(lines)
    return "\n".join(lines[start:end])


def _keyword_section_block(text: str, keyword: str) -> Optional[str]:
    """Return the text under the first "## " heading containing keyword, through the next "## " heading."""
    lines = text.splitlines()
    heading_idxs = _heading_line_indexes(lines)
    start = next((i for i in heading_idxs if keyword in lines[i].lower()), None)
    if start is None:
        return None
    later = [i for i in heading_idxs if i > start]
    end = later[0] if later else len(lines)
    return "\n".join(lines[start + 1:end])


def _table_rows(block: str) -> Optional[list[dict[str, str]]]:
    """Parse the first pipe table in block into a list of {header: cell} dicts, by header name, not position."""
    lines = block.splitlines()
    header_idx = next((i for i, l in enumerate(lines) if l.strip().startswith("|") and "claim" in l.lower()), None)
    if header_idx is None:
        return None
    headers = [c.strip() for c in lines[header_idx].strip().strip("|").split("|")]
    rows = []
    for line in lines[header_idx + 2:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if stripped == "":
                continue
            break
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


EMPTY_ROW_MARKERS = {"none", "(none)"}


# A Source cell may cite a site's front page only when the claim is about the organization
# itself, its name, address, phone, or the fact that it exists, rather than about something
# printed on a deeper page. Each exemption is the exact Source cell text plus the reason it
# is allowed, so the list cannot grow by accident, and a stale entry fails its own test
# below rather than sitting there granting cover to a row that has since changed.
HOMEPAGE_SOURCE_EXEMPTIONS = {
    ("ma", "<https://www.masscsb.org/> (homepage)"):
        "The Board states its no-limitations, no-caps policy and its cumulative payout "
        "figures on its front page and nowhere deeper; both rows record that, and that "
        "the figures are live numbers which will change without notice.",
    ("mi", "Attorney Grievance Commission homepage, agcmi.org, <https://www.agcmi.org/>"):
        "Claim is that the AGC exists and is reached at this address.",
    ("mo", "OCDC homepage, <https://mochiefcounsel.org/>"):
        "Claim is that the OCDC exists and is reached at this address.",
    ("wa", "Resolution Washington homepage, <https://www.resolutionwa.org/>"):
        "Claim is that Resolution Washington exists and is reached at this address.",
    ("wv", "<https://wvodc.org/> (home page)"):
        "wvodc.org is a single page; there is no deeper page to cite.",
}


# A pack section may point the reader at a site's front page only when that front page is
# genuinely where the thing lives. Same shape and same reasoning as the exemptions above.
HOMEPAGE_PACK_EXEMPTIONS = {
    ("nh", 4):
        "The sentence names the Attorney Discipline Office and its site, and promises the "
        "reader nothing more specific than that.",
    ("wv", 4):
        "wvodc.org is a single page. The pack tells the reader which buttons on it open the "
        "complaint packet and the complaint form, which is as specific as that site allows.",
}




# ---------------------------------------------------------------------------
# 1. Every pack has a matching verification file, and vice versa.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("code", STATE_CODES)
def test_every_pack_has_a_verification_file(code: str) -> None:
    verification = REFERENCES / f"verification_{code}.md"
    assert verification.exists(), f"references/state_{code}.md has no matching references/verification_{code}.md"


@pytest.mark.parametrize(
    "path",
    [p for p in REFERENCES.glob("verification_*.md") if p.name != "verification_national.md"],
    ids=lambda p: p.name,
)
def test_every_verification_file_has_a_pack(path: Path) -> None:
    code = path.stem[len("verification_"):]
    pack = REFERENCES / f"state_{code}.md"
    assert pack.exists(), f"{path.name} has no matching references/state_{code}.md"


# ---------------------------------------------------------------------------
# 2. Every pack carries all eight numbered sections, in order.
#
# The template's own section titles vary in wording pack to pack by design
# (section 6 in particular names the state's actual court, per
# state_template.md's own instruction), so the check here is structural:
# section numbers 1 through 8 must each appear exactly once, in ascending
# order. This is what the template's "in this order, with these headings"
# rule reduces to once heading prose is allowed to be state-specific.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("code", STATE_CODES)
def test_pack_has_eight_numbered_sections_in_order(code: str) -> None:
    text = _read(REFERENCES / f"state_{code}.md")
    found = re.findall(r"^## (\d+)\.\s", text, re.MULTILINE)
    expected = TEMPLATE_SECTION_NUMBERS
    assert found == expected, (
        f"state_{code}.md has numbered sections {found}, expected {expected} in order "
        f"(from state_template.md)"
    )


# ---------------------------------------------------------------------------
# 3. Sections 1, 3, 4, and 5 each carry at least one complete URL.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("code", STATE_CODES)
@pytest.mark.parametrize("section_number", [1, 3, 4, 5])
def test_pack_section_has_a_complete_url(code: str, section_number: int) -> None:
    text = _read(REFERENCES / f"state_{code}.md")
    block = _section_block(text, section_number)
    assert block is not None, f"state_{code}.md is missing section {section_number}"
    candidates = URL_RE.findall(block)
    complete = [u for u in candidates if _is_complete_url(u)]
    if not complete and (code, section_number) in HOMEPAGE_PACK_EXEMPTIONS:
        assert candidates, (
            f"state_{code}.md section {section_number} is exempt from needing a deep URL but "
            f"has no URL at all"
        )
        return
    assert complete, (
        f"state_{code}.md section {section_number} has no complete http(s) URL "
        f"(found candidates: {candidates!r})"
    )


# ---------------------------------------------------------------------------
# 4. Every verification file has the three-part structure: a Confirmed
#    table, a Flagged table, and a Gap list. Each part may be empty, but an
#    empty part must be stated, not simply absent.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("code", STATE_CODES)
@pytest.mark.parametrize("keyword", ["confirmed", "flagged", "gap"])
def test_verification_file_has_required_part(code: str, keyword: str) -> None:
    text = _read(REFERENCES / f"verification_{code}.md")
    headings = HEADING_RE.findall(text)
    assert any(keyword in h.lower() for h in headings), (
        f"verification_{code}.md has no heading naming its {keyword!r} part "
        f"(headings found: {headings!r})"
    )


# ---------------------------------------------------------------------------
# 5. Every row in a Confirmed or Flagged table has a non-empty Claim cell
#    and a non-empty Source cell. A row that plainly states the table is
#    empty (Claim "None" / "(none)", per the corpus's own convention, see
#    references/verification_or.md and references/verification_sc.md) is
#    not a row to check, it is the required statement that the part is
#    empty.
#
#    Not every Source cell is expected to carry its own URL: this project's
#    own scripts/check_sources.py already treats a citation row without a
#    URL as something to skip rather than a defect (many rows cite a prior
#    row's source, a filed document by name, or an absence finding with
#    nothing to link). What is checked here is narrower and unambiguous:
#    any URL that IS present in a Source cell must be complete, not a bare
#    domain and not truncated with an ellipsis.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("code", STATE_CODES)
@pytest.mark.parametrize("keyword", ["confirmed", "flagged"])
def test_verification_rows_have_claim_and_source(code: str, keyword: str) -> None:
    path = REFERENCES / f"verification_{code}.md"
    text = _read(path)
    block = _keyword_section_block(text, keyword)
    if block is None:
        pytest.skip(f"{path.name} has no {keyword!r} heading; covered by test_verification_file_has_required_part")
    rows = _table_rows(block)
    if not rows:
        pytest.skip(f"{path.name} {keyword!r} part has no table to check row by row")

    bad_rows = []
    for row in rows:
        claim_key = next((k for k in row if k.strip().lower() == "claim"), None)
        source_key = next((k for k in row if k.strip().lower() == "source"), None)
        if claim_key is None or source_key is None:
            continue
        claim = row[claim_key]
        source = row[source_key]
        if claim.strip().lower() in EMPTY_ROW_MARKERS and not source.strip():
            continue  # the table's own "stated as empty" placeholder row
        if not claim.strip():
            bad_rows.append(f"empty Claim cell (Source: {source[:60]!r})")
        if not source.strip():
            bad_rows.append(f"empty Source cell (Claim: {claim[:60]!r})")

    assert not bad_rows, f"{path.name} {keyword!r} table has rows with missing cells: {bad_rows}"


@pytest.mark.parametrize("code", STATE_CODES)
@pytest.mark.parametrize("keyword", ["confirmed", "flagged"])
def test_verification_source_urls_are_complete(code: str, keyword: str) -> None:
    path = REFERENCES / f"verification_{code}.md"
    text = _read(path)
    block = _keyword_section_block(text, keyword)
    if block is None:
        pytest.skip(f"{path.name} has no {keyword!r} heading; covered by test_verification_file_has_required_part")
    rows = _table_rows(block)
    if not rows:
        pytest.skip(f"{path.name} {keyword!r} part has no table to check row by row")

    bad_sources = []
    for row in rows:
        source_key = next((k for k in row if k.strip().lower() == "source"), None)
        if source_key is None:
            continue
        source = row[source_key]
        candidates = URL_RE.findall(source)
        if not candidates:
            continue  # no URL attempted in this cell; not this test's concern, see docstring above
        if any(_is_complete_url(u) for u in candidates):
            continue
        if (code, source.strip()) in HOMEPAGE_SOURCE_EXEMPTIONS:
            continue  # front page is the right cite here; see HOMEPAGE_SOURCE_EXEMPTIONS
        bad_sources.append(source[:120])

    assert not bad_sources, (
        f"{path.name} {keyword!r} table has Source cells with a bare-domain or truncated URL: {bad_sources}"
    )


# ---------------------------------------------------------------------------
# 6. The count of packs matches the count stated in the docs.
#
# Neither docs/INDEX.md nor README.md states a bare number of packs;
# README.md says "the fifty states or the District of Columbia" in prose,
# and references/VERIFICATION.md states the count directly as "States
# covered: N of N, plus the District of Columbia." Both are checked against
# the actual file count, and against each other.
# ---------------------------------------------------------------------------


def test_pack_count_matches_documented_count() -> None:
    actual = len(STATE_CODES)

    verification_text = _read(VERIFICATION_INDEX_PATH)
    match = re.search(r"States covered:\s*(\d+)\s*of\s*(\d+),\s*plus the District of Columbia", verification_text)
    assert match, "references/VERIFICATION.md no longer states \"States covered: N of N, plus the District of Columbia\""
    states_covered, states_total = int(match.group(1)), int(match.group(2))
    assert states_covered == states_total, (
        f"references/VERIFICATION.md says {states_covered} of {states_total} states are covered, "
        f"not all of them"
    )
    verification_count = states_total + 1  # the states, plus the District of Columbia

    readme_text = _read(README_PATH)
    assert re.search(r"\bfifty states\b", readme_text, re.IGNORECASE), (
        "README.md no longer says \"fifty states\"; find where the pack count now lives and update this test"
    )
    readme_count = 50 + 1  # "fifty states or the District of Columbia"

    assert readme_count == verification_count, (
        f"README.md implies {readme_count} packs, references/VERIFICATION.md implies {verification_count}; "
        f"the two disagree"
    )
    assert actual == verification_count, (
        f"{actual} references/state_XX.md packs exist on disk, but the docs say {verification_count}"
    )


# ---------------------------------------------------------------------------
# 7. No em dash or curly quote in the reference layer. The section sign is
#    explicitly allowed.
# ---------------------------------------------------------------------------


EM_DASH = "—"
CURLY_QUOTES = "‘’“”"
SECTION_SIGN = "§"


@pytest.mark.parametrize(
    "path",
    sorted(REFERENCES.glob("*.md")),
    ids=lambda p: p.name,
)
def test_no_em_dash_or_curly_quote(path: Path) -> None:
    # The section sign (SECTION_SIGN) is not scanned for here; it is allowed and must never fail this test.
    text = _read(path)
    assert EM_DASH not in text, f"{path.name} contains an em dash (\\u2014)"
    found_curly = [c for c in CURLY_QUOTES if c in text]
    assert not found_curly, f"{path.name} contains a curly quote: {found_curly!r}"


def test_homepage_source_exemptions_are_all_still_in_use() -> None:
    """Every homepage exemption still matches a real Source cell, so the list cannot go stale."""
    unused = []
    for (code, source_text), reason in HOMEPAGE_SOURCE_EXEMPTIONS.items():
        text = _read(REFERENCES / f"verification_{code}.md")
        found = False
        for keyword in ("confirmed", "flagged"):
            block = _keyword_section_block(text, keyword)
            if block is None:
                continue
            for row in _table_rows(block) or []:
                source_key = next((k for k in row if k.strip().lower() == "source"), None)
                if source_key and row[source_key].strip() == source_text:
                    found = True
        if not found:
            unused.append(f"{code}: {source_text!r} ({reason})")
    assert not unused, (
        "HOMEPAGE_SOURCE_EXEMPTIONS entries no longer match any Source cell; "
        f"remove them or fix the text: {unused}"
    )


@pytest.mark.parametrize("code,section_number", sorted(HOMEPAGE_PACK_EXEMPTIONS))
def test_homepage_pack_exemptions_are_all_still_in_use(code: str, section_number: int) -> None:
    """Every pack exemption still covers a section that would otherwise fail, so none goes stale."""
    block = _section_block(_read(REFERENCES / f"state_{code}.md"), section_number)
    assert block is not None, f"state_{code}.md has no section {section_number} to exempt"
    complete = [u for u in URL_RE.findall(block) if _is_complete_url(u)]
    assert not complete, (
        f"state_{code}.md section {section_number} now has a complete URL "
        f"({complete!r}); remove its HOMEPAGE_PACK_EXEMPTIONS entry"
    )


# ---------------------------------------------------------------------------
# 9. No blank line splits a table. A pipe row after a blank line has no
#    header: GitHub renders it as a paragraph and scripts/check_sources.py
#    cannot tell which cell is the claim. Found in five files on 2026-08-22,
#    36 rows in all; _table_rows() above reads past a blank line, so every
#    other test here saw those rows as ordinary table rows.
# ---------------------------------------------------------------------------


VERIFICATION_FILES = sorted(p.name for p in REFERENCES.glob("*.md") if p.name.lower().startswith("verification"))


def _is_separator_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped) <= set("|:- ")


@pytest.mark.parametrize("name", VERIFICATION_FILES)
def test_no_blank_line_splits_a_table(name: str) -> None:
    lines = _read(REFERENCES / name).splitlines()
    orphans = []
    in_table = False
    for number, line in enumerate(lines, start=1):
        if not line.strip().startswith("|"):
            in_table = False
            continue
        if in_table:
            continue
        next_line = lines[number] if number < len(lines) else ""
        if _is_separator_row(next_line):
            in_table = True
        else:
            orphans.append(number)
    assert not orphans, (
        f"{name} has table rows with no header row above them at lines {orphans}; "
        "a blank line inside the table cuts them off, delete it so the rows rejoin the table"
    )
