#!/bin/bash
#PBS -q copyq
#PBS -l ncpus=1
#PBS -l wd
#PBS -l walltime=1:00:00,mem=2GB
#PBS -P v45
#PBS -N RM_SYNCHED_OUTPUT

source sync_output_to_gdata.sh # to define GDATADIR and cd archive

rsync --remove-source-files --exclude "*.nc.*" --exclude "*ocean_*_3hourly*" --exclude "*iceh_03h*" -vrltoD --safe-links output1?? ${GDATADIR}
