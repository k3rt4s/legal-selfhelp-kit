# Security

The kit ships no telemetry and no code a reader has to run; the one script that touches the network is the maintainer's source checker, run by hand and never automatically.

Three optional standard-library scripts live under `scripts/`. One validates a local tracker CSV and one exports a chronology from it; neither opens a network connection. The third, `check_sources.py`, is for maintainers only: it fetches the URLs cited under `references/` to check that each page still carries the claim the kit attributes to it. That is the only network code in the repository, it writes its report outside the repository, and nothing runs it on a schedule.

## Nothing personal belongs here

This repository contains no real matter details, and none should ever be committed to it. Examples use invented facts. The `.gitignore` blocks a filled tracker and a `my_matter/` directory so an accidental commit is harder.

If you fork this to work on your own dispute, keep your documents outside the repository.

## Your own privacy

Uploading documents to a language model sends them to that provider. Before you do:

1. Understand that provider's data handling and retention.
2. Consider redacting account numbers, social security numbers, and details about third parties who are not part of your dispute.
3. Remember that your legal matter may carry confidentiality obligations of its own.

## Reporting a problem

Open a GitHub issue. If the problem is that a legal claim in the kit is wrong, that is a security issue in the sense that matters here, because someone may act on it. Say which file and which claim.
