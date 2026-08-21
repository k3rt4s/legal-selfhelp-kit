# Changelog

All notable changes to legal-selfhelp-kit, in plain English.

## Unreleased (0.2.0, all fifty states)

Not shipped yet. This section describes what is on the `feature/all-fifty-states`
branch.

- Generalized the kit from Tennessee to every state. It now ships a national baseline built on the ABA Model Rules plus one pack per state, each following the same eight sections, with its own verification file.
- Added `references/national_baseline.md` and `references/state_template.md`, and turned `references/VERIFICATION.md` into the citation standard plus an index of every per-state verification file.
- Rewrote the forum selection rule, the decision tree and the templates to branch on the reader's state rather than assuming Tennessee's forums.
- Folded the three Tennessee reference files into `references/state_tn.md` and removed them. Tennessee readers lose nothing; the same claims are in the pack, with the same sourcing.

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
