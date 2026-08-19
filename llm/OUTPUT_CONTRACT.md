# Output contract

Produce these shapes exactly, so a later session with a different model can pick up where this one stopped.

## Timeline entry

```text
DATE | EVENT | SOURCE
2026-03-04 | Engagement letter signed, flat fee stated as $3,500 | engagement_letter.pdf p1
```

Unknown date is `????-??-??`. Never guess a date.

## Ledger line

```text
ITEM | QUOTED | BILLED | PAID | DISPUTED | BASIS
Trial preparation | not quoted | $4,200 | $4,200 | $4,200 | no written change to the flat fee, RPC 1.5(b) communication
```

## Issue record

```text
ID: I-03
BUCKET: money | communication | property | conduct
SUMMARY: one sentence, factual
EVIDENCE: file and page or email date, for each supporting fact
RPC TOUCHPOINT: rule number and what it requires, never quoted text
FORUM: the forum from tennessee-remedies.md
STATUS: open | asked | escalated | resolved | dropped
NEXT ACTION: one concrete step with a date
```

## Draft letter

Always output as a complete letter ready to review, never a fragment. Include:

1. Date, sender block, recipient block.
2. A subject line naming the matter.
3. What is being requested, numbered.
4. A response date.
5. A closing that keeps the door open.

Never include a rule quotation. Reference rules by number and requirement only.

## Session handoff

End every session with this block so the next one can resume:

```text
MATTER: short name
STAGE: 0-6
OPEN ISSUES: I-01, I-03
SENT: what went out, when, how
AWAITING: what, from whom, by when
NEXT: the single next action
UNKNOWNS: what is still missing
```
