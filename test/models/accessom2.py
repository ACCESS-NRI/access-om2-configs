"""Specific Access-OM2 Model setup and post-processing"""

# NOTE for developers: `f90nml` is imported implicitly when this code is running in
# the `Payu` conda environment.
from collections import defaultdict
import f90nml
import re
from pathlib import Path

from models.model import Model

BASE_SCHEMA_URL = "https://raw.githubusercontent.com/ACCESS-NRI/schema/main/au.org.access-nri/model/access-om2/experiment/reproducibility/checksums"

SCHEMA_VERSION_1_0_0 = "1-0-0"
DEFAULT_SCHEMA_VERSION = SCHEMA_VERSION_1_0_0
SUPPORTED_SCHEMA_VERSIONS = [SCHEMA_VERSION_1_0_0]

class AccessOm2(Model):
    def __init__(self, experiment):
        super(AccessOm2, self).__init__(experiment)
        self.output_file = self.experiment.output000 / 'access-om2.out'

        self.accessom2_config = experiment.control_path / 'accessom2.nml'
        self.ocean_config = experiment.control_path / 'ocean' / 'input.nml'
        self.default_schema_version = DEFAULT_SCHEMA_VERSION

    def set_model_runtime(self,
                          years: int = 0,
                          months: int = 0,
                          seconds: int = 10800):
        """Set config files to a short time period for experiment run.
        Default is 3 hours"""
        with open(self.accessom2_config) as f:
            nml = f90nml.read(f)

        nml['date_manager_nml']['restart_period'] = [years, months, seconds]
        nml.write(self.accessom2_config, force=True)

    def output_exists(self):
        """Check for existing output file"""
        return self.output_file.exists()

    def extract_checksums(self,
                          output_directory: Path = None,
                          schema_version: str = None):
        """Parse output file and create checksum using defined schema"""
        if output_directory:
            output_filename = output_directory / 'access-om2.out'
        else:
            output_filename = self.output_file

        # Regex pattern for checksums in the `<model>.out` file
        # Examples:
        # [chksum] ht              -2390360641069121536
        # [chksum] hu               6389284661071183872
        # [chksum] htr               928360042410663049
        pattern = r'\[chksum\]\s+(.+)\s+(-?\d+)'

        # checksums outputted in form:
        # {
        #   "ht": ["-2390360641069121536"],
        #   "hu": ["6389284661071183872"],
        #   "htr": ["928360042410663049"]
        # }
        # with potential for multiple checksums for one key.
        output_checksums: dict[str, list[any]] = defaultdict(list)

        with open(output_filename) as f:
            for line in f:
                # Check for checksum pattern match
                match = re.match(pattern, line)
                if match:
                    # Extract values
                    field = match.group(1).strip()
                    checksum = match.group(2).strip()

                    output_checksums[field].append(checksum)

        if schema_version is None:
            schema_version = DEFAULT_SCHEMA_VERSION

        if schema_version == SCHEMA_VERSION_1_0_0:
            checksums = {
                "schema_version": schema_version,
                "output": dict(output_checksums)
            }
        else:
            raise NotImplementedError(
                f"Unsupported checksum schema version: {schema_version}")

        return checksums
