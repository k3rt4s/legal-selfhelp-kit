# legal-selfhelp-kit

An LLM-droppable instruction toolkit for a Tennessee client handling a fee, communication, or file dispute with their own lawyer, covering which forum fits the problem and what to put in writing.

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
- [tests/](tests/README.md): Pytest suite covering the optional tracker validator against conforming and non-conforming fixtures.
- [tracker/](tracker/README.md): The CSV you carry between sessions so a new conversation, on any model, can pick up where the last one stopped.
- [BUILD_PLAN.md](BUILD_PLAN.md): What is built, what is not, and the order the rest arrives in.
- [CHANGELOG.md](CHANGELOG.md): All notable changes to the kit, in plain English.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): The Contributor Covenant 2.1 applies to everyone participating in this project.
- [CONTRIBUTING.md](CONTRIBUTING.md): How to contribute, and the citation standard every legal claim must meet.
- [FAQ.md](FAQ.md): Answers to the questions people ask before they start.
- [FUTURE_FEATURES.md](FUTURE_FEATURES.md): Backlog of work not yet scheduled.
- [SECURITY.md](SECURITY.md): The kit ships no network code, and nothing personal belongs in this repository.
- [USER_STORIES.md](USER_STORIES.md): Who this serves and what outcome each person needs.

<!-- END CONTENTS -->

## What this is

A pack of Markdown rules, TOML schemas, letter templates, and a CSV tracker that you load into a language model along with your own documents. The model helps you build a timeline, find what is actually disputable, choose the right forum, and draft correspondence you review and send yourself.

The repository holds no code you need to run. The optional script in `scripts/` only checks the format of your tracker file.

## Scope

Tennessee. The forums, dollar limits, and programs named here are Tennessee-specific. The general approach transfers to other states. The specifics do not.

The kit covers disputes with your own lawyer: fees, billing, communication, getting your file back, and unearned advances. It does not cover suing a lawyer for malpractice, which needs real counsel and has deadlines.

## Quick start

1. Read [docs/START_HERE.md](docs/START_HERE.md).
2. Open a new session with a model that accepts file uploads.
3. Paste [llm/SYSTEM_PROMPT.md](llm/SYSTEM_PROMPT.md), then [llm/WORKFLOW.md](llm/WORKFLOW.md) and [llm/OUTPUT_CONTRACT.md](llm/OUTPUT_CONTRACT.md).
4. Paste both files in [references/](references/README.md).
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
