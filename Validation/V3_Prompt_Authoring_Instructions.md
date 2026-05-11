# Prompt Authoring Instructions For Agents (v3.0)

Use this guide when writing a user prompt for any NL-to-SQL task. The goal is to write a prompt that sounds like a real business request, is completely and unambiguously aligned to the SQL logic, and maintains high linguistic diversity across the dataset.

---

## Primary Objective

Write a prompt that a reviewer would score as **Pass** on all of the following rubric axes:

| Rubric Axis | What it tests |
|---|---|
| Natural Business Language | Sounds like a real analyst, not a machine |
| No SQL Keywords / SQL-in-Words | Zero implementation leakage |
| Logic Delta Anchoring | All filters and conditions explicitly stated |
| Linguistic Diversity | Significant lexical difference from neighboring prompts |
| Benchmark Clarity | Global vs. correlated references distinguished |
| Deterministic Ordering | Clear sort logic when SQL has ORDER BY |
| Aggregation Scope Accuracy | Single-row vs. multi-row output handled correctly |
| **Prompt-SQL Full Coverage** | Every SQL element traceable to a phrase in the prompt |

---

## Rule 1 — Write Like a User, Not a Query Planner

The prompt must read like a request from a real analyst or business stakeholder, not a description of database mechanics.

**Pass:**
> `Which customer state and product category combinations generated the most revenue?`

**Fail:**
> `Join debt records to country profiles and series definitions and filter by income group.`

The reader must never sense that a SQL query is being transcribed. The focus is on the business question, not the implementation.

---

## Rule 2 — Never Tell the Model How to Build SQL

Do not use SQL construction language. The prompt must describe *what* the user wants, never *how* to retrieve it.

**Prohibited terms and their permitted replacements:**

| Prohibited | Permitted alternative |
|---|---|
| `join` / `linked` / `match on` / `correspondence` | Describe the business relationship: "for each patient's visits", "across countries that have…" |
| `where` | `restricted to`, `that have`, `limiting results to`, `among`, `only for` |
| `group by` | `broken down by`, `segmented by`, `for each combination of`, `categorized by` |
| `select` | `report`, `show`, `return`, `include`, `extract` |
| `having` | `only for groups that exceed`, `limiting to combinations where`, `that appear more than` |
| `CTE` / `subquery` / `scalar subquery` | `reference values`, `system-wide benchmarks`, `independently drawn from` |
| `union` | `combined with`, `merged across`, `pooled from` |
| `order by` | `ranked by`, `sorted from highest to lowest`, `arranged by` |
| `fetch first N rows` / `limit` | `top N results`, `the leading N records` |

---

## Rule 3 — Anchor on Logic Deltas (Filter Alignment)

Every specific filter, threshold, or condition in the SQL must appear **prominently** in the prompt — not buried at the end or paraphrased so loosely that it is ambiguous.

**Filter-Heavy queries:** Move the most restrictive condition to the opening of the sentence.
> `Among low-income nations only, identify the top 100 long-term external debt repayment records…`

**HAVING conditions:** State the threshold explicitly in plain English.
> `…restricting results to only those combinations that appear more than once.`

**Correlated subquery filters:** Name both the condition and the scope.
> `…focusing only on the earliest year where a non-missing population figure exists for each country.`

**Aggregation type:** Distinguish between listing individual rows and a grouped summary.
> `For each group, report the total count and the average claim cost.`

---

## Rule 4 — Linguistic and Structural Diversity

To prevent high similarity scores across a dataset of prompts:

- **Template Rotation**: Do not open with the same structure as the immediately preceding task. Avoid using "Which top N…" or "List all…" consecutively.
- **Perspective Shifting**: Alternate between styles:
  - Analytical: `Analyze the distribution of…`
  - Operational: `Extract a ranked list of…`
  - Inquiry-based: `How does X vary across Y for…?`
- **Synonym Mapping**: Rotate domain vocabulary:
  - `Payer` ↔ `Insurance carrier` ↔ `Coverage provider`
  - `Encounter` ↔ `Visit` ↔ `Admission` ↔ `Clinical event`
  - `Country` ↔ `Nation` ↔ `Economy`
  - `Clinician` ↔ `Provider` ↔ `Specialist`

