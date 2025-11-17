"""
Schema generation functionality for OpenAPI to AsciiDoc conversion.
"""

import os
import json

# Handle both direct execution and package import
try:
    from .utils import example_from_schema
except ImportError:
    from utils import example_from_schema


def write_schema_to_adoc(schema_name, schema, output_dir, data=None):
    """
    Write a single schema definition to an AsciiDoc file.
    
    Args:
        schema_name (str): Name of the schema
        schema (dict): Schema definition from OpenAPI
        output_dir (str): Directory to write the file to
        data (dict, optional): Complete OpenAPI data for resolving refs
    """
    adoc_lines = []
    adoc_lines.append(f"=== {schema_name}\n")
    
    if 'description' in schema:
        adoc_lines.append(schema['description'] + "\n")

    adoc_lines.append("|===")
    adoc_lines.append("| Feld | Typ | Beschreibung")

    props = schema.get('properties', {})
    for prop, propinfo in props.items():
        prop_type = propinfo.get('type', '')
        description = propinfo.get('description', '')
        adoc_lines.append(f"| {prop} | {prop_type} | {description}")

    adoc_lines.append("|===\n")

    # Add example if possible
    example = schema.get('example')
    if not example:
        example = example_from_schema(schema, data)
    
    if example:
        adoc_lines.append(".Beispiel")
        adoc_lines.append("[source,json]")
        adoc_lines.append("----")
        adoc_lines.append(json.dumps(example, indent=2, ensure_ascii=False))
        adoc_lines.append("----\n")

    # Write to file
    output_file = os.path.join(output_dir, f"{schema_name}.adoc")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(adoc_lines))


def process_schemas(data, output_dir):
    """
    Process all schemas from OpenAPI data and generate AsciiDoc files.
    
    Args:
        data (dict): Complete OpenAPI specification data
        output_dir (str): Base output directory
        
    Returns:
        str or None: Path to schemas directory if schemas were processed, None otherwise
    """
    schemas = data.get('components', {}).get('schemas', {})
    
    if not schemas:
        return None
        
    schema_dir = os.path.join(output_dir, "schemas")
    os.makedirs(schema_dir, exist_ok=True)
    
    for schema_name, schema in schemas.items():
        write_schema_to_adoc(schema_name, schema, schema_dir, data)
    
    return schema_dir
