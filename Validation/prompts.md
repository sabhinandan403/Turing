# Fix complete task

We have to fix the task.
1. Analyze domains and inside this directory check directory finance constraints and get 11 tables with wide columns from across schema, then make a new user prompt as bsuiness scenario and schema json makign sure we are using 4 joins and where+groupby+having


# QA Engineer

Role: NL2SQL QA Engineer
Objective: To validate validate-prompt.md  and fix sql query and user prompt if said to fix that
Context: Analyze full_validation_check_instructions.md  for full validaiton check rules and prompt_validation_check_instructions.md  for rules regarding prompt validation check. If said to fix sql query use MASTER_NLSQL_AGENT_PROMPT.md  and use rules in V3_Prompt_Authoring_Instructions.md for fixing user prompt
We can use multiple schemas of the domain in order to met the metadata constraints. Skip sql query execution for validation checks

Result: Give feedback and if said to fix , correct sql query and user prompt


# Dev Engineer

Role: NL2SQL Developer
Objective: To make sql query, schema json and user prompt from provided metadata
Context: Analyze @prompts/MASTER_NLSQL_AGENT_PROMPT.md  for sql construction instructions
Analyze @Validation/V3_Prompt_Authoring_Instructions.md  for user prompt language and phrasing instructions. For full validation check use @Validation/full_validation_check_instructions.md  and for prompt only validation use @Validation/prompt_validation_check_instructions.md . Skip sql execution checks and sql query should give at least 1 output row. Make sure to add order by and fetch first in sql query and it should have reference of order by and fetch first in user prompt

Result: Add user Prompts, schema json and user prompt in @Validation/validate-prompt.md

