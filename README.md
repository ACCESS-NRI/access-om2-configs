# 1deg_jra55_iaf with BGC
Standard configuration for 1 degree [ACCESS-OM2](https://github.com/COSIMA/access-om2) experiment (ACCESS-OM2) with JRA55-do interannual forcing (IAF) and coupled biogeochemistry in the ocean and sea ice.

This is the BGC version, on the `master+bgc` branch. For the physics-only version (no BGC), use the `master` branch.

For usage instructions, see the [ACCESS-OM2 wiki](https://github.com/COSIMA/access-om2/wiki).

Run length and timestep are set in `accessom2.nml`. The default timestep for this configuration is 5400 seconds, and the model is stable with this timestep right from the start. However if you alter the configuration you may need a shorter timestep during the first year or two of model equilibration.

**NOTE:** All ACCESS-OM2 model components and configurations are undergoing continual improvement. We strongly recommend that you "watch" this repo (see button at top of screen; ask to be notified of all conversations) and also watch [ACCESS-OM2](https://github.com/COSIMA/access-om2), all the [component models](https://github.com/COSIMA/access-om2/tree/master/src), and [payu](https://github.com/payu-org/payu) to be kept informed of updates, problems and bug fixes as they arise.

The default setup will run the model with physics only. To run the model with BGC, do:
```
cd ocean
cp field_table_no_bgc field_table
cat field_table_bgc >> field_table
cp diag_table_source_no_bgc.yaml diag_table_source.yaml
cat diag_table_source_bgc.yaml >> diag_table_source.yaml
./make_diag_table.py
```

The default BGC setup will include both ocean and sea-ice BGC. To turn off the sea-ice BGC, set `skl_bgc = .false.` in `ice/cice_input.nml`.

To revert to physics-only, do:
```
cd ocean
cp field_table_no_bgc field_table
cp diag_table_source_no_bgc.yaml diag_table_source.yaml
./make_diag_table.py
```
If `archive/restart*` exists, you'll also need to remove any BGC-related files from `archive/restartXXX/ocean`, where `restartXXX` is the latest restart directory.

## Conditions of use

We request that users of this or other ACCESS-OM2 model code:
1. consider citing Kiss et al. (2020) ([http://doi.org/10.5194/gmd-13-401-2020](http://doi.org/10.5194/gmd-13-401-2020))
2. include an acknowledgement such as the following:
*The authors thank the Consortium for Ocean-Sea Ice Modelling in Australia (COSIMA; [http://www.cosima.org.au](http://www.cosima.org.au)) for making the ACCESS-OM2 suite of models available at [https://github.com/COSIMA/access-om2](https://github.com/COSIMA/access-om2).*
3. let us know of any publications which use these models or data so we can add them to [our list](https://scholar.google.com/citations?hl=en&user=inVqu_4AAAAJ).
