#!/usr/bin/env python3
"""
Installation script for default_test_suite test suite
This script handles the installation and configuration of the test suite.
"""

import json
import os
import shutil
import sys
from pathlib import Path

def main():
    """Main installation function"""
    print(f"Installing default_test_suite test suite...")

    # Detect Django project root (look for manage.py)
    current_dir = Path.cwd()
    django_root = None

    for parent in [current_dir] + list(current_dir.parents):
        if (parent / 'manage.py').exists():
            django_root = parent
            break

    if not django_root:
        print("Error: Could not find Django project root (manage.py not found)")
        sys.exit(1)

    print(f"Found Django project at: {django_root}")

    # Set up paths
    tests_dir = django_root / 'tests'
    suite_path = tests_dir / 'default_test_suite'
    main_config_path = django_root / 'tests' / 'configuration_file_tests.json'

    # Create tests directory
    tests_dir.mkdir(exist_ok=True)

    # Copy test suite (excluding installer script)
    if suite_path.exists():
        response = input(f"Test suite '{suite_path}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            sys.exit(0)
        shutil.rmtree(suite_path)

    # Copy current directory contents (excluding installer)
    current_path = Path(__file__).parent
    shutil.copytree(current_path, suite_path, ignore=shutil.ignore_patterns('install.py'))

    print(f"✓ Test suite copied to {suite_path}")

    # Update main configuration
    try:
        suite_config_path = suite_path / 'configuration_file_tests.json'

        # Load main configuration
        if main_config_path.exists():
            with open(main_config_path, 'r') as f:
                main_config = json.load(f)
        else:
            main_config = {'tests': []}
            main_config_path.parent.mkdir(exist_ok=True)

        # Load suite configuration
        with open(suite_config_path, 'r') as f:
            suite_config = json.load(f)

        # Remove existing tests from this suite
        main_config['tests'] = [
            test for test in main_config['tests']
            if test.get('_suite') != 'default_test_suite'
        ]

        # Add suite tests
        suite_tests_added = 0
        for test in suite_config.get('tests', []):
            if '_suite' not in test:
                test['_suite'] = 'default_test_suite'
            main_config['tests'].append(test)
            suite_tests_added += 1

        # Write updated main configuration
        with open(main_config_path, 'w') as f:
            json.dump(main_config, f, indent=2)

        print(f"✓ Updated main configuration with {suite_tests_added} tests")

    except Exception as e:
        print(f"Warning: Failed to update main configuration: {e}")

    print(f"""
✅ Test suite 'default_test_suite' installed successfully!

Next steps:
  1. Install dependencies: pip install -r tests/default_test_suite/requirements.txt
  2. Run tests: python pybirdai/utils/run_tests.py --config-file tests/configuration_file_tests.json
  3. Edit configuration: tests/default_test_suite/configuration_file_tests.json
""")

if __name__ == '__main__':
    main()
