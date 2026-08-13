# governance-research-regime

**A logging protocol for developers who ship code they did not write.**

When an AI agent authors most of a codebase, the developer who publishes it still
carries every obligation that authorship used to imply — the App Store declarations, the
privacy manifest, the terms of service, the answer to "does this do what you say it
does." Reading every diff is no longer how that obligation gets met. This is a protocol
for meeting it a different way: standing rules born from caught defects, machine-checkable
gates that do not depend on anyone paying attention, and a record structured well enough
that the whole chain can be audited afterwards by someone who was not there.

It is a *research instrument* first. It produces a dataset designed to answer questions
about where verification effort actually goes, which failures are catchable by cheap
automation and which are not, and what a person has to already know in order to catch a
machine's mistake. It happens to also be a workable engineering discipline, which is why
it survives contact with real deadlines.

**This repository contains the protocol and no data.** Templates are blank, the
integrity gate ships with empty exemption tables, and no defect, session, or attestation
record appears anywhere in it. See [LIMITATIONS.md](LIMITATIONS.md) before adopting
anything here.

---

## Provenance

Developed and run continuously since July 2026 by a single operator on one production
iOS application. It is still running. The dataset it produces is held privately for the
duration of the study window and is intended for separate release afterwards, under its
own identifier.

The protocol has never been executed by anyone other than its author. That is the
central limitation and it is stated in full in [LIMITATIONS.md](LIMITATIONS.md), not
buried.

---

## The four artifacts

| artifact | what it holds | cadence |
|---|---|---|
| **Session log** | one file per directed working session: what was attempted, what changed, what was verified and by whom | every session, ~2–3 min |
| **Defect ledger** | one row per defect or near-miss, 18 columns, written the turn it is identified | on identification, ~90 s |
| **Attestation register** | one row per formal promise the product makes to a platform, regulator or user, tracked against ground truth | when a promise or its ground truth moves |
| **Session index** | the join between logs and rows, plus append-only notes recording anything the schema cannot express | with each log |

A fifth artifact is not a file: **standing rules**, written into whatever configuration
your agent actually reads, each one born from a specific caught defect, and each one
backed by a machine check wherever a machine check is possible.

---

## The five ideas that make it work

**1. A defect is only a row if it would have mattered.** The threshold is explicit: a
catch becomes a row when the issue, if merged, would have altered runtime behaviour,
persisted data, security posture, regulatory or app-store compliance posture, or
user-visible content. Style and formatting catches do not qualify. Without a threshold
the ledger fills with noise and stops being queryable.

**2. Near-misses are data, not luck.** Roughly half the value of the record is in
defects that never shipped, because those are the ones that tell you which check caught
what. A ledger of shipped bugs measures your failures; a ledger that includes near-misses
measures your *instruments*.

**3. Every firing of a gate is itself a row.** When a standing check blocks something,
that is evidence the governance works, recorded at the moment it works. Systems that only
log failures cannot demonstrate their own value.

**4. Rules are born from incidents, and gates enforce rules.** A rule with no
precipitating defect is speculation. A rule with no machine check behind it is a wish.
The record links incident → rule → gate → subsequent non-recurrence, which is the only
form of evidence that governance is doing anything.

**5. The record is written by the agent and corrected by the human, and that is
disclosed.** The agent drafts every log and row; the human reviews and corrects before
anything is written. This is a real conflict of interest — the system under study is
also the system keeping the notes — and the protocol instruments it (a verbatim
corrections field) rather than pretending it away.

---

## Repository contents

```
PROTOCOL.md      what gets logged, when, by whom, in what order
CODEBOOK.md      operational definition of every column and every legal value
RATIONALE.md     why each rule exists, stated as the failure class it prevents
LIMITATIONS.md   what this is not, and what would have to be true for it to be more
templates/       blank session log, ledger header, attestation register, index
scripts/         the integrity gate
.github/         the enforcement wiring
```

---

## Adopting it

Start with [PROTOCOL.md](PROTOCOL.md). Copy `templates/` into a repository that is *not*
the repository being studied — the record should be independently publishable, and
keeping it separate stops it from being edited to match the code. Wire
`scripts/integrity-check.py` into CI on day one, before there is anything for it to
check; a gate added later is a gate that has never been watched to fail.

Expect the first two weeks to produce schema changes. That is normal and the protocol is
designed for it: change the schema early, record the change, never rewrite past rows.

---

## Licence

Prose and templates: [CC-BY-4.0](LICENSE-docs). Code in `scripts/` and `.github/`:
[MIT](LICENSE). Attribution appreciated but the point is that you run it, not that you
credit it.