---

## Rule 5 — Phrase Global vs. Correlated Benchmarks Correctly

Scalar subqueries that pull a single constant value for all rows must be described differently from row-specific computations.

**Global (scalar subquery — same value appended to every row):**
> `…attach system-wide reference highs drawn independently from the full clinical dataset.`
> `…append the overall maximum across the entire trading platform for context.`

**Correlated (row-specific computation):**
> `…compare each result against its own category's historical average.`
> `…show the specific threshold applicable to that country's income tier.`

Mixing these up is a **critical alignment failure** — a global benchmark described as row-specific implies a join that does not exist in the SQL.

---

## Rule 6 — Make Multi-Row Outputs Deterministic

If the SQL contains `ORDER BY` or `FETCH FIRST N ROWS ONLY`, the prompt must state:

1. The sort field(s) in business terms
2. The sort direction (highest to lowest, ascending, chronological, etc.)
3. The row cap (top N, leading N, first N)
4. Tie-breaking fields if present in the SQL

**Pass:**
> `Return the top 100 results ranked by debt value from highest to lowest, with ties broken first by country code and then by year in ascending order.`

**Fail:**
> `Organize the results for easy comparison.`

If the SQL has **no** `ORDER BY`, do not invent ordering language.

---

## Rule 7 — Global Aggregation vs. Row Limits

If the SQL aggregates the entire dataset into a single row (e.g., no `GROUP BY`, or `GROUP BY NULL`, or a standalone `SELECT COUNT(*) FROM …`):

- **Never** add ordering or row-cap language to the prompt
- **Never** say "ranked by" or "top N"
- **Always** phrase it as a single summarizing request

**Pass:**
> `Provide a single overall summary of the total number of active policies across the entire portfolio.`

**Fail:**
> `Return the top results for total active policies, ordered from highest to lowest.`

If the SQL produces multiple rows, use Rule 6 instead.

---

## Rule 8 — Prompt-SQL Full Coverage Alignment

**This is the strictest rule and supersedes all others in case of conflict.**

The prompt must completely and unambiguously describe every logical element of the SQL. A reviewer must be able to reconstruct the full SQL structure from the prompt alone — no element should be invisible, implied, or missing.

### Coverage Requirements

Every element in the SQL must have a corresponding phrase in the prompt:

| SQL Element | Prompt must cover |
|---|---|
| Every JOIN relationship | The business relationship between the entities being combined |
| Every WHERE filter (including IS NOT NULL) | The specific filter value or condition in business terms |
| Every correlated subquery filter | Both the condition and the per-row scope ("for each country") |
| Every GROUP BY column | Each grouping dimension, named or described in business terms |
| Every HAVING condition | The threshold or restriction on grouped results |
| COUNT(*) / COUNT(DISTINCT …) | "total number of", "unique count of" |
| AVG(…) | "average", "mean" |
| SUM(…) | "total", "combined value of" |
| MAX(…) / MIN(…) | "highest", "lowest", "peak", "earliest", "latest" |
| Every scalar subquery (global lookup) | The source domain and the nature of the benchmark (global/system-wide) |
| Every output column | Named or translated into a business phrase |
| ORDER BY fields and direction | Sort field, direction, and tie-breakers in plain English |
| FETCH FIRST N ROWS ONLY | Row cap stated as "top N" or "leading N results" |

### Failure Examples

| What the SQL has | Prompt says | Verdict |
|---|---|---|
| 6 scalar subqueries from 6 different tables | "reference highs from related records" | **FAIL** — sources not named |
| HAVING COUNT(*) > 1 | *(omitted entirely)* | **FAIL** — threshold missing |
| GROUP BY on 3 columns | Only 2 grouping dimensions mentioned | **FAIL** — one dimension missing |
| Global scalar subquery (no correlation) | "compare against each group's benchmark" | **FAIL** — described as correlated |
| ORDER BY col1 DESC, col2 ASC | "sorted by the main field" | **FAIL** — direction and tie-breaker missing |
| IS NOT NULL filter on a column | *(omitted)* | **FAIL** — non-null requirement missing |

