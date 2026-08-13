# RATIONALE

Every rule in this protocol was written in response to a specific failure. This file
records the **failure classes** — the mechanism, stated generally enough to be useful to
someone whose specifics will differ. No incident detail from the originating study
appears here.

A protocol whose rules arrive without reasons is a checklist, and checklists get skipped
under pressure. The reasons are what make a rule survive the day you do not want to
follow it.

---

## On identifiers

**An approval lag is not a neutral delay in a multi-writer record.** Identifiers assigned
when a draft is written are claims on a shared sequence. Between drafting and approval,
another writer can consume every one of them. The draft still looks correct — the ids are
well-formed, sequential, and plausible — and writing it produces duplicates in a record
built for public release.

*Rule:* placeholders in drafts; real ids read from head at write time; cross-references
resolved in the same pass.

**A malformed row can be invisible to every check that would catch it.** If a validator
selects rows by prefix match, a row whose prefix is subtly wrong is not checked — it is
excluded from the input set. The validator then reports a clean pass over a silently
shrunken corpus.

*Rule:* read every table row, and fail on any that does not parse, rather than filtering
to the ones that do.

**Filenames are a shared namespace exactly like identifiers, and no check here covers
them.** Two agents can write different content to the same path; the second save
destroys the first with no error, and unstaged work has no recovery path at all. This is
an unsolved gap in the protocol, recorded rather than papered over.

---

## On gates and their verdicts

**A gate that has never been watched to fail is not evidence.** A check that is
misconfigured, unregistered, or pointed at the wrong input passes silently and
indistinguishably from a check that is working. Silent success is the failure mode that
costs the most, because it manufactures confidence.

*Rule:* every check is proven by mutation — introduce the violation, watch the non-zero
exit, remove it — before it is trusted. Record the demonstration.

**A passing verdict must name the inputs it read.** A gate reporting PASS over an empty
or truncated input set produces exactly the confidence it exists to earn. If the corpus
shrinks, a pass should become suspicious, and it cannot unless the counts are printed.

*Rule:* print what was examined alongside the verdict, always.

**A gate's first verdict is a hypothesis about the data, not a fact about it.** A tool
disagreeing with committed data is at least as likely to be wrong as the data. Acting on
a first failure — especially by editing the data — inverts the burden of proof.

*Rule:* when a new check fails, verify the check before believing it. Assert that an edit
script's target exists before it edits, so a wrong assumption produces an error rather
than a silent no-op.

**A check keyed on proximity rather than on the thing it detects will flag every
discussion of the defect it detects.** A detector that fires on any mention of its
subject makes documenting that subject cost an exemption every time, and that friction
turns into deferral.

*Rule:* match the *syntax* of the thing being detected, not its vicinity. Where genuine
exceptions exist, exempt them by identifier with a written reason rather than weakening
the rule for everyone.

**An empty result is the same shape whether the data is absent, the query is wrong, or
access is denied.** On a deadline, an empty result reads as catastrophe and gets escalated.

*Rule:* run a positive control on a known-populated input before believing any empty.

**An exit code describes the last command in a chain, not the work.** A pipeline ending
in a formatter reports success over any failure upstream.

*Rule:* verify the artifact, not the exit status. The only evidence a build happened is
the build.

---

## On the record itself

**A debt restated in every close-out still reads as compliance to both parties.**
Acknowledging owed rows repeatedly produces a record of intent without a record of fact,
and it is a worse failure mode than forgetting, because everyone believes it is handled.

*Rule:* write the row in the turn the defect is identified. Only the write discharges it.

**A row's date and session belong to the moment of identification, not of writing.**
Rows written in one batch about different days will inherit a single session id unless
this is explicit, which credits catches to sessions incapable of making them and corrupts
any latency measure.

*Rule:* date and session are the identification moment. Where a batch write spans days,
each row carries its own.

**No check can catch a semantically wrong join.** When every cell is individually
well-formed, in-vocabulary and mutually consistent, only the mapping to reality is wrong.
A script claiming to cover this would manufacture confidence.

*Rule:* this one is a review convention, explicitly not enforced — *"was this identified
in the session it names?"* — and it is documented as unenforced so nobody assumes
coverage.

**Prose cross-references are load-bearing claims with no referential integrity.** A
sentence pointing at a document by date and description is followed by readers and
checked by nothing.

*Rule:* scan for pointer syntax that resolves to no file. Where the artifact holding the
error is immutable, put the correction where readers actually land.

**Line-number references break most reliably when you improve the file they point into.**

*Rule:* treat anchors as pointers requiring maintenance, or avoid them.

**A sentinel value is a claim about the record's own coverage, and it goes stale
silently.** A cell meaning "we have not recorded this yet" becomes false the moment it is
recorded, and an immutability rule that freezes sentinels ships a knowingly broken join.

*Rule:* sentinels are resolvable to real values when the record already documents them.
Content cells are not.

---

## On verification

**A not-found is a claim needing the same evidence as a found, and it degrades faster.**
Each restatement strips the hedge. By the third hand, an absence observed once is a fact
being acted upon.

*Rule:* trace a premise in shipped code before acting on it, including — especially —
when the premise is that something does not exist.

**A brief's stated blocker is a hypothesis with a citation attached.** Documentation
describes the system as it was understood when written.

*Rule:* verify the environment before designing against it; verify a claim before filing
it as a permanent record.

**A correction is a change and needs its own verification pass.** Re-reading only the
fields you believed were wrong misses the ones the fix touched, and sweeping removals
overshoot more often than targeted ones.

**Instrumenting a build can replace the build under test.** "I ran it to get logs"
silently changes what the logs describe.

**An explained failure mode recurs until the workflow changes**, not merely until it is
understood.

---

## On the human in the loop

**The agent drafts the record and the human corrects it.** This is a genuine conflict —
the system under study keeps the notes — and no instrument available at this scale
removes it.

*Rule:* disclose it, and instrument it with a verbatim corrections field, so how much
correction the record receives is itself measurable. Do not call agent-produced counters
"objective."

**The drafting agent has usually read the study's own thesis**, because it is in the
standing instructions. An agent that knows which variable is measured, asked at session
end to count that variable, has an obvious gradient.

*Rule:* declare it. Where possible, re-derive a sample of counters from session
transcripts and report the discrepancy as a measurement-error estimate.

**A rule locked mid-stream needs a full baseline sweep, not a touched-region scan.**
Edited-region checks never revisit legacy text, so violations predating the rule persist
indefinitely.

**Documentation decays toward pessimism.** It describes the tooling that existed when it
was written, and nothing prompts a re-read when the tooling improves. Readers pay in
time.
