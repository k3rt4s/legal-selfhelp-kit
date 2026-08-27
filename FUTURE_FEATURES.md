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
