# Example: no fee arbitration program in Alabama

**Alabama example.** This walkthrough assumes an Alabama client and uses only facts stated in
`references/state_al.md`. It exists to show a state where the fee arbitration route is closed
before it starts, not a state where the routing merely differs. If you are in another state,
check `references/state_XX.md` section 3 before assuming a program exists where you are, or
that none does.

All facts invented.

## Stage 1, assemble

The client, a fictional person named Denise Okafor, uploads an engagement letter dated
2026-01-15 with a Huntsville, Alabama firm, Vance and Whitlow LLC, stating a flat fee of
$2,500 for a contract dispute matter. A later invoice adds $1,200 for "case management," never
covered by a written change to the fee agreement and never separately discussed with the
client before it was billed.

The model notes what is missing: no written amendment to the fee agreement, and nothing in the
file showing the client agreed to the additional charge before it was billed.

## Stage 2, timeline and ledger

```text
2026-01-15 | Engagement letter signed, flat fee $2,500 | engagement_letter.pdf p1
2026-02-20 | Invoice 1, $2,500, paid in full | invoice_001.pdf, payment_2026-02-20.pdf
2026-03-30 | Invoice 2, $1,200, described as "case management" | invoice_002.pdf
```

Ledger:

```text
Flat fee       | quoted 2500 | billed 2500 | paid 2500 | disputed 0
Case management | quoted none | billed 1200 | paid 0    | disputed 1200 | no written change, no shown consent
```

## Stage 3, classify

One issue, bucket `money`. Rule touchpoint: Alabama Rule of Professional Conduct 1.5(a).
Alabama's ninth factor, at Rule 1.5(a)(9), asks whether there is a written fee agreement signed
by the client. There is one for the $2,500 flat fee. There is none for the $1,200 add-on.

The model does not say the lawyer violated anything. It says the additional billing has no
written basis, and that this is exactly what Alabama's added ninth factor is built to catch.

## Stage 4, check section 3, find no program

The model checks `references/state_al.md` section 3 before recommending anything. Alabama runs
no statewide fee arbitration or mediation program. The Alabama State Bar's own complaint
brochure lists resolving a disputed attorney fee among the things its complaint process does
not handle. Two county bar associations, Birmingham and Mobile, run their own free, binding fee
committees, but Vance and Whitlow LLC is in Huntsville, in neither county. So for this client,
no arbitration forum exists at all, statewide or local.

This is the point where a reader following the two-letters pattern from other states would
stop and ask what replaces the missing step. Nothing replaces it. The written demand simply
carries more weight than it would in a state with a program, because it is the only formal
record the client will have before going to court.

## Stage 5, routing decision

Per `rules/10_forum_selection.md`, a bill dispute with no fee arbitration program routes to a
written demand, then the small claims equivalent named in section 6. The model also checks
whether anything here looks like misconduct rather than a fee disagreement, because Alabama's
bar complaint process is closed for a pure fee dispute but stays open for things like failing
to communicate or failing to return a file or unearned money. Nothing in this file shows that.
It is a billing disagreement, so the bar complaint route stays closed and the model does not
recommend it.

## Stage 6, what gets written

The model drafts the demand letter using template `04_demand_letter.md`, citing Rule 1.5(a) and
the missing written basis for the $1,200 charge, and naming the forum for the next step: the
Small Claims Division of the district court, Madison County, under Ala. Code Section 12-12-31.
The $1,200 in dispute is well inside that court's $6,000 jurisdictional limit, so small claims
stays available if the letter goes nowhere.

Template `07_fee_dispute_submission.md` is not used. Its own first line tells the reader to stop
if their state pack says there is no program, and Alabama's does.

## Stage 7, what happens next

The letter goes out by certified mail, giving the firm fourteen days to respond or refund. If
nothing comes back, the client's next document is a small claims filing in Madison County
district court for the $1,200, not a second letter and not a bar complaint.

## Outcome

Not stated, because this kit does not predict outcomes.

## What made it work

Checking section 3 before drafting anything, instead of assuming a program exists because two
other examples in this kit use one. Recognizing that a closed arbitration route does not close
the bar complaint route for everything, only for a pure fee dispute, and keeping those two
questions separate at Stage 5. Ending on the forum that was actually open, the demand letter and
small claims, rather than writing toward a program that would never answer.
