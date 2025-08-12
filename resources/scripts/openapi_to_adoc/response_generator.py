"""
Response file generation for OpenAPI to AsciiDoc conversion.
"""

import os
import json

# Handle both direct execution and package import
try:
    from .utils import get_list, resolve_ref, example_from_schema
    from .request_generator import _add_example_to_adoc, _process_examples
except ImportError:
    from utils import get_list, resolve_ref, example_from_schema
    from request_generator import _add_example_to_adoc, _process_examples


def _process_response_headers(responses):
    """
    Process response headers from all response codes.
    
    Args:
        responses (dict): Response definitions keyed by status code
        
    Returns:
        dict: Dictionary mapping status codes to header lists
    """
    responses_headers = {}
    
    for code, response in responses.items():
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
    
    return responses_headers


def _process_response_codes(responses):
    """
    Process response codes and categorize them.
    
    Args:
        responses (dict): Response definitions keyed by status code
        
    Returns:
        list: List of (code, type, description) tuples
    """
    response_codes = []
    
    for code, response in responses.items():
        resp_description = response.get('description', '')
        
        if str(code).startswith('2'):
            resp_type = 'Success'
        elif str(code).startswith('4'):
            resp_type = 'Client Error'
        elif str(code).startswith('5'):
            resp_type = 'Server Error'
        else:
            resp_type = 'Unknown'
        
        response_codes.append((code, resp_type, resp_description))
    
    return response_codes


def _process_response_examples(responses, data):
    """
    Process examples from response definitions.
    
    Args:
        responses (dict): Response definitions keyed by status code
        data (dict): Complete OpenAPI data for resolving refs
        
    Returns:
        dict: Dictionary mapping status codes to example lists
    """
    responses_examples = {}
    
    for code, response in responses.items():
        if 'content' in response:
            for mime_type, content_details in response['content'].items():
                examples = _process_examples(content_details, data)
                if examples:
                    responses_examples.setdefault(code, []).extend(examples)
    
    return responses_examples


def _process_response_fhir_profiles(responses):
    """
    Process FHIR profiles from response definitions.
    
    Args:
        responses (dict): Response definitions keyed by status code
        
    Returns:
        dict: Dictionary mapping status codes to FHIR profile lists
    """
    response_fhir_profiles = {}
    
    for code, response in responses.items():
        response_fhir_profiles[code] = get_list(response.get('x-fhir-profile'))
    
    return response_fhir_profiles


def generate_response_file(output_file_path, endpoint_data, data):
    """
    Generate a response AsciiDoc file for an OpenAPI endpoint.
    
    Args:
        output_file_path (str): Path to write the response file
        endpoint_data (dict): Processed endpoint data
        data (dict): Complete OpenAPI specification data
    """
    with open(output_file_path, 'w', encoding='utf-8') as adoc_file:
        adoc_lines = []
        
        # Title
        adoc_lines.append('==== Response')
        adoc_lines.append('')
        adoc_lines.append(f'[cols="h,a", width="100%", separator=¦]')
        adoc_lines.append('[%autowidth]')
        adoc_lines.append('|===')
        
        # HTTP Headers (combined from all responses)
        combined_response_headers = []
        for headers_list in endpoint_data["responses_headers"].values():
            combined_response_headers.extend(headers_list)
        
        if combined_response_headers:
            adoc_lines.append('¦HTTP Header ¦')
            adoc_lines.append('----')
            adoc_lines.extend(combined_response_headers)
            adoc_lines.append('----')
        
        # Payload section
        adoc_lines.append('¦Payload ¦')
        
        any_response_examples = False
        for code, examples_list in endpoint_data["responses_examples"].items():
            for example_name, example_ref in examples_list:
                any_response_examples = True
                
                # Check if this is inline JSON content (starts with {, [, or is a quoted JSON string)
                is_inline_json = (example_ref and 
                                 (str(example_ref).strip().startswith('{') or 
                                  str(example_ref).strip().startswith('[') or
                                  (str(example_ref).strip().startswith('"') and str(example_ref).strip().endswith('"'))))
                
                if is_inline_json:
                    adoc_lines.append(f'.Beispiel Response Body ({code})')
                    adoc_lines.append('[source,json]')
                    adoc_lines.append('----')
                    adoc_lines.append(example_ref)
                    adoc_lines.append('----')
                else:
                    label = f"Response Body ({code})"
                    if example_name:
                        label += f" für {example_name}"
                    adoc_lines.append(f'.{label} (Klicken zum Ausklappen)')
                    adoc_lines.append('[%collapsible]')
                    adoc_lines.append('====')
                    
                    extension = os.path.splitext(example_ref)[1].lower() if example_ref else ''
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
                
                # Add FHIR profiles if present
                if code in endpoint_data["response_fhir_profiles"] and endpoint_data["response_fhir_profiles"][code]:
                    for url in endpoint_data["response_fhir_profiles"][code]:
                        name = url.rstrip('/').split('/')[-1]
                        adoc_lines.append(f"FHIR-Profil: link:{url}[{name}]")
                    adoc_lines.append('\n')
        
        if not any_response_examples:
            adoc_lines.append('No response body.')
        
        # Response codes section
        adoc_lines.append('')
        adoc_lines.append('2+¦Response Codes')
        
        for code, resp_type, desc in endpoint_data["response_codes"]:
            adoc_lines.append('')
            adoc_lines.append(f'¦{code} ¦ {resp_type} +')
            adoc_lines.append(f'[small]#{desc}#')
        
        adoc_lines.append('')
        adoc_lines.append('|===')
        
        adoc_content = '\n'.join(adoc_lines)
        adoc_file.write(adoc_content)
