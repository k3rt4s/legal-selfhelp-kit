"""Check every source URL cited in the reference layer and report which no longer support their claim."""
from __future__ import annotations

import argparse
import html
import io
import re
import socket
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

# ---------------------------------------------------------------------------
# Claim-text matching
#
# A row's Claim cell is reduced to its "significant words": alphanumeric
# tokens of four or more characters, lowercased, with a short stopword list
# removed. The fetched page body is stripped of HTML tags, HTML entities are
# unescaped, curly quotes and other typographic punctuation are folded to
# their plain-ASCII equivalents, and all whitespace (including the newlines
# HTML tag-stripping introduces) is collapsed to single spaces. A claim
# "matches" the page when at least MATCH_THRESHOLD of its significant words
# appear somewhere in that normalized text. This survives reformatted
# whitespace, markup, and quote style, while still failing outright when a
# page genuinely does not discuss the claim (an error page, a nav-only
# shell, or a page about something else shares almost none of the claim's
# distinctive words).
# ---------------------------------------------------------------------------

MATCH_THRESHOLD = 0.5
MIN_SIGNIFICANT_WORDS = 3
CLIENT_RENDERED_VISIBLE_TEXT_MAX = 600
CLIENT_RENDERED_RAW_BODY_MIN = 8000

STOPWORDS = {
    "this", "that", "with", "from", "have", "must", "shall", "into", "under",
    "over", "than", "then", "when", "where", "which", "while", "before",
    "after", "about", "there", "their", "these", "those", "being", "been",
    "does", "each", "same", "such", "only", "also", "more", "most", "some",
    "will", "would", "could", "should", "state", "rule", "rules",
}

WORD_RE = re.compile(r"[a-z0-9]{4,}")
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

CURLY_MAP = {
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u00a0": " ",
}

BUCKETS = [
    "OK",
    "NO_CLAIM_TEXT",
    "LIKELY_CLIENT_RENDERED",
    "BLOCKED",
    "REDIRECTED",
    "HTTP_ERROR",
    "UNREACHABLE",
    "PDF_UNCHECKED",
    "UNPARSEABLE_ROW",
]

# The report is generated data, so it never lands in the repository. The temp directory is
# the one place that exists on every machine a contributor might run this from. Pass --out
# to send it somewhere you keep.
DEFAULT_OUT_DIR = Path(tempfile.gettempdir()) / "legal-selfhelp-kit" / "source_health"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
DEFAULT_DELAY = 1.5
DEFAULT_TIMEOUT = 20

# Nothing cited in this kit is a large download, and the checker only needs enough of a page
# to look for a claim in it. The cap keeps a runaway or hostile response from filling memory.
MAX_RESPONSE_BYTES = 5_000_000

# The URLs come out of Markdown tables anyone can send a pull request against, so the fetcher
# only ever speaks http and https. A file:// or ftp:// row is reported, not opened.
ALLOWED_SCHEMES = ("http", "https")


def fold_typography(text: str) -> str:
    for src, dst in CURLY_MAP.items():
        text = text.replace(src, dst)
    return text


def strip_html(body: str) -> str:
    text = html.unescape(body)
    text = fold_typography(text)
    text = TAG_RE.sub(" ", text)
    text = WS_RE.sub(" ", text)
    return text.strip()


def significant_words(text: str) -> list[str]:
    text = fold_typography(text).lower()
    words = WORD_RE.findall(text)
    return [w for w in words if w not in STOPWORDS]


def claim_match_fraction(claim: str, page_text: str) -> Optional[float]:
    """Return the fraction of the claim's significant words found in page_text, or None if the claim has too few to judge."""
    words = significant_words(claim)
    if len(words) < MIN_SIGNIFICANT_WORDS:
        return None
    hay_words = set(significant_words(page_text))
    found = sum(1 for w in words if w in hay_words)
    return found / len(words)


# ---------------------------------------------------------------------------
# Parsing references/*.md
# ---------------------------------------------------------------------------


@dataclass
class SourceRow:
    file: str
    state: str
    section: str
    claim: str
    source_cell: str
    url: str
    retrieved: str
    row_number: int
    inherited_from: Optional[int] = None


@dataclass
class UnparseableRow:
    file: str
    section: str
    row_number: int
    reason: str
    raw: str


