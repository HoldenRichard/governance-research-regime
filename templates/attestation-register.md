# Attestation Register

One row per formal promise the product makes to a platform, regulator or user. Any change
touching a declared promise updates this file in the same turn; platform events append to
the gatekeeper log below.

Status values: `accurate` (verified, no known drift) · `drift-found` (divergence
identified, uncorrected) · `fixed` (drift corrected, cite the commit) ·
`declared-unverified` (promise made, never checked) · `retired` (surface no longer
exists — resolved by removal rather than repair).

State each promise as a checkable proposition, and name the ground truth specifically
enough that someone else could repeat the check.

| id | surface | the promise | declared where | ground truth | status | drift events | last verified (date · method) |
|---|---|---|---|---|---|---|---|

## Gatekeeper log (append-only)

One line per platform event — submission, rejection, approval, reviewer question, policy
notice — recording what the platform caught versus what this register already knew.
Record the register's state at the time of the event, before any response arrives, so a
prediction is never written after its outcome.

| date | event | what review caught | register state at that date |
|---|---|---|---|
