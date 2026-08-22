# Future features

Backlog of work not yet scheduled. Nothing here is promised.

## Coverage

Nothing queued. Four items that were here all shipped into the national baseline: contingent-fee
disputes, clients whose lawyer died, was disciplined, or left practice, a lawyer who keeps the
file under a claimed retaining lien, and a fee paid by someone other than the client.

## Product

Nothing queued. Six items that were here have shipped: the worked example where the client is
wrong, the printable one-page decision tree, the tracker-to-chronology exporter, the delivery
and local-program guidance, `scripts/check_sources.py`, and `tests/test_reference_layer.py`.

## Maintenance, unscheduled

Nothing here is a defect today. Each is a thing that will drift and nobody would notice.

1. Run `scripts/check_sources.py` across all 51 packs and act on the report. It has only
   ever been run against a handful of states. The first full run is the one that will find
   how much of the reference layer has rotted, and it is also the run most likely to find
   a bug in the checker itself, so read the UNPARSEABLE_ROW count before trusting the rest
   of the summary.
2. Two Massachusetts client-protection figures, the fund's cumulative payout and the number
   of clients reimbursed, appear only on the fund's front page and nowhere in its annual
   reports. They are live numbers on a page that will change without notice. Both rows say
   so, and the honest fix is to recheck them rather than to cite them harder.
3. Abel v. Austin, the Kentucky decision on the KRS 413.245 limitation period, is flagged
   rather than confirmed because no official Kentucky source served the opinion. A session
   with law library, Westlaw, or Lexis access could retire that flag. The pack does not
   rely on the case, so this is a provenance improvement, not a correction.

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
