# 1deg_jra55_iaf
Standard configuration for 1 degree [ACCESS-OM2](https://github.com/COSIMA/access-om2) experiment (ACCESS-OM2) with JRA55-do interannual forcing (IAF).

For usage instructions, see the [ACCESS-OM2 wiki](https://github.com/COSIMA/access-om2/wiki).

Run length and timestep are set in `accessom2.nml`. The default timestep for this configuration is 5400 seconds, and the model is stable with this timestep right from the start. However if you alter the configuration you may need a shorter timestep during the first year or two of model equilibration.

**NOTE:** All ACCESS-OM2 model components and configurations are undergoing continual improvement. We strongly recommend that you "watch" this repo (see button at top of screen; ask to be notified of all conversations) and also watch [ACCESS-OM2](https://github.com/COSIMA/access-om2), all the [component models](https://github.com/COSIMA/access-om2/tree/master/src), and [payu](https://github.com/payu-org/payu) to be kept informed of updates, problems and bug fixes as they arise.
