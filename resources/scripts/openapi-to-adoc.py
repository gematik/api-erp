import os
import yaml

def get_list(value):
    if isinstance(value, list):
        return value
    elif value is not None:
        return [value]
    else:
        return []

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

                # Extract request body examples
                request_body_examples = []
                if 'content' in request_body:
                    for mime_type, content_details in request_body['content'].items():
                        if 'examples' in content_details:
                            examples = content_details['examples']
                            for example_name, example_details in examples.items():
                                example_ref = example_details.get('$ref', '')
                                request_body_examples.append((example_name, example_ref))
                        elif 'example' in content_details:
                            example = content_details['example']
                            if isinstance(example, dict) and '$ref' in example:
                                request_body_examples.append((None, example['$ref']))
                            elif '$ref' in content_details:
                                request_body_examples.append((None, content_details['$ref']))

                # Process responses
                response_codes = []
                responses_examples = {}  # Dictionary to hold response examples per status code
                responses_headers = {}   # Dictionary to hold response headers per status code
                response_fhir_profiles = {}  # Dictionary to hold x-fhir-profile per status code
                for code, response in responses.items():
                    resp_description = response.get('description', '')
                    resp_type = ''
                    # Determine type based on code
                    if code.startswith('2'):
                        resp_type = 'Success'
                    elif code.startswith('4'):
                        resp_type = 'Client Error'
                    elif code.startswith('5'):
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

                    # Extract response examples
                    if 'content' in response:
                        for mime_type, content_details in response['content'].items():
                            if 'examples' in content_details:
                                examples = content_details['examples']
                                for example_name, example_details in examples.items():
                                    example_ref = example_details.get('$ref', '')
                                    responses_examples.setdefault(code, []).append((example_name, example_ref))
                            elif 'example' in content_details:
                                example = content_details['example']
                                if isinstance(example, dict) and '$ref' in example:
                                    responses_examples.setdefault(code, []).append((None, example['$ref']))
                                elif '$ref' in content_details:
                                    responses_examples.setdefault(code, []).append((None, content_details['$ref']))

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