GAP_SECTION_RE = re.compile(r"gap list", re.IGNORECASE)
SUPERSEDED_RE = re.compile(r"^\s*superseded\b", re.IGNORECASE)
SEPARATOR_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
BACKREF_RE = re.compile(r"\bsame\b|\babove\b", re.IGNORECASE)

BACKREF_HOST_RE = re.compile(
    r"\b([a-z0-9][a-z0-9-]{2,}(?:\.[a-z0-9-]+)*\.(?:org|gov|com|net|edu|us))\b", re.IGNORECASE
)
ADJACENT_RE = re.compile(r"\babove\b", re.IGNORECASE)
# Words that locate a passage inside a source rather than name the source. A descriptor built
# only from these tells you nothing about which earlier row is meant, and matching on one sends
# the row to whichever earlier row happens to use the same word: "Same page, Comment [3]" is the
# page above, not the last row that mentioned a comment.
BACKREF_STOPWORDS = frozenset(
    "same as source sources above rule rules section sections page pages the a an and or of for at in "
    "id ibid see also cited prior previous document doc url text full pdf "
    "official annotation annotations comment comments paragraph paragraphs".split()
)


CITATION_RE = re.compile(r"\b\d+[a-z]?(?:[.\-]\d+[a-z]?)+\b", re.IGNORECASE)


def backref_citations(cell: str) -> list[str]:
    """Return the section or rule numbers a backreference names, such as 25-222 or 9.112."""
    stripped = re.sub(r"<[^>]*>", " ", cell.lower())
    seen = []
    for found in CITATION_RE.findall(stripped):
        if found not in seen:
            seen.append(found)
    return seen


def cites(haystack: str, citation: str) -> bool:
    """True when the number appears in the text as its own citation, not inside a longer one."""
    return re.search(r"(?<![\d.\-])" + re.escape(citation) + r"(?![\d.\-])", haystack) is not None


def prose(cell: str) -> str:
    """Return a cell's words with its URLs removed, lowercased."""
    return re.sub(r"<[^>]*>", " ", URL_RE.sub(" ", cell)).lower()


def descriptor_words(cell: str) -> set[str]:
    """Return every whole word a cell offers a descriptor to match, prose and URL path alike.

    A URL contributes the words of its path, split the way a person reading it would: "ACAB-Fee-
    Arbitration-Rules" offers acab, and "addmrpc1.19.pdf" does not offer mrpc. That distinction
    is the whole point of matching whole words rather than substrings. Michigan cites both its
    rules book and the order adopting one rule, and both have mrpc somewhere in the path.
    """
    return set(re.findall(r"[a-z]{2,}", cell.lower()))


def backref_tokens(cell: str) -> set[str]:
    """Return the distinctive words a backreference uses to name the source it means."""
    stripped = re.sub(r"<[^>]*>", " ", cell.lower())
    return {w for w in re.findall(r"[a-z]{4,}", stripped) if w not in BACKREF_STOPWORDS}


