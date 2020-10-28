#!/bin/bash
#PBS -q copyq
#PBS -l ncpus=1
#PBS -l wd
#PBS -l walltime=10:00:00,mem=12GB
#PBS -l storage=gdata/hh5+gdata/ik11+gdata/cj50+scratch/v45+scratch/x77+scratch/g40
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
exclude="--exclude *.nc.* --exclude iceh.????-??-??.nc --exclude *-DEPRECATED --exclude *-DELETE --exclude *-IN-PROGRESS"
rsyncflags="-vrltoD --safe-links"
rmlocal=false
backward=false

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
        -b)
            echo "backward sync (from SYNCDIR to local)"
            backward=true
            ;;
        -D)
        # --remove-source-files tells rsync to remove from the sending side the files (meaning non-directories)
        # that are a part of the transfer and have been successfully duplicated on the receiving side.
        # This option should only be used on source files that are quiescent.
        # Require interaction here to avoid syncing and removing partially-written files.
            echo "DELETING SOURCE COPIES OF SYNCED FILES!"
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
    echo "  -b: backward sync, i.e. from SYNCDIR to local dir (default is from local to SYNCDIR)."
    echo "  -D: delete all source copies (i.e. local copies, or copies on SYNCDIR if -b is used) of synced output or restart files (depending on -r), retaining only the empty directories. Must be done interactively. If -b is not used, the most recent synced local files are not deleted, so model run can continue. Does not delete non-output/restart files. (Default leaves all source copies intact.)"
    exit $exitcode
fi

sourcepath="$PWD"
mkdir -p $SYNCDIR || { echo "Error: cannot create $SYNCDIR - edit $0 to set SYNCDIR"; exit 1; }

# concatenate ice daily files
module load nco
for d in archive/output*/ice/OUTPUT; do
    for f in $d/iceh.????-??.nc; do
        if [[ -f ${f/.nc/-01.nc} ]] && [[ ! -f ${f/.nc/-IN-PROGRESS} ]] && [[ ! -f ${f/.nc/-daily.nc} ]];
        then
            touch ${f/.nc/-IN-PROGRESS}
            echo "doing ncrcat -O -L 5 -7 ${f/.nc/-??.nc} ${f/.nc/-daily.nc}"
            ncrcat -O -L 5 -7 ${f/.nc/-??.nc} ${f/.nc/-daily.nc} && chmod g+r ${f/.nc/-daily.nc} && rm ${f/.nc/-IN-PROGRESS}
            if [[ ! -f ${f/.nc/-IN-PROGRESS} ]] && [[ -f ${f/.nc/-daily.nc} ]];
            then
                for daily in ${f/.nc/-??.nc}
                do
                    # rename individual daily files - user to delete
                    mv $daily $daily-DELETE
                done
            else
                rm ${f/.nc/-IN-PROGRESS}
            fi
        fi
    done
done

cd archive || exit 1

# copy all outputs/restarts
if [ $backward == true ]; then
    rsync $exclude $rsyncflags $SYNCDIR/${dirtype}[0-9][0-9][0-9] .
    if [ $rmlocal == true ]; then
        rsync --remove-source-files $exclude $rsyncflags $SYNCDIR/${dirtype}[0-9][0-9][0-9] .
    fi
    # Also sync error and PBS logs and metadata.yaml and run summary
    rsync $rsyncflags $SYNCDIR/error_logs .
    rsync $rsyncflags $SYNCDIR/pbs_logs .
    cd $sourcepath
    rsync $rsyncflags $SYNCDIR/metadata.yaml .
    rsync $rsyncflags $SYNCDIR/run_summary*.csv .
else
    # normal case: forward sync from current dir to SYNCDIR
    # first delete any cice log files that only have a 105-character header and nothing else
    find output* -size 105c -iname "ice.log.task_*" -delete

    rsync $exclude $rsyncflags ${dirtype}[0-9][0-9][0-9] $SYNCDIR
    if [ $rmlocal == true ]; then
        # Now do removals. Don't remove final local copy, so we can continue run.
        rsync --remove-source-files --exclude `\ls -1d ${dirtype}[0-9][0-9][0-9] | tail -1` $exclude $rsyncflags ${dirtype}[0-9][0-9][0-9] $SYNCDIR
        for d in ${dirtype}[0-9][0-9][0-9]/ice/OUTPUT; do
            rm $d/iceh.????-??-??.nc-DELETE
        done
    fi
    # Also sync error and PBS logs and metadata.yaml and run summary
    rsync $rsyncflags error_logs $SYNCDIR
    rsync $rsyncflags pbs_logs $SYNCDIR
    cd $sourcepath
    rsync $rsyncflags metadata.yaml $SYNCDIR
    rsync $rsyncflags run_summary*.csv $SYNCDIR

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
fi

echo "$0 completed successfully"
