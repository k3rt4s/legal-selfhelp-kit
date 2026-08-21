# Changelog

All notable changes to legal-selfhelp-kit, in plain English.

## Unreleased (0.3.0)

Not shipped yet. This section describes what is on `main` since 0.2.0.

- Added `examples/hourly_retainer_not_a_cap.md`, the first worked example where the client turns out to be wrong. Every other example ends with a claim the reader can act on. This one shows what the session says when the record does not support the complaint, and what the client can still legitimately ask for without a demand letter.
- Added `docs/DECISION_TREE_ONE_PAGE.md`, a printable one-sheet condensation of the decision tree. It adds no facts. Every branch and every condition from the full tree survives.
- Added `scripts/export_chronology.py` and its tests. It turns a filled-in tracker into a date-sorted plain-text chronology for a bar complaint or fee arbitration submission. It refuses to export a tracker the validator would reject, and rows with an unparseable date are reported rather than silently dropped.
- Added `docs/PROVABLE_DELIVERY.md`, on choosing a delivery method that lets you prove a letter arrived. It covers proving delivery, not legal service of process, and says so. Two facts that only commercial sources would confirm, how long USPS keeps a delivery record and how long an uncollected certified letter is held, were cut rather than stated.
- Added contingent-fee dispute guidance to section 4 of the national baseline. Model Rule 1.5(a) reasonableness applies to a contingent fee with no carve-out, and a contingent dispute is about the closing statement arithmetic rather than hours worked. No percentage cap or dollar figure is stated; those belong to the state packs.
- Added section 10 of the national baseline, for clients whose lawyer died, was suspended or disbarred, or left practice. The duty to return the file and refund unearned money is not conditioned on why the representation ended. The section routes the reader to their state pack's disciplinary authority to find who now holds the file.
- Sourced the New Jersey contingent-fee sliding scale to the Judiciary's own archived site rather than the two commercial mirrors it had rested on. The current njcourts.gov does not serve the rule text to automated retrieval, so the confirmed source is a 2015 capture of the Judiciary's predecessor domain. Both the pack and the row now say plainly that the kit confirmed the 2015 wording and not today's, and tell the reader to confirm the percentages with the court or a lawyer.
- Added `docs/FIND_YOUR_LOCAL_PROGRAM.md`, a search procedure and confirmation checklist for readers whose state runs fee arbitration through local committees. It names no state, county, program, deadline, or dollar figure, so it makes no claim needing a verification row. It also tells the model working with the reader that "I could not confirm a local program in your county" is a correct answer.
- Retired per-county fee dispute compilation from the backlog to the explicitly rejected list. The kit will not try to cover every county in the country. Local programs change faster than a kit like this could track, and a stale committee name reads exactly like a current one. The search document above is the answer instead, and a contributor who confirms a local program against a primary source can still add it to a state pack.

## 2026-08-21 (0.2.0, all fifty states and the District of Columbia)

Shipped. Merged to main on 2026-08-21.

- Generalized the kit from Tennessee to every state. It now ships a national baseline built on the ABA Model Rules plus one pack per state, each following the same eight sections, with its own verification file.
- Added `references/national_baseline.md` and `references/state_template.md`, and turned `references/VERIFICATION.md` into the citation standard plus an index of every per-state verification file.
- Rewrote the forum selection rule, the decision tree and the templates to branch on the reader's state rather than assuming Tennessee's forums.
- Folded the three Tennessee reference files into `references/state_tn.md` and removed them. Tennessee readers lose nothing; the same claims are in the pack, with the same sourcing.
- Added a District of Columbia pack. DC is not a state, but it has its own bar, its own disciplinary system, its own client protection fund, and a fee arbitration rule that binds the lawyer once a qualifying client files, so it needed a pack of its own rather than being read off a neighbor.
- Added two worked examples for the routing branches Tennessee does not show: Maine, where the client can require the lawyer into fee arbitration, and Alabama, where no fee arbitration program exists at all and a demand letter and small claims are the only path.
- Added the informal conciliation step to the Virginia pack. The Virginia State Bar fee dispute program opens with a discretionary conciliation attempt by the committee chair before mediation or arbitration. It is described only in the program manual, not on the program page, which is why it was missed.
- Repaired dead source links in eight state packs (Montana, Indiana, North Carolina, South Dakota, Arkansas, New Mexico, Utah, Michigan). Every claim was re-read at its current official location. No dollar figure, deadline, or program name changed. South Dakota moved off a Wayback snapshot onto a live official source, and Indiana now states plainly that its fee dispute page is gone rather than suggesting a reader might reach it.
- Changed the Oregon client protection fund contact from a named bar staff member, with a direct email and phone, to the bar main line with the fund named. A public kit should route a reader to a program, not to one person, and a named contact goes stale when that person changes roles.
- Corrected the workflow stage count in `llm/WORKFLOW.md`, which said seven stages while defining eight. Adding the state-establishing Stage 0 created the off-by-one.

