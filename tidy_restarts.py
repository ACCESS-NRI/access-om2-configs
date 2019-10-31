#!/usr/bin/env python
"""

Tidy up restart directories - see argparse desciption below.

This is best used with restart_freq: 1 in config.yaml.

Author: Andrew Kiss, ANU

"""

from __future__ import print_function
import os
import sys
from glob import glob

def tidy(yearskip=1, keeplast=6):
    yearskip = abs(yearskip)
    keeplast = max(1, abs(keeplast))  # always keep the last restart
    restarts = glob('archive/restart???')
    restarts.sort()

    keptyear = None
    for r in restarts[:-keeplast]:  # don't touch the most recent |keeplast| restarts
        try:
            fn = os.path.join(r, 'ocean/ocean_solo.res')
            with open(fn, 'r') as f:
                lineList = f.readlines()
                year = int(lineList[-1].split()[0])  # the year of the final time in the run
                if (keptyear is not None) and (year < keptyear+yearskip):
                    print('Moving ' + r + ' to ' + r.replace('archive', 'archive/CHUCKABLE'))
                    os.renames(r, r.replace('archive', 'archive/CHUCKABLE'))
                else:  # always keep the earliest restart, so tidy has a consistent reference point
                    print('Keeping ' + r + ': ending time is' + lineList[-1], end='')
                    keptyear = year
        except:
            print('Error in', fn+':', sys.exc_info())

    for r in restarts[-keeplast:]:  # this just reports dates of the most recent |keeplast| restarts
        try:
            fn = os.path.join(r, 'ocean/ocean_solo.res')
            with open(fn, 'r') as f:
                lineList = f.readlines()
                print('Keeping ' + r + ': ending time is' + lineList[-1], end='')
        except:
            print('Error in', fn+':', sys.exc_info())

    print("Note: it's up to you to delete anything moved to archive/CHUCKABLE")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=
        'Tidy up restart directories, keeping only the most recent \
        --keep-last restarts and the first \
        restart each --year-skip years (counting from the earliest forward, \
        keeping the last one written from the previous year, \
        dated 1 Jan 00:00:00, if available), \
        and moving the rest to archive/CHUCKABLE/ \
        from which the user can delete them manually if needed. \
        This is best used with restart_freq: 1 in config.yaml.')
    parser.add_argument('-y', '--year-skip', type=int,
                        metavar='n', default=1,
                        help="keep one restart every n years")
    parser.add_argument('-k', '--keep-last', type=int,
                        metavar='n', default=6,
                        help="keep last n restarts")
    args = parser.parse_args()
    yearskip = vars(args)['year_skip']
    keeplast = vars(args)['keep_last']
    tidy(yearskip=yearskip, keeplast=keeplast)
