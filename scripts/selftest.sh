#!/usr/bin/env bash
# Proves the integrity gate works, by building a throwaway record from the
# templates and watching the gate PASS on it, then FAIL on each violation it
# claims to catch, then pass again.
#
# This exists because the protocol's own rule is that a gate you have never
# watched fail is not a gate. This repository contains no record of its own, so
# CI cannot run the gate against real data — it runs this instead.
#
# Usage: bash scripts/selftest.sh   (from the repository root)
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/session-logs" "$WORK/scripts"
cp "$ROOT/templates/defect-ledger.md"        "$WORK/defect-log.md"
cp "$ROOT/templates/attestation-register.md" "$WORK/attestation-register.md"
cp "$ROOT/templates/INDEX.md"                "$WORK/session-logs/INDEX.md"
cp "$ROOT/scripts/integrity-check.py"        "$WORK/scripts/"
cd "$WORK"

ROW='| DEF-001 | 2026-01-01 | same-turn | defect | runtime | ex-ante-gate | none | open | a description | AI | unknown | agent | code read-through | shipped | what you had to know | S-2026-01-01-1 | link | execution |'
printf '# S-2026-01-01-1 — probe\n' > session-logs/2026-01-01-probe.md
printf '| S-2026-01-01-1 | 2026-01-01-probe.md | v2 |\n' >> session-logs/INDEX.md
printf '%s\n' "$ROW" >> defect-log.md
cp defect-log.md .clean-ledger; cp session-logs/INDEX.md .clean-index

fails=0
expect() { # expect <0|1> <label>
  python3 scripts/integrity-check.py >/dev/null 2>&1; rc=$?
  if [ "$rc" = "$1" ]; then printf '  ok    %s (exit %s)\n' "$2" "$rc"
  else printf '  FAIL  %s (expected exit %s, got %s)\n' "$2" "$1" "$rc"; fails=$((fails+1)); fi
}
restore() { cp .clean-ledger defect-log.md; cp .clean-index session-logs/INDEX.md; }

echo "integrity-check self-test"
expect 0 "clean record passes"

printf '%s\n' "$ROW" >> defect-log.md;                                    expect 1 "duplicate id"; restore
sed -i.bak 's/| defect | runtime |/| oopsie | runtime |/' defect-log.md;  expect 1 "out-of-vocabulary value"; restore
sed -i.bak 's/S-2026-01-01-1 | link/S-2099-01-01-9 | link/' defect-log.md; expect 1 "broken session join"; restore
sed -i.bak 's/| a description | AI |/| a | b | AI |/' defect-log.md;      expect 1 "unescaped pipe splits the row"; restore
printf '**Defect rows written:** DEF-NNN\n' >> session-logs/2026-01-01-probe.md
                                                                          expect 1 "placeholder in committed data"
sed -i.bak '/DEF-NNN/d' session-logs/2026-01-01-probe.md
mv session-logs/2026-01-01-probe.md held.md;                              expect 1 "index row names a missing file"
mv held.md session-logs/2026-01-01-probe.md
expect 0 "record recovers to clean"

echo
if [ "$fails" -eq 0 ]; then echo "self-test PASSED — every check fires and recovers"; exit 0
else echo "self-test FAILED — $fails case(s) did not behave as claimed"; exit 1; fi
