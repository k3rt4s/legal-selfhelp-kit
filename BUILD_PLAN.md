# Build plan

What is built, what is not, and what has to be true before anything ships.

## Shipped in the first release

| Area                 | State                                                                               |
| -------------------- | ----------------------------------------------------------------------------------- |
| LLM layer            | Complete. System prompt, workflow, output contract, quickstart                      |
| Rules                | Fifteen numbered files covering every workflow stage                                |
| Templates            | Eleven letters and submissions                                                      |
| Tennessee references | Professional conduct provisions, six forums, verification file                      |
| Reader docs          | Start here, decision tree, anti-patterns, common outcomes, records retention, index |
| Tracker              | Template CSV, column dictionary, TOML schema                                        |
| Examples             | Three worked walkthroughs, invented facts                                           |
| Scripts and tests    | Standard-library tracker validator, thirteen passing tests                          |

## Not built, and why

**Current official rule text.** The Tennessee Rules of Professional Conduct are published at tncourts.gov, which did not return readable rule text to automated retrieval, and neither did an archived copy. The rule content here came from a Tennessee Bar Association redline comparison document. Until someone confirms the current text against the official source, the kit references rules by number rather than quoting them, and `references/VERIFICATION.md` says so plainly.

**Deadlines and limitation periods.** No verified research exists behind any filing window for a disciplinary complaint, a fee claim, or a client protection fund claim. Rather than guess, the kit refuses to assert deadlines and tells the user to confirm. This is the largest single gap.

**Tennessee Consumer Protection Act analysis.** Whether and when the TCPA reaches a lawyer's professional services is not settled in the way consumer kits often assume. Not researched, not claimed.

**Other states.** Tennessee only. The structure is built to take state packs, and the citation standard applies to any that arrive.

**County-level fee dispute program detail.** The kit names the counties the Board identifies as having programs. It does not carry each program's rules, forms, or whether participation is mandatory, because those are set locally and change.

## Shipping rules

1. No legal claim ships without a row in `references/VERIFICATION.md` naming its source and retrieval date.
2. No template ships containing quoted rule text.
3. No file asserts a deadline.
4. Examples use invented facts only.
5. If `scripts/` changes, the test suite passes first.

## Order for the next release

1. Confirm the current text of RPC 1.5, 1.4, 1.15, and 1.16 against the official source, and move those rows in the verification file.
2. Research and source the filing deadlines that currently cannot be stated.
3. Add per-county fee dispute program detail with sources.
4. Add a second state pack, which will prove whether the structure actually generalizes.
