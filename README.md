# legal-selfhelp-kit

An LLM-droppable instruction toolkit for a client in any of the fifty states or the District of Columbia handling a fee, communication, or file dispute with their own lawyer, covering which forum fits the problem and what to put in writing.

This kit is not legal advice and its author is not a lawyer. It helps you organize your own facts and draft your own correspondence. Read [docs/START_HERE.md](docs/START_HERE.md) first.

## Contents

<!-- BEGIN CONTENTS (auto-generated, do not edit by hand) -->

- [docs/](docs/README.md): Reader-facing guidance for a person handling their own dispute, covering where to start, how to choose a path, what goes wrong, and what to keep.
- [examples/](examples/README.md): Worked end-to-end walkthroughs showing how a session runs, using invented facts.
- [llm/](llm/README.md): Files loaded directly into a language model at the start of a session, defining how the model behaves, what it may assert, and what it must refuse.
- [references/](references/README.md): Primary-source material the kit cites when analyzing a legal bill or drafting a letter, with the retrieval date and a verification status for every citation.
- [rules/](rules/README.md): The operating manual the model follows, one numbered file per decision point, from intake through closing the matter.
- [schemas/](schemas/README.md): Field definitions for the structured records the model produces, so output stays consistent across sessions and across models.
- [scripts/](scripts/README.md): Optional helpers that run with the Python standard library and no installed packages, for anyone who prefers to check their tracker before a session.
- [templates/](templates/README.md): Ready-to-adapt letters and submissions, with every legal reference given by rule number rather than quoted text.
- [tests/](tests/README.md): Pytest suite covering the optional tracker validator, the source-health checker, and the structure of the reference layer itself, no network calls.
- [tracker/](tracker/README.md): The CSV you carry between sessions so a new conversation, on any model, can pick up where the last one stopped.
- [BUILD_PLAN.md](BUILD_PLAN.md): What is built, what is not, and what has to be true before anything ships.
- [CHANGELOG.md](CHANGELOG.md): All notable changes to legal-selfhelp-kit, in plain English.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): This project follows the Contributor Covenant 2.1, committing all community members to a harassment-free experience regardless of background.
- [CONTRIBUTING.md](CONTRIBUTING.md): How to contribute to legal-selfhelp-kit, which is open under MIT and where corrections are more valuable than additions.
- [FAQ.md](FAQ.md): Common questions about what this kit is, what it covers, and what it will not do.
- [FUTURE_FEATURES.md](FUTURE_FEATURES.md): Backlog of work not yet scheduled.
- [MAINTAINING.md](MAINTAINING.md): How the kit is kept current once its scope is complete, which is one bounded sweep on a schedule rather than an open-ended project.
- [requirements.txt](requirements.txt): Pinned runtime Python dependencies.
- [roadmap.json](roadmap.json): Machine-readable release history and what is planned next.
- [SECURITY.md](SECURITY.md): The kit ships no telemetry and no code a reader has to run; the one script that touches the network is the maintainer's source checker, run by hand and never automatically.
- [THEORY.md](THEORY.md): The working mental model for changing legal-selfhelp-kit, what a maintainer knows that the files do not say.
- [USER_STORIES.md](USER_STORIES.md): Who this serves and what each person needs.

<!-- END CONTENTS -->

## What this is

A pack of Markdown rules, TOML schemas, letter templates, and a CSV tracker that you load into a language model along with your own documents. The model helps you build a timeline, find what is actually disputable, choose the right forum, and draft correspondence you review and send yourself.

The repository holds no code you need to run. The optional scripts in `scripts/` check the format of your tracker file and export a chronology from it; the third is a maintainer's link checker you never need.

## Scope

All fifty states and the District of Columbia. The kit is built in two layers: a national baseline describing the ABA Model Rules, and one pack per state describing what that state actually did with them, plus its fee arbitration, disciplinary authority, client protection fund, small claims equivalent, and limitation periods. Load your own state pack and no other. The forums, dollar limits, deadlines, and program names in a pack are that state's and no one else's.

The kit covers disputes with your own lawyer: fees, billing, communication, getting your file back, and unearned advances. It does not cover suing a lawyer for malpractice, which needs real counsel and has deadlines.

## Quick start

1. Read [docs/START_HERE.md](docs/START_HERE.md).
2. Open a new session with a model that accepts file uploads.
3. Paste [llm/SYSTEM_PROMPT.md](llm/SYSTEM_PROMPT.md), then [llm/WORKFLOW.md](llm/WORKFLOW.md) and [llm/OUTPUT_CONTRACT.md](llm/OUTPUT_CONTRACT.md).
4. Paste [references/national_baseline.md](references/national_baseline.md), then your own state pack, `references/state_XX.md`, where `XX` is your two-letter state code.
5. Upload your fee agreement, invoices, proof of payment, and correspondence.
6. Ask it to run Stage 0.

Short on context? Use [llm/QUICKSTART.md](llm/QUICKSTART.md) instead.

## The citation standard

Every legal claim in this kit is listed in [references/VERIFICATION.md](references/VERIFICATION.md) with its source and retrieval date. Claims that could not be confirmed against a current official source are marked as such, and the kit is written so you never send quoted rule text on the strength of a secondary source.

If you find a claim here that is wrong or out of date, open an issue. Accuracy matters more than completeness in a kit people act on.

## Disclaimer

This is not legal advice. Using it does not create an attorney-client relationship with anyone. Nothing here is a prediction about your matter. Rules and dollar limits change, and only you can confirm the current state of the law before you act on it. When the stakes are meaningful, talk to a lawyer.

## License

MIT. See [LICENSE](LICENSE).
