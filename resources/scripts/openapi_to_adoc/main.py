"""
Main orchestration logic for OpenAPI to AsciiDoc conversion.
"""

import os
import yaml
import json
import sys

# Handle both direct execution and package import
try:
    # Try relative imports first (when used as package)
    from .config import INPUT_FOLDER, OUTPUT_FOLDER
    from .utils import get_list, resolve_ref
    from .schema_generator import process_schemas
    from .request_generator import generate_request_file, _process_parameters, _format_uri_with_path_params, _process_examples
    from .response_generator import (
        generate_response_file, 
        _process_response_headers, 
        _process_response_codes, 
        _process_response_examples, 
        _process_response_fhir_profiles
    )
except ImportError:
    # Fall back to absolute imports (when run directly)
    from config import INPUT_FOLDER, OUTPUT_FOLDER
    from utils import get_list, resolve_ref
    from schema_generator import process_schemas
    from request_generator import generate_request_file, _process_parameters, _format_uri_with_path_params, _process_examples
    from response_generator import (
        generate_response_file, 
        _process_response_headers, 
        _process_response_codes, 
        _process_response_examples, 
        _process_response_fhir_profiles
    )


def _get_server_urls(data):
    """
    Extract server URLs from OpenAPI data.
    
    Args:
        data (dict): OpenAPI specification data
        
    Returns:
        tuple: (default_server_url, internet_server_url)
    """
    servers = data.get('servers', [])
    
    if servers and len(servers) >= 2:
        server_url_default = servers[0]['url']
        server_url_internet = servers[1]['url']
    elif servers:
        server_url_default = servers[0]['url']
        server_url_internet = servers[0]['url']
    else:
        server_url_default = ''
        server_url_internet = ''
    
    # Correcting the typo in the second server URL if necessary
    if server_url_internet.startswith('https://https://'):
        server_url_internet = server_url_internet.replace('https://https://', 'https://', 1)
    
    return server_url_default, server_url_internet


def _select_server_url(request_routes, server_url_default, server_url_internet):
    """
    Select the appropriate server URL based on request routes.
    
    Args:
        request_routes (list): List of request routes
        server_url_default (str): Default server URL
        server_url_internet (str): Internet server URL
        
    Returns:
        str: Selected server URL
    """
    if 'internet' in request_routes:
        return server_url_internet
    else:
        return server_url_default


def _resolve_request_body(request_body, data):
    """
    Resolve request body references.
    
    Args:
        request_body (dict): Request body definition
        data (dict): Complete OpenAPI data
        
    Returns:
        tuple: (resolved_request_body, fhir_profiles)
    """
    if '$ref' in request_body:
        request_body = resolve_ref(request_body['$ref'], data)
    
    request_body_fhir_profile = get_list(request_body.get('x-fhir-profile'))
    return request_body, request_body_fhir_profile


def _resolve_responses(responses, data):
    """
    Resolve response references.
    
    Args:
        responses (dict): Response definitions
        data (dict): Complete OpenAPI data
        
    Returns:
        dict: Resolved response definitions
    """
    resolved_responses = {}
    
    for code, resp in responses.items():
        if isinstance(resp, dict) and '$ref' in resp:
            resolved = resolve_ref(resp['$ref'], data)
            if resolved:
                resolved_responses[code] = resolved
            else:
                resolved_responses[code] = resp
        else:
            resolved_responses[code] = resp
    
    return resolved_responses


def _process_request_body_examples(request_body, data):
    """
    Process request body examples.
    
    Args:
        request_body (dict): Request body definition
        data (dict): Complete OpenAPI data
        
    Returns:
        list: List of (example_name, example_ref) tuples
    """
    request_body_examples = []
    
    if 'content' in request_body:
        for mime_type, content_details in request_body['content'].items():
            examples = _process_examples(content_details, data)
            request_body_examples.extend(examples)
    
    return request_body_examples


