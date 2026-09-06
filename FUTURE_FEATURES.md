# Future features

Backlog of work not yet scheduled. Nothing here is promised.

## Scored index

One bullet per unshipped feature, with the score block the developer challenges and the return
block that says what the number stands for. Every item below is queued for the February 2027
sweep under Maintenance. Keep this list current: add a bullet when a feature is added, and mark
one moved or dropped on the day it leaves.

- **fetcher** Give the checker a transport that reaches the hosts urllib cannot. Maintenance item 1.
  `score: kind=toil gain=0.5/1/2.5 p=0.85 freq=2 hours=0.5/1/2 ai=3 risk=0.1x1 rev=two-way conf=measured id=fetcher`
  `return: likelihood 1 in 1 per sweep, about 2 sweeps a year, so about twice a year, counted from the 30 UNREACHABLE rows in the August 2026 sweep reports under the data root at source_health/chunked_20260822 dated 2026-08-22, every one of which MAINTAINING.md step 5 records as false; impact one manual curl pass over about 30 rows before any of them can be judged, 0.5 to 2.5 h of the maintainer's time per sweep, and a sweep report that overstates rot until the pass is done; evidence the 30 UNREACHABLE rows aggregated across the chunked source_health reports of 2026-08-22, MAINTAINING.md steps 4 and 5, and the urllib transport at scripts/check_sources.py lines 12 to 13 and 495 to 515`
  - worker: sonnet 1.5/3/5 h.
- **sizecap** Raise or bypass the response size cap for cited sources that are large archives. Maintenance item 2.
  `score: kind=toil gain=0.05/0.15/0.4 p=1 freq=2 hours=0.15/0.25/0.5 ai=1 rev=two-way conf=measured id=sizecap`
  `return: likelihood 1 in 1 per sweep, about 2 sweeps a year, so about twice a year, from the one New Jersey row that cites an archive larger than the 5 MB cap and that MAINTAINING.md step 4 records as reporting an error every time; impact one row reports as an error and is triaged by hand, about 3 to 25 minutes of the maintainer's time per sweep, and no reader sees anything wrong; evidence MAX_RESPONSE_BYTES 5,000,000 at scripts/check_sources.py line 85 and the capped reads at lines 506 and 512, and the New Jersey note in MAINTAINING.md step 4 dated 2026-08-27`
  - worker: haiku 0.25/0.5/1 h.
- **prompttest** Test the rules layer and the system prompt against each other. Maintenance item 3.
  `score: kind=prevent gain=2/8/40 p=0.8 freq=0.4 hours=0.5/1/2 ai=4 risk=0.05x1 rev=two-way conf=assessed flags=legal id=prompttest`
  `return: likelihood about 1 in 7 per edit to rules/ or llm/, about 3 such edits a year in maintenance, so about 0.4 drifts a year, the 1 in 7 counted from the 7 commits touching rules/ or llm/ since the repo opened on 2026-08-19, of which one, 82fe1b1, was the drift itself, n 7 and too small to narrow the range; impact the two prose layers disagree and the model is barred from stating a filing window the pack carries, 2 to 40 h to notice, trace and correct, and a reader who acts on the gap can miss a fee arbitration deadline; evidence commit 82fe1b1 and its 1.0.0 CHANGELOG entry, git log over rules/ and llm/ from 2026-08-19 to 2026-09-06, and the boundaries stated twice in rules/01_scope_and_limits.md line 9 and llm/SYSTEM_PROMPT.md`
  - worker: sonnet 1.5/3/6 h.
- **hostmatch** Match a backreference host on the parsed host with a dot boundary, not a raw substring. Maintenance item 4.
  `score: kind=prevent gain=0.25/1/4 p=0.05 hours=0.15/0.25/0.5 ai=1 rev=two-way conf=assessed id=hostmatch`
  `return: likelihood none in the 2,000 rows the August 2026 sweep read, so at most 3 in 2,000 per row by the rule of three, and about 4,000 row-checks a year at 2 sweeps, so about 1 in 20 within the year, held down further because every URL in the corpus is one a maintainer reviewed; impact one row is checked against a page it never cited and its verdict is wrong in either direction, 0.25 to 4 h to notice and unpick, and no reader-facing claim changes; evidence the substring test at scripts/check_sources.py line 243 inside resolve_backref, and the 2,000 rows judged in the chunked source_health reports of 2026-08-22`
  - worker: haiku 0.25/0.5/1 h.
