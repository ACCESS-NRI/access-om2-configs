#!/usr/bin/bash
#concatenate sea-ice daily output
#script inspired from https://github.com/COSIMA/1deg_jra55_ryf/blob/master/sync_data.sh#L87-L108

out_dir=$(ls -td archive/output??? | head -1)/ice/OUTPUT #latest output dir only

for f in $out_dir/iceh.????-??-01.nc; do
    #concat daily files for this month
    echo "doing ncrcat -O -L 5 -4 ${f/-01.nc/-??.nc} ${f/-01.nc/-daily.nc}"
    ncrcat -O -L 5 -4 ${f/-01.nc/-??.nc} ${f/-01.nc/-daily.nc} 
    
    if [[ $? == 0 ]]; # ncrcat succeeded
    then 
        #set permissions and delete indidual dailys
        chmod g+r ${f/-01.nc/-daily.nc}
        rm ${f/-01.nc/-??.nc}
    fi
done