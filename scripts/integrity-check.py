#!/usr/bin/env python3
"""Integrity gate for a governance-research record.

Enforces the structural invariants the protocol depends on: unique and unbroken
identifier sequences, a working join between session logs and ledger rows,
controlled vocabularies, no draft placeholders reaching committed data, and no
prose pointers naming a session log that does not exist.

Usage:  python3 scripts/integrity-check.py   (from the record repository root)
Exit 0 pass, 1 fail.

Two design decisions worth keeping if you adapt this:

  1. A passing verdict NAMES THE INPUTS IT READ. A gate reporting PASS over an
     empty or silently truncated input set manufactures exactly the confidence
     it exists to earn. Counts are printed on every run so a shrinking corpus
     becomes visible rather than reassuring.

  2. Known exceptions are EXEMPTED BY IDENTIFIER WITH A WRITTEN REASON rather
     than by relaxing a rule for everyone. The exemption tables below ship
     EMPTY. Populate them from a calibration run over your own corpus, and put
     the reason in the value — an exemption without a reason is a weakened rule
     wearing a disguise.

Every check here should be proven by mutation before you trust it: introduce the
violation on a scratch copy, watch the non-zero exit, remove it. A gate you have
never watched fail is not a gate.
"""
import os, re, sys

LEDGER, INDEX, LOGDIR = "defect-log.md", "session-logs/INDEX.md", "session-logs"
REGISTER = "attestation-register.md"
NCOLS = 18
COLS = {"logged": 2, "type": 3, "class": 4, "tier": 5,
        "remedy": 7, "caught by": 11, "how caught": 12, "stage": 13, "lane": 17}
VOCAB = {
    "logged":    {"retro", "same-turn", "same-day"},          # plus +Nd
    "type":      {"defect", "near-miss"},
    "class":     {"runtime", "data", "security", "compliance",
                  "content", "evolvability", "process"},
    "tier":      {"ex-ante-gate", "directed-investigation", "human-only", "none"},
    "remedy":    {"open", "point-fix", "rule", "gate", "rule+gate",
                  "none", "unknown"},
    "caught by": {"human", "agent", "human+agent", "tool", "unknown"},
    # Values may be joined with ' + ' and may carry a trailing note, either
    # parenthesised or bare, so the vocabulary value is a PREFIX of the cell
    # rather than the whole of it.
    "how caught": {"build", "unit-suite", "machine-script check",
                   "code read-through", "simulator drive", "device pass",
                   "console-server check", "shipped-to-user", "human-read",
                   "trace-the-premise", "external-source check", "unknown"},
    "stage":     {"pre-edit", "pre-commit", "pre-merge",
                  "post-merge-unshipped", "shipped", "unknown"},
    # A row carries its own lane. It is NOT derivable from the session join: a
    # session in one lane routinely records another lane's errors, so the join
    # gives the SESSION's lane rather than the ROW's.
    "lane":      {"execution", "planning", "content"},
}
PLACEHOLDERS = ("DEF-NNN", "S-YYYY-MM-DD-N", "ATT-NN")

# ---- exemption tables, intentionally empty -------------------------------
# Populate as {identifier: "why this exception is legitimate"}. Content cells
# are immutable, so a genuine known-and-ruled exception is recorded here and
# stays auditable, rather than the rule being softened for every row.
DATE_SESSION_EXEMPT = {}   # {"DEF-NNN": "session genuinely crossed midnight; ..."}
HOWCAUGHT_EXEMPT = {}      # {"DEF-NNN": "legacy free-text cell, immutable; ..."}
POINTER_EXEMPT = {}        # {("<file>.md", "see the YYYY-MM-DD log"): "reason"}

errors, inputs = [], []

def cells(line):
    """Split a markdown table row on UNESCAPED pipes.

    `\\|` is a literal pipe in GFM and does not end a cell. Splitting on raw
    '|' mis-parses any row quoting piped output or shell syntax.
    """
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]

