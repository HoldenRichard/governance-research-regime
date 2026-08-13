# PROTOCOL

Executable steps. Written so a stranger can run this without contacting the author.

---

## 0. Setup, once

1. Create a record repository, separate from the codebase being studied. Copy
   `templates/` into its root. You now have `defect-log.md`, `attestation-register.md`,
   `session-logs/_template.md` and `session-logs/INDEX.md`.
2. Copy `scripts/integrity-check.py` and `.github/workflows/integrity.yml`. Push once
   and confirm the workflow runs and passes on an empty record. **Then deliberately
   break something — duplicate an id, delete a file an index row names — and confirm it
   fails.** A gate you have never watched fail is not a gate.
3. Write the standing instructions your agent reads (`CLAUDE.md`, `AGENTS.md`,
   `.cursorrules`, whatever your tooling uses). At minimum: draft the session log at
   session end and show it before writing; write a defect row the turn a defect is
   identified; update the attestation register in the same turn a declared promise
   changes.
4. Enable commit signing. Register the public key with your host so signatures verify
   for third parties, not just locally — an unverifiable signature is decorative.

---

## 1. Every session

A **session** is one directed unit of work: one substantive prompt and everything that
follows from it, including approval checkpoints. Bare "go" or "continue" turns are part
of the session, not new sessions.

**At session end, the agent drafts the log and shows it. The human corrects. Only then
is it written.** Show-before-write is not ceremony; it is the only point where a human
sees what is about to enter the permanent record.

Log verification-only sessions. Log sessions that produced nothing. Log sessions in
projects other than the primary one. A session that is deliberately not logged is
recorded as such in the index, never reconstructed later from memory.

Fill `Logged:` honestly — `same-turn`, or `+Nd` if the write lagged. Lag is data about
the protocol's own fidelity and hiding it corrupts the one field that measures whether
the protocol is being followed.

---

## 2. Every defect or near-miss

**Threshold.** A catch becomes a row when the issue, if merged, would have altered
runtime behaviour, persisted data, security posture, regulatory or app-store compliance
posture, or user-visible content. Style and formatting catches do not qualify.

**Two worked negatives**, so the threshold is usable rather than aspirational:

- *Not a row:* an agent proposes a variable name that violates house style; you correct
  it before the edit lands. Nothing about the shipped artifact would have differed in
  any of the five categories.
- *Not a row:* a doc comment describes a function's old signature. Stale, worth fixing,
  but no behaviour, data, posture or user-visible content changes if it ships.
  *(Judgement call: if the stale documentation is operationally load-bearing — a runbook
  step executed under time pressure — it can clear. Record the reasoning either way.)*

**Two worked positives:**

- *A row:* a proposed validation check would have rejected legitimate writes in
  production. Never shipped; near-miss; the catch is the datum.
- *A row:* a formal declaration to a platform describes data handling the binary does
  not perform. Nothing crashes; compliance posture is wrong.

Write the row **in the same turn the defect is identified**, not at session end.
Deferral produces a record of intent without a record of fact, and the debt compounds
silently.

**Every firing of a standing gate is itself a near-miss row**, with the actor recorded as
the tool.

---

## 3. Every declared promise

When a change touches a formal promise — privacy manifest, policy page, terms, age
rating, data-sharing declaration, store metadata — update the attestation register in the
same turn. When the platform acts (submission, rejection, approval, policy notice),
append to the gatekeeper log.

The register's value is that it names the **ground truth** each promise is checked
against, so the check is repeatable by someone else. "The privacy policy is accurate" is
not a row. "The privacy policy's data-collection paragraph, checked against every capture
site in the auth and upload paths" is.

---

## 4. Identifier discipline

Identifiers are claims on a sequence shared by more than one writer.

1. Drafts shown for approval use **placeholders**: `DEF-NNN`, `S-YYYY-MM-DD-N`, `ATT-NN`.
2. Real identifiers are read from the current head of the record **at the moment of
   writing**, never carried over from a draft.
3. Cross-references inside a draft use the same placeholders, resolved in the same pass.

An approval lag is not a neutral delay when more than one writer exists. Between draft
and write, another writer may consume every id yours claimed.

**Filenames are the same shared namespace and are not covered by any check here.** Two
writers can save different content to the same path; the second silently destroys the
first, and unstaged work has no recovery path. Coordinate paths out of band.

---

## 5. Write order

When a session produces multiple artifacts, write in this order:

**session log → index row → ledger rows → attestation register**

The log names the rows it will produce; the index makes the log joinable; the rows point
back at the session; the register cites the rows. Writing out of order produces
references to things that do not exist yet, and an interruption mid-sequence leaves the
record inconsistent in a way the gate can see. Run the gate before you start and after
you finish.

---

## 6. Immutability, and its one exception

Session logs and ledger content cells are **immutable once committed**. A record whose
value is that it was not tidied cannot be tidied.

Corrections are made by **superseding rows** — a new row stating the corrected reading
and naming what it corrects — or by **append-only index notes** where the erroneous
artifact is a log rather than a row.

The one mutable column is `remedy`, because it tracks a lifecycle rather than a fact
fixed at catch time. A remedy frozen at `open` makes the governance-conversion measure
permanently wrong. Any such change is dated and named in the session log that makes it.

A second narrow exception, adopted after a stale sentinel broke a join: `session` may
move from the sentinel `unlogged` to a real id **when the index already documents that
id**. The sentinel is metadata about the record's own coverage, not a fact about the
defect, and leaving a stale one makes the ledger contradict the index.

---

## 7. Pre-registration

Before running an analysis, write down what you expect and what result would prove you
wrong. Append it, dated, to a file that is never edited afterwards. Sign the commit.

A prediction with no operational definition cannot be scored, so name the measure, the
threshold and the date. "Verification will dominate" is not a prediction. "No defect
class covered by a machine-enforced gate will recur in the study window; one clean
recurrence falsifies it" is.

Deposit periodic immutable snapshots with a third-party archive. Append-only is a policy;
an external timestamp is a mechanism.

---

## 8. Honesty rules, binding

1. **Observational only.** Never alter an engineering decision to make the record look
   better, and never soften a defect entry because an agent wrote the code.
2. **Write `unknown` rather than guess**, on any field.
3. **Redact at write time**, never as later cleanup. Secrets by last four characters
   only; no third-party personal data in any artifact, ever.
4. **If overhead exceeds ten minutes per session, propose a trim** — never silently skip
   fields. A protocol nobody fills produces no data.
