"""Specific Access-OM2 Model setup and post-processing"""

import f90nml
import re
from pathlib import Path

from models.model import Model

SCHEMA_NAME = "access-om2-checksums.json"
#TODO:
# Depending on where/how schema is stored and versioned:
#BASE_SCHEMA_URL = "https://raw.githubusercontent.com/ACCESS-NRI/schema"

# Add to schema properties:
# "schema": {
#     "type": "string",
#     "const": "https://raw.githubusercontent.com/ACCESS-NRI/schema/access-om2-checksums-v1.0/access-om2-checksums.json"
# }

SCHEMA_VERSION_v1_0 = "access-om2-checksums-v1.0"
DEFAULT_SCHEMA_VERSION = SCHEMA_VERSION_v1_0
SUPPORTED_SCHEMA_VERSIONS = [SCHEMA_VERSION_v1_0]

class AccessOm2(Model):
    def __init__(self, experiment):
        super(AccessOm2, self).__init__(experiment)
        self.output_file = self.experiment.output000 / 'access-om2.out'

        self.accessom2_config = experiment.control_path / 'accessom2.nml'
        self.ocean_config = experiment.control_path / 'ocean' / 'input.nml'

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
        
        # Regex pattern
        pattern = r'\[chksum\]\s+(.+)\s+(-?\d+)'

        output_checksums = []
        with open(output_filename) as f:
            for line in f:
                # Check for checksum pattern match
                match = re.match(pattern, line)
                if match:
                    # Extract values
                    field = match.group(1).strip()
                    checksum = match.group(2).strip()
                    output_checksums.append({
                        "field": field,
                        "checksum": checksum,
                    })

        if schema_version is None:
            schema_version = DEFAULT_SCHEMA_VERSION

        if schema_version == SCHEMA_VERSION_v1_0:
            checksums = {
                "schema_name": SCHEMA_NAME,
                "schema_version": schema_version,
                "output": output_checksums
            }
        else:
            raise NotImplementedError(
                f"Unsupported checksum schema version: {schema_version}")

        # TODO:
        # Add "schema": f"{BASE_SCHEMA_URL}/{schema_version}/{SCHEMA_NAME}""
        # Could remove the schema_name and just keep schema_version for
        # easy extraction of version. 

        return checksums
