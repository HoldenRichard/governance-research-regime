# LIMITATIONS

What this protocol is not, stated first rather than buried.

---

## It has been run by one person, on one project

A protocol whose only application is by its author is a personal habit with a README.
That is the honest description of this repository's evidential status today.

- **One operator.** No second person has executed it.
- **One primary project.** A single production iOS application, plus incidental use on
  adjacent work.
- **No inter-rater agreement.** The coding scheme in [CODEBOOK.md](CODEBOOK.md) has never
  been applied by an independent coder. Nobody knows whether two people reading the same
  session would produce the same row.
- **The author is subject, instrument and analyst simultaneously.**

The standard rubric applied to artifact contributions in software engineering research
names "evaluation relying solely on the author's own opinion" as an antipattern. This
repository currently sits inside that antipattern, and no amount of internal rigour
moves it out. What would: a second coder's kappa on an existing corpus, and a second site
running the protocol independently.

---

## The record is kept by the system under study

The agent that writes the code also drafts the session log, writes the defect row,
records who caught what, and assigns provenance to its own output. The human corrects
before anything is written, and the protocol instruments that correction — but disclosure
is not independence.

Concretely: any counter produced this way is a self-report by the measured system, and
the drafting agent has usually read the study's own aims because they sit in its standing
instructions. Treat agent-produced counts as evidence *about* the agent's account, not as
objective measurement. The only partial mitigation available at this scale is
re-deriving a sample from session transcripts and reporting the discrepancy.

---

## Selection is structural, not incidental

The record fires when the agent is present. Work done without it is invisible unless
deliberately logged, which means the corpus over-represents agent-assisted work by
construction. Any rate is a rate *within* logged sessions and cannot be generalised to
the developer's whole practice, let alone anyone else's.

Retrospectively seeded rows — those reconstructed at the start rather than logged live —
are systematically biased toward defects that were caught *and* documented. Keep them
marked and quarantined; they cannot support claims about detection.

---

## What the schema cannot see

- **Semantically wrong joins.** Every cell can be well-formed, in-vocabulary and mutually
  consistent while the mapping to reality is wrong. This is deliberately not checked; a
  script claiming to cover it would manufacture confidence.
- **Same-filename collisions.** Identifier discipline governs ids and says nothing about
  paths. Two writers can destroy each other's uncommitted work silently, with no error
  and no recovery.
- **Whether a rule caused a non-recurrence.** The record can show a covered class did not
  recur; it cannot show exposure to the triggering condition. Absence of recurrence is
  weak evidence when you do not know the class was retested.
- **Anything below the threshold.** The inclusion rule admits only functionality-affecting
  issues, which excludes essentially the whole maintainability class. Published review
  studies find that class to be the majority of what review catches, so **no
  functional-versus-maintainability distribution comparison should be drawn from a ledger
  kept this way.** The difference would be manufactured by the inclusion rule.

---

## Overhead is real and the budget is a constraint, not a target

Roughly two to three minutes per session, ninety seconds per defect row, and the
attestation register only when a promise moves. That is achievable and has held.

It holds because fields were cut aggressively. Earlier versions carried
minute-level effort splits, self-assessed comprehension flags and per-proposal ratings;
they were removed after producing values that turned out to measure something other than
what they named. **A protocol nobody fills produces no data, and a field that quietly
measures the wrong construct is worse than no field.** Resist additions.

---

## It was rebuilt once, after its original framing failed

An earlier version of this regime served a different research question and collected
fields suited to it. An adversarial review found that its primary measured variable was
recording two incompatible constructs, that several planned analyses rested on fields with
no variance, and that its central claim had been published elsewhere at larger scale.

The instrument was rebuilt around what the record could actually support. Fields that
served the dead framing were removed rather than carried forward, and the failure is part
of the record rather than edited out of it.

The general lesson, offered to anyone adopting this: **run an adversarial review of your
own design before the corpus is large enough for schema changes to be expensive.** The
window in which changing the shape of your data is nearly free is measured in weeks.

---

## What would make this stronger

In rough order of value per hour:

1. **A second coder.** One other person, the codebook alone, re-coding an existing corpus
   blind, with agreement reported and disagreements listed. Hours of work; changes the
   evidential category.
2. **A second site.** The protocol run by someone else, on their own project. This is the
   thing that turns a habit into a method, and it is outside the author's control.
3. **Transcript re-derivation.** Sampled counters recomputed from session transcripts to
   estimate measurement error on the self-reported ones.
4. **External timestamping.** Immutable third-party snapshots, so append-only stops being
   a claim only the author can verify.
5. **Machine-readable export.** The record is markdown tables; escaped separators inside
   cells mis-parse under naive splitting. A properly quoted export should be the
   machine-readable artifact of record.

---

## Scope of any claim made from a record kept this way

No causal claim. No generalisation to other developers, projects or tools. No rate that
implies a population.

What a record like this *can* support: worked examples at full documentation depth, a
mechanism catalogue, and a defensible account of where a particular practice's
verification effort went and what it caught — offered as an exemplar, not as a sample.
