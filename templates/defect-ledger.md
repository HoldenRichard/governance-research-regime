# Defect Ledger

One row per defect or near-miss, written the turn it is identified. Column definitions
and legal values are in CODEBOOK.md; the inclusion threshold and its worked examples are
in PROTOCOL.md §2.

Rows are appended in WRITE order, not event order — sort on `date` for event order.
Content cells are immutable once committed; corrections are made by superseding rows.
`remedy` is the one post-write-mutable column. Derived cells carry a trailing `†`.

A pipe inside a cell must be escaped as `\|` or it will split the row.

| id | date | logged | type | class | tier | rule | remedy | description | introduced by | introduced at | caught by | how caught | stage | knowledge needed to catch it | session | link | lane |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
