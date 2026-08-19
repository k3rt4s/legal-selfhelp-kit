# Start here

## What this is

A pack of instructions, rules, and letter templates you load into a language model along with your own documents. The model helps you organize a dispute with your own lawyer and draft correspondence. You review and send everything yourself.

It covers Tennessee. The forums, the dollar limits, and the programs named here are Tennessee-specific and do not transfer to other states.

## What this is not

1. Not legal advice, and not a substitute for a lawyer.
2. Not a way to get a lawyer disciplined on demand. Discipline is the Board's call and it is not a refund.
3. Not a guarantee of any outcome.
4. Not a source of current rule text. It tells you what the rules require and sends you to the official source to confirm before you quote anything.

## Before you start, know the difference between two goals

Getting your money back and getting the lawyer sanctioned are different goals, in different forums, on different timelines.

1. Money back: fee dispute committee, direct negotiation, or General Sessions court.
2. Conduct on the record: Board of Professional Responsibility.
3. Money gone because of dishonesty: Board complaint plus the Client Protection Fund.

People who chase both at once without separating them usually make both harder. Decide which one you actually want most, and say so out loud in your first session.

## The honest odds

A fee dispute where you were billed more than you were told, and you have the fee agreement and the invoices, is a reasonable case to press. Most resolve through a letter or a local fee dispute committee.

A complaint that amounts to "my lawyer was unresponsive and I lost my case" is much harder. Disappointing representation is not automatically a rules violation, and the Board is not a malpractice forum.

If your real claim is malpractice, meaning the lawyer's error caused you a quantifiable loss, this kit is not the right tool. That is a case you take to a malpractice lawyer, and there are deadlines.

## How to run a session

1. Open a new conversation with a model that accepts file uploads.
2. Paste `llm/SYSTEM_PROMPT.md`.
3. Paste `llm/WORKFLOW.md` and `llm/OUTPUT_CONTRACT.md`.
4. Paste `references/tennessee-professional-conduct.md` and `references/tennessee-remedies.md`.
5. Paste the rules files from `rules/` that apply to your stage.
6. Upload your documents.
7. Ask it to run Stage 0, then work through the stages.
8. At the end, save the session handoff block and the tracker.

If your model has a small context window, use `llm/QUICKSTART.md` instead.

## One rule that matters more than the rest

Put things in writing and keep proof you sent them. Almost every forum in this kit asks the same first question: did you ask the lawyer directly, and what happened. A clear written request with a date is the foundation of everything that follows.
