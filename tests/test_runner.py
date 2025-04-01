#!/usr/bin/env python
"""
Test runner script for the e-learning platform.

This script runs all tests for the project, including:
- Model tests
- View tests
- API tests
- WebSocket tests (if enabled)

Usage:
    python tests/test_runner.py
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'education.settings.test'
    django.setup()
    
    # Get the test runner class
    TestRunner = get_runner(settings)
    
    # Create an instance of the test runner
    test_runner = TestRunner(verbosity=2, interactive=True)
    
    # Set up the test environment
    failures = test_runner.run_tests([
        'courses',
        'students',
        'chat',
    ])
    
    # Output test summary
    print("\n=== TEST SUMMARY ===")
    if failures:
        print(f"❌ TESTS FAILED: {failures} test(s) failed")
    else:
        print("✅ ALL TESTS PASSED!")
    
    # Exit with appropriate code
    sys.exit(bool(failures)) 