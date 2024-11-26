# conftest.py

import pytest
import os

def pytest_configure(config):
    """
    Pytest configuration hook
    Sets up coverage and other global configurations
    """
    # Ensure JWT_SECRET is set for testing
    os.environ.setdefault("JWT_SECRET", "test_secret_key")

def pytest_addoption(parser):
    """
    Add custom command line options for pytest
    """
    parser.addoption(
        "--runslow", 
        action="store_true", 
        default=False, 
        help="run slow tests"
    )

def pytest_collection_modifyitems(config, items):
    """
    Modify test collection based on markers
    """
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)