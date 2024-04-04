"""Tests for checking configs and valid metadata files"""

from pathlib import Path
import re
import warnings

import pytest
import requests
import jsonschema
import yaml

BASE_SCHEMA_URL = "https://raw.githubusercontent.com/ACCESS-NRI/schema"
BASE_SCHEMA_PATH = "au.org.access-nri/model/output/experiment-metadata"
DEFAULT_SCHEMA_VERSION = "1-0-0"
DEFAULT_SCHEMA_COMMIT = "bfc15e3c6fa20d492ccfa0c4706805d64c531e7c"


@pytest.fixture(scope="class")
def exe_manifest_fullpaths(control_path: Path):
    manifest_path = control_path / 'manifests' / 'exe.yaml'
    with open(manifest_path) as f:
        _, data = yaml.safe_load_all(f)
    exe_fullpaths = {item['fullpath'] for item in data.values()}
    return exe_fullpaths


def insist_array(str_or_array):
    if isinstance(str_or_array, str):
        str_or_array = [str_or_array,]
    return str_or_array


@pytest.mark.config
class TestConfig:
    """General configuration tests"""

    @pytest.mark.parametrize(
        "field", ["project", "shortpath"]
    )
    def test_field_is_not_defined(self, config, field):
        assert field not in config, (
            f"{field} should not be defined: '{field}: {config[field]}'"
        )

    def test_absolute_input_paths(self, config):
        for path in insist_array(config.get('input', [])):
            assert Path(path).is_absolute(), (
                f"Input path should be absolute: {path}"
            )

    def test_absolute_submodel_input_paths(self, config):
        for model in config.get('submodels', []):
            for path in insist_array(model.get('input', [])):
                assert Path(path).is_absolute(), (
                    f"Input path for {model['name']} submodel should be " +
                    f" absolute: {path}"
                )

    def test_no_storage_qsub_flags(self, config):
        qsub_flags = config.get('qsub_flags', '')
        assert 'storage' not in qsub_flags, (
            "Storage flags defined in qsub_flags will be silently ignored"
        )

    def test_runlog_is_on(self, config):
        runlog_config = config.get('runlog', {})
        if isinstance(runlog_config, bool):
            runlog_enabled = runlog_config
        else:
            runlog_enabled = runlog_config.get('enable', True)
        assert runlog_enabled

    def test_absolute_exe_path(self, config):
        assert 'exe' not in config or Path(config['exe']).is_absolute(), (
            f"Executable for model should be an absolute path: {config['exe']}"
        )

    def test_absolute_submodel_exe_path(self, config):
        for model in config.get('submodels', []):
            if 'exe' not in model:
                # Allow models such as couplers that have no executable
                if 'ncpus' in model and model['ncpus'] != 0:
                    pytest.fail(f"No executable for submodel {model['name']}")
                continue

            assert Path(model['exe']).is_absolute(), (
                f"Executable for {model['name']} submodel should be " +
                f"an absolute path: {config['exe']}"
            )

    def test_exe_paths_in_manifest(self, config, exe_manifest_fullpaths):
        if 'exe' in config:
            assert config['exe'] in exe_manifest_fullpaths, (
                f"Model executable path should be in Manifest file " +
                f"(e.g. manifests/exe.yaml): {config['exe']}"
            )

    def test_sub_model_exe_paths_in_manifest(self, config,
                                             exe_manifest_fullpaths):
        for model in config.get('submodels', []):
            if 'exe' in model:
                assert model['exe'] in exe_manifest_fullpaths, (
                    f"Submodel {model['name']} executable path should be in " +
                    f"Manifest file (e.g. manifests/exe.yaml): {config['exe']}"
                )

    def test_restart_freq_is_date_based(self, config):
        assert "restart_freq" in config, "Restart frequency should be defined"
        frequency = config["restart_freq"]
        # String of an integer followed by a YS/MS/W/D/H/T/S unit,
        # e.g. 1YS for 1 year-start
        pattern = r'^\d+(YS|MS|W|D|H|T|S)$'
        assert isinstance(frequency, str) and re.match(pattern, frequency), (
           "Restart frequency should be date-based: " +
           f"'restart_freq: {frequency}'"
        )

    def test_sync_is_not_enabled(self, config):
        if 'sync' in config and 'enable' in config['sync']:
            assert not config['sync']['enable'], (
                "Sync to remote archive should not be enabled"
            )

    def test_sync_path_is_not_set(self, config):
        if 'sync' in config:
            assert not ('path' in config['sync']
                        and config['sync']['path'] is not None), (
                "Sync path to remote archive should not be set"
            )

    def test_manifest_reproduce_exe_is_on(self, config):
        manifest_reproduce = config.get('manifest', {}).get('reproduce', {})
        assert 'exe' in manifest_reproduce and manifest_reproduce['exe'], (
            "Executable reproducibility should be enforced, e.g set:\n" +
            "manifest:\n    reproduce:\n        exe: True"
            )

    def test_metadata_is_enabled(self, config):
        if 'metadata' in config and 'enable' in config['metadata']:
            assert config['metadata']['enable'], (
                "Metadata should be enabled, otherwise new UUIDs will not " +
                "be generated and branching in Payu would not work - as " +
                "branch and UUIDs are not used in the name used for archival."
            )

    def test_experiment_name_is_not_defined(self, config):
        assert 'experiment' not in config, (
            f"experiment: {config['experiment']} should not set, " +
            "as this over-rides the experiment name used for archival. " +
            "If set, branching in payu would not work."
        )

    def test_no_scripts_in_top_level_directory(self, control_path):
        exts = {".py", ".sh"}
        scripts = [p for p in control_path.iterdir() if p.suffix in exts]
        assert scripts == [], (
            "Scripts in top-level directory should be moved to a " +
            "'tools' sub-directory"
        )

    def test_validate_metadata(self, metadata):
        # Get schema from Github
        schema_version = metadata.get("schema_version", DEFAULT_SCHEMA_VERSION)
        schema_path = f"{BASE_SCHEMA_PATH}/{schema_version}.json"
    
        url = f"{BASE_SCHEMA_URL}/main/{schema_path}"
        response = requests.get(url)
        if response.status_code != 200:
            # Use default schema
            warnings.warn(
                f"Failed to retrieve schema from url: {url}\n" +
                f"Defaulting to schema version: {DEFAULT_SCHEMA_VERSION}"
            )
            schema_path = f"{BASE_SCHEMA_PATH}/{DEFAULT_SCHEMA_VERSION}.json"

            url = f"{BASE_SCHEMA_URL}/{DEFAULT_SCHEMA_COMMIT}/{schema_path}"
            response = requests.get(url)
            assert response.status_code == 200
        schema = response.json()

        # In schema version (1-0-0), required fields are name, experiment_uuid,
        # description and long_description. As name & experiment_uuid are
        # generated for running experiments, the required fields are removed
        # from the schema validation for now
        schema.pop('required')

        # Validate field names and types
        jsonschema.validate(instance=metadata, schema=schema)

    @pytest.mark.parametrize(
        "field",
        ["description", "notes", "keywords", "nominal_resolution", "version",
        "reference", "url", "model", "realm"]
    )
    def test_metadata_contains_fields(self, field, metadata):
        assert field in metadata, f"{field} field shoud be defined in metadata"

    def test_metadata_license(self, metadata):
        assert 'license' in metadata and metadata['license'] == 'CC-BY-4.0', (
            "The license should be set to CC-BY-4.0"
            )
