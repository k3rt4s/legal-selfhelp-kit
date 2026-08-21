# Example: a flat fee that grew

**Tennessee example.** This walkthrough uses Tennessee's own numbers, including the Davidson
County General Sessions limit. Those figures are specific to Tennessee. If you are in another
state, read this for the shape of the session, then check `references/state_XX.md` for your
own state's small claims limit and forum before you rely on any number here.

All facts invented.

## Stage 1, assemble

The client uploads an engagement letter dated 2026-01-14 stating a flat fee of $3,500 for representation in a contract dispute, three invoices totaling $7,900, and proof of payment of $5,000.

The model notes what is missing: no itemized detail behind any invoice, and no written amendment to the fee agreement.

## Stage 2, timeline and ledger

```text
2026-01-14 | Engagement letter signed, flat fee $3,500 | engagement_letter.pdf p1
2026-02-02 | Invoice 1, $3,500 | invoice_001.pdf
2026-03-06 | Invoice 2, $2,400, described as "additional litigation work" | invoice_002.pdf
2026-04-02 | Invoice 3, $2,000 | invoice_003.pdf
2026-04-15 | Client emails asking why the total exceeds the flat fee | email_2026-04-15.pdf
```

Ledger:

```text
Flat fee | quoted 3500 | billed 3500 | paid 3500 | disputed 0
Additional work | quoted none | billed 4400 | paid 1500 | disputed 4400 | no written change to the flat fee
```

## Stage 3, classify

One issue, bucket `money`. Rule touchpoint: 1.5(b), communicating the basis or rate and any change to it. Also RPC 1.5(a) factor 10, whether the fee agreement is in writing, since the additional work has no written agreement at all.

The model does not say the lawyer violated anything. It says the invoices charge work the written agreement does not cover, and that this is what factor 10 and paragraph (b) address.

## Stage 4, ask in writing

Sends `templates/01_itemized_bill_request.md`, asking for the itemization and any written amendment, with a fourteen-day deadline.

The firm responds with an itemization and no amendment.

## Stage 5, escalate

The client is in Davidson County, so the General Sessions limit is $15,000 and the disputed $4,400 fits. Nashville is not on the list of counties with a fee dispute committee, so the model routes to a written demand.

Sends `templates/04_demand_letter.md` demanding $4,400.

## Outcome

The firm offers $2,600. The client accepts. Total elapsed time, seven weeks, two letters.

## What made it work

A written flat fee, invoices that exceeded it, and no written amendment. The client asked in writing first and gave real deadlines. Nothing in either letter accused anyone of anything.
