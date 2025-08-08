"""
OpenAPI to AsciiDoc Converter Package

This package converts OpenAPI specification files to AsciiDoc format
for documentation generation.
"""

__version__ = "1.0.0"
__author__ = "gematik"

from .main import main
from .utils import get_list, resolve_ref, example_from_schema
from .schema_generator import write_schema_to_adoc
from .request_generator import generate_request_file
from .response_generator import generate_response_file

__all__ = [
    'main',
    'get_list',
    'resolve_ref', 
    'example_from_schema',
    'write_schema_to_adoc',
    'generate_request_file',
    'generate_response_file'
]
