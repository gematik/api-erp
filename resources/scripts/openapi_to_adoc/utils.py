"""
Utility functions for OpenAPI to AsciiDoc conversion.
"""

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
    if not ref.startswith('#/'):
        return None
    
    parts = ref.lstrip('#/').split('/')
    value = data
    
    for part in parts:
        value = value.get(part)
        if value is None:
            return None
            
    return value


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