- **aboveorder** Stop the word above in a source cell overriding the document the cell names. Maintenance item 5.
  `score: kind=bug gain=2/4/8 p=0.7 freq=2 hours=0.5/1/2 ai=4 risk=0.15x2 rev=two-way conf=measured id=aboveorder`
  `return: likelihood 1 in 1 per sweep, about 2 sweeps a year, so about twice a year, counted from the 124 NO_CLAIM_TEXT verdicts in the August 2026 sweep, triaged down to the 20 rows reported as no longer carrying their claim, of which MAINTAINING.md step 6 records that most were tested against a page the row does not cite; impact a hand re-check of every false claim-missing verdict before any of them can be trusted, 2 to 8 h of the maintainer's time per sweep, and a real defect can hide inside a bucket the maintainer has learned to discount; evidence the 124 NO_CLAIM_TEXT rows aggregated across the chunked source_health reports of 2026-08-22, the consolidated defect_list.md beside them, MAINTAINING.md step 6, and the short-circuit at scripts/check_sources.py line 248 where the word above skips descriptor matching entirely`
  - worker: sonnet 1/2/4 h.
- **malformed** Fill in the two citations that are malformed rather than wrong. Maintenance item 6.
  `score: kind=bug gain=0.5/1.5/4 p=1 hours=0.25/0.5/1 ai=2 rev=two-way conf=tested flags=legal id=malformed`
  `return: likelihood 1 in 1, both rows carry the defect in the tree today, 2 rows out of the 2,000 the sweep read; impact a reader who tries to re-check either claim cannot, which standing rule 8 on this job calls a defect in its own right, 0.5 to 4 h to find the document and confirm the claim once someone reports it, and verification_or.md:61 may also be resting on the wrong page; evidence read 2026-09-06, references/verification_mn.md line 23 carries the literal placeholder in braces where a document ID belongs, and references/verification_or.md line 61 cites ors009.html by backreference with the sweep naming a candidate page it never confirmed`
  - worker: sonnet 0.5/1/2 h.
- **looserows** Rewrite the five rows that name a source too loosely to resolve. Maintenance item 7.
  `score: kind=debt gain=0.5/1.5/5 p=0.8 freq=2 hours=0.5/1/2 ai=4 rev=two-way conf=measured flags=legal id=looserows`
  `return: likelihood 1 in 1 per sweep, about 2 sweeps a year, so about twice a year, from the 5 rows named in THEORY.md as unreachable by any checker change, verification_in.md 47 and 48 and verification_ms.md 63 to 65, each of which lands in an unjudged bucket every sweep; impact 5 rows read as confirmed when no single page stands behind them and are hand-triaged again each sweep, 0.5 to 5 h per sweep, and verification_in.md:47 already cites IC 34-11-2-11 where the claim is about the IC 33-28-3-4 and IC 33-29-2-4 small claims limits, so one is a live wrong citation rather than only a loose one; evidence THEORY.md on rows no checker change can reach, the five rows read 2026-09-06, and the wrong-section finding in backref_recheck_1.md entries 5 and 6 under the data root, dated 2026-08-27`
  - worker: sonnet 1/2/4 h.

## Coverage

Nothing queued. Four items that were here all shipped into the national baseline: contingent-fee
disputes, clients whose lawyer died, was disciplined, or left practice, a lawyer who keeps the
file under a claimed retaining lien, and a fee paid by someone other than the client.

## Product

Nothing queued. Six items that were here have shipped: the worked example where the client is
wrong, the printable one-page decision tree, the tracker-to-chronology exporter, the delivery
and local-program guidance, `scripts/check_sources.py`, and `tests/test_reference_layer.py`.

## Maintenance

