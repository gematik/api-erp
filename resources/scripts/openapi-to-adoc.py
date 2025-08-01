
import os
import yaml
import json
import requests
from urllib.parse import urlparse

def get_list(value):
    if isinstance(value, list):
        return value
    elif value is not None:
        return [value]
    else:
        return []

def download_and_extract_examples(example_ref, example_name, examples_dir):
    """
    Download external reference file and extract specific example to separate file
    Returns the path to the extracted example file
    """
    try:
        # Download the external file
        response = requests.get(example_ref.split('#')[0])
        response.raise_for_status()
        
        # Parse the YAML/JSON content
        if example_ref.split('#')[0].endswith('.yaml') or example_ref.split('#')[0].endswith('.yml'):
            data = yaml.safe_load(response.text)
        else:
            data = json.loads(response.text)
        
        # Extract the specific example using JSON pointer
        if '#/' in example_ref:
            json_pointer = example_ref.split('#/', 1)[1]
            pointer_parts = json_pointer.split('/')
            
            # Navigate through the JSON pointer
            current_data = data
            for part in pointer_parts:
                if part in current_data:
                    current_data = current_data[part]
                else:
                    print(f"Warning: Could not find {part} in {example_ref}")
                    return None
            
            # Create filename for the extracted example
            base_url = example_ref.split('#')[0]
            original_filename = os.path.basename(urlparse(base_url).path)
            name_without_ext = os.path.splitext(original_filename)[0]
            
            if example_name:
                example_filename = f"{name_without_ext}_{example_name}_example.json"
            else:
                example_filename = f"{name_without_ext}_example.json"
            
            example_file_path = os.path.join(examples_dir, example_filename)
            
            # Ensure examples directory exists
            os.makedirs(examples_dir, exist_ok=True)
            
            # Write the extracted example to file
            with open(example_file_path, 'w', encoding='utf-8') as f:
                if 'value' in current_data:
                    # If the example has a 'value' field, use that
                    json.dump(current_data['value'], f, indent=2, ensure_ascii=False)
                else:
                    # Otherwise use the data as-is
                    json.dump(current_data, f, indent=2, ensure_ascii=False)
            
            return example_file_path
        else:
            # No JSON pointer, use the whole file
            original_filename = os.path.basename(urlparse(example_ref).path)
            example_file_path = os.path.join(examples_dir, original_filename)
            
            os.makedirs(examples_dir, exist_ok=True)
            
            with open(example_file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            return example_file_path
            
    except Exception as e:
        print(f"Error downloading/extracting example from {example_ref}: {e}")
        return None

def resolve_ref(ref_path, data):
    """
    Resolve a JSON reference like "#/components/responses/ErrorResponse400"
    Returns the resolved object or None if not found
    """
    if not ref_path.startswith('#/'):
        return None
    
    # Remove the '#/' prefix and split the path
    path_parts = ref_path[2:].split('/')
    
    # Navigate through the data structure
    current = data
    for part in path_parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            print(f"Warning: Could not resolve reference {ref_path}")
            return None
    
    return current

def get_response_description(response, data):
    """
    Get the description from a response, resolving $ref if necessary
    """
    # First check if there's a direct description
    if 'description' in response:
        return response['description']
    
    # If there's a $ref, resolve it
    if '$ref' in response:
        resolved = resolve_ref(response['$ref'], data)
        if resolved and 'description' in resolved:
            return resolved['description']
    
    # Fallback to empty string
    return ''

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define input and output folders relative to the script's directory
INPUT_FOLDER = os.path.join(script_dir, '../openapi')
OUTPUT_FOLDER = os.path.join(script_dir, '../openapi-adoc')

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith('.yml') or filename.endswith('.yaml'):
        input_file = os.path.join(INPUT_FOLDER, filename)
        with open(input_file, 'r', encoding='utf-8') as yf:
            data = yaml.safe_load(yf)

        base_name = os.path.splitext(filename)[0]
        dir_path = os.path.join(OUTPUT_FOLDER, base_name)
        examples_dir = os.path.join(dir_path, 'examples')  # New examples subdirectory
        os.makedirs(dir_path, exist_ok=True)

        # Get the list of servers
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

        # Navigate through the OpenAPI paths
        paths = data.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                # Prepare data for the AsciiDoc files
                # Remove leading '/', replace slashes with underscores, and append method
                path_formatted = path.lstrip('/').replace('/', '_').replace('{', '').replace('}', '')
                http_method = method.upper()

                # Filenames for Request and Response
                endpoint_filename_request = f"{path_formatted}_{http_method}_Request.adoc"
                endpoint_filename_response = f"{path_formatted}_{http_method}_Response.adoc"

                output_file_request = os.path.join(dir_path, endpoint_filename_request)
                output_file_response = os.path.join(dir_path, endpoint_filename_response)

                # Extracting data
                uri = path
                summary = details.get('summary', '')
                description = details.get('description', '')
                parameters = details.get('parameters', [])
                request_body = details.get('requestBody', {})
                request_body_fhir_profile = get_list(request_body.get('x-fhir-profile'))
                responses = details.get('responses', {})
                tags = details.get('tags', [])
                # Extract 'x-request-route'
                request_routes = details.get('x-request-route', [])
                request_routes = [route.lower() for route in request_routes]

                # Get the list of allowed requesters from 'x-allowed-requester' field
                allowed_requesters = details.get('x-allowed-requester', [])

                # Select the appropriate server URL based on 'x-request-route'
                if 'internet' in request_routes:
                    host = server_url_internet
                else:
                    host = server_url_default

                # Construct the full URI
                uri_formatted = f"{host}{uri}"

                # Check for path parameters and modify the URI accordingly
                for param in parameters:
                    if param.get('in') == 'path':
                        param_name = param.get('name', '')
                        param_example = param.get('schema', {}).get('example', None)
                        
                        # Replace the path parameter in the URI
                        if param_example is not None:
                            # Use the example if provided
                            uri_formatted = uri_formatted.replace(f"{{{param_name}}}", param_example)
                        else:
                            # Use the parameter name if no example is provided
                            uri_formatted = uri_formatted.replace(f"{{{param_name}}}", f"<{param_name}>")

                # Request Headers
                request_headers = []
                for param in parameters:
                    if param.get('in') == 'header':
                        name = param.get('name', '')
                        schema = param.get('schema', {})
                        header_type = schema.get('type', '')
                        required = param.get('required', False)
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

                # Query Parameters
                query_parameters = []
                for param in parameters:
                    if param.get('in') == 'query':
                        name = param.get('name', '')
                        required = ' (required)' if param.get('required', False) else ''
                        param_description = param.get('description', '')
                        query_parameters.append(f"{name}: {param_description}{required}")

                # Modified: Extract request body examples with separate files
                request_body_examples = []
                if 'content' in request_body:
                    for mime_type, content_details in request_body['content'].items():
                        if 'examples' in content_details:
                            examples = content_details['examples']
                            for example_name, example_details in examples.items():
                                example_ref = example_details.get('$ref', '')
                                if example_ref:
                                    # Download and extract to separate file
                                    extracted_file = download_and_extract_examples(
                                        example_ref, example_name, examples_dir
                                    )
                                    if extracted_file:
                                        # Make path relative to the adoc file
                                        relative_path = os.path.relpath(extracted_file, dir_path)
                                        request_body_examples.append((example_name, relative_path))
                        elif 'example' in content_details:
                            example = content_details['example']
                            if isinstance(example, dict) and '$ref' in example:
                                extracted_file = download_and_extract_examples(
                                    example['$ref'], None, examples_dir
                                )
                                if extracted_file:
                                    relative_path = os.path.relpath(extracted_file, dir_path)
                                    request_body_examples.append((None, relative_path))
                            elif '$ref' in content_details:
                                extracted_file = download_and_extract_examples(
                                    content_details['$ref'], None, examples_dir
                                )
                                if extracted_file:
                                    relative_path = os.path.relpath(extracted_file, dir_path)
                                    request_body_examples.append((None, relative_path))

                # Modified: Process responses with separate example files
                response_codes = []
                responses_examples = {}  # Dictionary to hold response examples per status code
                responses_headers = {}   # Dictionary to hold response headers per status code
                response_fhir_profiles = {}  # Dictionary to hold x-fhir-profile per status code
                for code, response in responses.items():
                    resp_description = get_response_description(response, data)
                    resp_type = ''
                    # Determine type based on code
                    if str(code).startswith('2'):
                        resp_type = 'Success'
                    elif str(code).startswith('4'):
                        resp_type = 'Client Error'
                    elif str(code).startswith('5'):
                        resp_type = 'Server Error'
                    else:
                        resp_type = 'Unknown'

                    response_codes.append((code, resp_type, resp_description))

                    # Extract x-fhir-profile
                    response_fhir_profiles[code] = get_list(response.get('x-fhir-profile'))

                    # Extract response headers
                    headers = response.get('headers', {})
                    header_list = []
                    for header_name, header_info in headers.items():
                        schema = header_info.get('schema', {})
                        header_type = schema.get('type', '')
                        example = schema.get('example', '')
                        required = header_info.get('required', False)
                        required_str = 'required' if required else ''
                        type_info = ''
                        if header_type or required_str:
                            type_info = f" ({header_type}"
                            if required_str:
                                type_info += f", {required_str}"
                            type_info += ")"
                        if header_name == 'Authorization':
                            header_value = f"Authorization: Bearer <JWT>{type_info}"
                        else:
                            if example:
                                header_value = f"{header_name}: {example}{type_info}"
                            else:
                                header_value = f"{header_name}: <value>{type_info}"
                        header_list.append(header_value)
                    responses_headers[code] = header_list

                    # Extract response examples with separate files
                    if 'content' in response:
                        for mime_type, content_details in response['content'].items():
                            if 'examples' in content_details:
                                examples = content_details['examples']
                                for example_name, example_details in examples.items():
                                    example_ref = example_details.get('$ref', '')
                                    if example_ref:
                                        extracted_file = download_and_extract_examples(
                                            example_ref, example_name, examples_dir
                                        )
                                        if extracted_file:
                                            relative_path = os.path.relpath(extracted_file, dir_path)
                                            responses_examples.setdefault(code, []).append((example_name, relative_path))
                            elif 'example' in content_details:
                                example = content_details['example']
                                if isinstance(example, dict) and '$ref' in example:
                                    extracted_file = download_and_extract_examples(
                                        example['$ref'], None, examples_dir
                                    )
                                    if extracted_file:
                                        relative_path = os.path.relpath(extracted_file, dir_path)
                                        responses_examples.setdefault(code, []).append((None, relative_path))
                                elif '$ref' in content_details:
                                    extracted_file = download_and_extract_examples(
                                        content_details['$ref'], None, examples_dir
                                    )
                                    if extracted_file:
                                        relative_path = os.path.relpath(extracted_file, dir_path)
                                        responses_examples.setdefault(code, []).append((None, relative_path))

                ### Generate Request File ###
                with open(output_file_request, 'w', encoding='utf-8') as adoc_file:
                    adoc_lines = []

                    # Build the Request section
                    adoc_lines.append('==== Request')  # Level 4 heading
                    adoc_lines.append(f'[cols="h,a", width="100%", separator=¦]')
                    adoc_lines.append('[%autowidth]')
                    adoc_lines.append('|===')
                    adoc_lines.append(f'¦URI        ¦{uri_formatted}')
                    adoc_lines.append(f'¦Method     ¦{http_method}')

                    # Include Requester images based on 'x-allowed-requester' array
                    if allowed_requesters:
                        images = ''.join([f'image:{{{requester}}}[] ' for requester in allowed_requesters])
                        adoc_lines.append(f'¦Requester  ¦{images.strip()}')

                    # Add HTTP Headers
                    adoc_lines.append('¦HTTP Header ¦')
                    adoc_lines.append('----')
                    if request_headers:
                        adoc_lines.extend(request_headers)
                    adoc_lines.append('----')

                    # Include Query Parameters if any
                    if query_parameters:
                        adoc_lines.append('¦Query Parameters ¦')
                        adoc_lines.append('----')
                        adoc_lines.extend(query_parameters)
                        adoc_lines.append('----')

                    # Add Payload
                    adoc_lines.append('¦Payload    ¦')

                    if request_body_examples:
                        for example_name, example_ref in request_body_examples:
                            label = f"Request Body"
                            if example_name:
                                label += f" für {example_name}"
                            adoc_lines.append(f'.{label} (Klicken zum Ausklappen)')
                            adoc_lines.append('[%collapsible]')
                            adoc_lines.append('====')
                            # Determine the file extension and set the source language
                            extension = os.path.splitext(example_ref)[1].lower()
                            if extension == '.xml':
                                source_lang = 'xml'
                            elif extension == '.json':
                                source_lang = 'json'
                            else:
                                source_lang = ''
                            adoc_lines.append(f'[source,{source_lang}]')
                            adoc_lines.append('----')
                            adoc_lines.append(f'include::{example_ref}[]')
                            adoc_lines.append('----')
                            adoc_lines.append('====')
                            # Add FHIR-Profil line if present
                            if request_body_fhir_profile:
                                for url in request_body_fhir_profile:
                                    name = url.rstrip('/').split('/')[-1]
                                    adoc_lines.append(f"FHIR-Profil: link:{url}[{name}]")
                                    adoc_lines.append('\n')
                    else:
                        adoc_lines.append('No request body.')

                    adoc_lines.append('|===')
                    adoc_lines.append('')

                    # Write the adoc_lines to the file
                    adoc_content = '\n'.join(adoc_lines)
                    adoc_file.write(adoc_content)

                ### Generate Response File ###
                with open(output_file_response, 'w', encoding='utf-8') as adoc_file:
                    adoc_lines = []

                    # Build the Response section
                    adoc_lines.append('==== Response')  # Level 4 heading
                    adoc_lines.append('')
                    adoc_lines.append(f'[cols="h,a", width="100%", separator=¦]')
                    adoc_lines.append('[%autowidth]')
                    adoc_lines.append('|===')

                    # Combine response headers across all status codes
                    combined_response_headers = []
                    for code, headers_list in responses_headers.items():
                        combined_response_headers.extend(headers_list)
                    adoc_lines.append('¦HTTP Header ¦')
                    adoc_lines.append('----')
                    if combined_response_headers:
                        adoc_lines.extend(combined_response_headers)
                    adoc_lines.append('----')

                    # Add Payload
                    adoc_lines.append('¦Payload    ¦')

                    any_response_examples = False
                    for code, examples_list in responses_examples.items():
                        for example_name, example_ref in examples_list:
                            any_response_examples = True
                            label = f"Response Body ({code})"
                            if example_name:
                                label += f" für {example_name}"
                            adoc_lines.append(f'.{label} (Klicken zum Ausklappen)')
                            adoc_lines.append('[%collapsible]')
                            adoc_lines.append('====')
                            # Determine the file extension and set the source language
                            extension = os.path.splitext(example_ref)[1].lower()
                            if extension == '.xml':
                                source_lang = 'xml'
                            elif extension == '.json':
                                source_lang = 'json'
                            else:
                                source_lang = ''
                            adoc_lines.append(f'[source,{source_lang}]')
                            adoc_lines.append('----')
                            adoc_lines.append(f'include::{example_ref}[]')
                            adoc_lines.append('----')
                            adoc_lines.append('====')
                            # Add FHIR-Profil line if present
                            if code in response_fhir_profiles and response_fhir_profiles[code]:
                                for url in response_fhir_profiles[code]:
                                    name = url.rstrip('/').split('/')[-1]
                                    adoc_lines.append(f"FHIR-Profil: link:{url}[{name}]")
                                    adoc_lines.append('\n')
                    if not any_response_examples:
                        adoc_lines.append('No response body.')

                    adoc_lines.append('')
                    adoc_lines.append('2+¦Response Codes')

                    for code, resp_type, desc in response_codes:
                        adoc_lines.append('')
                        adoc_lines.append(f'¦{code} ¦ {resp_type} +')
                        adoc_lines.append(f'[small]#{desc}#')

                    adoc_lines.append('')
                    adoc_lines.append('|===')

                    # Write the adoc_lines to the file
                    adoc_content = '\n'.join(adoc_lines)
                    adoc_file.write(adoc_content)
