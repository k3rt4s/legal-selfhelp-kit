# Example: a retainer with no work performed

All facts invented.

## The problem

The client paid a $6,000 advance in November for an immigration matter. By March, nothing had been filed, no documents had been requested, and the lawyer had stopped responding.

## Stage 0, safety check

The model flags this immediately. An advance paid, no work performed, and no communication is not an ordinary fee dispute. It tells the client so before analysis begins.

## Stage 3, classify

Two issues.

```text
I-01 | property | $6,000 advance unaccounted for | payment_receipt.pdf | RPC 1.15 client funds, RPC 1.16(d) refund of unearned advance | Board
I-02 | communication | no response since 2026-01-08 | email log | RPC 1.4 | CAP
```

## Stage 4, ask in writing

Sends `templates/02_unearned_fee_refund.md` requesting an accounting and a refund, with a fourteen-day deadline. No response.

## Stage 5, escalate

This is the branch where the routing matters. The model does not send the client to a fee dispute committee, because there is no fee dispute. There is an advance and no work.

It routes to a Board complaint using `templates/05_board_complaint_narrative.md`, and points to the Client Protection Fund section in `references/tennessee-remedies.md`, noting that the Fund covers unearned fees where there was a pattern of behavior evidencing no good faith intention to perform, that it does not cover fee disputes, and that awards are discretionary and paid at a percentage.

It also tells the client plainly that $6,000 with an unresponsive lawyer is worth a consultation with a real lawyer.

## Outcome

Not stated, because this kit does not predict outcomes.

## What made it work

Correct classification at Stage 3. Every step after that followed from recognizing this was not a billing disagreement.
