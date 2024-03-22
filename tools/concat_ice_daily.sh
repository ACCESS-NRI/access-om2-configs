#!/bin/bash
#concatenate sea-ice daily output
#script inspired from https://github.com/COSIMA/1deg_jra55_ryf/blob/master/sync_data.sh#L87-L108

for d in archive/output*/ice/OUTPUT; do
    for f in $d/iceh.????-??-01.nc; do
        if [[ ! -f ${f/-01.nc/-IN-PROGRESS} ]] && [[ ! -f ${f/-01.nc/-daily.nc} ]];
        then
            touch ${f/-01.nc/-IN-PROGRESS}
            echo "doing ncrcat -O -L 5 -4 ${f/-01.nc/-??.nc} ${f/-01.nc/-daily.nc}"
            ${PAYU_PATH}/ncrcat -O -L 5 -4 ${f/-01.nc/-??.nc} ${f/-01.nc/-daily.nc} && chmod g+r ${f/-01.nc/-daily.nc} && rm ${f/-01.nc/-IN-PROGRESS}
            if [[ ! -f ${f/-01.nc/-IN-PROGRESS} ]] && [[ -f ${f/-01.nc/-daily.nc} ]];
            then
                for daily in ${f/-01.nc/-??.nc}
                do
                    # mv $daily $daily-DELETE  # rename individual daily files - user to delete
                    rm $daily
                done
            else
                rm ${f/-01.nc/-IN-PROGRESS}
            fi
        fi
    done
done