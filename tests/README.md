# Tests

Pytest suite covering the optional tracker validator, the source-health checker, and the structure of the reference layer itself, no network calls.

Run from the repository root:

```text
python -m pytest tests -q
```

Most of the scripts here have logic to test directly. The reference layer is Markdown with no
logic of its own, so `test_reference_layer.py` tests its shape instead: the required sections,
the required citation structure, and the count of packs, read straight from the files on disk.

- `test_validate_tracker.py`, `test_export_chronology.py`: the tracker validator and chronology exporter, against conforming and non-conforming fixtures.
- `test_check_sources.py`: the `references/` source-health checker, covering table parsing (including the gap-list skip, the SUPERSEDED skip, and "Same URL as above" carry-forward) and result classification against fixture HTML strings. The fetch step is injected, so nothing here touches the network.
- `test_reference_layer.py`: every `references/state_XX.md` pack and its `verification_XX.md`, checked directly against the repository, not fixtures. Confirms every pack has a verification file and vice versa, the eight required sections appear in order, sections 1/3/4/5 each carry a complete URL, every verification file has its Confirmed/Flagged/Gap parts, every Confirmed/Flagged row has a Claim and a Source, any URL in a Source cell lands on the page holding the claim rather than on a bare domain, the documented pack count agrees with the file count, and no pack contains an em dash or a curly quote. The handful of places where a front page is the right cite are listed by name in the test file with the reason for each, and a further test fails if one of those entries stops matching, so the list cannot quietly grow or go stale.
