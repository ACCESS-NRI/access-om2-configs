"""Generic Model class"""
from pathlib import Path


class Model(object):
    def __init__(self, experiment):
        self.experiment = experiment

    def extract_checksums(self, output_directory: Path = None):
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
