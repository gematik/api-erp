"""
Request file generation for OpenAPI to AsciiDoc conversion.
"""

import os
import json

# Handle both direct execution and package import
try:
    from .utils import get_list, resolve_ref, example_from_schema
    from .config import SUPPORTED_EXTENSIONS
except ImportError:
    from utils import get_list, resolve_ref, example_from_schema
    from config import SUPPORTED_EXTENSIONS


def _process_examples(content_details, data=None):
    """
    Process examples from content details and return list of (name, ref) tuples.
    
    Args:
        content_details (dict): Content details from OpenAPI
        data (dict, optional): Complete OpenAPI data for resolving refs
        
    Returns:
        list: List of (example_name, example_ref) tuples
    """
    examples = []
    
    if 'examples' in content_details:
        for example_name, example_details in content_details['examples'].items():
            example_ref = example_details.get('$ref', '')
            examples.append((example_name, example_ref))
    elif 'example' in content_details:
        example = content_details['example']
        if isinstance(example, dict) and '$ref' in example:
            examples.append((None, example['$ref']))
    elif '$ref' in content_details:
        examples.append((None, content_details['$ref']))
    elif 'schema' in content_details:
        schema = content_details['schema']
        # Resolve $ref in schema if necessary
        if '$ref' in schema:
            schema = resolve_ref(schema['$ref'], data)
        example = example_from_schema(schema, data)
        if example:
            examples.append((None, json.dumps(example, indent=2)))
    
    return examples


def _add_example_to_adoc(adoc_lines, example_name, example_ref, label_prefix="Request Body"):
    """
    Add an example to AsciiDoc lines.
    
    Args:
        adoc_lines (list): List of AsciiDoc lines to append to
        example_name (str): Name of the example (can be None)
        example_ref (str): Reference or content of the example
        label_prefix (str): Prefix for the label
    """
    if example_ref and (str(example_ref).strip().startswith('{') or str(example_ref).strip().startswith('[')):
        # Inline JSON example
        adoc_lines.append(f'.Beispiel {label_prefix}')
        adoc_lines.append('[source,json]')
        adoc_lines.append('----')
        adoc_lines.append(example_ref)
        adoc_lines.append('----')
    else:
        # File reference example
        label = label_prefix
        if example_name:
            label += f" für {example_name}"
        adoc_lines.append(f'.{label} (Klicken zum Ausklappen)')
        adoc_lines.append('[%collapsible]')
        adoc_lines.append('====')
        
        extension = os.path.splitext(str(example_ref))[1].lower() if example_ref else ''
        
        if extension in SUPPORTED_EXTENSIONS:
            source_lang = extension.lstrip('.')
            adoc_lines.append(f'[source,{source_lang}]')
            adoc_lines.append('----')
            adoc_lines.append(f'include::{example_ref}[]')
            adoc_lines.append('----')
        else:
            adoc_lines.append('[source]')
            adoc_lines.append('----')
            adoc_lines.append(str(example_ref))
            adoc_lines.append('----')
        
        adoc_lines.append('====')


def _process_parameters(parameters):
    """
    Process parameters and categorize them by type.
    
    Args:
        parameters (list): List of parameter definitions
        
    Returns:
        tuple: (request_headers, query_parameters, path_params)
    """
    request_headers = []
    query_parameters = []
    path_params = []
    
    for param in parameters:
        param_in = param.get('in')
        name = param.get('name', '')
        required = param.get('required', False)
        schema = param.get('schema', {})
        
        if param_in == 'header':
            header_type = schema.get('type', '')
            required_str = 'required' if required else ''
            type_info = ''
            
            if header_type or required_str:
                type_info = f" ({header_type}"
                if required_str:
                    type_info += f", {required_str}"
                type_info += ")"
            
            if name == 'Authorization':
                header_value = f"Authorization: Bearer <JWT>{type_info}"
            else:
                header_value = f"{name}: <value>{type_info}"
            
            request_headers.append(header_value)
            
        elif param_in == 'query':
            required_str = ' (required)' if required else ''
            param_description = param.get('description', '')
            query_parameters.append(f"{name}: {param_description}{required_str}")
            
        elif param_in == 'path':
            path_params.append(param)
    
    return request_headers, query_parameters, path_params


def _format_uri_with_path_params(uri_formatted, path_params):
    """
    Format URI by replacing path parameters with examples or placeholders.
    
    Args:
        uri_formatted (str): The URI to format
        path_params (list): List of path parameter definitions
        
    Returns:
        str: Formatted URI with path parameters replaced
    """
    for param in path_params:
        param_name = param.get('name', '')
        param_example = param.get('schema', {}).get('example', None)
        
        if param_example is not None:
            uri_formatted = uri_formatted.replace(f"{{{param_name}}}", str(param_example))
        else:
            uri_formatted = uri_formatted.replace(f"{{{param_name}}}", f"<{param_name}>")
    
    return uri_formatted


def generate_request_file(output_file_path, endpoint_data, data):
    """
    Generate a request AsciiDoc file for an OpenAPI endpoint.
    
    Args:
        output_file_path (str): Path to write the request file
        endpoint_data (dict): Processed endpoint data
        data (dict): Complete OpenAPI specification data
    """
    with open(output_file_path, 'w', encoding='utf-8') as adoc_file:
        adoc_lines = []
        
        # Title
        adoc_lines.append('==== Request')
        adoc_lines.append(f'[cols="h,a", width="100%", separator=¦]')
        adoc_lines.append('[%autowidth]')
        adoc_lines.append('|===')
        
        # URI and Method
        adoc_lines.append(f'¦URI ¦{endpoint_data["uri_formatted"]}')
        adoc_lines.append(f'¦Method ¦{endpoint_data["http_method"]}')
        
        # Requester images
        if endpoint_data["allowed_requesters"]:
            images = ''.join([f'image:{{{requester}}}[] ' for requester in endpoint_data["allowed_requesters"]])
            adoc_lines.append(f'¦Requester ¦{images.strip()}')
        
        # HTTP Headers
        if endpoint_data["request_headers"]:
            adoc_lines.append('¦HTTP Header ¦')
            adoc_lines.append('----')
            adoc_lines.extend(endpoint_data["request_headers"])
            adoc_lines.append('----')
        
        # Query Parameters
        if endpoint_data["query_parameters"]:
            adoc_lines.append('¦Query Parameters ¦')
            adoc_lines.append('----')
            adoc_lines.extend(endpoint_data["query_parameters"])
            adoc_lines.append('----')
        
        # Payload section
        adoc_lines.append('¦Payload ¦')
        
        if endpoint_data["request_body_examples"]:
            for example_name, example_ref in endpoint_data["request_body_examples"]:
                _add_example_to_adoc(adoc_lines, example_name, example_ref, "Request Body")
        elif endpoint_data["request_body_fhir_profile"]:
            for url in endpoint_data["request_body_fhir_profile"]:
                name = url.rstrip('/').split('/')[-1]
                adoc_lines.append(f"FHIR-Profil: link:{url}[{name}]")
            adoc_lines.append('\n')
        else:
            adoc_lines.append('No request body.')
        
        adoc_lines.append('|===')
        adoc_lines.append('')
        
        adoc_content = '\n'.join(adoc_lines)
        adoc_file.write(adoc_content)
