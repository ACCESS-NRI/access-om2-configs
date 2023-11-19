
# ACCESS-OM2 Model Configurations

## About

This repo contains standard global configurations for 
[ACCESS-OM2](https://github.com/ACCESS-NRI/ACCESS-OM2), the ACCESS Ocean-Sea Ice model.

All confgurations were developed by [COSIMA](https://cosima.org) and adapted by ACCESS-NRI.

This is an "omnibus repository": it contains multiple related configurations, and each 
configuration is stored in a separate branch. 

Branches utilise a naming scheme of specifiers separated by underscores (`_`):
```
{resolution}_{atmosforcing}_{forcingmode}[_{option}]
```

Where `resolution` is a representative "nominal resolution" because resolution typically 
varies across a global domain; `atmosforcing` is the atmospheric forcing product being 
used; `forcingmode` is how the forcing is applied over time; and `option` is additional 
options  that are necessary to identify. 

Some examples of possible values of the specifiers:
- **`resolution`**: `1deg` (1&deg;), `025deg` (0.25&deg;), `01deg` (0.1&deg;), `005deg` (0.05&deg;)
- **`atmosforcing`**: `jra55`, `era5`
- **`forcingmode`**: `iaf` (interannual forcing), `ryf` (repeat year forcing), `rdf` (repeat decadal forcing)
- **`option`**: `bgc` (Biogeochemistry)

## Supported configurations

All available configurations are browsable under the list of branches

https://github.com/ACCESS-NRI/accessom2-configs/branches

and should also be listed below:

| Branch | Configuration Description |
---|---|
[`1deg_jra55_ryf`](https://github.com/ACCESS-NRI/accessom2-configs/tree/global/1deg/jra55/ryf) | Global 1&deg; model forced with JRA55-do atmospheric reanalysis in repeat-year forcing mode|
[`1deg_jra55_iaf`](https://github.com/ACCESS-NRI/accessom2-configs/tree/global/1deg/jra55/iaf)| Global 1&deg; model forced with JRA55-do atmospheric reanalysis in interannual forcing mode|

There are more detailed notes contained in the respective branches for each configuration.

More supported configurations will be added over time.

## How to use this repository to run a model

All configurations use [payu](https://github.com/payu-org/payu) to run the model. 

This repository contains many related experimental configurations to make support 
and discovery easier. As a user it does not necessarily make sense to clone all the 
configurations at once.

In many (most?) cases only a single experiment that is required. If that is the case choose which experiment and then run 
```
git clone -b <experiment> https://github.com/ACCESS-NRI/accessom2-configs/ <experiment>
```
and replace `<experiment>` with the branch name of the experiment you wish to run. 

[ACCESS-Hive](https://access-hive.org.au/) contains [detailed instructions for how to configure and run ACCESS-OM2 with `payu`](https://access-hive.org.au/models/run-a-model/run-access-om/).

## Conditions of use

COSIMA request that users of this or other ACCESS-OM2 model code:
1. consider citing Kiss et al. (2020) ([http://doi.org/10.5194/gmd-13-401-2020](http://doi.org/10.5194/gmd-13-401-2020))
2. include an acknowledgement such as the following:
*The authors thank the Consortium for Ocean-Sea Ice Modelling in Australia (COSIMA; [http://www.cosima.org.au](http://www.cosima.org.au)) for making the ACCESS-OM2 suite of models available at [https://github.com/COSIMA/access-om2](https://github.com/COSIMA/access-om2).*
3. let them know of any publications which use these models or data so they can add them to [their list](https://scholar.google.com/citations?hl=en&user=inVqu_4AAAAJ).
