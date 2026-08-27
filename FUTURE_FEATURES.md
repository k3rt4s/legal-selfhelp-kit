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

## Maintenance

The standing maintenance is the scheduled source sweep, whose procedure, cadence, and triage
rules live in `MAINTAINING.md` rather than here. Eight items came out of the August 2026
sweep and are queued for the February 2027 one rather than done now. The first four are
checker work and change nothing a reader is told. The last four are rows whose citation is
weaker than the file claims, none of which was reachable in one attempt during the sweep,
which is the bar `MAINTAINING.md` sets for fixing a row in the sweep that found it.

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

5. Re-source the twenty rows whose cited page no longer carries the claim. Each was fetched and
   read during the sweep, and no replacement source turned up in one attempt: az 15, 16, 26, dc
   13, 14, 15, 16, 24, id 39, ks 28, ma 24, 25, 26, 27, md 41, nc 50, ut 43, 57, 58, va 26. Two
   need care rather than searching. `verification_ut.md:57` cites a rule page that answers 200
   with the body "This Rule cannot be found", so it is dead rather than merely unmatched.
   `verification_nc.md:50` says its rule sections were fetched and read directly but cites only
   the index page above them, so the URLs it was actually checked against are recorded nowhere.
   Six of them are compound citations, dc 24, ma 24 to 27 and va 26, where only one of the two
   cited documents was tested; test the other before concluding anything about those.
6. Fill in three citations that are malformed rather than wrong. `verification_mn.md:23` carries
   the literal placeholder `{N}` in its Source cell where a document ID belongs; the surrounding
   pattern is live and consistent with the claim, so this is a value to supply, not a source to
   find. `verification_ut.md:58` reads "Same PDF as sc78a8.pdf above" and nothing earlier in the
   file defines that name, so the backreference resolves to a neighboring rule page that has
   nothing to do with the claim; the rows above it cite dated PDFs at a fixed le.utah.gov pattern
   and the section 78A-8-106 equivalent is the likely target. `verification_or.md:61` cites the
   wrong page and the sweep named a candidate without confirming the claim is on it.
7. Rewrite the five rows that name a source too loosely to resolve, `verification_in.md` 47 and
   48 and `verification_ms.md` 63 to 65. `THEORY.md` explains why no checker change reaches
   them: one names a host that carries thousands of pages, the others reason by elimination over
   rows above and have no single page behind them. The cure is naming the document in the cell.
8. Judge the five rows that cite a Wayback capture and could not be reached during the sweep:
   `verification_in.md:30`, `verification_ma.md` 15 and 17, and `verification_mn.md` 16 and 17.
   web.archive.org reset every connection from the maintainer's machine that day while its own
   availability API answered. Unverified for that reason is not a defect.

Closed, and here for the record: the first full sweep ran, the two Massachusetts front-page
figures are a step in every sweep, Abel v. Austin stays flagged as a recorded soft spot in
`THEORY.md` because the pack does not rely on it, and `scripts/README.md` now states the Python
version the scripts are tested on.

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
