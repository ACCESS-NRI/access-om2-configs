
## Overview

ACCESS-OM2 is a global coupled model with dynamic ocean (MOM v5.1) and ice (CICE v5.2) components and a static or file based atmosphere called YATM. There is no land surface and river-runoff is prescribed. The models exchange coupling fields using the OASIS3-MCT (v2.0) coupler. The JRA55-do model configurations and performance are described in [Kiss et al. (2019)](https://doi.org/10.5194/gmd-2019-106), with further details in the [ACCESS-OM2 technical report](https://github.com/COSIMA/ACCESS-OM2-1-025-010deg-report).

MOM and CICE are flexible models designed to be used in a variety of applications, for example MOM is part of the GFDL CM3 model and CICE is used by the NCAR CESM model. To this end, in both cases, the model design consists of 'core' and 'driver' code. For ACCESS-OM2 major additions to MOM and CICE are generally confined to the ACCESS-OM2 driver within each model. In some cases it has been necessary to modify the core code as well. In the case of MOM all changes are pushed upstream and eventually become part of official repository. In the case of CICE a fork of the official repository is maintained. Any new bugfixes or changes to the official CICE repository are back-ported into the local fork.

Within the ACCESS-OM2 drivers the libaccessom2 libarary is used to acheive common tasks across models and simplify the OAISIS3-MCT interface. The diagram below outlines how all of these parts fit together. The larger grey arrows indicate continuous transfer of coupling fields via the coupler, while the smaller arrows indicate transfer of configuration information between models within libaccessom2.

[[https://github.com/OceansAus/access-om2/blob/master/doc/static/ACCESSOM2_System_Architecture.png|alt="ACCESS-OM2 System Architecture"]]

[[https://user-images.githubusercontent.com/31054815/81232150-b3101c80-9037-11ea-827f-abee1bfa4175.png]]

## Coupling strategy

There are 10 atmospheric forcing fields (including river runoff) which are read from files and passed by YATM to CICE. See [forcing.json](https://github.com/OceansAus/1deg_jra55_iaf/blob/master/atmosphere/forcing.json) as an example specification of these fields. The frequency of the exchange depends on the time resolution of the forcings. For example, in the case of the JRA55 forcing it is every 3 hours, and for CORE2 it is 6 hours. There are 15 fields passed from CICE to MOM and 7 fields passed from MOM back to CICE. The lists of these fields can be found in [input.nml](https://github.com/OceansAus/1deg_jra55_iaf/blob/master/ocean/input.nml) and the [namcouple](https://github.com/OceansAus/1deg_jra55_iaf/blob/master/namcouple). The ice-ocean coupling field exchange happens on each ocean baroclinic timestep, which is the same as the ice thermodynamic timestep.

Broadly speaking, the exchange of coupling fields consists of two main operations: routing and remapping. Given that each submodel is usually a distributed application, routing refers to moving data from one processing element (PE) within a model to the corresponding PE of the other model. For example, the YATM to CICE exchange involves one to many routing where the coupler must divide the source field up and send a small part to each one of the CICE PEs. The CICE to MOM exchange can be quite complex given the number of PEs being used by each model and the fact that there is not necessarily a relationship between geographic location and PE on the CICE side (more about this later). OASIS3-MCT uses [MCT](https://github.com/MCSclimate/MCT) to do routing.

Remapping refers to interpolating fields from one grid to another. In ACCESS-OM2 grid remapping needs to be done to get the atmospheric forcing onto the CICE grid. No remapping is needed between CICE and MOM because they use identical grids. ACCESS-OM2 uses OASIS3-MCT to apply interpolation weights to perform the remapping however the weights files are created offline using a more powerful tool, [ESMF_RegridWeightGen](https://www.earthsystemcog.org/projects/regridweightgen/). Further documentation on how weights files are created can be found [here in the wiki](https://github.com/OceansAus/access-om2/wiki/Technical-documentation#creating-remapping-weights).

## Starting and restarting

When YATM starts it reads the current time ...

When CICE starts ...

When MOM starts ... 

## Load balancing

## CICE block distribution

## Build system


