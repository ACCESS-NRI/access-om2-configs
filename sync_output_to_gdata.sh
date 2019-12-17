#!/bin/bash
#PBS -q copyq
#PBS -l ncpus=1
#PBS -l wd
#PBS -l walltime=1:00:00,mem=4GB
#PBS -P v45
#PBS -N output_to_gdata

# Set this directory to something in /g/data3/hh5/tmp/cosima/
# Make a unique path for your set of runs.
# DOUBLE-CHECK IT IS UNIQUE SO YOU DON'T OVERWRITE EXISTING OUTPUT!
GDATADIR=/ERROR/SET/GDATADIR/IN/sync_output_to_gdata.sh

mkdir -p ${GDATADIR}
cd archive
rsync --exclude "*.nc.*" --exclude "ocean_daily_3d_*" --exclude "*ocean_*_3hourly*" --exclude "*iceh_03h*" -vrltoD --safe-links output* ${GDATADIR}
rsync -vrltoD --safe-links error_logs ${GDATADIR}
rsync -vrltoD --safe-links pbs_logs ${GDATADIR}
