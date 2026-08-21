# Example: fee arbitration comes first in Maine

**Maine example.** This walkthrough assumes a Maine client and uses only facts stated in
`references/state_me.md`. It exists to show a state where the routing itself changes, not
just the names. If you are in another state, check `references/state_XX.md` section 3 before
assuming arbitration is available to you or that it works the same way.

All facts invented.

## Stage 1, assemble

The client, a fictional person named Rowan Cadigan, uploads an engagement letter dated
2026-02-03 for a Maine matter, stating a flat fee of $4,000. Two invoices follow totaling
$5,600, with $1,600 of that described only as "additional work," never covered by a written
change to the fee agreement, and never separately discussed with the client before it was
billed.

The model notes what is missing: no written amendment to the fee agreement, and nothing in
the file showing the client gave informed consent to the additional charge before it was
billed.

## Stage 2, timeline and ledger

```text
2026-02-03 | Engagement letter signed, flat fee $4,000 | engagement_letter.pdf p1
2026-03-10 | Invoice 1, $4,000 | invoice_001.pdf
2026-04-18 | Invoice 2, $1,600, described as "additional work" | invoice_002.pdf
2026-04-25 | Client pays $4,000 against the flat fee, disputes the $1,600 | payment_2026-04-25.pdf
```

Ledger:

```text
Flat fee | quoted 4000 | billed 4000 | paid 4000 | disputed 0
Additional work | quoted none | billed 1600 | paid 0 | disputed 1600 | no written change, no informed consent shown
```

## Stage 3, classify

One issue, bucket `money`. Rule touchpoint: Maine Rule of Professional Conduct 1.5(a). Maine's
list runs to eleven factors, not the model's eight, and two of the three Maine adds bear
directly here: whether the client gave informed consent to the fee arrangement, and whether
the fee agreement is in writing. Neither is shown for the $1,600 charge.

The model does not say the lawyer violated anything. It says the additional billing has no
written basis and no shown consent, and that this is exactly what Maine's own added factors
address.

## Stage 4, file for fee arbitration

This is the branch where Maine's routing differs from Tennessee's. Under MRPC Rule 1.5(g), a
Maine lawyer must submit to fee arbitration if the client requests it. That makes arbitration
the first real move here, not a last resort after a demand letter goes unanswered.

The model tells the client plainly what filing means: the Fee Arbitration Commission process
requires the client, in the petition itself, to agree to be bound by the panel's decision.
There is no filing fee and no dollar floor or ceiling in the rule that runs the program. The
filing deadline runs from the bill or the payment, not from the end of the representation, and
is generous, six years from whichever came first.

The client files a petition with the Fee Arbitration Commission describing the $1,600 dispute,
attaching the engagement letter, both invoices, and the payment record. No demand letter goes
out first, because the arbitration filing is itself the request the lawyer cannot decline.

## Stage 5, outcome path

Because filing binds the client to the panel's decision, the model flags this before the
client submits: there is no separate right to a trial afterward if the client is unhappy with
the result. The client confirms this is acceptable given the size of the dispute.

## Outcome

Not stated, because this kit does not predict outcomes.

## What made it work

Correct classification at Stage 3, using the factors Maine actually added rather than
Tennessee's. Recognizing at Stage 4 that Maine's arbitration duty runs to the lawyer, not the
client, and that this reorders the whole sequence: arbitration first, because it can be
requested rather than merely offered.
