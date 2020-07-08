#!/bin/bash
#PBS -q copyq
#PBS -l ncpus=1
#PBS -l wd
#PBS -l walltime=4:00:00,mem=4GB
#PBS -l storage=gdata/hh5+gdata/ik11+scratch/v45+scratch/x77+scratch/g40
#PBS -N sync

# Set SYNCDIR to the path you want your data copied to.
# This must be a unique absolute path for your set of runs.
# To share your data, sync to a subdirectory in /g/data/ik11/outputs/
# but first add an experiment description - see /g/data/ik11/outputs/README
# and make sure metadata.yaml is correct.
# DOUBLE-CHECK SYNCDIR PATH IS UNIQUE SO YOU DON'T OVERWRITE EXISTING OUTPUT!
SYNCDIR=/ERROR/SET/SYNCDIR/IN/sync_data.sh

exitcode=0
help=false
dirtype=output
exclude="--exclude *.nc.*"
rsyncflags="-vrltoD --safe-links"
rmlocal=false

# parse argument list
while [ $# -ge 1 ]; do
    case $1 in
        -h)
            help=true
            ;;
        -r)
            echo "syncing restarts instead of output directories"
            dirtype=restart
            ;;
        -u)
            echo "ignoring exclusions - syncing collated and uncollated .nc files"
            exclude=""
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
            exitcode=1
            ;;
        *)
            echo $1": invalid argument"
            exitcode=1
            ;;
    esac
    shift
done

if [ $exitcode != "0" -o $help == true ]; then
    echo "$0: rsync model run outputs (and optionally restarts) to another location."
    echo "  Must be invoked from a control directory."
    echo "  $0 should be edited to set SYNCDIR."
    echo "  Default will rsync all output directories, leaving local copies intact."
    echo "  Uncollated .nc files are not rsynced unless the -u option is used."
    echo "  Also rsyncs error_logs and pbs_logs."
    echo "  Also updates git-runlog, a git clone of the control directory (whose git history documents all changes in the run)."
    echo "  Also updates, rsyncs and commits run summary"
    echo "usage: $0 [-h] [-r] [-u] [-D]"
    echo "  -h: show this help message and exit"
    echo "  -r: sync all restart directories instead of output directories"
    echo "  -u: ignore exclusions - sync collated and uncollated .nc files (default is collated only)"
    echo "  -D: delete local copies of synced files in all but the most recent synced directories (outputs or restarts, depending on -r). Must be done interactively. (Default leaves local copies intact.)"
    exit $exitcode
fi

sourcepath="$PWD"
mkdir -p $SYNCDIR || { echo "Error: cannot create $SYNCDIR - edit $0 to set SYNCDIR"; exit 1; }
cd archive || exit 1

# first delete any cice log files that only have a 105-character header and nothing else
find output* -size 105c -iname "ice.log.task_*" -delete

# copy all collated outputs/restarts
rsync $exclude $rsyncflags $dirtype[0-9][0-9][0-9] $SYNCDIR
if [ $rmlocal == true ]; then
    # Now do removals. Don't remove final local copy, so we can continue run.
    rsync --remove-source-files --exclude `\ls -1d $dirtype[0-9][0-9][0-9] | tail -1` $exclude $rsyncflags $dirtype[0-9][0-9][0-9] $SYNCDIR
fi

# Also sync error and PBS logs and metadata.yaml
rsync $rsyncflags error_logs $SYNCDIR
rsync $rsyncflags pbs_logs $SYNCDIR
cd $sourcepath
rsync $rsyncflags metadata.yaml $SYNCDIR

# create/update a clone of the run history in $SYNCDIR/git-runlog
cd $SYNCDIR || exit 1
ls git-runlog || git clone $sourcepath git-runlog
cd git-runlog
git pull --no-rebase

# update and sync run summary - do this last in case it doesn't work
cd $sourcepath
module use /g/data/hh5/public/modules
module load conda/analysis3
module load python3-as-python
./run_summary.py --no_header
rsync $rsyncflags run_summary*.csv $SYNCDIR
git add run_summary*.csv
git commit -m "update run summary"
cd $SYNCDIR/git-runlog && git pull --no-rebase

echo "$0 completed successfully"
