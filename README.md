
# ACCESS-OM2 Model Configurations

## About

This repo contains standard global configurations for
[ACCESS-OM2](https://github.com/ACCESS-NRI/ACCESS-OM2), the ACCESS Ocean-Sea Ice model.

All confgurations were developed by [COSIMA](https://cosima.org) and adapted by ACCESS-NRI.

This is an "omnibus repository": it contains multiple related configurations, and each
configuration is stored in a separate branch.

Branches utilise a naming scheme of specifiers separated by underscores (`_`):

```txt
{resolution}_{atmosforcing}_{forcingmode}[_{option}]
```

Where `resolution` is a representative "nominal resolution" because resolution typically
varies across a global domain; `atmosforcing` is the atmospheric forcing product being
used; `forcingmode` is how the forcing is applied over time; and `option` is additional
options that are necessary to uniquely identify a configuration.

Some examples of possible values of the specifiers:

- **`resolution`**: `1deg` (1&deg;), `025deg` (0.25&deg;), `01deg` (0.1&deg;)
- **`atmosforcing`**: `jra55`, `era5`
- **`forcingmode`**: `iaf` (interannual forcing), `ryf` (repeat year forcing)
- **`option`**: `bgc` (Biogeochemistry)

## Supported configurations

All available configurations are browsable under [the list of branches](https://github.com/ACCESS-NRI/accessom2-configs/branches).

and should also be listed below:

| Branch | Configuration Description |
| ------ | ------------------------- |
| [`release-1deg_jra55_ryf`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-1deg_jra55_ryf) | Global 1&deg; model forced with JRA55-do atmospheric reanalysis in repeat-year forcing mode|
| [`release-1deg_jra55_iaf`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-1deg_jra55_iaf)| Global 1&deg; model forced with JRA55-do atmospheric reanalysis in interannual forcing mode|
| [`release-1deg_jra55_ryf_bgc`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-1deg_jra55_ryf_bgc) | Global 1&deg; model with BGC forced with JRA55-do atmospheric reanalysis in repeat-year forcing mode|
| [`release-1deg_jra55_iaf_bgc`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-1deg_jra55_iaf_bgc)| Global 1&deg; model with BGC forced with JRA55-do atmospheric reanalysis in interannual forcing mode|
| [`release-025deg_jra55_ryf`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-025deg_jra55_ryf) | Global 0.25&deg; model forced with JRA55-do atmospheric reanalysis in repeat-year forcing mode|
| [`release-025deg_jra55_iaf`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-025deg_jra55_iaf)| Global 0.25&deg; model forced with JRA55-do atmospheric reanalysis in interannual forcing mode|
| [`release-025deg_jra55_ryf_bgc`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-025deg_jra55_ryf_bgc) | Global 0.25&deg; model with BGC forced with JRA55-do atmospheric reanalysis in repeat-year forcing mode|
| [`release-025deg_jra55_iaf_bgc`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-025deg_jra55_iaf_bgc)| Global 0.25&deg; model with BGC forced with JRA55-do atmospheric reanalysis in interannual forcing mode|
| [`release-01deg_jra55_ryf`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-01deg_jra55_ryf) | Global 0.1&deg; model forced with JRA55-do atmospheric reanalysis in repeat-year forcing mode|
| [`release-01deg_jra55_iaf`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-01deg_jra55_iaf)| Global 0.1&deg; model forced with JRA55-do atmospheric reanalysis in interannual forcing mode|
| [`release-01deg_jra55_ryf_bgc`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-01deg_jra55_ryf_bgc) | Global 0.1&deg; model with BGC forced with JRA55-do atmospheric reanalysis in repeat-year forcing mode|
| [`release-01deg_jra55_iaf_bgc`](https://github.com/ACCESS-NRI/access-om2-configs/tree/release-01deg_jra55_iaf_bgc)| Global 0.1&deg; model with BGC forced with JRA55-do atmospheric reanalysis in interannual forcing mode|

There are more detailed notes contained in the respective branches for each configuration.

More supported configurations will be added over time.

## How to use this repository to run a model

All configurations use [payu](https://github.com/payu-org/payu) to run the model.

This repository contains many related experimental configurations to make support
and discovery easier. As a user it does not necessarily make sense to clone all the
configurations at once.

In most cases only a single experiment is required. If that is the case choose which experiment and then run

```sh
git clone -b <experiment> https://github.com/ACCESS-NRI/access-om2-configs/ <experiment>
```

and replace `<experiment>` with the branch name or tag of the experiment you wish to run.

[ACCESS-Hive](https://access-hive.org.au/) contains [detailed instructions for how to configure and run ACCESS-OM2 with `payu`](https://access-hive.org.au/models/run-a-model/run-access-om/).

## CI and Reproducibility Checks

This repository makes use of GitHub Actions to perform reproducibility checks on `ACCESS-OM2` config branches.

### Config Branches

Config branches are branches that store model configurations of the form: `release-<config>` or `dev-<config>`, for example: `release-1deg_jra55_iaf`. For more information on creating your own config branches, or for understanding the PR process in this repository, see the [CONTRIBUTING.md](CONTRIBUTING.md).

### Config Tags

Config tags are specific tags on config branches, whose `MAJOR.MINOR` version compares the reproducibility of the configurations. Major version changes denote that a particular config tag breaks reproducibility with tags before it, and a minor version change does not. These have the form: `release-<config>-<tag>`, such as `release-1deg_jra55_iaf-1.2`.

So for example, say we have the following config tags:

- `release-1deg_jra55_iaf-1.0`
- `release-1deg_jra55_iaf-1.1`
- `release-1deg_jra55_iaf-2.0`
- `release-1deg_jra55_iaf-3.0`

This means that `*-1.0` and `*-1.1` are configurations for that particular experiment type that are reproducible with each other, but not any others (namely, `*-2.0` or `*-3.0`).

`*-2.0` is not reproducible with `*-1.0`, `*.1.1` or `*-3.0` configurations.

Similarly, `*-3.0` is not reproducible with `*-1.0`, `*-1.1` or `*-2.0`.

### Checks

These checks are in the context of:

- PR checks: In which a PR creator can modify a config branch, create a pull request, and have their config run and checked for reproducibility against a 'ground truth' version of the config.
- Scheduled checks: In which config branches and config tags that are deemed especially important are self-tested monthly against their own checksums.

More information on submitting a Pull Request and on the specifics of this pipeline can be found in the [CONTRIBUTING.md](./.github/CONTRIBUTING.md) and [README-DEV.md](./README-DEV.md) respectively.

For more information on the manually running the pytests that are run as part of the reproducibility CI checks, see
[model-config-tests](https://github.com/ACCESS-NRI/model-config-tests/).

## Conditions of use

COSIMA request that users of this or other ACCESS-OM2 model code:

1. consider citing Kiss et al. (2020) ([http://doi.org/10.5194/gmd-13-401-2020](http://doi.org/10.5194/gmd-13-401-2020))
2. include an acknowledgement such as that suggested [here](https://cosima.org.au/index.php/get-involved/)
3. let COSIMA know of any publications which use these models or data so they can add them to [their list](https://scholar.google.com/citations?hl=en&user=inVqu_4AAAAJ).
