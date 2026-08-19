# Tracker columns

| Column              | Meaning                                                                     |
| ------------------- | --------------------------------------------------------------------------- |
| `issue_id`          | Stable identifier, `I-01`, `I-02`. Never reuse one                          |
| `bucket`            | `money`, `communication`, `property`, or `conduct`                          |
| `summary`           | One factual sentence. No adjectives                                         |
| `evidence`          | File and page, or email date, for each supporting fact                      |
| `rpc_touchpoint`    | Rule number and what it requires, in your own words. Never quoted rule text |
| `forum`             | Where this issue is headed, from `references/tennessee-remedies.md`         |
| `status`            | `open`, `asked`, `escalated`, `resolved`, or `dropped`                      |
| `action_taken`      | What you actually did                                                       |
| `action_date`       | ISO date, `YYYY-MM-DD`                                                      |
| `sent_method`       | How it went out, and how delivery is proven                                 |
| `response_due`      | The date you asked for a response by                                        |
| `response_received` | Date a response arrived, blank if none                                      |
| `amount_disputed`   | Number only, no currency symbol. Blank for non-money issues                 |
| `notes`             | Anything else. Keep it factual                                              |

Rules:

1. One row per issue, not per letter. Update the row as the issue moves.
2. Dates are ISO format so they sort correctly.
3. A blank is honest. A guess is not.
4. Run `scripts/validate_tracker.py` against your file before a session if you want to catch format problems early.
