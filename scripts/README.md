# Scripts

Optional helpers that run with the Python standard library and no installed packages, for anyone who prefers to check their tracker before a session.

The kit works without these. Nothing here is required.

## Contents

- [validate_tracker.py](validate_tracker.py): Checks a tracker CSV against the schema and prints every problem it finds.
- [export_chronology.py](export_chronology.py): Reads a filled-in tracker CSV and writes a plain-text chronology, one line for each row's `action_date` plus a second line where the row records a `response_received` date, sorted by date, in a format you can paste into a bar complaint or fee arbitration submission. It validates the tracker first and refuses to export if `validate_tracker.py` would report problems. Rows with a missing or unparseable `action_date` are not dropped; they are listed in a trailing section instead. Run it with `python scripts/export_chronology.py path/to/your/tracker.csv` and redirect the output to a file if you want to save it.
