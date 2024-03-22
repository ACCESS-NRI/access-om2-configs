"""Generic Model class"""
from pathlib import Path
from typing import Dict, Any


class Model(object):
    def __init__(self, experiment):
        self.experiment = experiment

    def extract_checksums(self,
                          output_directory: Path,
                          schema_version: str):
        """Extract checksums from output directory"""
        raise NotImplementedError

    def set_model_runtime(self,
                          years: int = 0,
                          months: int = 0,
                          seconds: int = 10800):
        """Configure model runtime"""
        raise NotImplementedError

    def output_exists(self):
        """Check for existing output files"""
        raise NotImplementedError

    def check_checksums_over_restarts(self,
                                      long_run_checksum,
                                      short_run_checksum_0,
                                      short_run_checksum_1) -> bool:
        """Compare a checksums from a long run (e.g. 2 days) against
        checksums from 2 short runs (e.g. 1 day)"""
        raise NotImplementedError
