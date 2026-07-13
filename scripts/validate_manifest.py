#!/usr/bin/env python3
"""Validate a BREAD manifest (slice.yaml, loaf.yaml or grain.yaml) against its schema.

Usage:
    python validate_manifest.py <path-to-manifest> [--schema <path-to-schema>]

The schema is auto-detected from the manifest filename:
    slice.yaml  →  schemas/slice.schema.json
    grain.yaml  →  schemas/grain.schema.json
    loaf.yaml   →  schemas/loaf.schema.json

Requires: pip install jsonschema pyyaml
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Error: PyYAML not installed. Run: pip install pyyaml")

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("Error: jsonschema not installed. Run: pip install jsonschema")


SCHEMA_MAP = {
    "slice.yaml": "slice.schema.json",
    "grain.yaml": "grain.schema.json",
    "loaf.yaml": "loaf.schema.json",
}


def find_schema(explicit_path: str | None, manifest_path: Path) -> Path:
    """Resolve schema: explicit arg > auto-detect from manifest filename."""
    if explicit_path:
        p = Path(explicit_path)
        if not p.exists():
            sys.exit(f"Error: Schema not found at {p}")
        return p

    schema_name = SCHEMA_MAP.get(manifest_path.name, "slice.schema.json")

    # Try relative to this script (bread-infra/scripts/ → bread-infra/schemas/)
    script_dir = Path(__file__).resolve().parent
    default = script_dir.parent / "schemas" / schema_name
    if default.exists():
        return default

    sys.exit(
        f"Error: Could not find {schema_name}. "
        "Pass --schema <path> or run from bread-infra."
    )


def validate(manifest_path: Path, schema_path: Path) -> list[str]:
    """Validate manifest against schema. Returns list of error messages."""
    with open(schema_path) as f:
        schema = json.load(f)

    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    if manifest is None:
        return ["Manifest file is empty or not valid YAML."]

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.path))

    messages = []
    for error in errors:
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"
        messages.append(f"  {path}: {error.message}")

    return messages


def main():
    parser = argparse.ArgumentParser(description="Validate a BREAD manifest (slice.yaml or grain.yaml).")
    parser.add_argument("manifest", help="Path to manifest file (slice.yaml or grain.yaml)")
    parser.add_argument("--schema", help="Path to slice.schema.json (auto-detected if omitted)")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        sys.exit(f"Error: Manifest not found at {manifest_path}")

    schema_path = find_schema(args.schema, manifest_path)
    errors = validate(manifest_path, schema_path)

    if errors:
        print(f"FAIL: {manifest_path.name} — {len(errors)} error(s):")
        for msg in errors:
            print(msg)
        sys.exit(1)
    else:
        print(f"OK: {manifest_path.name} is valid against schema {schema_path.name}")


if __name__ == "__main__":
    main()
