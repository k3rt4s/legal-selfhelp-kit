# Contributing

How to contribute to legal-selfhelp-kit, which is open under MIT and where corrections are more valuable than additions.

## The citation standard

Every legal claim in this kit carries a row in [references/VERIFICATION.md](references/VERIFICATION.md) naming its source and retrieval date, added in the same commit as the claim. A claim without a row is a defect, and a pull request that adds one will be asked to fix it.

If you cannot source a claim to a primary or official publication, do not add it. "I am a lawyer and I know this" is not a citation.

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

If you touch `scripts/`, run the suite:

```text
python -m pytest tests -q
```
