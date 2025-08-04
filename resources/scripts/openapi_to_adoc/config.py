"""
Configuration constants for the OpenAPI to AsciiDoc converter.
"""

import os

# Get the directory where this config file is located
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define input and output folders relative to the script's parent directory
INPUT_FOLDER = os.path.join(SCRIPT_DIR, '..', 'openapi')
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, '..', 'openapi-adoc')

# Supported file extensions for examples
SUPPORTED_EXTENSIONS = ['.xml', '.json']

# Default values
DEFAULT_STRING_EXAMPLE = 'string'
DEFAULT_INTEGER_EXAMPLE = 0
DEFAULT_BOOLEAN_EXAMPLE = True
DEFAULT_NUMBER_EXAMPLE = 0.0
