import pytest
import json
import requests
import yaml
import jsonschema
from pathlib import Path
from unittest.mock import Mock

# import jsonschema

from models.accessom2 import AccessOm2
from models.accessom2 import BASE_SCHEMA_URL, SUPPORTED_SCHEMA_VERSIONS

@pytest.mark.parametrize("version", SUPPORTED_SCHEMA_VERSIONS)
def test_extract_checksums(version):
    # Mock ExpTestHelper
    mock_experiment = Mock()
    mock_experiment.output000 = Path('test/resources')
    mock_experiment.control_path = Path('test/tmp')

    model = AccessOm2(mock_experiment)

    checksums = model.extract_checksums(
        schema_version=version
    )

    # Assert version is set as expected
    assert checksums["schema_version"] == version

    # Check the entire checksum file is expected
    with open(f'test/resources/{version}.yaml', 'r') as file:
        expected_checksums = yaml.safe_load(file)

    assert checksums == expected_checksums

    # Validate checksum file with schema
    schema = get_schema(checksums["schema"])
    with open(f'{BASE_SCHEMA_URL}/{version}.json') as f:
        schema = json.load(f)

    # Validate checksums against schema
    jsonschema.validate(instance=checksums, schema=schema)


def get_schema_from_url(url):
    """Retrieve schema from github"""
    response = requests.get(url)
    assert response.status_code == 200
    return response.json()
