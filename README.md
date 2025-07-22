# 1deg_jra55_ryf with WOMBATlite

Standard configuration for 1 degree global [ACCESS-OM2](https://github.com/ACCESS-NRI/access-om2) experiment with JRA55-do 1 May 1990 - 30 April 1991 repeat-year forcing (RYF9091) and WOMBATlite ocean biogeochemistry (BGC). This configuration includes ocean BGC but does not include sea ice BGC.

For usage instructions, see the [ACCESS-Hive docs](https://access-hive.org.au/models/run-a-model/run-access-om/)

Run length and timestep are set in `accessom2.nml`. The default timestep for this configuration is 5400 seconds, and the model is stable with this timestep right from the start. However if you alter the configuration you may need a shorter timestep during the first year or two of model equilibration.

## Conditions of use

COSIMA requests that users of this or other ACCESS-OM2 model code:
1. consider citing Kiss et al. (2020) ([http://doi.org/10.5194/gmd-13-401-2020](http://doi.org/10.5194/gmd-13-401-2020))
2. include an acknowledgement such as the following:
*The authors thank the Consortium for Ocean-Sea Ice Modelling in Australia (COSIMA; [http://www.cosima.org.au](http://www.cosima.org.au)) for making the ACCESS-OM2 suite of models available at [https://github.com/COSIMA/access-om2](https://github.com/COSIMA/access-om2).*
3. let COSIMA know of any publications which use these models or data they can add them to [their list](https://scholar.google.com/citations?hl=en&user=inVqu_4AAAAJ).