def resolve_backref(source_cell, url_cell, history):
    """Resolve a backreference row to the earlier source it names, not merely the nearest one.

    A row reading "Same Chapter 9 source, Rule 9.112" means the Chapter 9 row above it, which is
    not always the row directly above: a one-off source interleaved between them used to be
    inherited instead, and the claim was then checked against a page the row never cited.

    Four ways of naming a source, in order of how much they pin it down. A host wins outright and
    can point at any earlier row carrying a URL on it. The literal word "above" means the nearest
    preceding source and nothing cleverer. Otherwise the row is read as naming a document and then
    locating a passage inside it, so a descriptor such as "Chapter 9" or "Owens v. Purcel" is
    matched first, and only a row with no usable descriptor falls through to a section number such
    as 25-222. That order matters: "Same Owens v. Purcel opinion, quoting R.C. 2305.117(B)" is a
    cite to the opinion, not to the statute, while "Same section 25-222 page, official annotations"
    has nothing but the number to go on and must not settle for whichever section was cited last.

    A descriptor matches a prior row on whole words, in its prose and in its URL path, never on a
    substring. Many rows cite nothing but a link, so the path has to count; matching inside a word
    does not, because Michigan's rules PDF and the order adopting a single rule both carry "mrpc"
    somewhere in the path and only one of them carries it as a word.

    `history` holds this file's earlier rows, oldest first, as (row_number, source_cell, urls),
    where `urls` is every URL that row carries, primary first. Returns (url, row_number, reason).
    A non-empty reason means the row names a source no earlier row in this file carries, and the
    caller must not guess a URL for it.
    """
    if not history:
        return None, None, "backreference to a prior source, but no URL has appeared yet in this file"

    text = source_cell + " " + url_cell
    hosts = {h.lower() for h in BACKREF_HOST_RE.findall(text)}
    if hosts:
        for row_number, _prior_cell, prior_urls in reversed(history):
            for candidate in prior_urls:
                if any(h in candidate.lower() for h in hosts):
                    return candidate, row_number, ""
        named = ", ".join(sorted(hosts))
        return None, None, "backreference names " + named + ", but no earlier row in this file cites it"

    if not ADJACENT_RE.search(text):
        tokens = backref_tokens(text)
        if tokens:
            for row_number, prior_cell, prior_urls in reversed(history):
                words = descriptor_words(prose(prior_cell))
                for candidate in prior_urls:
                    words |= descriptor_words(candidate)
                if tokens & words:
                    return prior_urls[0], row_number, ""

        for citation in backref_citations(text):
            for row_number, prior_cell, prior_urls in reversed(history):
                haystack = prose(prior_cell) + " " + " ".join(prior_urls).lower()
                if cites(haystack, citation):
                    return prior_urls[0], row_number, ""

    row_number, _prior_cell, prior_urls = history[-1]
    return prior_urls[0], row_number, ""

# Column map for a well-formed table that is not a citation table (no Claim and Source header); its rows are skipped silently.
IGNORED_TABLE: dict[str, int] = {}


def state_for_file(path: Path) -> str:
    name = path.stem
    if name == "VERIFICATION":
        return "INDEX"
    if name == "verification_national":
        return "NATIONAL"
    if name.startswith("verification_"):
        return name[len("verification_"):].upper()
    return name.upper()


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def classify_header(cells: list[str]) -> Optional[dict[str, int]]:
    """Return a column-name to index map if this header row looks like a citation table, else None."""
    lowered = [c.lower() for c in cells]
    if not any("claim" in c for c in lowered):
        return None
    if not any("source" in c or "url" in c for c in lowered):
        return None
    mapping: dict[str, int] = {}
    for i, c in enumerate(lowered):
        if "claim" in c and "claim" not in mapping:
            mapping["claim"] = i
        elif "url" in c and "url" not in mapping:
            mapping["url"] = i
        elif "source" in c and "source" not in mapping:
            mapping["source"] = i
        elif "retriev" in c and "retrieved" not in mapping:
            mapping["retrieved"] = i
    return mapping if "claim" in mapping else None


def extract_url(*cells: str) -> str:
    for cell in cells:
        if not cell:
            continue
        m = URL_RE.search(cell)
        if m:
            return m.group(0).rstrip(">").rstrip(".").rstrip(")")
    return ""


def extract_date(*cells: str) -> str:
    for cell in cells:
        if not cell:
            continue
        m = DATE_RE.search(cell)
        if m:
            return m.group(0)
    return ""


