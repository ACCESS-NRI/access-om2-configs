## Introduction

COSIMA data is published through NCI, which stores, catalogues and provides services to access data collections through a [THREDDS server](http://dapds00.nci.org.au/thredds/catalogs/cj50/catalog.html).

Data as output from the model requires modification before it can be published in this way. This is a HOW-TO guide for the process of making the data suitable for publishing.

Before beginning this process you will need to contact Andy Hogg to get authorisation from NCI that this data set can be published.

## Required data structure and organisation

The general rules are:

1. One variable per file
2. CF-1.6 compliant file
2. Time series split into multiple files of an appropriate size, usually 1 year
3. Files named for the time period and variable, with underscores in variable names replaced with dashes, e.g. `age-global_access-om2-01_193901_193906.nc`
4. Files grouped into sub-directories by variable, and named the same as the variable, e.g.
```
aice-m
├── aice-m_access-om2-01_194301_194312.nc
├── aice-m_access-om2-01_194401_194412.nc
├── aice-m_access-om2-01_194501_194512.nc
└── aice-m_access-om2-01_194601_194612.nc
```
5. Variables from an experiment grouped as subdirectories named for the model type, with a top level directory with a unique experiment name, e.g. for experiment `jra55v13_ryf8485`:
```
jra55v13_ryf8485
├── ocean
│   ├── temp
│   ├── evap
│   ├── runoff
│   ├── u
│   ├── v
│   ├── salt
│   ├── pot-rho-2
│   ├── age-global
│   └── surface-salt
└── ice
    ├── hs-m
    ├── vicen-m
    ├── aice-m
    └── hi-m
```
6. Appropriate meta-data in all files

## Splitting variables

For datasets with multiple diagnostic/tracer variables per file, an initial variable split step is required.

[splitvar](https://github.com/coecms/splitvar) is a python tool developed for this purpose, as well as other transformations for CF compliance, and also generates an appropriate directory structure such that it covers steps 1-6 above. It has a number of options to allow customisation of the process, such as changing calendars, adding in grid information, and selecting or skipping variables.

An example set of scripts to process a suite of 1, 0.25 and 0.1 degree models for ACCESS-OM2 model output:

https://github.com/aidanheerdegen/publish_cosima_data

## Metadata

The last step required is adding and/or changing metadata for CF compliance and NCI publishing requirements.

[addmeta](https://github.com/coecms/addmeta) is a tool for editing meta-data in netCDF files. It takes a number of [YAML](https://yaml.org) formatted files and applies the transformations specified to the selected data files.

There is a repository which contains the meta-data applied to the same model suite above:

https://github.com/COSIMA/metadata

With instructions on how to apply them to the COSIMA model data files. As an example the commands used to apply the metadata for the data collection above are here:

https://github.com/aidanheerdegen/publish_cosima_data/blob/master/add_meta_data.sh

The script uses [gnu parallel](https://www.gnu.org/software/parallel/) to parallelise the operation to speed it up.

## Publishing

NCI will provide a location for the published data. It must be copied there, and then checked by NCI data folks to ensure CF compliance. You can try checking your data for CF compliance, and the [instructions are on the CMS Wiki](http://climate-cms.wikis.unsw.edu.au/CF_checker).
