import os
import yaml

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
                # Prepare data for the AsciiDoc file
                # Remove leading '/', replace slashes with underscores, and append method
                path_formatted = path.lstrip('/').replace('/', '_').replace('{', '').replace('}', '')
                http_method = method.upper()
                endpoint_filename = f"{path_formatted}_{http_method}.adoc"

                output_file = os.path.join(dir_path, endpoint_filename)

                with open(output_file, 'w', encoding='utf-8') as adoc_file:
                    # Extracting data
                    uri = path
                    summary = details.get('summary', '')
                    description = details.get('description', '')
                    parameters = details.get('parameters', [])
                    request_body = details.get('requestBody', {})
                    responses = details.get('responses', {})
                    tags = details.get('tags', [])

                    # Select the appropriate server URL based on tags
                    if 'internet' in tags:
                        host = server_url_internet
                    else:
                        host = server_url_default

                    # Construct the full URI
                    uri_formatted = f"{host}{uri}"

                    # Extract 'Requester' and 'Responder' from custom fields
                    requester = details.get('x-requester', None)
                    responder = details.get('x-responder', None)

                    # Request Headers
                    request_headers = []
                    for param in parameters:
                        if param.get('in') == 'header':
                            name = param.get('name', '')
                            required = ' (required)' if param.get('required', False) else ''
                            request_headers.append(f"{name}: <value>{required}")

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

                    # Response Headers (if any)
                    response_headers = ''  # This can be expanded if response headers are defined

                    # Process responses
                    response_codes = []
                    responses_examples = {}  # Dictionary to hold response examples per status code
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

                        # Extract response examples
                        if 'content' in response:
                            for mime_type, content_details in response['content'].items():
                                if 'examples' in content_details:
                                    examples = content_details['examples']
                                    examples_list = []
                                    for example_name, example_details in examples.items():
                                        example_ref = example_details.get('$ref', '')
                                        examples_list.append((example_name, example_ref))
                                    responses_examples[code] = examples_list
                                elif 'example' in content_details:
                                    example = content_details['example']
                                    if isinstance(example, dict) and '$ref' in example:
                                        responses_examples[code] = [(None, example['$ref'])]
                                    elif '$ref' in content_details:
                                        responses_examples[code] = [(None, content_details['$ref'])]

                    # Initialize adoc_content
                    adoc_lines = []

                    # Build the Request section
                    adoc_lines.append('==== Request')
                    adoc_lines.append('[cols="h,a", separator=¦]')
                    adoc_lines.append('[%autowidth]')
                    adoc_lines.append('|===')
                    adoc_lines.append(f'¦URI        ¦{uri_formatted}')
                    adoc_lines.append(f'¦Method     ¦{http_method}')

                    # Include Requester and Responder if available
                    if requester:
                        adoc_lines.append(f'¦Requester  ¦image:{{{requester}}}[]')
                    if responder:
                        adoc_lines.append(f'¦Responder  ¦image:{{{responder}}}[]')

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
                            adoc_lines.append('[source,xml]')
                            adoc_lines.append('----')
                            adoc_lines.append(f'include::{example_ref}[]')
                            adoc_lines.append('----')
                            adoc_lines.append('====')
                    else:
                        adoc_lines.append('No request body.')

                    adoc_lines.append('|===')
                    adoc_lines.append('')

                    # Build the Response section
                    adoc_lines.append('==== Response')
                    adoc_lines.append('')
                    adoc_lines.append('[cols="h,a", separator=¦]')
                    adoc_lines.append('[%autowidth]')
                    adoc_lines.append('|===')
                    adoc_lines.append('¦HTTP Header ¦')
                    adoc_lines.append('----')
                    # If you have response headers, include them here
                    # adoc_lines.extend(response_headers)
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
                            adoc_lines.append('[source,xml]')
                            adoc_lines.append('----')
                            adoc_lines.append(f'include::{example_ref}[]')
                            adoc_lines.append('----')
                            adoc_lines.append('====')
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