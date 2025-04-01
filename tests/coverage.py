#!/usr/bin/env python
"""
Test coverage script for the e-learning platform.

This script runs tests with coverage and generates a report.

Usage:
    python tests/coverage.py
"""

import os
import sys
import coverage
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # Set up Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'education.settings.test'
    django.setup()
    
    # Initialize coverage
    cov = coverage.Coverage(
        source=['courses', 'students', 'chat'],
        omit=[
            '*/migrations/*',
            '*/tests.py',
            '*/admin.py',
            '*/apps.py',
        ]
    )
    
    # Start coverage measurement
    cov.start()
    
    # Run tests
    print("Running tests with coverage...")
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(['courses', 'students', 'chat'])
    
    # Stop coverage
    cov.stop()
    cov.save()
    
    if not failures:
        # Generate reports
        print("\n=== COVERAGE REPORT ===")
        cov.report()
        
        # Generate HTML report
        print("\nGenerating HTML report...")
        cov.html_report(directory='htmlcov')
        
        print("\nHTML report generated in 'htmlcov' directory")
        print("Open htmlcov/index.html in your browser to view the report")
    
    print("\n=== TEST SUMMARY ===")
    if failures:
        print(f"❌ TESTS FAILED: {failures} test(s) failed")
    else:
        print("✅ ALL TESTS PASSED!")
    
    # Exit with appropriate code
    sys.exit(bool(failures)) 