def parse_reference_file(path: Path) -> tuple[list[SourceRow], list[UnparseableRow]]:
    rows: list[SourceRow] = []
    problems: list[UnparseableRow] = []
    state = state_for_file(path)

    with io.open(path, encoding="utf-8", newline="") as fh:
        lines = fh.readlines()

    section = ""
    in_skip_section = False
    col_map: Optional[dict[str, int]] = None
    expect_separator = False
    url_history: list[tuple[int, str, list[str]]] = []

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if stripped.startswith("## "):
            section = stripped[3:].strip()
            in_skip_section = bool(GAP_SECTION_RE.search(section))
            col_map = None
            expect_separator = False
            continue

        if in_skip_section:
            continue

        if not stripped.startswith("|"):
            col_map = None
            expect_separator = False
            continue

        cells = split_row(line)

        if col_map is None:
            # A table starts with a header row followed by a separator row. A
            # pipe row with no separator after it is a row that lost its table,
            # almost always because a blank line was inserted above it; report
            # it rather than guessing its columns or dropping it silently.
            next_line = lines[lineno].rstrip("\r\n") if lineno < len(lines) else ""
            if not SEPARATOR_RE.match(next_line):
                problems.append(UnparseableRow(
                    file=path.name, section=section, row_number=lineno,
                    reason="table row with no header row above it (a blank line splits the table)",
                    raw=line[:300],
                ))
                continue
            header_map = classify_header(cells)
            col_map = header_map if header_map is not None else IGNORED_TABLE
            expect_separator = True
            continue

        if expect_separator:
            expect_separator = False
            if SEPARATOR_RE.match(line):
                continue
            # Not actually a separator row; fall through and treat as data.

        if col_map is IGNORED_TABLE:
            continue

        claim_idx = col_map.get("claim")
        claim = cells[claim_idx] if claim_idx is not None and claim_idx < len(cells) else ""

        if SUPERSEDED_RE.search(claim):
            continue

        source_idx = col_map.get("source")
        url_idx = col_map.get("url")
        retrieved_idx = col_map.get("retrieved")

        source_cell = cells[source_idx] if source_idx is not None and source_idx < len(cells) else ""
        url_cell = cells[url_idx] if url_idx is not None and url_idx < len(cells) else ""
        retrieved_cell = cells[retrieved_idx] if retrieved_idx is not None and retrieved_idx < len(cells) else ""

        url = extract_url(url_cell, source_cell, *cells)
        retrieved = extract_date(retrieved_cell, *cells) if not retrieved_cell else extract_date(retrieved_cell)
        if not retrieved:
            retrieved = extract_date(*cells)

        inherited_from: Optional[int] = None
        is_backref = bool(BACKREF_RE.search(source_cell) or BACKREF_RE.search(url_cell))

        if not url and is_backref:
            url, inherited_from, reason = resolve_backref(source_cell, url_cell, url_history)
            if reason:
                problems.append(UnparseableRow(
                    file=path.name, section=section, row_number=lineno,
                    reason=reason, raw=line[:300],
                ))
                continue

        if not url:
            problems.append(UnparseableRow(
                file=path.name, section=section, row_number=lineno,
                reason="no URL found in row", raw=line[:300],
            ))
            continue

        seen_here = [url]
        for extra in URL_RE.findall(source_cell + " " + url_cell):
            extra = extra.rstrip(">").rstrip(".").rstrip(")")
            if extra not in seen_here:
                seen_here.append(extra)
        url_history.append((lineno, source_cell, seen_here))

        if not claim.strip():
            problems.append(UnparseableRow(
                file=path.name, section=section, row_number=lineno,
                reason="empty Claim cell", raw=line[:300],
            ))
            continue

        rows.append(SourceRow(
            file=path.name, state=state, section=section, claim=claim,
            source_cell=source_cell or url, url=url, retrieved=retrieved,
            row_number=lineno, inherited_from=inherited_from,
        ))

    return rows, problems


def discover_files(references_dir: Path) -> list[Path]:
    files = sorted(references_dir.glob("verification_*.md"))
    top = references_dir / "VERIFICATION.md"
    if top.exists():
        files.append(top)
    return files


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------


@dataclass
class FetchResult:
    requested_url: str
    final_url: str
    status: Optional[int]
    content_type: str
    body: str
    error: Optional[str] = None
    redirected: bool = False


