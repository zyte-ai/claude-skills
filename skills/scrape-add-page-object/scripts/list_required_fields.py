"""Print required fields of an item class (fields with no default value).

Runs in the user project env (the item class and itemadapter must be importable).

Usage:
    uv run --project PROJECT_DIR list_required_fields.py ITEM_CLASS

Example:
    uv run --project ./books_project list_required_fields.py books_project.items.ProductItem

Outputs a JSON array of required field names.

Based on vscode-zyte's list_required_fields.py.
"""

from __future__ import annotations

__version__ = "0.1.0"

import argparse
import json
import sys
from importlib import import_module

from itemadapter import ItemAdapter


def _get_type(import_path: str) -> type:
    module, name = import_path.rsplit(".", 1)
    return getattr(import_module(module), name)


def get_required_fields(to_return_name: str) -> list[str]:
    to_return: type = _get_type(to_return_name)
    return ItemAdapter.get_json_schema(to_return).get("required", [])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List required fields of an item class"
    )
    parser.add_argument("item_class", help="Item class import path (e.g., books_project.items.ProductItem)")
    args = parser.parse_args()

    if not hasattr(ItemAdapter, "get_json_schema"):
        print("itemadapter 0.12.0+ is required", file=sys.stderr)
        sys.exit(1)

    sys.path.insert(0, ".")
    fields = get_required_fields(args.item_class)
    print(json.dumps(fields))


if __name__ == "__main__":
    main()
