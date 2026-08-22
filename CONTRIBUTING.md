# Contributing

How to contribute to legal-selfhelp-kit, which is open under MIT and where corrections are more valuable than additions.

## The citation standard

Every legal claim in this kit carries a row in [references/VERIFICATION.md](references/VERIFICATION.md) naming its source and retrieval date, added in the same commit as the claim. A claim without a row is a defect, and a pull request that adds one will be asked to fix it.

If you cannot source a claim to a primary or official publication, do not add it. "I am a lawyer and I know this" is not a citation.

Cite it with a URL that lands on the page holding the claim. A bare domain is a defect when the claim lives on a deeper page, because a reader who clicks it has to go hunting. A front page is the right cite in two situations only: the claim is about the organization itself, its name, address, phone, or the fact that it exists, or the front page is genuinely where the text is and no deeper page carries it. Those exceptions are listed by name in `tests/test_reference_layer.py` with a reason for each, and a test fails if one stops matching, so adding one is a deliberate act rather than a link quietly going shallow.

Fetch the page and read it before you cite it. A status code proves nothing here. Pages in this corpus have returned success with an error body, returned nothing but navigation with the content rendered in the browser, and returned an empty body from a bot filter. If you did not find the claim in what came back, you have not sourced it.

## What is especially welcome

1. Corrections where a rule, dollar limit, phone number, or program has changed.
2. Confirmation of the current text of a state's rules of professional conduct from the official source, which would let that state's verification file move rows out of the needs-confirmation section.
3. Additional local programs within a state pack, with a source.
4. New or corrected state packs. This is now the main way anyone contributes. See [references/state_template.md](references/state_template.md) for the required shape of a pack and [references/VERIFICATION.md](references/VERIFICATION.md) for the citation standard every claim in it must meet.

## What will be declined

1. Anything that turns the kit into a prediction engine. No estimated recoveries, no odds.
2. Quoted rule text placed into letter templates.
3. Asserted deadlines or limitation periods without a primary source.
4. Anything adversarial in tone. The templates work because they are calm.
5. Real matter details. Examples use invented facts, always.

## Style

Short sentences. Plain language. No em dashes. Write for someone who is stressed and not a lawyer.

## Tests

Run the suite before you open a pull request, whether you touched `scripts/` or `references/`:

```text
python -m pytest tests -q
```

The reference layer has no logic to test, so `tests/test_reference_layer.py` tests its shape instead, reading the files on disk. It will tell you if a pack is missing a section, if a verification file is missing its Confirmed, Flagged, or Gap part, or if a source cell points at a bare domain.

`scripts/check_sources.py` is the other half of that, and it is a maintenance tool rather than a test. It fetches every cited URL and reports which pages no longer carry the claim they are cited for. It makes network requests, so it is not part of the suite and nothing runs it automatically. Check one state while you work:

```text
python scripts/check_sources.py --state ak
```

It writes its report outside the repository and changes nothing.
