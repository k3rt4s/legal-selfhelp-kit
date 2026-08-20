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

## Closed since the first release

**Current official rule text, closed.** Confirmed the Tennessee Bar Association's *Tennessee Rules of Professional Conduct, 2023 Edition* (amendments through November 30, 2022) as a citable, dated current-text source, and corrected a real defect it turned up: RPC 1.16(d) lists six steps to protect a client's interests, not five, because surrendering papers and property is a separate step from surrendering other work product. `references/tennessee-professional-conduct.md` and `references/VERIFICATION.md` are updated accordingly. tncourts.gov itself, the official publication point, remains unreachable to automated retrieval.

**Deadlines and limitation periods, closed.** Sourced five deadlines: no time bar on a Board disciplinary complaint, the Client Protection Fund's 60-day complaint gate plus its separate 3-year and 5-year loss-based limits, the six-year contract limitation, the one-year legal malpractice limitation with its five-year repose, and the confirmed-versus-unconfirmed filing-window status of the seven local fee dispute programs. Added `references/tennessee-deadlines.md` and updated `references/VERIFICATION.md`.

## Not built, and why

**Tennessee Consumer Protection Act analysis.** Whether and when the TCPA reaches a lawyer's professional services is not settled in the way consumer kits often assume. Not researched, not claimed.

**Other states.** Tennessee only. The structure is built to take state packs, and the citation standard applies to any that arrive.

**County-level fee dispute program detail.** The kit names the counties the Board identifies as having programs. It does not carry each program's rules, forms, or whether participation is mandatory, because those are set locally and change.

## Shipping rules

1. No legal claim ships without a row in `references/VERIFICATION.md` naming its source and retrieval date.
2. No template ships containing quoted rule text.
3. No deadline ships without a source in `references/VERIFICATION.md`.
4. Examples use invented facts only.
5. If `scripts/` changes, the test suite passes first.

## Order for the next release

1. Add per-county fee dispute program detail with sources.
2. Add a second state pack, which will prove whether the structure actually generalizes.
