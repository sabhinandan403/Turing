# Prompt Authoring Instructions For Agents

Use this guide when you need to write a user prompt for an NL-to-SQL task in this repo.

The goal is not just to write a readable prompt. The goal is to write a prompt that:
- sounds like a real user request,
- is aligned to the SQL,
- is deterministic when the SQL returns multiple rows,
- avoids SQL-in-words,
- and matches the calibrated rubric used in this repo.

This guide is based on:
- `Validation/rubric_points.md`
- `Validation/rework_prompt.md`
- `Validation/session_context.md`

## Primary Objective

Write a prompt that another reviewer would score as:
- `Natural Business Language`: pass
- `No SQL Keywords / SQL-in-Words`: pass
- `No Schema / Column Leakage`: pass
- `Output Control`: pass
- `Deterministic Prompt Ordering`: pass
- `Prompt-SQL Alignment`: pass
- `Reasonable Prompt Scope`: pass

## Core Rules

### 1. Write like a user, not like a query planner

The prompt must sound like a realistic analyst or business request.

Good:
- `Which customer state and product category combinations generated the most item revenue...?`
- `Provide the first 25 international debt records...`
- `Summarize monthly online sales from January 2013 onward...`

Bad:
- `Join debt records to country profiles and series definitions...`
- `Use left joins to attach payer and provider details...`
- `Group by region and indicator topic, then order by total debt...`

### 2. Never tell the model how to build SQL

Do not use SQL-construction language.

Do not write:
- `join`
- `left join`
- `inner join`
- `where`
- `group by`
- `having`
- `order by`
- `select`
- `subquery`
- `CTE`
- `union`
- `match on`
- `join on`
- `use table`

Important:
- Natural analytical phrases like `broken down by`, `segmented by`, `arranged by`, `ranked by`, `earliest`, `latest`, `highest`, `average`, `total`, and `unique` are acceptable when they sound like business language.

### 3. Keep the prompt aligned to the SQL

The prompt must describe what the SQL actually returns.

That means:
- mention the real filtering logic in business terms,
- mention the real row limit if there is one,
- mention the real grouping if the SQL is grouped,
- mention the real ranking or ordering,
- do not ask for fields the SQL does not return,
- do not omit important requirements enforced by the SQL.

If the SQL does any of the following, the prompt should usually reflect it:
- strict filters
- row caps
- grouped summaries
- top-N / bottom-N ranking
- special tie-break rules
- inner-join style “must have matching record” behavior

### 4. Make multi-row outputs deterministic

If the SQL returns multiple rows, the prompt should clearly state the intended order.

Good:
- `Return the top 30 results ranked by total item revenue from highest to lowest.`
- `Show up to 100 results, arranged by patient identifier in ascending order.`
- `Return the first 50 groups arranged by region, income group, and indicator topic.`

Weak:
- `Organize them so they are easy to compare.`
- `Show the latest rows.`
- `List some results.`

Primary ordering is usually enough for prompt-only review.
Add tie-break wording only when the SQL logic makes it necessary.

### 5. Control output size

Do not write open-ended extraction prompts unless the task is strongly narrowed.

Preferred ways to control output:
- explicit row cap: `top 20`, `first 100`, `up to 200`
- strong filters
- grouped summaries
- thresholds such as `more than 5` or `at least 50`
- ranking patterns

Good:
- `Return up to 100 rows...`
- `Keep only categories with more than 100 distinct orders.`
- `Show the top 25 by average covered charges.`

Bad:
- `Show all orders with customer and product details.`
- `List every debt record with country profile details.`

### 6. Avoid schema-style phrasing

Do not write the prompt like a select list.

Too schema-like:
- `Return customer ID, employee ID, supplier ID, total quantity, and average unit price.`

Better:
- `For each result, include the customer, handling employee, supplier, total quantity ordered, and average unit price.`

Important:
- Some business-facing field names are fine when natural:
  - `country code`
  - `indicator code`
  - `patient identifier`
  - `order status`
  - `review score`

The problem is not every identifier.
The problem is prompts that read like raw column inventory.

### 7. Keep one coherent reporting objective

Large prompts can still pass.
Many metrics can still pass.
Benchmark blocks can still pass.

But everything should still support one clear reporting goal.

Good:
- a grouped debt summary with related benchmark context
- a healthcare encounter report with related patient, provider, and payer context
- a city-level sales summary with product and seller context

Bad:
- a prompt that combines unrelated business questions
- a prompt that feels like several separate tasks stitched together