def split_plus(s):
    """Split a `how caught` cell on ' + ' at PAREN DEPTH ZERO only.

    Notes routinely contain their own ' + ', and a naive split cuts them in half
    and then reports the halves as unknown values.
    """
    parts, depth, cur, i = [], 0, "", 0
    while i < len(s):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth = max(0, depth - 1)
        if depth == 0 and s[i:i + 3] == " + ":
            parts.append(cur); cur, i = "", i + 3; continue
        cur += s[i]; i += 1
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]

def starts_with_value(part, vocab):
    """A part is legal if it IS a vocabulary value or begins with one.

    Longest-first, so a value that prefixes another cannot mask it.
    """
    if part in vocab:
        return True
    return any(part.startswith(v + " ") or part.startswith(v + "(")
               for v in sorted(vocab, key=len, reverse=True))

# ---- ledger -------------------------------------------------------------
# Collect EVERY table line, not just those matching a DEF- prefix. A row that
# fails the prefix would otherwise be invisible to every check below, and the
# gate would report PASS over a silently shrunken corpus.
if not os.path.exists(LEDGER):
    print(f"{LEDGER} not found — run from the record repository root."); sys.exit(1)

raw = [l for l in open(LEDGER).read().split("\n")
       if l.lstrip().startswith("|") and set(l) - set("|- \t")]
rows = [l for l in raw if not l.lstrip().startswith("| id ")]
inputs.append(f"{LEDGER}: {len(rows)} table rows (excluding header/separator)")

for l in rows:
    first = cells(l)[0]
    if not re.fullmatch(r"DEF-\d{3,}", first):
        errors.append(f"{LEDGER}: table row whose first cell is '{first[:40]}' "
                      "is not a DEF id — a malformed row must not be skipped")

seen, nums = set(), []
for line in rows:
    c = cells(line)
    rid = c[0]
    if len(c) != NCOLS:
        errors.append(f"{rid}: {len(c)} columns, expected {NCOLS} "
                      "(an unescaped '|' in a cell will do this)")
        continue
    if rid in seen:
        errors.append(f"{rid}: duplicate id")
    seen.add(rid)
    m = re.fullmatch(r"DEF-(\d{3,})", rid)
    if not m:
        errors.append(f"{rid}: malformed id, expected DEF-NNN")
        continue
    nums.append(int(m.group(1)))
    for name, i in COLS.items():
        v = c[i].replace("†", "").strip()
        if name == "logged" and re.fullmatch(r"\+\d+d", v):
            continue
        if name == "how caught":
            if rid in HOWCAUGHT_EXEMPT:
                continue
            bad = [p for p in split_plus(v) if not starts_with_value(p, VOCAB[name])]
            if bad:
                errors.append(f"{rid}: {name}={bad!r} not in the controlled vocabulary")
            continue
        if v not in VOCAB[name]:
            errors.append(f"{rid}: {name}='{v}' not in the controlled vocabulary")

if nums:
    gaps = sorted(set(range(min(nums), max(nums) + 1)) - set(nums))
    if gaps:
        errors.append(f"{LEDGER}: gaps in the DEF sequence: "
                      + ", ".join(f"DEF-{n:03d}" for n in gaps))
    if nums != sorted(nums):
        errors.append(f"{LEDGER}: ids are not ascending — rows are appended in "
                      "write order, so this means a row was inserted")

# ---- index --------------------------------------------------------------
irows = [l for l in open(INDEX).read().split("\n")
         if re.match(r"\| S-\d{4}-\d{2}-\d{2}-\d+ ", l)] if os.path.exists(INDEX) else []
inputs.append(f"{INDEX}: {len(irows)} rows")

sids, listed = set(), set()
for line in irows:
    c = cells(line)
    sid, fname = c[0], c[1]
    if sid in sids:
        errors.append(f"{sid}: duplicate session id in INDEX")
    sids.add(sid); listed.add(fname)
    if not os.path.exists(os.path.join(LOGDIR, fname)):
        errors.append(f"{sid}: INDEX names '{fname}', which does not exist")

