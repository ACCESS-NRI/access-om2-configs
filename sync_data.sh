#!/bin/bash
#PBS -q copyq
#PBS -l ncpus=1
#PBS -l wd
#PBS -l walltime=4:00:00,mem=4GB
#PBS -P v45
#PBS -l storage=gdata/hh5+gdata/ik11+scratch/v45
#PBS -N sync

# Set SYNCDIR to the path you want your data copied to.
# This must be a unique absolute path for your set of runs.
# If you want to share your data, use SYNCDIR=/g/data/ik11/outputs/<your expt name>
# but first add an experiment description - see /g/data/ik11/outputs/README
# DOUBLE-CHECK SYNCDIR PATH IS UNIQUE SO YOU DON'T OVERWRITE EXISTING OUTPUT!
SYNCDIR=/ERROR/SET/SYNCDIR/IN/sync_data.sh

exitcode=0
help=false
restarts=false
rmlocal=false

# parse argument list
while [ $# -ge 1 ]; do
    case $1 in
        -h)
            help=true
            ;;
        -r)
            echo "syncing restarts instead of output directories"
            restarts=true
            ;;
        -D)
        # --remove-source-files tells rsync to remove from the sending side the files (meaning non-directories) 
        # that are a part of the transfer and have been successfully duplicated on the receiving side.
        # This option should only be used on source files that are quiescent.
        # Require interaction here to avoid syncing and removing partially-written files.
            echo "DELETING LOCAL COPIES OF SYNCED FILES!"
            echo "WARNING: to avoid losing data, do not proceed if there are any running jobs or collations underway."
            read -p "Proceed? (y/n) " yesno
            case $yesno in
                [Yy] ) rmlocal=true;;
                * ) echo "Cancelled. Wait until all jobs are finished before trying again."; exit 0;;
            esac
            ;;
        -*)
            echo $1": invalid option"
            help=true
            exitcode=1
            ;;
        *)
            echo $1": invalid argument"
            help=true
            exitcode=1
            ;;
    esac
    shift
done

if [ $exitcode != "0" -o $help == true ]; then
    echo $0": rsync model run outputs (and optionally restarts) to another location."
    echo "  Must be invoked from a control directory."
    echo "  "$0" should be edited to set SYNCDIR."
    echo "  Default will rsync all output directories, leaving local copies intact."
    echo "  Also rsyncs error_logs and pbs_logs."
    echo "  Also updates git-runlog, a git clone of the control directory (whose git history documents all changes in the run)."
    echo "usage: "$0" [-h] [-r] [-D]"
    echo "  -h: show this help message and exit"
    echo "  -r: sync all restart directories (default syncs output directories)"
    echo "  -D: delete local copies of synced files in all but the most recent synced directories (outputs or restarts, depending on -r). Must be done interactively. (Default leaves local copies intact.)"
    exit $exitcode
fi

sourcepath="$PWD"
mkdir -p ${SYNCDIR} || exit 1
cd archive || exit 1

if [ $restarts == true ]; then
    # only sync/remove restarts
    rsync -vrltoD --safe-links restart* ${SYNCDIR}
    if [ $rmlocal == true ]; then
        # Now do removals. Don't remove final local copy, so we can continue run.
        rsync --remove-source-files --exclude `\ls -1d restart[0-9][0-9][0-9] | tail -1` -vrltoD --safe-links restart* ${SYNCDIR}
    fi
else
    # default - only sync/remove outputs
    rsync --exclude "*.nc.*" --exclude "ocean_daily_3d_*" --exclude "*ocean_*_3hourly*" --exclude "*iceh_03h*" -vrltoD --safe-links output* ${SYNCDIR}
    if [ $rmlocal == true ]; then
        # Now do removals. Don't remove final local copy, so we can continue run.
        rsync --remove-source-files --exclude `\ls -1d output[0-9][0-9][0-9] | tail -1` --exclude "*.nc.*" --exclude "ocean_daily_3d_*" --exclude "*ocean_*_3hourly*" --exclude "*iceh_03h*" -vrltoD --safe-links output* ${SYNCDIR}
    fi
fi

# Also sync error and PBS logs
rsync -vrltoD --safe-links error_logs ${SYNCDIR}
rsync -vrltoD --safe-links pbs_logs ${SYNCDIR}

# create/update a clone of the run history in ${SYNCDIR}/git-runlog
cd ${SYNCDIR} || exit 1
ls git-runlog || git clone $sourcepath git-runlog
cd git-runlog
git pull

echo $0" completed successfully"