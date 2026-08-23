# Maintaining

How the kit is kept current once its scope is complete, which is one bounded sweep on a schedule rather than an open-ended project.

## What done means

The kit covers all fifty states and the District of Columbia. Nothing is queued in `FUTURE_FEATURES.md` beyond the sweep described here, and the rejected list there is firm. New work comes from two places only: a reader's issue on GitHub, and the scheduled sweep. A maintainer who finds nothing on either has nothing to do, and that is the intended state.

## The sweep

Run it twice a year, or when a reader reports a source that no longer says what the kit cites it for. One session, budgeted at a morning. It fixes or cuts; it does not add coverage, reopen a rejected feature, or widen scope.

1. From the repo root, `python scripts/check_sources.py`. It makes about two thousand fetches at a polite delay, takes about an hour, and writes its report to the OS temp directory (`--out` chooses another place). Run it somewhere its progress lines do not have to be read.
2. Read `Rows skipped as unparseable` before anything else in the report. The baseline from the last sweep is 37 of 1,986 rows, no file worse than four. If that moved, the parser broke or a file's table shape changed; fix that and rerun, because until the count matches, the summary above it is meaningless.
3. Triage NO_CLAIM_TEXT first. It is the bucket the tool exists for: the page answered and no longer carries the claim. Fetch and read each page before deciding. Some moved the text behind a tab or a script, some genuinely changed. A row whose detail says the claim cell was too short to judge is a row to reword, not a broken source.
4. The other buckets are not defects by themselves. LIKELY_CLIENT_RENDERED and BLOCKED describe how a site serves robots. REDIRECTED is usually a domain move, but the checker does not claim-check the final page, so fetch it once and look for the claim. HTTP_ERROR splits into real 404s and bot-blocking 403s; read the status. PDF_UNCHECKED and UNREACHABLE mean unchecked.
5. For each genuine change: fix the claim and its row if a primary source turns up in one attempt. Otherwise cut the claim to that file's gap list and add a CHANGELOG correction line naming it, so a reader who acted on the old text can see that it moved.
6. Recheck the two Massachusetts front-page figures by hand (see `THEORY.md`, Known soft spots).
7. Run `python -m pytest tests -q`, update the baseline in step 2, record the sweep in `CHANGELOG.md`, and cut a patch release.

## Releases

Patch for corrections and sweeps. Minor when a reader-facing file gains or loses a section. Major only if the tracker columns or the rules layer change shape, which is not planned. `CHANGELOG.md` and `roadmap.json` carry the record.

## Python

The scripts are standard-library only. The version they are tested on is in `scripts/README.md`.
