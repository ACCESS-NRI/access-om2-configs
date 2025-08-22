
## Creating remapping weights

The first step in coupling models together is the generation of remapping weights files. The weights files are used by the coupler (OASIS3-MCT or [Tango](https://github.com/DoublePrecision/tango)) at runtime to transfer the coupling fields.

### ESMFRegridWeightGen

For the 1 and 0.25 degree ACCESS-OM configurations OASIS3-MCT/SCRIP has always been used to generate the remapping weights. This approach does not scale well. At 1 deg the generation step takes several minutes, at 0.25 deg it takes 5-6 hours. This approach is impractical for a 0.1 degree grid.

Fortunately [ESMF](https://www.earthsystemcog.org/projects/regridweightgen/) can be used instead. It supports multiprocessing and outputs weights files in a format that OASIS can use during runtime. In effect we are just replacing the SCRIP part of OASIS with ESMF. Furthermore the latest versions also support higher order interpolation schemes.

A tool, make_remap_weights.py, is included within the ACCESS-OM2 repository that uses ESMF to create weights files.

Regenerate the weights:
```
qsub make_remap_weights.sh
```

#### Compiling ESMF_RegridWeightGen
You shouldn't need to do this, as `make_remap_weights.sh` loads the appropriate ESMF module. But just for reference this is done with:

```
cd $ACCESS_OM_DIR/tools/contrib
./build_esmf_on_raijin.sh
```

Check that the new ESMF_RegridWeightGen executable has been built successfully:

```
ls $ACCESS_OM_DIR/tools/contrib/bin/ESMF_RegridWeightGen
```
and then regenerate the weights as above.

### Comparison of OASIS3-MCT/SCRIP and ESMF weight files

This section shows some runtime and error comparisons between OASIS-MCT/SCRIP and ESMF. They pass a field from a CORE2 grid to a MOM 1 degree grid and calculate the conservativeness and runtime of the remapping.

The tests on the 1 degree grid show that EMSF is more conservative than OASIS3-MCT/SCRIP:

| Remapper | Relative Error | Runtime (s) |
|----------|----------------|-------------|
| OASIS-MCT/SCRIP | 9.5e-10 |  118.5      |
| ESMF            | 3.4e-16 |  23.2       |

From the CORE2 to a MOM 0.1 degree grid:

| Remapper | Relative Error | Runtime (s) |
|----------|----------------|-------------|
| OASIS-MCT/SCRIP | -       |  -          |
| ESMF            | 1.6e-14 |  169.7      |


There are no numbers for OASIS on the 0.1 degree grid, this did not complete after several hours. 

The runtimes give the time it takes to build the weights file and remap a single field. They are rough and unoptimised, for example, the OASIS remapping is done in Fortran, while the ESMF one uses Python. 

The OASIS3-MCT/SCRIP error looks high. It might be worth further investigation if this remapping approach is to be used. For the 0.1 degree configuration we are restricted to ESMF in any case for performance reasons.

### Test status

Remapping weight creation and remapping error are tested by [ARCCSS Jenkins](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/job/remapping/)

### Summary

This section introduced new Python tools and packages that can:
 * Generate weight files using the ESMF_RegridWeightGen tool. Using this overcomes performance limitation with OASIS3-MCT/SCRIP and makes it possible to easily build weights files for high resolution grids. 
 * Compare how well ESMF and SCRIP conserve fields passed between atmosphere and ocean grids. This shows that there is no downside to using ESMF over SCRIP.


## Creating OASIS coupling fields restarts

This section describes how to create the initial coupling field restarts. 


## MOM5 diagnostics list

### The list
is here: [MOM_diags.txt](https://github.com/OceansAus/access-om2/blob/master/MOM_diags.txt) (best viewed as "[raw](https://raw.githubusercontent.com/COSIMA/access-om2/master/MOM_diags.txt)").

### Background

A comprehensive tabulation of [MOM5](https://mom-ocean.github.io) diagnostics does not exist. 

A set of Unix commands to generate such a list is offered on p.413 of S. M. Griffies "Elements of the Modular Ocean Model (MOM) 5 (2012 release with updates)" [Technical Report 7, NOAA/Geophysical Fluid Dynamics Laboratory Ocean Group, February 2012] but this does not deal well with diagnostic registrations that span multiple lines. 

The list offered here is more complete, but not without its own problems. Hopefully it will be of some use.

### Caveats

This is a work in progress.

Some of these diags may not actually be available because the functions may not be called.

Also many names are programmatically generated so you have to dive into the code to figure out what they are, eg
```
e:   id_yflux_adv_int_z ( n ) = register_diag_field ( 'ocean_model' , trim ( t_prog ( n ) % name ) // '_yflux_adv_int_z' , grd % tracer_axes_flux_y ( 1 : 2 ) , time % model_time , 'z-integral of cp*rho*dxt*v*temp' , 'Watts' , missing_value = missing_value , range = ( / - 1.e18 , 1.e18 / ) ) 
```
(we are working on dealing with that case)

### How the list was generated
The diag list was produced by [Marshall Ward](https://github.com/marshallward) using [flint](https://github.com/marshallward/flint) to parse the entire MOM codebase via this script (named `parse.py`):
```
   from flint.project import Project

   proj = Project(verbose=True)
   proj.parse('mom5/mom5')
```
The `parse.py` script was run (`python` works fine if 3.x is installed):
```
   python3 parse.py > out
```
The parsed output `out` is then filtered with `grep` to just list the lines with diag_table field registrations:
```
   grep -e "^mom5" -e "= *register_diag_field" out > MOM_diags.txt
```

## Outputting grid files with no processor land masking

MOM5 and CICE5 normally run with processor land masking (no processors allocated to tiles that are all-land), so grid data from production runs has regions which are NaN, which then causes problems with plotting and analysis.

We therefore have separate grid files specially created by a short run with no processor land masking:
```
/g/data/ik11/grids/ocean_grid_01.nc
/g/data/ik11/grids/ocean_grid_025.nc
/g/data/ik11/grids/ocean_grid_10.nc
```

Here's how to do it (using 1 deg as an example)

1. clone the model repo
```
git clone https://github.com/COSIMA/1deg_jra55_ryf.git 1deg_jra55_ryf_grid
cd 1deg_jra55_ryf_grid
```

2. open `config.yaml` to identify the [ocean input directory](https://github.com/COSIMA/1deg_jra55_ryf/blob/e9796f2c1617cbc47ba0e1ab25c30fc084779aff/config.yaml#L32), make a local symbolic copy of it, and remove `ocean_mask_table` so processor masking won't be used, e.g.
```
cp -sr /g/data/ik11/inputs/access-om2/input_20201102/mom_1deg mom_input
rm mom_input/ocean_mask_table
```
3. replace the ocean input directory in `config.yaml` with the full path of the `mom_input` directory you just created. Also use the ocean executable `/g/data/ik11/inputs/access-om2/bin/fms_ACCESS-OM_3256c3e_libaccessom2_d750b4b.x` which incorporates [these changes](https://github.com/mom-ocean/MOM5/commit/3256c3e970c51848e48b82efb14ef93a26cd34aa) to remove the land masking from dxt, dyt, dxu, dyu.
4. set `restart_period = 0, 0, 86400` in `accessom2.nml` to run for 1 model day.
5. `cd ocean`, and edit `diag_table_source.yaml`:

  - in the `defaults` section of `'static 2d grid data'`
     - add `packing: 1` (for double precision)
     - set `file_name_dimension` to the file name you want (e.g. `ocean_grid_10`)
     - comment out everything but `file_name_dimension` in the `file_name` subsection
  - include all the fields you want in the `fields` section of `'static 2d grid data'`, e.g.
```
         fields:
            area_t:
            area_u:
            dxt:
            dxu:
            dyt:
            dyu:
            geolat_c:
            geolat_t:
            geolon_c:
            geolon_t:
```
  - delete everything after this in `diag_table_source.yaml`
6. do `./make_diag_table.py` to regenerate `diag_table`, and check that `diag_table` looks ok

Try running it (`payu run`). It will fail with something like this in `access-om2.err`:
```
FATAL from PE     0: MPP_DEFINE_DOMAINS2D: incorrect number of PEs assigned for this layout and maskmap. Use      240 PEs for this domain decomposition for mom_domain
```
so use this to edit `config.yaml` to set the ocean `ncpus` to the number of PEs suggested.

Run again
```
payu sweep
payu run
```

Hopefully it will work this time! The grid data will be in `archive/output000/ocean/ocean_grid_10.nc` (or whatever filename you used).

[This commit](https://github.com/COSIMA/1deg_jra55_ryf/commit/ff52b251a5fc973e8b644e5a02b2301ec60dbdcc) shows the changes that were made to generate the 1deg grid output (the `ocean/diag_table` changes were generated by `ocean/make_diag_table.py`). **TODO:** update to omit drag_coeff:
            ht:
            hu:
            kmt:
            kmu: