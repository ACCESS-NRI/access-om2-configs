import os
import pytest
from pathlib import Path

import yaml


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


@pytest.fixture(scope="session")
def metadata(control_path: Path):
    """Read the metadata file in the control directory"""
    metadata_path = control_path / 'metadata.yaml'
    with open(metadata_path) as f:
        content = yaml.safe_load(f)
    return content


@pytest.fixture(scope="session")
def config(control_path: Path):
    """Read the config file in the control directory"""
    config_path = control_path / 'config.yaml'
    with open(config_path) as f:
        config_content = yaml.safe_load(f)
    return config_content


@pytest.fixture(scope="session")
def target_branch(request):
    """Set the target branch - i.e., the branch the configuration will be
    merged into. This used is to infer configuration information, if the
    configuration branches follow a common naming scheme (e.g. ACCESS-OM2)"""
    return request.config.getoption('--target-branch')


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
    
    parser.addoption("--target-branch",
                     action="store",
                     help="Specify the target branch name")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: mark tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "test: mark tests as testing test functionality"
    )
    config.addinivalue_line(
        "markers", "checksum: mark tests to run as part of reproducibility CI tests"
    )
    config.addinivalue_line(
        "markers", "config: mark as configuration tests in quick QA CI checks"
    )
    config.addinivalue_line(
        "markers", "access_om2: mark as access-om2 specific tests in quick QA CI checks"
    )
