import json
from pathlib import Path

from jsonschema import Draft202012Validator

from app.config import settings

SCHEMA_ROOT = settings.schema_root

KNOWN_SCHEMAS = {
    "site_settings": "site_settings.schema.json",
    "homepage": "homepage.schema.json",
    "blog_post": "blog_post.schema.json",
}


def validate_doc(doc_type: str, payload: dict) -> list[str]:
    filename = KNOWN_SCHEMAS.get(doc_type)
    if not filename:
        return []
    schema_path = SCHEMA_ROOT / filename
    if not schema_path.is_file():
        return [f"Schema file missing for {doc_type}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [e.message for e in sorted(validator.iter_errors(payload), key=lambda e: e.path)]
