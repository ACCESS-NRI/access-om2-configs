# 01deg_jra55_iaf with BGC
Standard configuration for 0.1 degree [ACCESS-OM2](https://github.com/COSIMA/access-om2) experiment (ACCESS-OM2-01) with JRA55-do interannual forcing (IAF) and coupled biogeochemistry in the ocean and sea ice.

This is the BGC version.

This BGC setup includes both ocean and sea ice BGC. To turn off the sea ice BGC and have BGC only in the ocean, set `skl_bgc = .false.` in `ice/cice_input.nml`.

For usage instructions, see the [ACCESS-Hive docs](https://access-hive.org.au/models/run-a-model/run-access-om/).

Run length and timestep are set in `accessom2.nml`. The configuration is supplied with a 300s timestep which is stable for a startup from rest, but very slow. **After the model has equilibrated for a few months you should increase the timestep to 450s and then to 540s** for improved throughput. You may even find it runs stably at 600s.

## Conditions of use

COSIMA request that users of this or other ACCESS-OM2 model code:
1. consider citing Kiss et al. (2020) ([http://doi.org/10.5194/gmd-13-401-2020](http://doi.org/10.5194/gmd-13-401-2020))
2. include an acknowledgement such as the following:
*The authors thank the Consortium for Ocean-Sea Ice Modelling in Australia (COSIMA; [http://www.cosima.org.au](http://www.cosima.org.au)) for making the ACCESS-OM2 suite of models available at [https://github.com/COSIMA/access-om2](https://github.com/COSIMA/access-om2).*
3. let COSIMA know of any publications which use these models or data so they can add them to [their list](https://scholar.google.com/citations?hl=en&user=inVqu_4AAAAJ).
