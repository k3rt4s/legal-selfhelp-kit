# Maintaining

How the kit is kept current once its scope is complete, which is one bounded sweep on a schedule rather than an open-ended project.

## What done means

The kit covers all fifty states and the District of Columbia. Nothing is queued in `FUTURE_FEATURES.md` except work the sweep itself found and handed to the next sweep, and the rejected list there is firm. New work comes from two places only: a reader's issue on GitHub, and the scheduled sweep. A maintainer who finds nothing on either has nothing to do, and that is the intended state.

## The sweep

Run it twice a year, or when a reader reports a source that no longer says what the kit cites it for. One session, budgeted at a morning. It fixes or cuts; it does not add coverage, reopen a rejected feature, or widen scope.

1. From the repo root, `python scripts/check_sources.py`. It makes about two thousand fetches at a polite delay, takes about an hour, and writes its report to the OS temp directory (`--out` chooses another place). Run it somewhere its progress lines do not have to be read.
2. Read `Rows skipped as unparseable` before anything else in the report. The baseline from the last sweep is 33 of 1,967 rows, no file worse than three. If that moved, the parser broke or a file's table shape changed; fix that and rerun, because until the count matches, the summary above it is meaningless.
3. Triage NO_CLAIM_TEXT first. It is the bucket the tool exists for: the page answered and no longer carries the claim. Fetch and read each page before deciding. Some moved the text behind a tab or a script, some genuinely changed. A row whose detail says the claim cell was too short to judge is a row to reword, not a broken source.
4. The other buckets are not defects by themselves. LIKELY_CLIENT_RENDERED and BLOCKED describe how a site serves robots. REDIRECTED is usually a domain move, but the checker does not claim-check the final page, so fetch it once and look for the claim. HTTP_ERROR splits into real 404s, bot-blocking 403s, and sites that were simply down during the sweep; read the status and refetch before believing it. PDF_UNCHECKED and UNREACHABLE mean unchecked. A row citing a Wayback capture is judged only if web.archive.org answers that day; it reset every connection during the August 2026 sweep and seventeen rows went unjudged, which is not a defect. One New Jersey row cites an archive larger than the fetcher's five megabyte cap and reports as an error every time.
5. Re-check every UNREACHABLE row with `curl` before treating any of them as a dead link. The checker uses Python's urllib, which some official sites refuse at the TLS handshake while curl reaches them fine; see `THEORY.md`. In the August 2026 sweep all thirty were false and none was a broken link.
6. For each genuine change: fix the claim and its row if a primary source turns up in one attempt. Otherwise cut the claim to that file's gap list and add a CHANGELOG correction line naming it, so a reader who acted on the old text can see that it moved. The August 2026 sweep is the one exception on record: it found twenty rows whose page no longer carries the claim, sourced none of them in one attempt, and queued them in `FUTURE_FEATURES.md` instead of cutting twenty reader-facing claims in a release week. February 2027 sources them or cuts them. Do not read that as permission to defer a row again.
7. Recheck the two Massachusetts front-page figures by hand (see `THEORY.md`, Known soft spots).
8. Run `python -m pytest tests -q`, update the baseline in step 2, record the sweep in `CHANGELOG.md`, and cut a patch release.

## Releases

Patch for corrections and sweeps. Minor when a reader-facing file gains or loses a section. Major only if the tracker columns or the rules layer change shape, which is not planned. `CHANGELOG.md` and `roadmap.json` carry the record.

## Python

The scripts are standard-library only. The version they are tested on is in `scripts/README.md`.
