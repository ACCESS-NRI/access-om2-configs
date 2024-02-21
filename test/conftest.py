import os
import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def output_path(request):
    """Set the output path: This contains control and lab directories for each
    test and test output files - e.g. CHECKSUMS
    """
    path = request.config.getoption('--output-path')
    if path is None:
        # Set default to /scratch/PROJECT/USER/test-model-repro/
        project = os.environ.get('PROJECT')
        user = os.environ.get('USER')
        path = f'/scratch/{project}/{user}/test-model-repro'
    return Path(path)


@pytest.fixture(scope="session")
def control_path(request):
    """Set the path of the model configuration directory to test"""
    path = request.config.getoption('--control-path')
    if path is None:
        # Set default to current working directory
        path = Path.cwd()
    return Path(path)


@pytest.fixture(scope="session")
def checksum_path(request, control_path):
    """Set the path of the model configuration directory to test"""
    path = request.config.getoption('--checksum-path')
    if path is None:
        # Set default to checksum stored on model configuration
        path = control_path / 'testing' / 'checksum' / 'historical-3hr-checksum.json'
    return Path(path)


# Set up command line options and default for directory paths
def pytest_addoption(parser):
    """Attaches optional command line arguments"""
    parser.addoption("--output-path",
                     action="store",
                     help="Specify the output directory path for test output")

    parser.addoption("--control-path",
                     action="store",
                     help="Specify the model configuration path to test")

    parser.addoption("--checksum-path",
                     action="store",
                     help="Specify the checksum file to compare against")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: mark tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "checksum: mark tests to run as part of reproducibility CI tests"
    )
    config.addinivalue_line(
        "markers", "test: mark tests as testing test functionality"
    )
