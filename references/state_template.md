# State pack template

The required shape of every `references/state_XX.md` file. Fifty packs follow it exactly, in
this order, with these headings, so that a reader, a template, and the LLM layer can rely on
finding the same thing in the same place in every state.

This file is a specification for contributors. It is not loaded into a session.

The worked model is [state_tn.md](state_tn.md). The national layer every pack sits on top of
is [national_baseline.md](national_baseline.md).

## The rule that governs this file

Every legal claim in a pack gets a row in that state's `references/verification_XX.md`,
naming its source and its retrieval date, added in the same commit as the claim. A claim
without a row is a defect.

If a claim cannot be sourced to a primary or official publication, it does not go in the
pack. It goes in the gap list at the bottom of the verification file instead, saying what was
looked for and where the search stopped. An omission a reader can see is safe. An invented
statute number or an invented filing deadline reads perfectly and can cost a real person
their claim.

Never quote long passages of rule text. Describe what the rule requires and cite it by
number. This is the same rule the templates follow, and for the same reason.

## Source ranking

Use the highest source available and say which one you used.

1. The state supreme court or judiciary site publishing the rules of professional conduct.
2. The state's own code or legislature site for statutes.
3. The state bar's own publication of the rules, a dated edition.
4. A dated publication of the regulator running the program, for example the disciplinary
   board or the client protection fund.
5. A dated bar association publication.

Never confirm anything against an undated source. Never confirm anything against a law firm
blog or a commercial summary. If a commercial mirror is the only thing that could be reached,
the claim is sourced but flagged, and the flag says so in the verification row.

## The eight required sections

Every pack carries all eight headings below, in this order, even when the answer for a state
is "none" or "not found." A missing heading is a defect. A heading that says the state has no
such program is correct and useful.

### Header block

Open with the state name, one sentence on who the pack is for, and the retrieval date for the
pack as a whole. Then a short list, three to five items, of what a reader in this state most
needs to know that a reader in another state does not. That list is the part people actually
read. Put the fee arbitration answer in it if the state has a statewide program.

### 1. Rules of professional conduct, numbering and adoption

How the state adopts its rules of professional conduct and how a client cites them. Cover:

- The adopting authority and the instrument, for example a supreme court rule number.
- The citation form a reader should use in a letter, for example "Rule 1.5" versus "RPC 1.5"
  versus a state-specific numbering scheme.
- The official publication point, with its URL.
- The effective date of the current version, and the date of the last amendment if published.
- Whether the state departed from model rule numbering in any way that would make a reader
  looking for 1.5, 1.4, 1.15, or 1.16 fail to find it.

### 2. Deviations from the model reasonableness factors

The most valuable section in the pack. The national baseline covers the eight model factors.
This section covers only what this state does differently.

- Any factor the state adds beyond the model list, given by number and described, not
  reproduced at length. Tennessee adds two: prior advertisements or statements about fees,
  and whether the fee agreement is in writing.
- Any model factor the state omits or materially rewords.
- Any state-specific writing requirement, for example a state that requires a written fee
  agreement above a dollar threshold or in particular matter types.
- Any state-specific contingent fee limit, for example a statutory percentage cap or a
  sliding scale in medical or personal injury matters.
- Any rule the state has that the model rules do not have at all and that bears on fees, for
  example a nonrefundable fee rule or a required fee agreement disclosure.

If the state tracks the model rule with no deviation, say that plainly and say what was
checked to establish it. "No deviation found" with a source is a real finding.

### 3. Attorney fee arbitration

This section changes the recommended path more than any other, so get it right.

- Whether the state runs a statewide program, a set of local programs, or nothing.
- The body that runs it and its URL.
- Whether participation is mandatory on the lawyer when the client requests it. Several
  states make it mandatory on the lawyer and voluntary for the client. That asymmetry is the
  single most useful fact in those states.
- Whether the award binds one side, both sides, or neither, and whether there is a right to a
  trial afterward.
- Any dollar ceiling or floor on what the program will hear.
- Any filing deadline or window, and whether it runs from the bill, the payment, or the end
  of the representation.
