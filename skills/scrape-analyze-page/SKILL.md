---
name: scrape-analyze-page
description: Extract all available fields with values from a detail page
argument-hint: "[page-html-path] [work-path] [schema-path] [strict]"
allowed-tools: Skill, Bash, Read, Write
---

You are extracting structured data from a detail page. Given saved HTML, identify all available fields and extract their values.

## Input

The raw argument string is `$ARGUMENTS`. Split it into up to 4 whitespace-separated positional arguments:

1. **page_html_path**: path to saved HTML file, e.g. `.scrape/spec/pages/detail-1/rendered.html`
2. **work_path**: path to working directory for saving analysis, e.g. `.scrape/.work/spec`
3. **schema_path**: optional, path to data-type spec.json. When provided, guides extraction using schema field names, descriptions, and examples.
4. **strict**: optional, literal string `strict`. Only valid with schema_path. When set, extract only schema fields — no extras.

The page directory (parent of the HTML file) also contains `meta.json` with the source URL and other metadata.

## Process

### 1. Clean and read the page

Derive the page ID from the directory name (e.g. `detail-1` from `.../detail-1/rendered.html`).
Derive the html_variant from the filename (e.g. `raw` from `raw.html`, `rendered` from `rendered.html`).

Read `meta.json` from the same directory for the source URL.

**Only process this one page.** Do not read or compare with other pages' analysis files — the orchestrator handles cross-page concerns.

Clean the HTML and extract metadata, saving outputs to the work directory. Use `{page_id}.{html_variant}` as the filename base to avoid collisions:
```
mkdir -p {work_path}/analysis
uv run ${CLAUDE_SKILL_DIR}/scripts/clean_html.py PAGE.html -l1 -o {work_path}/analyze-page/{page_id}.{html_variant}.cleaned.html
uv run ${CLAUDE_SKILL_DIR}/scripts/extract_metadata.py PAGE.html -u PAGE_URL -o {work_path}/analyze-page/{page_id}.{html_variant}.metadata.json
```

Read **only** the cleaned HTML (never the original) and the metadata JSON. The metadata may be empty `{}` if the page has no structured data.

### 2. Extract fields

**IMPORTANT**: Never read the original HTML file (PAGE.html). Only use the cleaned HTML output from step 1 as your HTML source.

Use **both** the cleaned HTML and the metadata as data sources. Metadata (especially JSON-LD) often has cleaner, more complete values than what's visible in the HTML — e.g., structured `price`/`priceCurrency` vs rendered "$29.99", `aggregateRating` with review count, `brand` as a structured object. Some fields may only exist in metadata (e.g., `sku`, `gtin`, `@type`).

Examine both sources and extract all meaningful data fields. For each field, determine:
- **name**: descriptive snake_case field name
- **type**: str, float, int, list, or dict
- **value**: the extracted value

**Three modes** depending on arguments:

- **No schema** (Stage 1 — discovery): Extract all meaningful fields from the page. Invent descriptive snake_case names.
- **Schema** (Stage 2 — default): Extract schema fields using their exact names, descriptions, and `examples` for formatting. Also extract additional fields not in the schema — they may reveal data the user didn't know about.
- **Schema + strict** (Stage 2 — re-analysis): Extract only the schema fields. No extras.

### 3. Handle large values

For fields with large values (long text, HTML content, nested structures):
- Extract the full value for the saved output
- Prepare a truncated version (first 100 chars) for the summary

### 4. Save full output

Save complete extraction to `{work_path}/analyze-page/{page_id}.{html_variant}.json`:
```json
{
  "url": "https://...",
  "page_id": "detail-1",
  "html_variant": "rendered",
  "fields": {
    "name": {"type": "str", "value": "Widget X"},
    "price": {"type": "str", "value": "$29.99"},
    "description": {"type": "str", "value": "Full long description..."}
  }
}
```

### 5. Return summary

Return a concise summary for the orchestrator. Truncate large values:
```
detail-1 (https://...):
  name (str): "Widget X"
  price (str): "$29.99"
  description (str): "Premium widget with advanced..." (2340 chars)
  rating (float): 4.5
```

Keep the summary compact — it will be loaded into the orchestrator's main context alongside summaries from other pages.
