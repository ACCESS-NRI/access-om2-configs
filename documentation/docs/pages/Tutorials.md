## Archiving model output

Check that the line
```
# postscript: sync_output_to_gdata.sh
```
is commented out in `$ACCESS_OM_DIR/control/1deg_jra55_ryf/config.yaml`, or if not, that `GDATADIR` in `sync_output_to_gdata.sh` is in fact where you want output and restarts to be written.
**WARNING: double-check `GDATADIR` so you don't overwrite existing output!** - see below.

## Updating an experiment

**CAUTION: OUT OF DATE!** SEE [ISSUE 42](https://github.com/COSIMA/access-om2/issues/42#issuecomment-346602379)

### Use a git branch for each experiment 

Each experiment can be assigned a separate git branch via
```
git branch expt
git checkout expt
```
where `expt` is the name for your experiment. For clarity it's best if this matches the name of the output directory used for the COSIMA Cookbook (e.g. `1deg_jra55_ryf_spinupN` in the next section).
For that matter you could also put the experiment name as the first line of `$ACCESS_OM_DIR/control/1deg_jra55_ryf/ocean/diag_table` which will make it appear in the MOM output netcdf file metadata as the global title field.

More details [here](https://github.com/COSIMA/access-om2/wiki/Contributing-to-model-configurations). 

## Starting a new experiment using restarts from a previous experiment
**WARNING:** If re-running an identical experiment you _should_ get identical results; however [runs are occasionally not reproducible](https://forum.access-hive.org.au/t/how-do-i-start-a-new-perturbation-experiment/262/5) so you should **always do a test run to check for reproducibility** (identical md5 hashes in `manifests/restart.yaml` for everything but `ocean_barotropic.res.nc.*`).

The first step is to find the correct copy of the configuration files used for the previous experiment. There are a few options here:
- If you are starting from a run that was archived using the `sync_data.sh` script, then there will be a copy of the configuration files from the final state of the run within the `git-runlog` folder within the archive directory. This is also a git repository, so you can see the run history by changing to the `git-runlog` directory and doing `gitk --all &`.
- Many of the run configurations are available from github as branches and/or forks of the [standard configurations](https://github.com/COSIMA/access-om2/tree/master/control). You can clone these and then use `git checkout` to switch the relevant branch or specific commit (use `git branch -va` and/or `gitk --all &` to discover these).
- If you are starting from a standard COSIMA control run, more information can be found here: https://forum.access-hive.org.au/t/access-om2-control-runs/258/18
- Otherwise, you can always ask the person who performed the previous experiment.

The second step is to work out which restart you want to begin from. [run_summary.py](https://github.com/aekiss/run_summary) can help - it will show you which run number corresponds to which date. There's a collection of run summaries in `/g/data/hh5/tmp/cosima/access-om2-run-summaries`.

### Simple case: no date change

It's pretty straightforward if you want to continue from some restart in another experiment and have the start date of your experiment match the date in the initial restart: 

1. git clone the control directory from the experiment you are starting from, e.g. `git clone --no-hardlinks prev_control_dir my_new_experiment`, where `prev_control_dir` is the control directory (or `git-runlog` folder or github URL) of the experiment you're starting from, and `my_new_experiment` is whatever you want to call your new experiment. This creates a new directory `my_new_experiment` that copies the contents of `prev_control_dir`, including its entire git commit history. Using `--no-hardlinks` avoids potential permissions issues in git.
2. `cd my_new_experiment`
3. view your git remotes with `git remote -v`. You may wish to fix `origin` if you don't want it to refer to `prev_control_dir`, e.g. `git remote set-url origin https://github.com/COSIMA/1deg_jra55_iaf.git` if you're using that config.
4. decide which restart you want to start from (let's call it `restart567`). Note that not all run restarts have been kept - e.g they might only be annual or 5-yearly. It's a good idea to check out the branch and commit corresponding to the run that started from `restart567` in case the configuration for that run was different from the latest. First you need to work out the branch and commit you want. Use `git branch -va` and/or `gitk --all &` and/or `git log` to discover the relevant branch and git hash. If there's a `run_summary_*.csv` file in `my_new_experiment` (or `/g/data/hh5/tmp/cosima/access-om2-run-summaries` or the branch of interest in the github repo, e.g. [here](https://github.com/COSIMA/01deg_jra55_iaf/blob/01deg_jra55v140_iaf_cycle2/run_summary_home_156_aek156_payu_01deg_jra55v140_iaf_cycle2.csv)) you can use that to work out the run git hash for each model run number and start date - see [run_summary.py](https://github.com/aekiss/run_summary) for details. Then checkout the commit that generated `restart567`, e.g. `git checkout abc123`.
5. check out a new branch for the new experiment (e.g. `git checkout -b my_new_experiment`; it avoids confusion if this matches your directory name)
6. change `SYNCDIR` in `sync_data.sh` (or `GDATADIR` in `sync_output_to_gdata.sh` in older configurations) to a currently non-existent path (for clarity it should match your branch name from the previous step) **CHANGING SYNCDIR/GDATADIR IS CRUCIAL TO PREVENT POSSIBLE DATA LOSS!**
7. make an `archive`: do `payu setup && payu sweep` which will create an archive directory named the same as the control directory in the archive path (archive path is printed to the terminal during `setup`)
8. copy (or link) the required restart and output directories from the previous experiment (say, `restart123` and `output123`) into the newly created archive directory (you will need the output directory due to this bug https://github.com/payu-org/payu/issues/193)
9. load the conda environment containing `payu`
```bash
module use /g/data/hh5/public/modules
module load conda/analysis3
```
10. run `payu setup` to check the correct restart files are being picked up and added to `manifests/restart.yaml`
11. make whatever other configuration changes you want - e.g. see step 7 [here](https://github.com/COSIMA/access-om2/wiki/Getting-started#quick-start)
12. update `metadata.yaml` to document how your new experiment differs from `prev_control_dir`
13. git commit your changes with an informative message: `git commit -am "rerun from date XXXX to ... bla bla"`
14. sweep with `payu sweep` 
15. run your experiment with `payu run`

### More complicated cases

Things are more complicated if you want to change the run start date, for example continuing with interannual forcing after spinning up with repeat-year forcing.
As an example, the following steps show how the IAF run `01deg_jra55v13_iaf` was started from year 40 in the RYF run `01deg_jra55v13_ryf8485_spinup6`.

Follow steps as above, but the following may also be required:

1. check that `atmosphere/forcing.json` specifies the right forcing files (NB: wildcards such as `*` cannot be used following [this commit](https://github.com/COSIMA/libaccessom2/commit/5ec57165fb132cc28ecba5344701a1bc3cbac10d))
2. check/fix `forcing_start_date` and `forcing_end_date` in `accessom2.nml`
3. check/fix `FORCING_CUR_DATE` and `EXP_CUR_DATE ` in `archive/restart000/accessom2_restart.nml` (you'll probably want `FORCING_CUR_DATE` to be the date of the start of your new run, since CICE will use this if `use_restart_time = .false.` in `ice/cice_in.nml`)
4. check/fix calendar (should be gregorian for IAF, noleap for RYF) and current model time in `archive/restart000/ocean/ocean_solo.res`
5. for the first run you'll need to set `use_restart_time = .false.` in `ice/cice_in.nml`
6. after the first run you'll need to set `use_restart_time = .true.` in `ice/cice_in.nml`

Check `archive/output*/atmosphere/log/matmxx.pe00000.log` to see if the correct forcing files are being read. Also check that `archive/output*/ice/OUTPUT` file dates are correct and that `archive/output*/ocean/time_stamp.out` is correct.

If you can't get this to work you may need alter the timing information in the restart file as discussed [here](https://github.com/COSIMA/libaccessom2/issues/22#issuecomment-520298303).

Be aware that there can be subtle problems with calendars and leap years, which can trigger a `forcing and experiment dates are out of sync` error - see https://github.com/COSIMA/access-om2/issues/117 and https://github.com/COSIMA/access-om2/issues/149. If it doesn't bother you to have the forcing and run dates differing in more than just the year, set `allow_forcing_and_exp_date_mismatch = .true.` in the `date_manager_nml` group in `accessom2.nml`.

### FIXME: integration information from the following conversation

aidan [09:28 AM]
Care to share in case anyone else has the same problem?

nic [10:35 AM]
yes, sorry.
The problem was/is that CICE figures out its restart date based on an offset kept in the netcdf header of the restart file. This offset is from the beginning of the experiment and counted in seconds.
the other models just use a restart date.
the problem was that my experiment start date was different from Andrew, hence the ice restart date calculation came up with something different.
so when I said that I dont see any difference between our configs I wasn't looking very hard.

aidan [10:40 AM]
You had to edit the cice restart file to make this work?

nic [10:41 AM]
no, I had to edit the accessom2.nml to make the forcing_start_date the same as his.
this setup is not very clear/intuitive

however fixing cice date handling might be biting of more than we want to chew

aidan [10:51 AM]
I'm thinking this might be a pretty common thing to want to do, so as long as we have clear guidelines/instructions on how to use someone else's restarts, what to do if you do need to change the model date etc.

## Updating restarts for new bathymetry 

If the MOM bathymetry file (topog.nc) needs to be changed on an existing run it's ocean restarts will need to be fixed up. Otherwise the restarts may not contain valid data at all points. This section describes a method for doing this. [This github issue comment](https://github.com/COSIMA/access-om2/issues/99#issuecomment-401532257) may also be helpful.

The approach taken is to create ocean restart files that match the new bathymetry (we call these the template restarts), then copy over all valid data from restarts for the existing run (call these the old restarts). The end result will be a restart that is the same as the existing run at all points which exist in both the old and the template (we call these the new restarts). Any new points that don't exist in the old restarts will contain whatever existed in the template restarts. This approach is very simple but does have a downside - if the bathymetry has changed a lot then there may be many points whose state is not consistent with the old restarts.

Step by step: 

1. Download topogtools. This contains a simple script that does the copying described above.

```{bash}
git clone https://github.com/COSIMA/topogtools.git
```

2. You'll need template restarts from a run with the new bathymetry. If no previous run exists you'll need to create the restarts with a very short run from rest using the new `topog.nc` and matching CICE and MOM land masks `kmt.nc` and `ocean_mask.nc` as inputs (see step 7; create the land masks with `topogtools/topog2mask.py topog.nc kmt.nc ocean_mask.nc`).

3. Collate the MOM restarts from both the template run with the new bathymetry and the run with the old bathymetry, e.g:

```{bash}
module use /g/data/hh5/public/modules
module load conda/analysis3
payu collate -d template-run/archive/restart000/ocean
payu collate -d old-topo-run/archive/restart123/ocean
```

4. Get an interactive PBS session with additional CPUs and memory, e.g.:

```{bash}
qsub -I -v DISPLAY -q normalbw -l ncpus=4,mem64Gb,walltime=10:00:00,storage=gdata/hh5+gdata/ik11+gdata/cj50
```

(add other `storage` points as appropriate)

5. Run the `fix_restarts.py` script to create new MOM restarts based on the old restarts but with the new bathymetry and any new ocean points filled in with the template, e.g.:

```{bash}
cd topogtools
fix_restarts.py --help
./fix_restarts.py template-run/archive/restart000/ocean old-topo-run/archive/restart123/ocean new-topo-run/archive/restart123/ocean
``` 

This can take quite a while.
Note that `fix_restarts.py` requires Python 3 - you might need to do `module use /g/data/hh5/public/modules; module load conda/analysis3` first.

6. Copy the restart files for the other model components, including the appropriate `kmt.nc`, e.g.:

```{bash}
cp old-topo-run/archive/restart123/accessom2_restart.nml new-topo-run/archive/restart123/
cp -r old-topo-run/archive/restart123/atmosphere new-topo-run/archive/restart123/
cp -r old-topo-run/archive/restart123/ice new-topo-run/archive/restart123/
cp template-run/archive/restart000/ice/kmt.nc new-topo-run/archive/restart123/ice
```

7. Edit submodel input directories in `config.yaml` to ensure that MOM is using `topog.nc` and the matching land mask `ocean_mask.nc`, and that CICE is using the matching land mask `kmt.nc`. You might want to do `payu setup` to check that the resulting work directory links to the correct input files (then `payu sweep` to tidy up).

The configuration should now be ready to run.

## Scaling the forcing fields

YATM supports the scaling and offsetting of forcing (e.g. JRA55-do) fields. This can be useful for perturbation experiments or to eliminate occasional timestep-limiting storms. This is controlled by through the `forcing.json` YATM configuration file. A forcing field `f` is perturbed according to:

```
f = scaling(x,y,t)*f + offset(x,y,t)
```

The scaling and offset fields can be multiple and any combination of:

1. An arbitrary spatiotemporal variation, or
2. a sum of (arbitrary spatial patterns multiplied by arbitrary temporal variations), e.g. an EOF reconstruction, or
3. an arbitrary spatial variation (temporally constant), or
4. arbitrary temporal variation (spatially constant), or
5. constant in both space and time

Furthermore the temporal variation can be either:

- referenced to the experiment calendar, allowing progressive changes spanning multiple RYF years (e.g. a ramp over several RYF years), or
- referenced to the forcing calendar, and therefore repeating in each RYF year (e.g. to damp out a storm)

An example of the `forcing.json` syntax is as follows:

```
{
  "description": "JRA55-do V1.3 RYF 1990-91 forcing",
  "inputs": [
    {
      "filename": "/g/data/ua8/JRA55-do/RYF/v1-3/RYF.rsds.1990_1991.nc",
      "fieldname": "rsds",
      "cname": "swfld_ai",
      "perturbations": [
        {
          "type": "scaling",
          "dimension": "spatiotemporal",
          "value": "../test_data/scaling.RYF.rsds.1990_1991.nc",
          "calendar": "forcing",
          "comment": ""
        },
        {
          "type": "offset",
          "dimension": "constant",
          "value": 5,
          "calendar": "forcing",
          "comment": ""
        },
        {
          "type": "separable",
          "dimension": ["temporal", "spatial"],
          "value": ["../test_data/temporal.RYF.rsds.1990_1991.nc", "../test_data/spatial.RYF.rsds.1990_1991.nc"]
          "calendar": "forcing"
          "comment": ""
        },
      ]
    }
 ]
}
```

The `perturbations` list of elements each of which describes how to perform a scaling or offset. Within each element there are 5 configuration fields as follows:

- `"type"`: This can be either `"scaling"`, `"offset"` or `"separable"`. 
- `"dimension"`: This can be either `"spatial"`, `"temporal"`, `"spatiotemporal"`, `"constant"`, or `["temporal", "spatial"]`. The last option is only valid when the `"type"` is `"separable"`.
- `"value"`: Can be a string, an integer/float or list depending on the value for `"dimension"`. For `"spatial"` this needs to be the path to a netcdf with a 2 dimensional variable. For dimension `"temporal"` the perturbation variable should be 1 dimensional. For dimension `"spatiotemporal"` the perturbation variable should be 3 dimensional. For dimension `"constant"` this should be a single float or integer. For dimension `["temporal", "spatial"]` this needs to be a 2-element list with first element being a filename that has a temporal dimension only and second element a filename with a spatial dimension only. 
- `"calendar"`: This can be either `"forcing"` or `"experiment"`.
- `"comment"`: This must be present, even if it is empty.

All of the above five fields must be present in each perturbation element.  

The perturbation netcdf files specified by the `"value"` field should have the same structure (variable and dimension names and order) as the forcing file that it will scale, specified by `"filename"`. Note that the scaling fields only need to be defined for the forcing times they are required.

The scaling values are arbitrary. See [this tutorial](https://github.com/rmholmes/cosima-scripts/blob/master/ACCESS-OM2_forcing_perturbation_tutorial.ipynb) and [this notebook](https://github.com/aekiss/notebooks/blob/master/make-jra55-scaling.ipynb) for examples of how to create them.

There are a couple of things that can be done to sanity check a perturbations configuration. They are:

1. Look at the YATM log file `atmosphere/log/matmxx.pe00000.log`. It contains output that indicates how many perturbations are being applied for a particular field and time point. It also prints a checksum for each atmospheric field being passed to the coupler. This checksum is calculated as the sum of all field values. Therefore it's possible to compare the checksums with and without perturbations and verify that they are as expected. 
2. The ice model (CICE) has a namelist parameter in `cice/input_ice.nml` called `chk_a2i_fields`. If this is set to `.true.` then a file called `ice/fields_a2i_in_ice.nc` will be dumped as the model runs. This contains the coupling fields at every timestep received by the ice model. Try comparing these fields with and without the perturbations.
3. There are detailed tests in `src/libaccessom2/tests/FORCING_SCALING_AND_OFFSET` and `src/libaccessom2/libforcing/test`. The perturbation configuration in these tests can be modified.

Note that, in the case of JRA55-do forcing, if you plan to perturb the surface air temperature without also perturbing the specific humidity then the relative humidity of the air will be altered in a manner which may have unintended impacts on the latent heat flux (e.g. the relative humidity could go outside its physical range, or the air could be unphysically dried out). This can be avoided by providing the relative humidity as a forcing field rather than the specific humidity as described at https://github.com/COSIMA/make_rhuss.

Finally, please look at the reference issues below, they contain a detailed and useful discussion of this feature.  

References: 

- https://github.com/COSIMA/libaccessom2/issues/30
- https://github.com/COSIMA/libaccessom2/issues/31


## Changing the bathymetry, land-sea mask and OASIS remapping weights
This tutorial describes the process to follow when changing the bathymetry and land-sea mask for the purposes of, say, opening a strait or simulating a paleo-oceanographic situation.

### 1. Make your changes to the MOM `topog.nc` file

All changes to the bathymetry are made by creating a custom version of the `topog.nc` located in the MOM folder of the input (e.g. `/g/data/ik11/inputs/access-om2/input_236a3011/mom_1deg` for the 1-degree model). Any locations with a depth greater than 0 will be considered sea points subsequently for mask creation, while anything that has depth 0 (or negative depth) will be considered land. Place the new topography file in your own input folder (e.g. `/scratch/e14/rmh561/access-om2/input/custom_topog_test/mom_1deg/`). This new input folder needs to be refered to in your `config.yaml` in the mom submodule section *above* the default input folder (a similar line is needed to include the other custom input files below):

```
    - name: ocean
      model: mom
      exe: /g/data/ik11/inputs/access-om2/bin/fms_ACCESS-OM_1c1f23e_libaccessom2_b6caeab.x
      input:
         - /scratch/e14/rmh561/access-om2/input/custom_topog_test/mom_1deg
         - /g/data/ik11/inputs/access-om2/input_236a3011/mom_1deg
```

### 2. Changing the associated land–sea masks
Since the input `topog.nc` file has been changed, MOM's & CICE's land-sea masks will also need to be changed to match the new topography. The **topog2mask** script will create the corresponding CICE mask file (`kmt.nc`) and MOM mask file (`ocean_grid.nc`).

Download _topogtools_ via:
```{bash}
git clone https://github.com/COSIMA/topogtools.git
```
This [repository](https://github.com/COSIMA/topogtools) contains a simple python script (`topog2mask.py`) that will create the matching land–sea masks through the command:
`./topog2mask.py topog.nc kmt.nc ocean_mask.nc`

Place the new files in your input folder, referring to them in `config.yaml` above the public inputs (`kmt.nc` in the `cice` submodule).

### 3. Changing the OASIS remapping files
The OASIS coupler is in charge of feeding CICE with the correct atmospheric forcings. To do this, OASIS remaps the atmosphere grid into the corresponding CICE grid according to the remapping weights files specified for each field in the `ATMOSPHERE  --->>>  ICE` section of `namcouple`. The default remapping weights files (`rmp_jra55_cice_conserve.nc` and `rmp_jra55_cice_smooth.nc`) mask out the atmospheric forcings over land. If they are not remade then OASIS will feed the model 0's over every land point, which can result in a variety of errors (e.g. a **division-by-zero** runtime error associated with the air temperature, or problems with the air-sea heat flux, see [Issue 173](https://github.com/COSIMA/access-om2/issues/173).

To remake the mapping files using the new land-sea masks use the script `make_remap_weights.py` in the `access-om2/tools/` directory of [the main access-om2 repository](https://github.com/COSIMA/access-om2). This script needs the `ocean_mask.nc` and `ocean_hgrid.nc` input files from mom (which should be in the `mom_1deg/` subdirectory of your working directory), as well as the JRA55 data directories and the `yatm_1deg` directory (not sure why for this last one?). I used the following command from a qsub script (executed from my `custom_topog_test` working directory) to get this working (where `../../tools/make_remap_weights.py` should point at where your `make_remap_weights.py` script is, which also needs the `esmgrids` subdirectory in that folder).

`../../tools/make_remap_weights.py ./ /g/data/ik11/inputs/JRA-55/RYF/v1-4/ /g/data/ik11/inputs/access-om2/input_236a3011/yatm_1deg/ --atm JRA55 --ocean MOM1 --npes 16`

For an example, see the `make_remap_weights.sh` qsub script in the access-om2 repository. Note that the 1/4-degree and 1/10-degree models likely require more resources and a longer processing time (see the `tools/make_remap_weights.sh` qsub script).

This command produces `JRA55_MOM1_conserve.nc`, `JRA55_MOM1_patch.nc` and `JRA55_MOM1_conserve2nd.nc` remapping weights files that should be copied into a `commmon_1deg_jra55/` input directory and then referenced in `config.yaml` under the common inputs. For example:

```
model: access-om2
input:
     - /scratch/e14/rmh561/access-om2/input/custom_topog_test/common_1deg_jra55
     - /g/data/ik11/inputs/access-om2/input_236a3011/common_1deg_jra55
```

Finally, the `ATMOSPHERE --->>> ICE` section of `namcouple` needs to be changed to refer to these new remap weights files. Replace all appearances of `rmp_jra55_cice_conserve.nc` with `JRA55_MOM1_conserve.nc` and `rmp_jra55_cice_smooth.nc` with `JRA55_MOM1_patch.nc`.

### 4. Checks
You should now be good to go. It is worth doing a `payu setup` to check that all input folders' paths are correct. Note that some of the problems won't neccessarily result in a error being thrown by the model (e.g. incorrect `conserve` remapping weights - see [Issue 173](https://github.com/COSIMA/access-om2/issues/173)). A useful field to look at to check that things are working is the net surface heat flux `net_sfc_heating`. Note that you will likely still have problems if you're trying to restart from a previous run, as the initial conditions won't be defined if you've created new ocean points. However, it will work if starting from WOA initial conditions as these are defined everywhere. See the [Updating restarts for new bathymetry section above](https://github.com/COSIMA/access-om2/wiki/Tutorials#updating-restarts-for-new-bathymetry).
