# Example: a retainer that was never a cap

**Tennessee example.** This walkthrough uses only facts stated in `references/state_tn.md`.
Every other example in this folder ends with a claim the client can act on. This one does
not. It exists to show what the session says when the record does not support the
complaint.

All facts invented.

## Stage 1, assemble

The client, a fictional person named Marcus Whitfield, uploads an engagement letter dated
2026-01-08 for a Tennessee contract matter. It states an hourly rate of $275, and a $3,000
retainer described as "an advance deposit against fees, billed hourly and applied to each
invoice." Two invoices follow, each showing total hours and a dollar amount, but no
line-by-line breakdown of what the hours were spent on. The client also uploads an email he
sent asking why the second invoice was not simply covered by the retainer he already paid.

The model notes what is missing: the invoices give hours and totals but not the underlying
time entries, so the work behind each number cannot be checked yet.

## Stage 2, timeline and ledger

```text
2026-01-08 | Engagement letter signed, hourly rate $275, $3,000 retainer as deposit against fees | engagement_letter.pdf p1
2026-01-08 | Client pays retainer, $3,000 | payment_2026-01-08.pdf
2026-02-05 | Invoice 1, 10.5 hours, $2,887.50, applied against retainer | invoice_001.pdf
2026-03-06 | Invoice 2, 14.25 hours, $3,918.75, remaining retainer applied, balance due $3,806.25 | invoice_002.pdf
2026-03-10 | Client emails asking why the retainer did not cover the case | email_2026-03-10.pdf
```

Ledger:

```text
Retainer | quoted 3000 as deposit against fees | billed n/a | paid 3000 | applied in full across both invoices
Hourly fees | quoted rate 275/hr | billed 6806.25 (24.75 hrs) | paid 3000 via retainer | disputed 3806.25 | rate matches engagement letter, no undisclosed change
```

## Stage 3, classify

One issue, bucket `money`. Rule touchpoint: RPC 1.5(b), which requires the basis or rate of
the fee, and any later change to it, to be communicated to the client, preferably in
writing, before or within a reasonable time after the representation begins. Also
Tennessee's added factor 10, whether the fee agreement is in writing.

Here both point away from the client's complaint rather than toward it. The rate was
disclosed in writing at the start, at $275 an hour. The retainer was described in writing as
a deposit against that hourly rate, not a fixed price for the matter. Nothing in either
invoice shows a rate change, and the hours billed, 24.75 across two invoices, produce
exactly $6,806.25 at the disclosed rate. $3,000 of that was paid from the retainer. The
$3,806.25 balance is the arithmetic of the agreement, not a departure from it.

## Stage 4, what the record shows

The model tells Marcus plainly that the record does not support treating $3,000 as the
total cost of the matter. The engagement letter he signed calls the retainer a deposit
against hourly fees, not a cap, and he paid it as such. Reading a retainer as a ceiling on
what a lawyer can bill is a common and understandable misreading, especially when the same
word gets used loosely elsewhere, but this particular letter does not support that reading.

What would have supported his complaint: an engagement letter that called the $3,000 a flat
fee or a "not to exceed" amount instead of a deposit, a rate that changed from $275 without
a written notice under RPC 1.5(b), or invoices that did not match the disclosed rate when
the hours were multiplied out. None of those are present here.

What he can still legitimately ask for, without a demand letter: the underlying time entries
behind each invoice's hour total, since neither invoice itemizes what the hours were spent
on. He can send `templates/01_itemized_bill_request.md` for that detail alone, and he can
ask for a short conversation about how many hours the remaining work is likely to take,
so a third invoice is not another surprise. Neither of those is a dispute over what is
already billed.

## Outcome

Not stated, because this kit does not predict outcomes.

## What made it work

Correct classification at Stage 3, reading RPC 1.5(b) and factor 10 for what they actually
show here rather than assuming a fee complaint must have a fee problem behind it. The
session did not soften the answer or draft a demand letter to preserve the relationship. It
named the one real gap, the missing time entries, and separated that from the much larger
claim the client walked in with.
