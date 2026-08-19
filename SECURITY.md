# Security

The kit ships no network code, no telemetry, and no executable content beyond one optional standard-library script that reads a local CSV.

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
