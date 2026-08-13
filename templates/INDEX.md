# Session Index

Session ids are `S-YYYY-MM-DD-n`, `n` ordinal within the calendar day by WRITE order.
This file is the join between session logs and ledger rows.

It is also where anything the schema cannot express is recorded. Session logs are
immutable once committed, so corrections to a log live here as append-only notes — a
note superseding an earlier note rather than editing it. Sessions deliberately not
logged are recorded here as `unlogged`, never reconstructed.

| id | file | format |
|---|---|---|