The standing maintenance is the scheduled source sweep, whose procedure, cadence, and triage
rules live in `MAINTAINING.md` rather than here. Seven items came out of the August 2026
sweep and are queued for the February 2027 one rather than done now. The first five are
checker work and change nothing a reader is told. The last two are rows that name their
source too loosely for any checker to resolve, and the cure is a maintainer naming the
document, not a code change.

1. Give the checker a fetcher that reaches the hosts urllib cannot. Python's OpenSSL handshake
   is reset by some official sites, jud.ct.gov reliably among them, while curl on the Windows
   Schannel stack retrieves the same URLs without trouble. No header or user-agent combination
   changes it, so this needs a different transport, not a tweak. It costs about thirty rows of
   false UNREACHABLE per sweep and a manual curl pass to clear them.
2. Raise or bypass the response size cap for the few cited sources that are large archives. One
   New Jersey row cites a zip the checker abandons at the cap and then reports as an error.
3. Test the rules layer and the system prompt against each other. `rules/01_scope_and_limits.md`
   and `llm/SYSTEM_PROMPT.md` encode the same boundaries twice, in prose, and they drifted: the
   rules file limited deadlines to a list of section numbers that excluded the fee arbitration
   section, which carries the filing windows in most packs. Nothing catches that today.

4. Tighten how the backreference resolver matches a host. It asks whether the host name appears
   anywhere inside an earlier row's URL, so `foo.gov` would match `https://notfoo.gov.example/`.
   Nothing in the corpus trips it today and the checker only ever reads URLs a maintainer has
   reviewed, but the comparison belongs on the parsed host with a dot boundary, not on the raw
   string.

5. Stop the word "above" in a source cell from overriding the document the cell names. The
   resolver treats the literal word as adjacency and short-circuits descriptor matching, so a
   cell reading "Fee Arbitration Program Rules PDF, same URL as above" resolves to whatever row
   sits directly above it rather than to the rules PDF it names. That is what produced most of
   the sweep's claim-missing verdicts: the checker tested rows against pages they do not cite.
   Adjacency should be the fallback when the cell names nothing, not the first thing tried.
   That order is what this release shipped and what the changelog entry describes, so this is
   a change to make, not a report that the code and the docs disagree.
6. Fill in two citations that are malformed rather than wrong. `verification_mn.md:23` carries
   the literal placeholder `{N}` in its Source cell where a document ID belongs; the surrounding
   pattern is live and consistent with the claim, so this is a value to supply, not a source to
   find. `verification_or.md:61` cites the wrong page and the sweep named a candidate without
   confirming the claim is on it.
7. Rewrite the five rows that name a source too loosely to resolve, `verification_in.md` 47 and
   48 and `verification_ms.md` 63 to 65. `THEORY.md` explains why no checker change reaches
   them: one names a host that carries thousands of pages, the others reason by elimination over
   rows above and have no single page behind them. The cure is naming the document in the cell.

Closed, and here for the record: the first full sweep ran; the twenty rows it reported as no
longer carrying their claim were re-checked by hand before the release and every one was
resolved in place, so none is deferred; the five Wayback-sourced rows now say in their own note
that the archive was unreachable; the two Massachusetts front-page figures are a step in every
sweep; Abel v. Austin stays flagged as a recorded soft spot in `THEORY.md` because the pack does
not rely on it; and `scripts/README.md` now states the Python version the scripts are tested on.

## Explicitly rejected

1. Anything that estimates a recovery or predicts an outcome.
2. Automated filing or submission on the user's behalf.
3. Quoted rule text inside letter templates.
4. Any feature that requires the user to upload documents to a service this project controls.
5. Compiling per-county fee dispute program detail. Fee arbitration runs through local
   committees in several states, so the accurate answer for a given reader is often county
   level. This kit will not try to cover every county in the country: the compilation would be
   enormous, every entry would need its own sourced row, and local programs change faster than
   a kit like this could track them. A stale committee name reads exactly like a current one.
   The kit ships `docs/FIND_YOUR_LOCAL_PROGRAM.md` instead, which teaches the reader and the
   model a search procedure and a confirmation checklist. A contributor who confirms a local
   program against a primary source is still welcome to add it to that state's pack; see
   `CONTRIBUTING.md`.