def _process_endpoint(path, method, details, data, output_dir, server_url_default, server_url_internet):
    """
    Process a single endpoint and generate request/response files.
    
    Args:
        path (str): API path
        method (str): HTTP method
        details (dict): Endpoint details from OpenAPI
        data (dict): Complete OpenAPI data
        output_dir (str): Output directory
        server_url_default (str): Default server URL
        server_url_internet (str): Internet server URL
    """
    # Generate filenames
    path_formatted = path.lstrip('/').replace('/', '_').replace('{', '').replace('}', '')
    http_method = method.upper()
    
    endpoint_filename_request = f"{path_formatted}_{http_method}_Request.adoc"
    endpoint_filename_response = f"{path_formatted}_{http_method}_Response.adoc"
    
    output_file_request = os.path.join(output_dir, endpoint_filename_request)
    output_file_response = os.path.join(output_dir, endpoint_filename_response)
    
    # Extract basic data
    uri = path
    summary = details.get('summary', '')
    description = details.get('description', '')
    parameters = details.get('parameters', [])
    
    # Process request body
    request_body = details.get('requestBody', {})
    request_body, request_body_fhir_profile = _resolve_request_body(request_body, data)
    
    # Process responses
    responses = details.get('responses', {})
    responses = _resolve_responses(responses, data)
    
    # Process routing
    tags = details.get('tags', [])
    request_routes = details.get('x-request-route', [])
    request_routes = [route.lower() for route in request_routes]
    allowed_requesters = details.get('x-allowed-requester', [])
    
    # Select server URL
    host = _select_server_url(request_routes, server_url_default, server_url_internet)
    uri_formatted = f"{host}{uri}"
    
    # Process parameters
    request_headers, query_parameters, path_params = _process_parameters(parameters)
    uri_formatted = _format_uri_with_path_params(uri_formatted, path_params)
    
    # Process request body examples
    request_body_examples = _process_request_body_examples(request_body, data)
    
    # Process response data
    responses_headers = _process_response_headers(responses)
    response_codes = _process_response_codes(responses)
    responses_examples = _process_response_examples(responses, data)
    response_fhir_profiles = _process_response_fhir_profiles(responses)
    
    # Prepare endpoint data
    endpoint_data = {
        'uri_formatted': uri_formatted,
        'http_method': http_method,
        'allowed_requesters': allowed_requesters,
        'request_headers': request_headers,
        'query_parameters': query_parameters,
        'request_body_examples': request_body_examples,
        'request_body_fhir_profile': request_body_fhir_profile,
        'responses_headers': responses_headers,
        'response_codes': response_codes,
        'responses_examples': responses_examples,
        'response_fhir_profiles': response_fhir_profiles
    }
    
    # Generate files
    generate_request_file(output_file_request, endpoint_data, data)
    generate_response_file(output_file_response, endpoint_data, data)


def process_openapi_file(input_file):
    """
    Process a single OpenAPI file and generate AsciiDoc documentation.
    
    Args:
        input_file (str): Path to the OpenAPI YAML file
    """
    print(f"Processing {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as yf:
            data = yaml.safe_load(yf)
    except Exception as e:
        print(f"Error loading {input_file}: {e}")
        return
    
    # Create output directory
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(OUTPUT_FOLDER, base_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Process schemas
    try:
        schema_dir = process_schemas(data, output_dir)
        if schema_dir:
            print(f"  Generated schemas in {schema_dir}")
    except Exception as e:
        print(f"  Error processing schemas: {e}")
    
    # Get server URLs
    server_url_default, server_url_internet = _get_server_urls(data)
    
    # Process endpoints
    paths = data.get('paths', {})
    endpoint_count = 0
    
    for path, methods in paths.items():
        for method, details in methods.items():
            try:
                _process_endpoint(
                    path, method, details, data, output_dir,
                    server_url_default, server_url_internet
                )
                endpoint_count += 1
            except Exception as e:
                print(f"  Error processing {method.upper()} {path}: {e}")
    
    print(f"  Generated documentation for {endpoint_count} endpoints in {output_dir}")


def main():
    """
    Main function to process all OpenAPI files in the input directory.
    """
    print(f"OpenAPI to AsciiDoc Converter")
    print(f"Input directory: {INPUT_FOLDER}")
    print(f"Output directory: {OUTPUT_FOLDER}")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output directory: {OUTPUT_FOLDER}")
    
    # Check if input directory exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Input directory {INPUT_FOLDER} does not exist!")
        return
    
    # Process all YAML files in input directory
    yaml_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.yml', '.yaml'))]
    
    if not yaml_files:
        print(f"No YAML files found in {INPUT_FOLDER}")
        return
    
    print(f"Found {len(yaml_files)} YAML files to process")
    
    for filename in yaml_files:
        input_file = os.path.join(INPUT_FOLDER, filename)
        process_openapi_file(input_file)
    
    print("Processing complete!")


if __name__ == "__main__":
    main()