## Recommended Prompt Structure

Use this pattern when possible:

1. Start with the business ask
2. State the scope or filters
3. State the grouping or row-level shape
4. State the important fields or summaries
5. Add benchmark/reference context if needed
6. End with row limit and ordering

### Simple Row-Level Template

`Which [N] [records] [meeting filter conditions] should appear first when ordered by [field(s)]? For each result, include [business-facing fields].`

Example:

`Which 100 vegetable transactions with matching category, loss-rate, and wholesale pricing records come first by reference number? For each one, include the trade time, quantity sold, product details, loss rate, and the latest wholesale date and price.`

### Grouped Summary Template

`How does [business topic] vary by [grouping dimensions] for [filtered scope]? For each group, show [summary metrics]. Return up to [N] results, ordered by [fields/ranking].`

Example:

`How does debt vary by region, income group, and indicator topic for low-income countries? For each group, show the number of countries, indicators, years covered, and total debt value. Return the first 50 groups arranged by region, income group, and indicator topic.`

### Top-N Ranking Template

`Which [groups or records] generated the highest [metric] for [scope]? For each result, include [key summaries]. Return the top [N] results ranked from highest to lowest [metric].`

Example:

`Which customer state and product category combinations generated the most item revenue for orders placed on or after January 1, 2018? For each qualifying state and category, show order counts, customer and seller counts, average item price, total item revenue, and the most recent purchase timestamp. Return the top 30 results ranked by total item revenue from highest to lowest.`

## What Is Allowed

These patterns are acceptable in this repo when they sound natural:
- `for each`
- `broken down by`
- `segmented by`
- `arranged by`
- `ranked by`
- `highest`
- `earliest`
- `latest`
- `average`
- `total`
- `unique`
- `matched`
- `linked`
- `cross-referenced`
- `where available`

Do not remove these automatically.
Only remove them when they are being used as SQL instructions rather than business phrasing.

## What Usually Causes Failure

### Failure Type 1: SQL-in-words

Bad:

`Join international debt to country summary on country code and left join WDI data on country code and year.`

### Failure Type 2: Unbounded row dump

Bad:

`List all orders with customer, seller, payment, and review details.`

### Failure Type 3: Missing ordering

Bad:

`Show up to 100 patient records.`

Better:

`Show up to 100 patient records ordered by patient identifier from lowest to highest.`

### Failure Type 4: Schema-style field list

Bad:

`Return order ID, customer ID, employee ID, supplier ID, unit price, quantity, and freight.`

### Failure Type 5: Prompt-SQL mismatch

Bad:
- prompt asks for film title
- SQL returns only film ID

Bad:
- prompt says `up to 300 rows`
- SQL fetches `150`

Bad:
- prompt sounds like grouped output
- SQL is row-level

## Authoring Checklist

Before finalizing a prompt, verify all of these:

1. Does this sound like a real user or analyst request?
2. Did I avoid SQL-construction wording?
3. Did I avoid writing a raw select-list in prose?
4. Is the prompt logically aligned with the SQL?
5. Does it clearly describe whether the result is row-level or grouped?
6. Is the output bounded by a row cap, ranking, threshold, or selective filter?
7. If the output has multiple rows, did I clearly state the order?
8. If the SQL has strict matching behavior, did I reflect it naturally in the prompt?
9. If the SQL uses special tie-break logic, did I mention it when needed?
10. Does the entire prompt still feel like one coherent request?

If any answer is `no`, revise the prompt.

## Rewrite Guidance

When fixing a failing prompt:

### If it is too technical
- remove phrases like `combining`, `linked by`, `sharing the same identifier`, `corresponding entries`
- rewrite around the information need, not the data assembly

### If it is not deterministic
- add a clear ordering clause
- examples:
  - `ordered by patient identifier`
  - `ranked from highest to lowest total revenue`
  - `arranged alphabetically by region`

### If it is too extraction-like
- add analytical framing:
  - `Which...`
  - `How does...`
  - `For each...`
  - `Summarize...`
  - `Report...`

### If it leaks schema-like fields
- compress column lists into business phrasing
- example:
  - instead of `customer ID, company name, contact name, contact title`
  - use `customer company and contact details`

## Final Rule

Do not optimize for completeness at the expense of naturalness.

A good prompt in this repo is:
- natural,
- precise,
- bounded,
- deterministic,
- and clearly aligned to the SQL.

If you must choose, prefer:
- business wording over implementation wording,
- a coherent summary over a field dump,
- and explicit ordering over vague presentation language.
