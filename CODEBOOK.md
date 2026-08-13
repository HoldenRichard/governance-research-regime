# CODEBOOK

Operational definitions for every coded field. A second coder should be able to produce
the same values from the same evidence using only this file.

Where a column is free prose, that is stated — those columns are *not* codeable and no
claim should rest on aggregating them.

---

## Defect ledger — 18 columns

| # | column | type | definition |
|---|---|---|---|
| 1 | `id` | `DEF-NNN` | Assigned in file order at write time, monotonically. Never reused, never renumbered. |
| 2 | `date` | ISO date | The date the defect was **identified**, not the date the row was written and not the date the defect was introduced. |
| 3 | `logged` | enum | `retro` \| `same-turn` \| `same-day` \| `+Nd`. Gap between identification and the row being written. Measures the protocol's own fidelity. |
| 4 | `type` | enum | `defect` \| `near-miss`. A near-miss was caught before it could take effect. |
| 5 | `class` | enum | `runtime` \| `data` \| `security` \| `compliance` \| `content` \| `evolvability` \| `process`. What kind of harm was at stake. |
| 6 | `tier` | enum | **The check-constructibility axis.** See below. |
| 7 | `rule` | free / `none` | The standing rule or gate created in response, by name. |
| 8 | `remedy` | enum | `open` \| `point-fix` \| `rule` \| `gate` \| `rule+gate` \| `none` \| `unknown`. The only post-write-mutable column. |
| 9 | `description` | prose | What was wrong and how it was found. Not codeable. |
| 10 | `introduced by` | enum | `AI` \| `human` \| `mixed` \| `external` \| `unknown`. Who authored the defective artifact. Never softened. |
| 11 | `introduced at` | commit / date / `unknown` | When it entered. With `date`, gives detection latency. |
| 12 | `caught by` | enum | `human` \| `agent` \| `human+agent` \| `tool` \| `unknown`. Who or what made the catch. |
| 13 | `how caught` | controlled + note | The method. See vocabulary below. |
| 14 | `stage` | enum | `pre-edit` \| `pre-commit` \| `pre-merge` \| `post-merge-unshipped` \| `shipped`. How far it got. |
| 15 | `knowledge needed to catch it` | prose | **The distinctive field.** What a person had to already know. Not codeable; read as cases. |
| 16 | `session` | id / sentinel | Join key. A session id, or `retro-seed`, or `unlogged`. |
| 17 | `link` | free | Commit, file path, or a statement that no artifact changed. |
| 18 | `lane` | enum | Which lane made the error. A row carries its own lane; it is **not** derivable from the session join, because a session in one lane routinely records another lane's errors. |

### `tier` — the check-constructibility axis

The most analytically load-bearing field. It records **what kind of check could have
caught this**, which is a claim about the defect's nature rather than about what happened
to be run.

- **`ex-ante-gate`** — a cheap deterministic check existed or could trivially have
  existed: a grep, a byte-diff, a test count, an identity comparison. Catchable
  automatically and repeatedly, at negligible cost.
- **`directed-investigation`** — no cheap check reaches it; it requires someone to go
  looking, with a hypothesis. Cross-file invariants, declaration-versus-behaviour drift,
  compliance tracing. Expensive, schedulable, and invisible to routine work.
- **`human-only`** — not constructible as a check at all, because it needs a sensor,
  a credential, an external account, or a judgement no script can hold. Device runs,
  console captures, platform decisions.
- **`none`** — no check was possible or relevant.

Code this from the defect's *nature*, not from what was actually run. If a grep would
have caught it and nobody ran one, it is still `ex-ante-gate`.

### `how caught` — controlled vocabulary

`build` · `unit-suite` · `machine-script check` · `code read-through` · `simulator drive`
· `device pass` · `console-server check` · `shipped-to-user` · `human-read` ·
`trace-the-premise` · `external-source check` · `unknown`

Values may be joined with ` + ` and may carry a trailing note, parenthesised or bare.
The gate splits on ` + ` at paren depth zero and accepts a value as a prefix, because
notes routinely contain their own separators.

Two of these need definition because they are not obvious:

- **`trace-the-premise`** — locating a claim in shipped code before acting on it. Used
  when the catch *is* the discovery that a stated premise was false. Distinct from
  `code read-through`, which is reading code to understand it rather than to test an
  assertion about it.
- **`external-source check`** — verification against a source outside the repositories:
  vendor documentation, a platform's live console, a licensing term.

`unknown` is legal and required by honesty rule 2 whenever the method is not recoverable.

---

## Session log fields

| field | definition |
|---|---|
| `Session ID` | `S-YYYY-MM-DD-n`, `n` ordinal within the day **by write order**, not by clock order. |
| `Lane` | Which lane ran the session. Absence means the default lane. |
| `Window` | Agent-observed clock times. `unknown` if not captured — do not reconstruct. |
| `Commits` | Count and range, in the repository being studied. `none` is a real value. |
| `Logged` | `same-turn` or `+Nd`. Same definition as the ledger column. |
| `Decisions changed` | One entry per decision that **moved** during the session: what was decided, what changed it, and the reasoning that moved it. The reasoning is the record. Entered even when the original decision was reasonable on the information available — especially then. |
| `Defect rows written` | The ids produced. Must match the ledger exactly; the gate checks nothing here, so it is a review obligation. |
| `Rules/gates created` | Name plus `born from DEF-NNN`, or `speculative` if no precipitating incident. Speculative rules are legitimate and worth marking, because whether provenance predicts effectiveness is an open question. |
| `Attestation surfaces touched` | `ATT-NN: what changed`, or `none`. |
| `Verification lines` | One per distinct check: **value — actor — note**. The actor is separate from the method, because who verified is a different variable from how. |
| `Human corrections to this draft` | Verbatim. `none` is a real and expected answer. This is the instrument for the recursion problem: it measures how much the human corrects the agent's account of events. |

---

## Attestation register

| column | definition |
|---|---|
| `id` | `ATT-NN`, stable. |
| `surface` | The artifact carrying the promise. |
| `the promise` | Stated as a checkable proposition, not a topic. |
| `declared where` | Where a reader or regulator encounters it. |
| `ground truth` | **What it is checked against.** Name specific code paths or authorities so the check is repeatable by someone else. |
| `status` | `accurate` \| `drift-found` \| `fixed` \| `declared-unverified` \| `retired`. |
| `drift events` | Dated, citing the defect rows. Append-only. |
| `last verified` | Date **and method**. A date alone is not evidence. |

`declared-unverified` is the honest starting state for a promise made but never checked
— distinct from `accurate`, which asserts a check happened.

`retired` means the surface no longer exists: the promise was resolved by **removal**
rather than repair. Distinguish it from `fixed`, or you lose the difference between
"we corrected the claim" and "we stopped making the claim."

---

## Coding conventions

**Derived cells carry a dagger (`†`).** Any value filled retrospectively during a schema
migration is marked, filled only where the row's own existing text already states the
fact, and left `unknown` otherwise. No new judgement about a past defect is formed during
a migration.

**One event, one row.** Two defects in one commit are two rows. One defect found twice
is one row plus, if the second finding corrects the first, a superseding row.

**When two codings are defensible, record the reasoning in the description** and pick the
one that is falsifiable later.