### Corrections to claims that were public in 0.1.0

- Removed the claim that a consumer assistance program will follow up with a lawyer who has not responded to correspondence within ten days. That was a Tennessee program with a Tennessee deadline, stated in `rules/07_communication.md` and `rules/08_file_and_property.md` as though it applied to any reader. Most states run no such program, and those that do do not all use ten days. The rules now point at whatever intake track section 4 of the reader's own state pack names, and say not to promise a response time the pack does not state.
- Corrected `rules/04_fee_agreement.md`, which asserted a tenth reasonableness factor under Rule 1.5(a). Tennessee has ten factors. The ABA model has eight, and most states follow the model. The rule now tells the reader to check section 2 of their own state pack before naming a factor by number.
- Replaced the abbreviation RPC throughout the templates and rules. RPC is Tennessee's own name for its rules. Templates now refer to a rule by number and say it is a rule of professional conduct in the reader's state.
- Renamed the tracker's `rpc_touchpoint` column to `rule_touchpoint`, in the column dictionary, both TOML schemas, the validator, the CSV template and the tests.

## 2026-08-10 (reference layer accuracy follow-up)

- Confirmed the Tennessee Rules of Professional Conduct content against a current, dated source: the Tennessee Bar Association's 2023 Edition, amendments through November 30, 2022, replacing the redline document the rule text was originally checked against.
- Corrected RPC 1.16(d) in `references/tennessee-professional-conduct.md`: the rule lists six steps to protect a client's interests on discharge or withdrawal, not five. Surrendering papers and property the client is entitled to and surrendering other work product are separate steps.
- Added `references/tennessee-deadlines.md`, sourcing five deadlines: no time bar on a Board disciplinary complaint, the Client Protection Fund's 60-day complaint gate and its separate 3-year and 5-year loss-based limits, the six-year contract limitation, the one-year legal malpractice limitation with its five-year repose, and the confirmed-versus-unconfirmed filing-window status of the seven local fee dispute programs.
- Updated `references/VERIFICATION.md` with the new sourcing and two caveats: the statute text came from a commercial code mirror rather than the official Tennessee Code, and tncourts.gov remains unreachable to automated retrieval.

## 2026-08-10

- First release. Tennessee scope.
- Added the LLM layer: system prompt, six-stage workflow, output contract, and a short-context quickstart.
- Added fifteen numbered rule files covering intake, timeline, fee agreement and invoice analysis, the ten reasonableness factors, communication, file and property, unearned fees, forum selection, letter drafting, escalation, Board complaints, dishonesty signals, and when to stop.
- Added eleven letter and submission templates, none of which quote rule text.
- Added the Tennessee reference layer: the professional conduct provisions that matter to a client, the six forums a Tennessee client can use, and a verification file recording the source and retrieval date of every legal claim.
- Added reader docs: start here, decision tree, anti-patterns, common outcomes, records retention, and an index.
- Added the CSV tracker, its column dictionary, TOML schemas, three worked examples with invented facts, an optional standard-library tracker validator, and thirteen tests covering it.