onfs = ({f for f in os.listdir(LOGDIR) if re.match(r"20\d\d-\d\d-\d\d-.*\.md$", f)}
        if os.path.isdir(LOGDIR) else set())
inputs.append(f"{LOGDIR}/: {len(onfs)} session-log files")
for f in sorted(onfs - listed):
    errors.append(f"{f}: session log with no INDEX row")

# ---- ledger -> index join ----------------------------------------------
for line in rows:
    c = cells(line)
    if len(c) != NCOLS:
        continue
    v = c[15].replace("†", "").strip()
    if v not in sids and v not in ("retro-seed", "unlogged"):
        errors.append(f"{c[0]}: session='{v}' is not an INDEX id "
                      "(nor retro-seed/unlogged)")

# ---- row date vs the date embedded in its session id --------------------
# A session crossing midnight can legitimately produce a row dated the following
# day, so a real mismatch is exempted by id with a reason rather than by
# weakening the rule.
checked = 0
for line in rows:
    c = cells(line)
    if len(c) != NCOLS:
        continue
    sv = c[15].replace("†", "").strip()
    m = re.fullmatch(r"S-(\d{4}-\d{2}-\d{2})-\d+", sv)
    if not m:                      # retro-seed / unlogged sentinels
        continue
    checked += 1
    if c[1].strip() != m.group(1) and c[0] not in DATE_SESSION_EXEMPT:
        errors.append(f"{c[0]}: date='{c[1].strip()}' disagrees with session "
                      f"'{sv}' — a row's date is its IDENTIFICATION date; exempt "
                      "it by id with a reason if the session crossed midnight")
inputs.append(f"date/session agreement: {checked} rows compared, "
              f"{len(DATE_SESSION_EXEMPT)} exempted")

# ---- prose pointers naming a session log that does not exist ------------
# Matches POINTER SYNTAX ("see/in/per/from the <date> <desc>"), not mere
# date-adjacency: a log that DESCRIBES a dangling pointer is not itself one, and
# adjacency matching flags every such description. Searched over
# whitespace-normalised text because logs are hard-wrapped and a pointer can
# straddle a line break.
DESC = r"(catch-up|catchup|log|session|pass|entry|turn)"
ptr = re.compile(r"\b(?:see|in|per|from)\s+the\s+(20\d\d-\d\d-\d\d)\s+" + DESC + r"\b", re.I)
names = sorted(onfs)
for f in names:
    txt = re.sub(r"\s+", " ", open(os.path.join(LOGDIR, f)).read())
    for mm in ptr.finditer(txt):
        date = mm.group(1)
        desc = mm.group(2).lower().replace("catchup", "catch-up")
        if any(nm.startswith(date) and desc in nm for nm in names):
            continue
        if (f, mm.group(0)) in POINTER_EXEMPT:
            continue
        errors.append(f"{f}: '{mm.group(0)}' names a session log that does not "
                      "exist — session logs are immutable, so the fix is a "
                      "pointer in the index, not an edit")
inputs.append(f"dangling-pointer scan: {len(names)} session logs, "
              f"{len(POINTER_EXEMPT)} exempted")

# ---- placeholders in committed data ------------------------------------
data = [p for p in [LEDGER, REGISTER] if os.path.exists(p)] + [
    os.path.join(LOGDIR, f) for f in sorted(onfs)]
inputs.append(f"placeholder scan: {len(data)} data files "
              "(templates are excluded by design)")
for path in data:
    for n, line in enumerate(open(path).read().split("\n"), 1):
        for p in PLACEHOLDERS:
            if p in line:
                errors.append(f"{path}:{n}: placeholder '{p}' reached a committed "
                              "data file — ids are assigned at write time")

# ---- verdict ------------------------------------------------------------
print("inputs read:")
for i in inputs:
    print(f"  - {i}")
if errors:
    print(f"\nFAIL — {len(errors)} problem(s):")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
print("\nPASS — all checks clean over the inputs named above.")
