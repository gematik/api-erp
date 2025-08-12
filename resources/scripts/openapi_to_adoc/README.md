# OpenAPI to AsciiDoc Converter (Modular Version)

This is a modular version of the OpenAPI to AsciiDoc converter script, refactored for better maintainability and error tracking.

## Structure

The original `openapi-to-adoc.py` script has been split into the following modules:

### Core Modules

- **`__init__.py`** - Package initialization and public API
- **`main.py`** - Main orchestration logic and file processing
- **`config.py`** - Configuration constants and settings
- **`utils.py`** - Utility functions (get_list, resolve_ref, example_from_schema)

### Specialized Generators

- **`schema_generator.py`** - Schema processing and AsciiDoc generation
- **`request_generator.py`** - Request documentation generation
- **`response_generator.py`** - Response documentation generation

## Usage

### Running the Modular Version

```bash
# From the scripts directory
python3 openapi-to-adoc-modular.py
```

### Using as a Python Package

```python
from openapi_to_adoc import main

# Run the converter
main()
```

### Importing Individual Components

```python
from openapi_to_adoc.utils import resolve_ref, example_from_schema
from openapi_to_adoc.schema_generator import write_schema_to_adoc
from openapi_to_adoc.request_generator import generate_request_file
from openapi_to_adoc.response_generator import generate_response_file
```

## Benefits of the Modular Structure

### 1. **Separation of Concerns**
- Each module has a specific responsibility
- Schema generation is isolated from request/response processing
- Utility functions are centralized

### 2. **Improved Maintainability**
- Changes to request generation don't affect response generation
- Bug fixes are easier to locate and implement
- Code is more readable and self-documenting

### 3. **Better Error Tracking**
- Errors can be traced to specific modules
- Each function has clear input/output contracts
- Logging can be added per module for detailed debugging

### 4. **Testability**
- Individual modules can be unit tested
- Mock data can be easily injected
- Edge cases can be tested in isolation

### 5. **Reusability**
- Individual components can be imported and used separately
- Custom processing pipelines can be built
- Extensions can be added without modifying core logic

## Configuration

The `config.py` file contains all configuration constants:

- `INPUT_FOLDER` - Directory containing OpenAPI YAML files
- `OUTPUT_FOLDER` - Directory for generated AsciiDoc files
- `SUPPORTED_EXTENSIONS` - File extensions for examples
- Default values for various data types

## Error Handling

Each module includes proper error handling:

- File I/O errors are caught and reported
- Missing references are handled gracefully
- Invalid schema types are logged with context
- Processing continues even if individual endpoints fail

## Migration from Original Script

The modular version maintains full compatibility with the original script:

- Same input/output directory structure
- Identical generated file formats
- Same command-line interface (via `openapi-to-adoc-modular.py`)

The original `openapi-to-adoc.py` can be kept for backwards compatibility or removed once the modular version is validated.

## Development

### Adding New Features

1. **New generators**: Add to appropriate generator module or create new one
2. **New utilities**: Add to `utils.py`
3. **Configuration changes**: Update `config.py`
4. **Main logic changes**: Modify `main.py`

### Testing

Each module can be tested independently:

```python
# Test utility functions
from openapi_to_adoc.utils import resolve_ref
result = resolve_ref('#/components/schemas/MySchema', openapi_data)

# Test schema generation
from openapi_to_adoc.schema_generator import write_schema_to_adoc
write_schema_to_adoc('TestSchema', schema_data, output_dir)
```

### Debugging

Enable detailed logging by modifying individual modules or adding logging configuration to `main.py`.
