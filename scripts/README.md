# Scripts

Optional helpers that run with the Python standard library and no installed packages, for anyone who prefers to check their tracker before a session.

The kit works without these. Nothing here is required.

They are tested on Python 3.13. Older interpreters may well work, since the scripts use nothing beyond the standard library and ordinary syntax, but no older version is tested and none is promised.

## Contents

- [validate_tracker.py](validate_tracker.py): Checks a tracker CSV against the schema and prints every problem it finds.
- [export_chronology.py](export_chronology.py): Reads a filled-in tracker CSV and writes a plain-text chronology, one line for each row's `action_date` plus a second line where the row records a `response_received` date, sorted by date, in a format you can paste into a bar complaint or fee arbitration submission. It validates the tracker first and refuses to export if `validate_tracker.py` would report problems. Rows with a missing or unparseable `action_date` are not dropped; they are listed in a trailing section instead. Run it with `python scripts/export_chronology.py path/to/your/tracker.csv` and redirect the output to a file if you want to save it.
- [check_sources.py](check_sources.py): A maintenance tool, not part of the kit itself. Fetches every cited URL under `references/`, checks the page actually still supports the row's claim (not just that it returned a status code), and writes a triage report grouped by outcome (OK, NO_CLAIM_TEXT, LIKELY_CLIENT_RENDERED, BLOCKED, REDIRECTED, HTTP_ERROR, UNREACHABLE, PDF_UNCHECKED, UNPARSEABLE_ROW). Fetches politely, with a delay between requests. Run it with `python scripts/check_sources.py --state ak --limit 10` to check one small pack, or with no flags to check everything; pass `--out` to choose where the report goes.
