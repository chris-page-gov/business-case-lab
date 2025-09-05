This document has been split into focused artifacts. Use the files
below for the canonical spec and prompts.

- Spec (narrative template): `spec/business_case_template.md`
- Interviewer prompt: `prompts/interviewer_prompt.md`
- Renderer prompt: `prompts/renderer_prompt.md`

For the original full conversion (for reference), see
`docs/full-conversion.md`.


- /spec/business_case_template.md (narrative spec)

- /schema/business_case.schema.json (JSON Schema)

- /prompts/interviewer_prompt.txt and /prompts/renderer_prompt.txt

- /tests/synthetic/{case_id}/input_pack/\*

- /tests/synthetic/{case_id}/gold.json and /gold/{case_id}.md

- /eval/scorecard.json and /eval/run_report.md

## Acceptance criteria

- Schema passes jsonschema validation; conditional rules proven by unit
  tests.

- Harness can run headless and produce a deterministic draft for a given
  gold.json.

- At least 16 synthetic cases with Golds; ≥90% average completeness,
  100% structural fidelity, 0 arithmetic errors.

## Starter artefacts

### 1) Minimal JSON Schema skeleton

{

"\$id": "https://example.org/schema/business_case.schema.json",

"\$schema": "https://json-schema.org/draft/2020-12/schema",

"title": "Public Sector Business Case (Five Case Model)",

"type": "object",

"required": \["metadata", "case_level", "strategic_case",
"economic_case", "commercial_case", "financial_case",
"management_case"\],

"properties": {

"metadata": {

"type": "object",

"required": \["title", "sro", "sponsoring_org", "date", "version"\],

"properties": {

"title": {"type": "string", "minLength": 5},

"sro": {"type": "string"},

"sponsoring_org": {"type": "string"},

"date": {"type": "string", "format": "date"},

"version": {"type": "string", "pattern": "^v\\d+\\.\\d+(\\.\\d+)?\$"}

}

},

"case_level": {"type": "string", "enum": \["BJC", "OBC", "FBC"\]},

"strategic_case": {

"type": "object",

"required": \["problem_statement", "objectives", "strategic_fit",
"stakeholders"\],

"properties": {

"problem_statement": {"type": "string"},

"objectives": {"type": "array", "items": {"type": "string"}, "minItems":
1},

"strategic_fit": {"type": "string"},

"stakeholders": {"type": "array", "items": {"type": "string"}}

}

},

"economic_case": {

"type": "object",

"required": \["options", "preferred_option", "npv", "sensitivity"\],

"properties": {

"options": {"type": "array", "minItems": 2, "items": {"type":
"string"}},

"preferred_option": {"type": "string"},

"npv": {"type": "number"},

"sensitivity": {"type": "string"}

}

},

"commercial_case": {

"type": "object",

"required": \["delivery_model", "route_to_market"\],

"properties": {

"delivery_model": {"type": "string", "enum": \["in-house", "outsourced",
"hybrid", "AIaaS"\]},

"route_to_market": {"type": "string"},

"lock_in_mitigations": {"type": "string"},

"data_ai_clauses": {"type": "string"}

}

},

"financial_case": {

"type": "object",

"required": \["capex", "opex", "funding_profile", "cashable_benefits"\],

"properties": {

"capex": {"type": "number", "minimum": 0},

"opex": {"type": "number", "minimum": 0},

"funding_profile": {"type": "array", "items": {"type": "object",
"required": \["year", "amount"\], "properties": {"year": {"type":
"integer"}, "amount": {"type": "number"}}}},

"cashable_benefits": {"type": "number", "minimum": 0},

"non_cashable_benefits": {"type": "string"}

}

},

"management_case": {

"type": "object",

"required": \["plan", "governance", "assurance", "measurement"\],

"properties": {

"plan": {"type": "string"},

"governance": {"type": "string"},

"assurance": {"type": "array", "items": {"type": "string", "enum":
\["Gate 0", "Gate 1", "Gate 2", "Gate 3", "Gate 4", "Gate 5"\]}},

"measurement": {"type": "string"},

"dpia_ref": {"type": "string"},

"eqia_ref": {"type": "string"},

"technical_feasibility": {"type": "string"}

}

}

},

"allOf": \[

{

"if": {"properties": {"commercial_case": {"properties":
{"delivery_model": {"const": "AIaaS"}}}}},

"then": {"properties": {"commercial_case": {"required":
\["data_ai_clauses", "lock_in_mitigations"\]}}}

}

\]

}

