"""Tests for model reproducibility"""

import yaml
import pytest
from pathlib import Path

from exp_test_helper import setup_exp


class TestBitReproducibility():

    @pytest.mark.checksum
    def test_bit_repro_historical(self, output_path: Path, control_path: Path,
                                  checksum_path: Path):
        """
        Test that a run reproduces historical checksums
        """
        # Setup checksum output directory
        # NOTE: The checksum output file is used as part of `repro-ci` workflow
        output_dir = output_path / 'checksum' 
        output_dir.mkdir(parents=True, exist_ok=True)
        checksum_output_file =  output_dir / 'CHECKSUM'
        if checksum_output_file.exists():
            checksum_output_file.unlink()
        
        # Setup and run experiment 
        exp = setup_exp(control_path, output_path, "test_bit_repro_historical")
        exp.model.set_model_runtime()
        exp.setup_and_run()

        assert exp.model.output_exists()

        # Check checksum against historical checksum file
        with open(checksum_path, 'r') as file:
            hist_checksum = yaml.safe_load(file)

        # Parse checksums using the same version
        hist_checksum_version = hist_checksum["schema_version"]

        checksums = exp.extract_checksums(schema_version=hist_checksum_version)

        # Write out checksums to output file
        with open(checksum_output_file, 'w') as file:
            yaml.dump(checksums, file, default_flow_style=False)

        assert hist_checksum == checksums

    @pytest.mark.slow
    def test_bit_repro_repeat(self, output_path: Path, control_path: Path):
        """
        Test that a run has same checksums when ran twice
        """
        exp_bit_repo1 = setup_exp(control_path, output_path,
                                  "test_bit_repro_repeat_1")
        exp_bit_repo2 = setup_exp(control_path, output_path,
                                  "test_bit_repro_repeat_2")

        # Reconfigure to a 3 hours (default) and run
        for exp in [exp_bit_repo1, exp_bit_repo2]:
            exp.model.set_model_runtime()
            exp.setup_and_run()

        # Compare expected to produced.
        assert exp_bit_repo1.model.output_exists()
        expected = exp_bit_repo1.extract_checksums()

        assert exp_bit_repo2.model.output_exists()
        produced = exp_bit_repo2.extract_checksums()

        assert produced == expected

    @pytest.mark.slow
    @pytest.mark.skip(reason="TODO:Check checksum comparision across restarts")
    def test_restart_repro(self, output_path: Path, control_path: Path):
        """
        Test that a run reproduces across restarts.
        """
        # First do two short (1 day) runs.
        exp_2x1day = setup_exp(control_path, output_path,
                               'test_restart_repro_2x1day')

        # Reconfigure to a 1 day run.
        exp_2x1day.model.set_model_runtime(seconds=86400)

        # Now run twice.
        exp_2x1day.setup_and_run()
        exp_2x1day.force_qsub_run()

        # Now do a single 2 day run
        exp_2day = setup_exp(control_path, output_path,
                             'test_restart_repro_2day')
        # Reconfigure
        exp_2day.model.set_model_runtime(seconds=172800)

        # Run once.
        exp_2day.setup_and_run()

        # Now compare the output between our two short and one long run.
        checksums_1d_0 = exp_2x1day.extract_checksums()
        checksums_1d_1 = exp_2x1day.extract_checksums(exp_2x1day.output001)

        # Adding checksums over two outputs might need to be model specific?
        checksums_2x1d = checksums_1d_0['output'] + checksums_1d_1['output']

        checksums_2d = exp_2day.extract_checksums()

        matching_checksums = True
        for item in checksums_2d['output']:
            if item not in checksums_2x1d:
                print("Unequal checksum:", item)
                matching_checksums = False

        if not matching_checksums:
            # Write checksums out to file
            with open(output_path / 'restart-1d-0-checksum.yaml', 'w') as file:
                yaml.dump(checksums_1d_0, file, default_flow_style=False)
            with open(output_path / 'restart-1d-1-checksum.yaml', 'w') as file:
                yaml.dump(checksums_1d_1, file, default_flow_style=False)
            with open(output_path / 'restart-2d-0-checksum.yaml', 'w') as file:
                yaml.dump(checksums_2d, file, default_flow_style=False)

        assert matching_checksums
