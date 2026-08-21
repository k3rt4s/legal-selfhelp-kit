# Index

Every file, and when to use it.

## Read first

| File                    | When                                              |
| ----------------------- | ------------------------------------------------- |
| `docs/START_HERE.md`    | Before anything else                              |
| `docs/DECISION_TREE.md` | When you know your facts and need the right forum |

## Load into the model

| File                     | When                                       |
| ------------------------ | ------------------------------------------ |
| `llm/SYSTEM_PROMPT.md`   | Every session, first                       |
| `llm/WORKFLOW.md`        | Every full session                         |
| `llm/OUTPUT_CONTRACT.md` | Every full session                         |
| `llm/QUICKSTART.md`      | Small-context model, or one quick question |

## Law and forums

`references/` holds a national baseline, one pack per state, a verification file per pack, a
citation standard, and the required shape of a pack.

| File                              | When                                                                                         |
| --------------------------------- | -------------------------------------------------------------------------------------------- |
| `references/national_baseline.md` | Any question about the model rules every state built from                                    |
| `references/state_XX.md`          | Any question about what the lawyer owed you, or where to take the problem, in your own state |
| `references/verification_XX.md`   | Before relying on or quoting a specific claim in your state pack                             |
| `references/VERIFICATION.md`      | The citation standard, and the index of every pack                                           |
| `references/state_template.md`    | The required shape of a pack, if you are contributing one                                    |

## Tactics

| File                      | When                            |
| ------------------------- | ------------------------------- |
| `rules/`                  | Stage by stage during a session |
| `docs/ANTI_PATTERNS.md`   | Before you send anything        |
| `docs/COMMON_OUTCOMES.md` | When setting your expectations  |

## Doing

| File                        | When                              |
| --------------------------- | --------------------------------- |
| `templates/`                | Drafting correspondence           |
| `tracker/`                  | After every action                |
| `docs/RECORDS_RETENTION.md` | From day one                      |
| `examples/`                 | To see a full run before your own |