### 2) Interviewer prompt (guided Q&A with auditing)

You are an Interviewer Agent completing a UK public-sector business case
using the Five Case Model.

Rules:

• Ask ONE field at a time following the JSON Schema order; show a short
example when useful.

• Never invent numbers; request source/provenance. If unknown, record
"TBD" and create a follow-up action.

• Validate each answer against the schema; if invalid, explain why and
re-ask.

• Keep a JSONL audit log. For each step append:

{"timestamp":"\<ISO8601\>","step_id":"\<uuid\>","field_path":"\<json-pointer\>","question":"...","response":"...","confidence":0..1,"provenance":"\<free
text or URL\>","validation":{"passed":true\|false,"errors":\[...\]}}

• Maintain a running summary (“working memory”) of agreed facts to
reduce re-asking.

• At the end of each Case section, present a concise recap for
confirmation.

• Stop when all required fields for the selected case_level are valid;
produce:

\(1\) the filled JSON, (2) the audit log JSONL, (3) a “gaps_and_actions”
list for any TBDs.

### 3) Deterministic renderer prompt (template filling)

You are a Renderer. Input: (a) VALIDATED business_case.json, (b) fixed
boilerplate.md.

Task: Compile a draft Business Case document with sections in this exact
order:

Strategic, Economic, Commercial, Financial, Management.

Rules:

• Deterministic: do NOT add facts; only rephrase minimally for
readability.

• If a required field is missing (shouldn’t happen), insert
"\[MISSING:\<field_path\>\]" and list it under "Gaps and Actions".

• Numbers, totals and funding profiles must be echoed EXACTLY as in
JSON; recalculate checksums and flag discrepancies.

Output: Markdown (or DOCX if the host app supports it) + a
machine-readable outline.json with section headings and paragraph
anchors.

### 4) Test & Evaluation harness (spec)

- **Inputs**: {case_id}/input_pack/\* (brief + exhibits) feed the
  Interviewer; expected outputs are {case_id}/gold.json and
  {case_id}.md.

- **Runner**: executes (1) Interviewer → JSON, (2) Renderer → Draft, (3)
  Validations → Score.

- **Checks**:

  - JSON **schema-valid**; conditional rules exercised.

  - **Arithmetic**: recompute NPV/funding sums; match.

  - **Structure**: required headings present; order exact.

  - **Content**: for numeric/text fields flagged “verbatim”, exact match
    to Gold; for narrative fields, allow semantic similarity ≥
    threshold.

  - **Audit**: audit file present; ≥ 95% steps have provenance; zero
    invalid fields at final state.

- **Outputs**: /eval/scorecard.json with per-metric scores and **delta
  vs previous run**.

## App vs Licensed AI tooling (e.g., Copilot) — pros & cons

| Option | Pros | Cons | When to prefer |
|----|----|----|----|
| **Dedicated app** (bespoke or low-code) | Full control of UX, security zones, data residency; offline/air-gapped possible; deterministic renderer is straightforward; easier to embed cost telemetry and audit; portable across models | Higher build/maintain cost; needs dev capacity; upgrades on you; integration work for sign-in and storage | When requirements are strict on data control, offline modes, custom workflow, or you want to avoid vendor lock-in |
| **Licensed ai tooling** (copilot-style) | Rapid start; enterprise SSO; rich authoring; good plugins; lower upfront cost; model updates managed by vendor | Less control over prompts/runtime; potential vendor lock-in; auditing may be coarser; determinism can be harder; usage-based cost drift | When speed-to-value matters, policies allow data processing with vendor, and you can live with platform constraints |

**Decision criteria:** data sensitivity/residency, auditability needs,
determinism, total cost of ownership, portability (exit), and speed to
deploy.
