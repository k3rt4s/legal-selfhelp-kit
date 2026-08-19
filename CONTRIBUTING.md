# Contributing

This project is open under MIT. Corrections are more valuable than additions.

## The citation standard

Every legal claim in this kit carries a row in [references/VERIFICATION.md](references/VERIFICATION.md) naming its source and retrieval date, added in the same commit as the claim. A claim without a row is a defect, and a pull request that adds one will be asked to fix it.

If you cannot source a claim to a primary or official publication, do not add it. "I am a lawyer and I know this" is not a citation.

## What is especially welcome

1. Corrections where a rule, dollar limit, phone number, or program has changed.
2. Confirmation of the current text of the Tennessee Rules of Professional Conduct from the official source, which would let the verification file move rows out of the needs-confirmation section.
3. Additional counties with fee dispute programs, with a source.
4. Packs for other states, following the same structure and the same citation standard.

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
