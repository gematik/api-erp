"""
Utility functions for OpenAPI to AsciiDoc conversion.
"""

import json
from functools import lru_cache
from urllib.parse import urlparse
from urllib.request import urlopen

import yaml

# Handle both direct execution and package import
try:
    from .config import DEFAULT_STRING_EXAMPLE, DEFAULT_INTEGER_EXAMPLE, DEFAULT_BOOLEAN_EXAMPLE, DEFAULT_NUMBER_EXAMPLE
except ImportError:
    from config import DEFAULT_STRING_EXAMPLE, DEFAULT_INTEGER_EXAMPLE, DEFAULT_BOOLEAN_EXAMPLE, DEFAULT_NUMBER_EXAMPLE


def get_list(value):
    """
    Convert a value to a list if it isn't already one.
    
    Args:
        value: Any value that should be converted to a list
        
    Returns:
        list: The value as a list, or empty list if value is None
    """
    if isinstance(value, list):
        return value
    elif value is not None:
        return [value]
    else:
        return []


def resolve_ref(ref, data):
    """
    Resolve a JSON reference within the OpenAPI data.
    Only supports local refs like "#/components/requestBodies/Login"
    
    Args:
        ref (str): The reference string to resolve
        data (dict): The complete OpenAPI data structure
        
    Returns:
        dict or None: The resolved reference data, or None if not found
    """
    if ref.startswith('#/'):
        return _resolve_fragment(data, ref[1:])

    # Support external refs, e.g.:
    # - https://.../file.yaml#/examples/foo
    # - ./file.yaml#/components/schemas/Bar
    base_ref, fragment = _split_ref(ref)
    if not base_ref:
        return None

    document = _load_external_document(base_ref)
    if document is None:
        return None

    if fragment:
        return _resolve_fragment(document, fragment)

    return document


def _split_ref(ref):
    """
    Split a ref into (base_ref, fragment_without_hash).
    """
    if '#' in ref:
        base_ref, fragment = ref.split('#', 1)
        return base_ref, fragment
    return ref, ''


def _resolve_fragment(document, fragment):
    """
    Resolve a JSON pointer-like fragment against a document.
    """
    if not fragment:
        return document

    fragment = fragment.lstrip('/')
    if not fragment:
        return document

    value = document
    for part in fragment.split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict):
            value = value.get(part)
        elif isinstance(value, list):
            try:
                index = int(part)
            except ValueError:
                return None
            if index < 0 or index >= len(value):
                return None
            value = value[index]
        else:
            return None

        if value is None:
            return None

    return value


@lru_cache(maxsize=128)
def _load_external_document(ref_path):
    """
    Load and parse an external YAML/JSON document from URL or local path.
    """
    try:
        parsed = urlparse(ref_path)
        if parsed.scheme in ('http', 'https'):
            with urlopen(ref_path, timeout=15) as response:
                raw = response.read().decode('utf-8')
        else:
            with open(ref_path, 'r', encoding='utf-8') as f:
                raw = f.read()
    except Exception:
        return None

    try:
        return yaml.safe_load(raw)
    except Exception:
        try:
            return json.loads(raw)
        except Exception:
            return None


def example_from_schema(schema, data=None):
    """
    Generate an example value from a JSON schema.
    
    Args:
        schema (dict): The JSON schema to generate an example from
        data (dict, optional): The complete OpenAPI data for resolving refs
        
    Returns:
        Any: An example value based on the schema type
    """
    # If schema is a ref, resolve it
    if data and '$ref' in schema:
        schema = resolve_ref(schema['$ref'], data)
        if schema is None:
            return None
    
    schema_type = schema.get('type')
    
    if schema_type == 'object':
        props = schema.get('properties', {})
        return {k: example_from_schema(v, data) for k, v in props.items()}
    elif schema_type == 'array':
        items_schema = schema.get('items', {})
        return [example_from_schema(items_schema, data)]
    elif schema_type == 'string':
        return schema.get('example', DEFAULT_STRING_EXAMPLE)
    elif schema_type == 'integer':
        return schema.get('example', DEFAULT_INTEGER_EXAMPLE)
    elif schema_type == 'boolean':
        return schema.get('example', DEFAULT_BOOLEAN_EXAMPLE)
    elif schema_type == 'number':
        return schema.get('example', DEFAULT_NUMBER_EXAMPLE)
    
    return None
