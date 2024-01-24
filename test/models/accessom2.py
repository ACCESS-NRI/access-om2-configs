"""Specific Access-OM2 Model setup and post-processing"""

import f90nml
import re

from models.model import Model

SCHEMA = "access-om2-checksums"
SCHEMA_VERSION = "1.0"

class AccessOm2(Model):
    def __init__(self, exp):
        super(AccessOm2, self).__init__(exp)
        self.output_file = self.experiment.output000 / 'access-om2.out'
        
        self.accessom2_config = exp.control_path / 'accessom2.nml'
        self.ocean_config = exp.control_path / 'ocean' / 'input.nml'
    
    def set_model_runtime(self, years=0, months=0, seconds=10800):
        """Set config files to a short time period for experiment run. 
        Default is 10800 seconds ~ 3 hours"""
        with open(self.accessom2_config) as f:
            nml = f90nml.read(f)

        # 3 hours: 10800 seconds, 24 hours: 86400 seconds
        nml['date_manager_nml']['restart_period'] = [years, months, seconds]
        nml.write(self.accessom2_config, force=True)
    
    def output_exists(self):
        """Check for existing output file"""
        return self.output_file.exists()
    
    def extract_checksums(self, output_directory=None):
        """Parse output file and create checksum using defined schema"""
        if output_directory:
            filename = output_directory / 'access-om2.out'
        else:
            filename = self.output_file
    
        checksums = {
            "version": SCHEMA_VERSION,
            "schema": SCHEMA,
            "description": "The checksums from access-om2.out after a 3hr run",
            "output": []
        }

        # Regex pattern
        pattern = r'\[chksum\]\s+(.+)\s+(-?\d+)'

        with open(filename) as f:
            for line in f:
                # Check for checksum pattern match
                match = re.match(pattern, line)
                if match:
                    # Extract values
                    checksum_type = match.group(1).strip()
                    checksum_value = match.group(2)

                    # Add to checksums
                    checksums["output"].append({
                        "field": checksum_type,
                        "checksum": checksum_value,
                    })

        # Currently using order in which checksums appear
        #checksums["output"].sort(key=lambda x: x['field'])

        return checksums
