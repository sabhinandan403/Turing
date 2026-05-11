# Full Validation Check Instructions

Use this workflow when the user asks for a full validation check.

## Scope

- Validate `Validation/validate-prompt.md` end to end.
- Review all four sections in that file:
  - User Prompt
  - SQL
  - Metadata
  - Schema JSON
- Do not use `test.sql` unless the user explicitly asks to validate it.
- Do not modify files during the check unless the user explicitly asks for fixes.

## Full Validation Checklist

### 1. Prompt Validation

Evaluate:

1. Natural Business Language
2. No SQL Keywords / SQL-in-Words
3. No Schema / Column Leakage
4. Output Control
5. Deterministic Prompt Ordering
6. Internal Coherence
7. Prompt-SQL Alignment

### 2. Metadata Validation

Check that the SQL matches metadata expectations:

- `number_of_joins`
- `schema_length_bucket`
- `columns_per_table_bucket`
- `clause_complexity`
- `table_and_column_naming_convention`

### 3. Schema JSON Validation

Check:

- Every table in schema JSON is referenced by the SQL.
- Every fully qualified column in schema JSON is used in the SQL.
- The SQL does not use extra tables not listed in schema JSON.
- The SQL does not use extra fully qualified columns not listed in schema JSON.
- Per-table column counts satisfy the bucket requirement.

### 4. SQL Validation

Check:

- SQL parses logically and is structurally complete.
- SQL ordering is deterministic when the result is row-based.
- SQL output is controlled through aggregation, thresholds, or explicit fetch/limit.
- SQL logic matches the prompt.
- SQL is executable in the local Oracle environment when feasible.
- SQL does not return 0 rows when non-empty output is expected.

## Execution Rules

- If local Oracle execution is possible, run the SQL from `Validation/validate-prompt.md`.
- If execution fails, report the exact Oracle error and the likely cause.
- If execution succeeds but returns 0 rows, report that as a failure.
- If the SQL in the file differs from `test.sql`, ignore `test.sql` unless the user explicitly asks to validate it.

## Output Format

Return results in these sections.

### Prompt Validation

Use this table:

| Prompt Check | Status | Reason |
|---|---|---|

Include rows for:

- Natural Business Language
- No SQL Keywords / SQL-in-Words
- No Schema / Column Leakage
- Output Control
- Deterministic Prompt Ordering
- Internal Coherence
- Prompt-SQL Alignment

Then include:

`Overall Prompt Status: PASS` or `Overall Prompt Status: FAIL`

### Full Validation Summary

Use this table:

| Check Area | Status | Reason |
|---|---|---|

Recommended rows:

- Metadata Alignment
- Schema JSON 1:1 Mapping
- Join Count Match
- Table Bucket Match
- Column Bucket Match
- Clause Complexity Match
- SQL Execution
- Non-Empty Output

Then include:

`Overall Full Validation Status: PASS` or `Overall Full Validation Status: FAIL`

## Decision Rules

- Fail full validation if any required area fails.
- Keep reasons direct and technical.
- Do not propose edits unless the user asks for fixes.
- If a failure comes from stale SQL, stale schema JSON, or a different file being executed, say that explicitly.

## Notes

- Be strict on prompt-SQL alignment.
- Be strict on schema JSON and SQL one-to-one mapping.
- Be explicit about whether the SQL being validated is the one embedded in `Validation/validate-prompt.md`.
