"""Tests for checking configs and valid metadata files"""

import pytest
from pathlib import Path
import re
import requests
import json
import jsonschema

import yaml

@pytest.fixture(scope="class")
def config(control_path: Path):
    config_path = control_path / 'config.yaml'
    with open(config_path) as f:
        config_content = yaml.safe_load(f)
    return config_content

@pytest.fixture(scope="class")
def exe_manifest_fullpaths(control_path: Path):
    manifest_path = control_path / 'manifests' / 'exe.yaml'
    with open(manifest_path) as f:
        _, data = yaml.safe_load_all(f)
    exe_fullpaths = {item['fullpath'] for item in data.values()}
    return exe_fullpaths

def insist_array(str_or_array):
    if type(str_or_array) == str:
        str_or_array = [ str_or_array, ]
    return str_or_array

@pytest.mark.config
class TestConfig:
    """Test contents of config.yaml files"""

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
        for model in config.get('submodels',[]):
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
        assert not 'exe' in config or Path(config['exe']).is_absolute(), (
            f"Executable for model should be an absolute path: {config['exe']}"
        )

    def test_absolute_submodel_exe_path(self, config):
        for model in config.get('submodels',[]):
            if 'exe' not in model:
                # Allow models such as couplers that have no executable
                # TODO: Should a similar check be for the top level model?
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
    
    def test_sub_model_exe_paths_in_manifest(self,config,
                                             exe_manifest_fullpaths):
        for model in config.get('submodels',[]):
            if 'exe' in model:
                assert model['exe'] in exe_manifest_fullpaths, (
                    f"Submodel {model['name']} executable path should be in " +
                    f"Manifest file (e.g. manifests/exe.yaml): {config['exe']}"
                )
    
    @pytest.mark.highres
    def test_mppncombine_fast_collate_exe(self, config):
        #TODO: how to check for mppncombine-fast?
        if 'collate' in config:
            assert config['collate']['exe'] == '/g/data/ik11/inputs/access-om2/bin/mppnccombine-fast'

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
            assert 'path' not in config['sync'], (
                "Sync path to remote archive should not be set"
            )


def test_no_scripts_in_top_level_directory(control_path):
    exts = {".py", ".sh"}
    scripts = [p for p in control_path.iterdir() if p.suffix in exts]
    assert scripts == [], (
        "Scripts in top-level directory should be moved to a " + 
        "'tools' sub-directory"
    )


# #TODO: Pointing to main, allows testing to point to recent schema versions, though makes this test code less robust. 
# BASE_SCHEMA_URL = "https://raw.githubusercontent.com/ACCESS-NRI/schema/main/au.org.access-nri/model/output/experiment-metadata/"
# DEFAULT_SCHEMA_VERSION = "1-0-0"


# class TestMetadata:

#     def setup_class(self, control_path):
#         metadata_path = control_path / 'metadata.yaml'
#         with open(metadata_path) as f:
#             self.metadata = yaml.safe_load(f)

#     def test_valid_metadata(self):
#         schema_version = self.metadata.get("schema_version", DEFAULT_SCHEMA_VERSION)
#         schema = get_schema_from_url()



# def test_valid_metadata(control_path):
#     metadata_path = control_path / 'metadata.yaml'
#     with open(metadata_path) as f:
#         metadata = yaml.safe_load(f)
    
#     schema = get_schema_from_url()

#     # Validate checksums against schema
#     jsonschema.validate(instance=metadata, schema=schema)

# #TODO: Move to utils
# def get_schema_from_url(url):
#     """Retrieve schema from github"""
#     response = requests.get(url)
#     assert response.status_code == 200
#     return response.json()
