# Prompt Validation Check Instructions

Use this workflow when the user asks to run a prompt validation check only.

## Scope

- Validate the user prompt in `Validation/validate-prompt.md`.
- Use only the prompt and the SQL embedded in the same `Validation/validate-prompt.md` file for prompt-SQL alignment.
- Do not use `test.sql` for prompt-SQL alignment unless the user explicitly asks for it.
- Do not modify any files during the check unless the user explicitly asks for fixes.

## What to Check

Evaluate the prompt against these checks:

1. Natural Business Language
2. No SQL Keywords / SQL-in-Words
3. No Schema / Column Leakage
4. Output Control
5. Deterministic Prompt Ordering
6. Internal Coherence
7. Prompt-SQL Alignment

## Prompt-SQL Alignment Rules

- Check whether the prompt matches what the SQL actually returns.
- Check filters, grouping, ranking, ordering, row limits, distinct logic, and benchmark/reference blocks.
- If the SQL uses a stricter rule than the prompt, mark alignment as FAIL.
- If the prompt promises output that the SQL does not actually produce, mark alignment as FAIL.
- If the SQL returns rows but a key business phrase in the prompt is not actually enforced, mark alignment as FAIL.

## Output Format

Always return the result in a table with exactly these columns:

| Prompt Check | Status | Reason |
|---|---|---|

Use one row for each check:

- Natural Business Language
- No SQL Keywords / SQL-in-Words
- No Schema / Column Leakage
- Output Control
- Deterministic Prompt Ordering
- Internal Coherence
- Prompt-SQL Alignment

After the table, always include:

`Overall Prompt Status: PASS` or `Overall Prompt Status: FAIL`

## Decision Rules

- FAIL the prompt if any one of the checks fails.
- Keep reasons short, specific, and tied to the current prompt and SQL.
- Do not suggest edits unless the user asks for a fix.
- If the prompt passes all checks, say so clearly.

## Notes

- Phrases like `arranged by`, `highest`, `latest`, `for each`, and `breakdown by` are acceptable if they read naturally.
- Do not over-flag common business terms like `country code`, `patient ID`, `review score`, or `order status`.
- Focus on real prompt issues, not style preferences.
