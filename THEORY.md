# Theory

The working mental model for changing legal-selfhelp-kit, what a maintainer knows that the files do not say.

## Invariants

- Every legal claim has a row in that state's `references/verification_XX.md` naming its source, URL, and retrieval date, added in the same commit as the claim. A claim without a row is a defect. An unverifiable claim is cut and the gap recorded in that file's gap list.
- A cited URL lands on the page holding the claim. A front page is correct only for a claim about the organization itself, or when the text lives nowhere deeper. The allowed cases are listed by name in `tests/test_reference_layer.py` with a reason each, and a test fails when one stops matching. Do not add one without reading why the existing ones are there.
- Templates never quote rule text. They cite rule numbers and describe what the rule requires.
- No deadline is asserted anywhere that is not in a verification file.
- Nothing from any real matter enters the repo. Examples use invented facts only.
- Drafting and verification are separate hands. Whoever wrote a claim does not verify it.
- Voice: short sentences, plain language, no em dashes, no hype. The section sign stays; spelling it out reads worse.
- Generated output never lands in the repository. `scripts/check_sources.py` writes to the OS temp directory because a contributor's machine has no data root.

## Load-bearing constraints

- An HTTP 200 with a healthy byte count proves nothing. Sites in this corpus return 200 with an error body (courts.wa.gov, caselaw.findlaw.com), 404 with a 222 KB page (njcourts.gov), 202 with an empty body to automated retrieval (courtlistener.com), and 200 with well-formed HTML that is all navigation because the text is rendered client-side (cobar.org, coloradolegalregulation.com). The only check that counts is finding the claim's words in the fetched body, and for a PDF, that the content type was actually application/pdf.
- A page being official, on the right domain, and thin is not evidence it supports the claim. The real source is sometimes a brochure PDF elsewhere on the same domain.
- A pack section can carry an inline URL, pass the presence test, and still link the wrong law. The prose and the verification row can both be right while the link a reader clicks is wrong. The URL has to point at the thing its sentence is about.
- CourtListener's search API confirms a case exists and is cited correctly; its opinion text needs credentials. Case metadata can be confirmed, holdings usually cannot, which is why several malpractice-accrual rows are flagged rather than confirmed.
- tncourts.gov and njcourts.gov do not serve rule text to automated retrieval. New Jersey's contingent-fee scale is confirmed against a Wayback capture of the Judiciary's earlier domain, and both the pack and the row say which year's wording was confirmed.
- The checker's parser skips a few dozen rows out of about two thousand, never more than a handful in one file; the current baseline is in `MAINTAINING.md`. If a report's UNPARSEABLE_ROW count moves far from it, the parser broke, not the corpus, and the summary above it is meaningless. A clean-looking summary has sat on top of thirty-three silently skipped rows before.
- The checker never claim-checks a redirected page, so REDIRECTED means unchecked, not fine. Redirects from leg.mt.gov to mca.legmt.gov and from vermontjudiciary.org to vtcourts.gov are official domain moves.
- When your own fetch contradicts a verified row, re-run the extraction a second way before calling the row wrong. A greedy HTML strip once deleted the body of a page whose claims were there the whole time.

## Decisions that look wrong

- Georgia's verification file has a separate URL column. The parser reads it, a test locks that in, and normalizing it would be churn.
- West Virginia's complaint packet is described by the buttons on wvodc.org rather than linked, because the files sit on Google Drive and a marketing CDN whose paths rotate. The row keeps the fetched URLs as provenance.
- Two North Carolina rows cite a secondary source and are labelled SUPERSEDED with the statute confirmation directly above them. A banned-source scan fires on them; that is expected.
- Two bylines, Martin A. Cole and Glendon Laird, appear in Source columns as authors of cited articles. Normal citation practice; a privacy sweep should not remove them.
- `scripts/validate_tracker.py` contains a pound sign and a euro sign on purpose: it checks whether a currency symbol was typed into the amount field.
- The checker has no private-address blocklist. It is a maintainer-run local tool over URLs a maintainer reviews; add one if it is ever wired into automation.
- 0.1.0 and 0.2.0 were never tagged. The CHANGELOG is the record of what shipped when.
- Per-county fee dispute detail is not compiled, by decision. `docs/FIND_YOUR_LOCAL_PROGRAM.md` teaches the search instead.

## Known soft spots

- Two Massachusetts client-protection figures, the fund's cumulative payout and the number of clients reimbursed, exist only on the fund's front page and change without notice. Recheck them on every sweep; do not cite them harder.
- Abel v. Austin (Kentucky, KRS 413.245) is flagged because no official source serves the opinion. The pack does not rely on it.
- Many cited sources are PDFs the checker cannot read. PDF_UNCHECKED means unchecked, not wrong.
