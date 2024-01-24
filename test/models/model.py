"""Generic Model class"""
from pathlib import Path

class Model(object):
    def __init__(self, experiment):
        self.experiment = experiment

    def extract_checksums(self):
        raise NotImplementedError