
This tutorial describes the steps to create a new experiment and to get the model to timestep.

### Compile all models

Instructions for this are [here](https://github.com/OceansAus/access-om). Note the special compile step for CICE at 0.1 degree resolution.

### Create new model input

Input for all models needs to be collected together and placed in $ACCESS_OM_DIR/input/01deg. 
  - The MOM inputs are taken from [this MOM+SIS configuration](https://github.com/aidanheerdegen/mom01v5_kds75.git). 
  - The MATM inputs can be copied from the 1 or 0.25 degree ACCESS-OM configuration, e.g at $ACCESS_OM_DIR/input/025deg. 
  - The CICE inputs output by the tests run in the previous section:
```bash
python -m test -m accessom test/test_remap.py
cd esmgrids
python -m pytest -m cice test/test_grids.py
cd ../
```
  - The OASIS weights and restarts are also created with the command from above:
```bash
python -m test -m accessom test/test_remap.py
```

### Setup MOM configuration (input.nml)

Broadly speaking the approach here is leave all ocean physics related options to be the same as for the MOM+SIS 0.1 degree config, remove all MOM+SIS coupling and SIS (ice) options, and add all ACCESS-OM coupling and time management options from the 0.25 degree ACCESS-OM MOM input.nml. The fresh water treatment also needs to be the same as for ACCESS-OM. 

### Setup CICE configuration (cice_in.nml)

Update the number of PEs used:
```
&domain_nml
    nprocs = 1440
```

### Setup OASIS configuration (namcouple)

Various changes are needed in the OASIS namcouple file:
  - Make sure the names of the remapping weights files are correct. These are the lines beginning with `rmp_`. 
  - Update MOM and CICE resolutions. These are lines with numbers like `1440 1080` or `192 94`.
  - Enable debug output: 

```
$NLOGPRT
2
$END
```
  - To print out field statistics use the `CHECKIN` and `CHECKOUT` options explained in the [OASIS manual](http://www.cerfacs.fr/oa4web/oasis3-mct_3.0/oasis3mct_UserGuide.pdf). 

### Setup the timestep and runtime of all models

To begin with we start with a very short timestep of 100 seconds for the ocean and ice. The coupling timestep between these models also needs to be 100 seconds. 

Changing this is tricky, there are not less than about 20 edits over 5 files! 

1. There are 3 changes needed in `input.nml` used by the ocean. Change `dt_ocean`, `dt_cpl` and `dt_cpld`.
2. In `input_ice.nml` change `dt_cpl_io` and `dt_cice`
3. In `cice_in.nml` change `dt`
4. In `input_atm.nml` change `dt_atm`
5. In the namecouple change the 4th field of the top configuration line for all fields being passed between the ice and ocean (in both directions). Also change the `LAG=+` for all fields passed between the atmosphere and ice (in both directions).

Inconsistencies in model timesteps will lead to very strange and hard to diagnose behaviour. For example deadlock, arcane OASIS error messages or even corrupted fields. 

For the runtimes this needs to be set in seconds and of course be consistent across all models and the coupler. Any inconsistencies here will most likely lead to deadlock at the end of the run. 

1. In `input.nml` set `days = 1` in `ocean_solo_nml`
2. In `input_ice.nml` set `runtime = 86400`
3. In `cice_in.nml` set `ntp = 864`. In this file the total runtime is counted in timesteps.
4. In `input_atm.nml` set `runtime = 86400`
5. In the `namcouple` set `$RUNTIME` to 86400

### Other changes/fixes

- Don't dump coupling fields, MOM crashes in the mpp_global ops. This could be a known problem on Raijin. There were similar problems with MOM+SIS+FMS initialisation when we first tried to run the 10th degree. FIXME: explain this further.
- Remove conservative field smoothing. (Aidan has fixed this in CICE mainline). 

### Run the model!

```{bash}
cd $ACCESS_OM_DIR/01_deg
mpirun -np 2698 $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x \
: -np 1440 $ACCESS_OM_DIR/src/cice4/build_access-om_3600x2700_1440p/cice_access-om_3600x2700_1440p.exe \
: -np 1 $ACCESS_OM_DIR/src/matm/build_nt62/matm_nt62.exe |& tee accessom.out
```

### Check output

With debugging options switched on the models produce a large amount of output in a multitude of different files. Here's a brief description of each:

- accessom.out: this is stdout and stderr from all models combined together. This is the first place to look for model status, errors etc. 
- iceout<number>: these are per-PE output files from CICE. Generally it contains output from the coupling interfaces and ACCESS-OM specific parts of CICE. 
- oceout<number>: as above except for MOM. Presently almost nothing is written to these files.
- atmout85: as above for MATM.
- debug.<model number>.<PE number>: These are per-model, per-PE output files coming from OASIS. There is a summary at the top of each file indicating which model it comes from. In the current configuration `debug.01.<number>` if from CICE, `debug.02.<number>` is from MATM and `debug.03.<number>` is MOM. These files show which coupling fields and being transferred and when.
- nout.000000: a central output from OASIS. Somtimes OASIS errors get printed here. 
- ice_diag.d and ice_diag_out: diagnostic output from CICE.
- logfile.000000.out: a record of all namelist options read in by MOM.

