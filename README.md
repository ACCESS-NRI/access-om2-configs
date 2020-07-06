# 025deg_jra55_ryf
Standard configuration for 0.25 degree [ACCESS-OM2](https://github.com/COSIMA/access-om2) experiment (ACCESS-OM2-025) with JRA55-do 1 May 1990 - 30 April 1991 repeat-year forcing (RYF9091).

For usage instructions, see the [ACCESS-OM2 wiki](https://github.com/COSIMA/access-om2/wiki).

Run length and timestep are set in `accessom2.nml`. The default timestep for this configuration is 1350 seconds, and the model is stable with this timestep right from the start. After the first year or two of model equilibration you may be able to run with a 1800s timestep for faster throughput.

**NOTE:** All ACCESS-OM2 model components and configurations are undergoing continual improvement. We strongly recommend that you "watch" this repo (see button at top of screen; ask to be notified of all conversations) and also watch [ACCESS-OM2](https://github.com/COSIMA/access-om2), all the [component models](https://github.com/COSIMA/access-om2/tree/master/src), and [payu](https://github.com/payu-org/payu) to be kept informed of updates, problems and bug fixes as they arise.
