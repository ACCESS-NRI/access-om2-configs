#!/bin/bash
#PBS -q copyq
#PBS -l ncpus=1
#PBS -l wd
#PBS -l walltime=1:00:00,mem=2GB
#PBS -P v45
#PBS -N RM_SYNCHED_OUTPUT

# This script will sync output to g/data and then remove from archive everything that was successfully synced.
# It should be run interactively.
# It doesn't sync or remove restarts.

# NB: from
# https://download.samba.org/pub/rsync/rsync.html
# --remove-source-files
# This tells rsync to remove from the sending side the files (meaning non-directories) that are a part of the transfer and have been successfully duplicated on the receiving side.
# Note that you should only use this option on source files that are quiescent. If you are using this to move files that show up in a particular directory over to another host, make sure that the finished files get renamed into the source directory, not directly written into it, so that rsync can't possibly transfer a file that is not yet fully written. If you can't first write the files into a different directory, you should use a naming idiom that lets rsync avoid transferring files that are not yet finished (e.g. name the file "foo.new" when it is written, rename it to "foo" when it is done, and then use the option --exclude='*.new' for the rsync transfer).
# 
# Starting with 3.1.0, rsync will skip the sender-side removal (and output an error) if the file's size or modify time has not stayed unchanged.

# As of 14 Sep 2018, raijin has rsync version 3.0.6 so we don't have this protection!
# So include this little warning.

echo "WARNING: do not proceed if there are any running jobs or collations underway."
read -p "Proceed? (y/n) " yesno
case $yesno in
    [Yy] ) break;;
    * ) echo "Cancelled. Wait until all jobs are finished before trying again."; exit 0;;
esac

source sync_output_to_gdata.sh # to define GDATADIR and cd archive

rsync --remove-source-files --exclude "*.nc.*" --exclude "ocean_daily_3d_*" --exclude "*ocean_*_3hourly*" --exclude "*iceh_03h*" -vrltoD --safe-links output??? ${GDATADIR}