- Any fee to file.
- Whether the lawyer must notify the client of the right to arbitrate before suing for fees.
  In some states this notice is a precondition to the lawyer's own fee suit.
- If the state has only local programs, name the ones that could be confirmed and say plainly
  that the list may be incomplete.

### 4. Bar complaint process

- The disciplinary body's name, its URL, and how a client files.
- Whether the state separates an informal assistance or consumer-help track from a formal
  complaint, and what each one does. Where that split exists, say which one a billing
  disagreement belongs in, because filing a fee dispute as a formal complaint usually ends in
  a closed file rather than a refund.
- Whether the state has a client-assistance or consumer-assistance intake program that will
  contact the lawyer on the client's behalf.
- Any time limit on filing a complaint, or a confirmed statement that there is none.
- What the process will and will not produce. Discipline is not a refund, and every pack says
  so.
- Whether the state has a disciplinary restitution mechanism that can order money returned,
  which a minority of states do.

### 5. Client protection fund

- The fund's name, the body administering it, and its URL.
- What it covers, in the state's own terms, usually dishonest conduct rather than a fee
  dispute or malpractice.
- Its exclusions, stated explicitly. Fee disputes are excluded nearly everywhere.
- The per-claim cap and the aggregate per-lawyer cap, with figures, or a confirmed statement
  that no published maximum exists.
- Any requirement that a disciplinary complaint be on file first, and any deadline attached
  to that.
- Any deadline running from the loss itself, including any discovery rule.
- Whether awards are discretionary and whether they are paid in full or at a percentage.

### 6. Small claims or equivalent court

- The court's name in this state. It is not "small claims" everywhere.
- The jurisdictional dollar limit, with its statutory citation.
- Any county, parish, or district level variation in that limit, named.
- Whether lawyers may appear, and whether a corporate party needs one.
- Whether either side can remove the case or appeal to a trial de novo.
- The filing fee, or a pointer to where the reader confirms it.
- Any rule specific to suing a lawyer, or a confirmed statement that none was found.

### 7. Statutes of limitation

Two periods, both required, plus their modifiers.

- The contract limitation period, with its citation, and whether written and oral contracts
  differ. A fee agreement dispute is usually a contract claim.
- The legal malpractice limitation period, with its citation.
- Any discovery rule, described precisely: what starts the clock and what the client must
  have known.
- Any statute of repose, with its length and what, if anything, tolls it.
- Whether malpractice in this state sounds in tort, contract, or either at the plaintiff's
  election, because in some states that choice changes the period available.

Every figure in this section is a deadline. Nothing here ships without a verification row.

### 8. Private right of action for a rules violation

- Whether a violation of the rules of professional conduct creates a private cause of action
  in this state. In nearly every state it does not.
- Where the state's rules say so, usually in the scope or preamble section, cited by number.
- Whether a violation is nonetheless admissible as evidence of a standard of care in a
  malpractice case, which varies and matters.
- What the client's actual money route is instead: contract, fee arbitration, the protection
  fund, or fee forfeiture where the state recognizes it.

### Closing block

Close with a short "confirm before you rely on this" note naming the two or three sources a
reader in this state should check for themselves, and a pointer to
`references/verification_XX.md`.

## What does not go in a pack

1. Malpractice strategy. The kit does not cover suing a lawyer for malpractice. The
   limitation periods are in the pack so a reader knows a clock exists and can get counsel in
   time, not so they can run the claim themselves.
2. Any prediction about what a remedy typically recovers. There is no verified dataset behind
   such a number.
3. Any dollar figure, phone number, deadline, or program name that is not in the verification
   file.
4. Quoted rule text of any length beyond a short phrase needed to make a point.
5. Anything from a real matter. Every pack is built from published law only.

## The companion verification file

Each pack ships with `references/verification_XX.md` in the same commit. It carries:

1. A confirmed table: the claim, the source, the retrieval date, and a note.
2. A flagged table: claims that are sourced but rest on something less than a primary or
   official publication, with the reason.
3. A gap list: what was looked for, could not be sourced, and was therefore cut from the
   pack, with where the search stopped.

The gap list is not a failure log. It is the most trustworthy part of the file, because it
tells a reader exactly where the pack stops knowing things.
