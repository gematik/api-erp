#!/usr/bin/env python3
"""
Standalone entry point for running the OpenAPI to AsciiDoc converter directly.
This script can be run from anywhere and will find the correct directories.
"""

import sys
import os

# Add the current directory to Python path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    from main import main
    main()
