---
name: scrape-add-page-object
description: Add an empty web-poet page object to a Scrapy project
argument-hint: "[file-path] [class-name] [domain] [base-class] [item-class]"
allowed-tools: Bash, Read, Write
---

You are adding an empty web-poet page object to a Scrapy project.

## Input

The raw argument string is `$ARGUMENTS`. Split it into up to 6 whitespace-separated positional arguments:

1. **file_path**: path to the .py file to create or append to (e.g. `books_project/pages/books_toscrape_com.py`)
2. **class_name**: page object class name (e.g. `ProductPage`)
3. **domain**: domain for `@handle_urls` (e.g. `books.toscrape.com`)
4. **base_class**: base class import path (e.g. `web_poet.WebPage`)
5. **item_class**: item class import path (e.g. `books_project.items.ProductItem`)
6. **fields**: optional, comma-separated field names (e.g. `name,price,rating`)

## Process

### 1. Determine required fields

Required fields (no default value in the item class) need `@field` stubs so the page
object doesn't fail on instantiation. Run in the **project's env**:

```bash
uv run --project PROJECT_DIR ${CLAUDE_SKILL_DIR}/scripts/list_required_fields.py \
    ITEM_CLASS
```

Outputs a JSON array of field names, e.g. `["name", "price"]`. If all fields have
defaults, the output is `[]` — no stubs needed.

### 2. Add the page object

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/add_page_object.py \
    FILE_PATH CLASS_NAME DOMAIN BASE_CLASS ITEM_CLASS \
    --fields FIELDS
```

Pass the required fields from step 1 as `--fields` (comma-separated). If no required
fields, omit `--fields` — the class body will be `pass`.

The script uses libcst for correct AST manipulation:
- Creates the file if it doesn't exist
- Appends to existing files with proper import merging
- Multiple page objects can share a module (e.g., `ProductPage` and `CategoryPage`)

Common base classes:
- `web_poet.WebPage` — for pages using HTTP responses (most common)