### Pass Criteria

Every row in the coverage table above has a matching phrase in the prompt. The prompt reads as a complete, natural business request with zero missing logic.

---

## Strict Prohibitions (The "Never" List)

- **Never** use `correspondence`, `linked`, `match on`, or `join` to describe a relationship — describe what the entities share instead
- **Never** use `where` to describe a filter — use `that have`, `restricted to`, `limiting results to`, `among`, or `only for`
- **Never** write the prompt as a raw list of column names
- **Never** omit row caps or ordering if they are present in the SQL
- **Never** add ordering language to a single-row aggregation result
- **Never** describe a global scalar subquery as if it were a correlated per-row computation

---

## Recommended Templates

### The Analytical Scenario
```
In the context of [Business Process], identify the [N] most critical [records] based on [Ordering Field] from [Direction].
Restrict results to [Filter Condition]. For each [Record], report [Output Fields].
Append system-wide reference highs from [Source Domains] for broader context.
```

### The Grouped Summary
```
How does [Business Topic] vary by [Grouping Dimensions] for [Filtered Scope]?
For each combination that [HAVING Condition], show [Aggregated Metrics].
Return up to [N] results, ranked by [Sort Field] from [Direction], with ties broken by [Tie-breaker].
```

### The Correlated Benchmark
```
For each [Entity], identify [Record Type] that [Filter Condition], focusing only on the [Correlated Subquery Condition] for that [Entity].
Include [Related Entity Details] and reference the [Global Benchmarks] drawn from [Source Domains].
```

### The Single Summary
```
Provide a single overall summary of [Global Aggregation Metric] across [Scope], restricted to [Filter Condition].
```

---

## Authoring Checklist

Before submitting a prompt, verify every item:

- [ ] **Rule 1** — Reads like a real business request, not a database description
- [ ] **Rule 2** — Zero SQL keywords or prohibited terms used
- [ ] **Rule 3** — Every filter, threshold, and condition is explicitly anchored in the prompt
- [ ] **Rule 4** — Opening template and phrasing differ from the immediately preceding task
- [ ] **Rule 5** — Global benchmarks described as system-wide; correlated benchmarks described as row-specific
- [ ] **Rule 6** — Sort field, direction, tie-breakers, and row cap all translated if present in SQL
- [ ] **Rule 7** — No ordering or row-cap language added if SQL returns a single aggregated row
- [ ] **Rule 8** — Every JOIN, WHERE, GROUP BY, HAVING, aggregate, scalar subquery, and output column is covered

---

## Quick Reference: SQL Element → Prompt Phrase Map

| SQL | Natural language equivalent |
|---|---|
| `INNER JOIN T ON A.id = T.id` | "for each [A]'s associated [T]", "across [A] and their [T]" |
| `LEFT JOIN T ON …` | "including [A] records even where no [T] exists" |
| `WHERE col = 'Value'` | "restricted to [Value] records only", "among [Value] [entities]" |
| `WHERE col IS NOT NULL` | "that carry a recorded [field]", "with a non-missing [field]" |
| `GROUP BY col1, col2` | "broken down by [col1] and [col2]" |
| `HAVING COUNT(*) > N` | "only for combinations that appear more than [N] times" |
| `COUNT(*)` | "total number of records", "volume of" |
| `COUNT(DISTINCT col)` | "number of unique [col]", "distinct [col] count" |
| `AVG(col)` | "average [col]" |
| `SUM(col)` | "total [col]", "combined [col]" |
| `MAX(col)` in scalar subquery | "system-wide highest [col]", "overall peak [col] across the full dataset" |
| `MIN(col)` correlated | "earliest [col] for each [entity]", "lowest [col] specific to that [entity]" |
| `ORDER BY col DESC` | "ranked by [col] from highest to lowest" |
| `ORDER BY col ASC` | "sorted by [col] in ascending order", "earliest [col] first" |
| `FETCH FIRST N ROWS ONLY` | "top [N] results", "the leading [N] records" |
