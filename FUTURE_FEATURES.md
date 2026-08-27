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
rules live in `MAINTAINING.md` rather than here. Three items came out of the August 2026 sweep
and are queued for the next one rather than done now, because none of them changes what a
reader is told.

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