class _RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def default_fetch(url: str, timeout: int = DEFAULT_TIMEOUT, user_agent: str = DEFAULT_USER_AGENT) -> FetchResult:
    """Fetch url with GET, a real browser User-Agent, and a timeout, returning a FetchResult (never raises)."""
    scheme = url.split(":", 1)[0].lower() if ":" in url else ""
    if scheme not in ALLOWED_SCHEMES:
        return FetchResult(requested_url=url, final_url=url, status=None, content_type="",
                           body="", error='refused: scheme %r is not http or https' % (scheme or 'none',))
    recorder = _RedirectRecorder()
    opener = urllib.request.build_opener(recorder)
    request = urllib.request.Request(url, method="GET", headers={
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with opener.open(request, timeout=timeout) as resp:
            status = resp.status
            final_url = resp.geturl()
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read(MAX_RESPONSE_BYTES)
    except urllib.error.HTTPError as exc:
        status = exc.code
        final_url = exc.geturl() if hasattr(exc, "geturl") else url
        content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        try:
            raw = exc.read(MAX_RESPONSE_BYTES)
        except Exception:
            raw = b""
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
        return FetchResult(requested_url=url, final_url=url, status=None, content_type="", body="", error=str(exc))
    except Exception as exc:  # pragma: no cover - defensive catch-all
        return FetchResult(requested_url=url, final_url=url, status=None, content_type="", body="", error=str(exc))

    try:
        body = raw.decode("utf-8", errors="replace")
    except Exception:  # pragma: no cover
        body = raw.decode("latin-1", errors="replace")

    return FetchResult(
        requested_url=url, final_url=final_url, status=status,
        content_type=content_type, body=body,
        redirected=bool(recorder.chain) or (final_url.rstrip("/") != url.rstrip("/")),
    )


FetchFn = Callable[[str], FetchResult]


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


@dataclass
class CheckOutcome:
    row: SourceRow
    bucket: str
    detail: str
    final_url: str = ""


def classify(row: SourceRow, result: FetchResult) -> CheckOutcome:
    if result.error is not None:
        return CheckOutcome(row=row, bucket="UNREACHABLE", detail=result.error)

    status = result.status
    body = result.body or ""
    content_type = (result.content_type or "").lower()

    if status == 202 and len(body.strip()) == 0:
        return CheckOutcome(row=row, bucket="BLOCKED", detail="HTTP 202 with an empty body, looks like an automated-retrieval block, not a dead link")

    if status is not None and status >= 400:
        return CheckOutcome(row=row, bucket="HTTP_ERROR", detail=f"HTTP {status}")

    if status is None:
        return CheckOutcome(row=row, bucket="UNREACHABLE", detail="no response")

    is_redirect = result.redirected and result.final_url and result.final_url != row.url

    if "pdf" in content_type:
        detail = "served as application/pdf, text content is not checked by this tool"
        if is_redirect:
            detail += f", redirected to {result.final_url}"
        outcome = CheckOutcome(row=row, bucket="PDF_UNCHECKED", detail=detail, final_url=result.final_url)
        return outcome

    if is_redirect:
        return CheckOutcome(
            row=row, bucket="REDIRECTED",
            detail=f"HTTP {status}, final URL {result.final_url} (likely an official domain move, not a defect)",
            final_url=result.final_url,
        )

    if status == 200:
        page_text = strip_html(body)
        fraction = claim_match_fraction(row.claim, page_text)
        if fraction is not None and fraction >= MATCH_THRESHOLD:
            return CheckOutcome(row=row, bucket="OK", detail=f"claim text match {fraction:.0%}")

        if len(page_text) < CLIENT_RENDERED_VISIBLE_TEXT_MAX and len(body) > CLIENT_RENDERED_RAW_BODY_MIN:
            return CheckOutcome(
                row=row, bucket="LIKELY_CLIENT_RENDERED",
                detail=f"HTTP 200, {len(body)} raw bytes but only {len(page_text)} visible chars after stripping markup, page is likely rendered by JavaScript",
            )

        note = "claim words not found in fetched text" if fraction is not None else "claim cell too short to judge"
        return CheckOutcome(row=row, bucket="NO_CLAIM_TEXT", detail=f"HTTP 200, {note} ({len(body)} bytes)")

    return CheckOutcome(row=row, bucket="HTTP_ERROR", detail=f"HTTP {status}, unhandled status")


# ---------------------------------------------------------------------------
# Runner and report
# ---------------------------------------------------------------------------


def run(
    references_dir: Path,
    fetch: FetchFn,
    state: Optional[str] = None,
    limit: Optional[int] = None,
    delay: float = DEFAULT_DELAY,
    progress: Optional[Callable[[int, int, SourceRow], None]] = None,
) -> tuple[list[CheckOutcome], list[UnparseableRow]]:
    all_rows: list[SourceRow] = []
    all_problems: list[UnparseableRow] = []

    for path in discover_files(references_dir):
        file_state = state_for_file(path)
        if state and file_state != state.upper():
            continue
        rows, problems = parse_reference_file(path)
        all_rows.extend(rows)
        all_problems.extend(problems)

    if limit is not None:
        all_rows = all_rows[:limit]

    outcomes: list[CheckOutcome] = []
    total = len(all_rows)
    for i, row in enumerate(all_rows):
        if progress:
            progress(i + 1, total, row)
        result = fetch(row.url)
        outcomes.append(classify(row, result))
        if i < total - 1 and delay > 0:
            time.sleep(delay)

    return outcomes, all_problems


def write_report(
    out_path: Path,
    outcomes: list[CheckOutcome],
    problems: list[UnparseableRow],
    args_summary: str,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    by_bucket: dict[str, list[CheckOutcome]] = {b: [] for b in BUCKETS}
    for outcome in outcomes:
        by_bucket[outcome.bucket].append(outcome)

    with io.open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("Source health report\n")
        fh.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
        fh.write(f"Parameters: {args_summary}\n")
        total_rows = len(outcomes) + len(problems)
        skip_fraction = (len(problems) / total_rows) if total_rows else 0.0
        fh.write(f"Rows checked: {len(outcomes)}\n")
        fh.write(f"Rows skipped as unparseable: {len(problems)} ({skip_fraction:.0%} of {total_rows})\n")
        if total_rows and skip_fraction > 0.25:
            fh.write(
                f"WARNING: more than a quarter of rows were skipped as unparseable "
                f"({len(problems)} of {total_rows}, {skip_fraction:.0%}). "
                f"This report does not cover most of the pack.\n"
            )
        fh.write("\n")

        fh.write("Summary\n")
        for bucket in BUCKETS:
            count = len(by_bucket.get(bucket, [])) if bucket != "UNPARSEABLE_ROW" else len(problems)
            fh.write(f"  {bucket}: {count}\n")
        fh.write("\n")

        for bucket in BUCKETS:
            if bucket == "UNPARSEABLE_ROW":
                if not problems:
                    continue
                fh.write(f"## {bucket} ({len(problems)})\n\n")
                for p in problems:
                    fh.write(f"- {p.file}:{p.row_number} [{p.section}] {p.reason}\n")
                    fh.write(f"    {p.raw}\n")
                fh.write("\n")
                continue

            items = by_bucket.get(bucket, [])
            if not items:
                continue
            fh.write(f"## {bucket} ({len(items)})\n\n")
            for outcome in items:
                r = outcome.row
                fh.write(f"- {r.file}:{r.row_number} [{r.state}] {r.url}\n")
                fh.write(f"    claim: {r.claim[:200]}\n")
                fh.write(f"    retrieved: {r.retrieved or 'unknown'}\n")
                if r.inherited_from is not None:
                    fh.write(f"    inherited URL from {r.file}:{r.inherited_from}\n")
                fh.write(f"    {outcome.detail}\n")
            fh.write("\n")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check whether cited sources in references/ are reachable and still support their claim.",
    )
    parser.add_argument("--limit", type=int, default=None, help="check at most N rows")
    parser.add_argument("--state", type=str, default=None, help="check only one state, e.g. --state ak (or NATIONAL)")
    parser.add_argument("--out", type=str, default=None, help="output file path, defaults under the data root")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="seconds to sleep between requests")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="per-request timeout in seconds")
    parser.add_argument("--references-dir", type=str, default=None, help="override the references/ directory")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    references_dir = Path(args.references_dir) if args.references_dir else repo_root / "references"

    if args.out:
        out_path = Path(args.out)
        if out_path.is_dir():
            out_path = out_path / f"source_health_{datetime.now():%Y%m%d_%H%M%S}.txt"
    else:
        out_path = DEFAULT_OUT_DIR / f"source_health_{datetime.now():%Y%m%d_%H%M%S}.txt"

    def fetch(url: str) -> FetchResult:
        return default_fetch(url, timeout=args.timeout)

    def progress(i: int, total: int, row: SourceRow) -> None:
        print(f"[{i}/{total}] {row.file}:{row.row_number} {row.url}", file=sys.stderr)

    outcomes, problems = run(
        references_dir=references_dir, fetch=fetch, state=args.state,
        limit=args.limit, delay=args.delay, progress=progress,
    )

    args_summary = f"limit={args.limit} state={args.state} delay={args.delay} timeout={args.timeout}"
    write_report(out_path, outcomes, problems, args_summary)

    total_rows = len(outcomes) + len(problems)
    skip_fraction = (len(problems) / total_rows) if total_rows else 0.0
    print(f"Checked {len(outcomes)} rows, {len(problems)} unparseable rows skipped ({skip_fraction:.0%}).")
    if total_rows and skip_fraction > 0.25:
        print(f"WARNING: more than a quarter of rows were skipped as unparseable ({skip_fraction:.0%}).")
    print(f"Report written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
