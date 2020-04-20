# 1deg_jra55_ryf
Standard configuration for 1 degree [ACCESS-OM2](https://github.com/COSIMA/access-om2) experiment (ACCESS-OM2) with JRA55-do 1 May 1990 - 30 April 1991 repeat-year forcing (RYF9091).

For usage instructions, see the [ACCESS-OM2 wiki](https://github.com/COSIMA/access-om2/wiki).

Run length and timestep are set in `accessom2.nml`. The timestep is normally set to a factor of the JRA55-do forcing period of 3hr = 10800s, for example one of 100, 108, 120, 135, 144, 150, 180, 200, 216, 225, 240, 270, 300, 360, 400, 432, 450, 540, 600, 675, 720, 900, 1080, 1200, 1350, 1800, 2160, 2700, 3600 or 5400s. The default timestep for this configuration is 5400 seconds, and the model is stable with this timestep right from the start. However if you alter the configuration you may need a shorter timestep during the first year or two of model equilibration.

**NOTE:** All ACCESS-OM2 model components and configurations are undergoing continual improvement. We strongly recommend that you "watch" this repo (see button at top of screen; ask to be notified of all conversations) and also watch [ACCESS-OM2](https://github.com/COSIMA/access-om2), all the [component models](https://github.com/COSIMA/access-om2/tree/master/src), and [payu](https://github.com/payu-org/payu) to be kept informed of updates, problems and bug fixes as they arise.
