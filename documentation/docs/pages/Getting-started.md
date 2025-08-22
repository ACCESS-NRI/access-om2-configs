
This page will help you to get to the point of running some basic test cases using ACCESS-OM2. It is divided into several sections:

  1. [Quick start for Gadi users](#quick-start)
  1. [Downloading source code](#downloading-access-om2-and-understanding-the-repository-layout)
  1. [Building the models](#building-the-models)
  1. [Running a test case](#running-a-test-case)
  1. [Checking model output](#checking-model-output)

## Quick start

If you have an account on the [Gadi](http://nci.org.au/our-systems/hpc-systems) supercomputer at [NCI](http://nci.org.au/) you can use pre-built executables and standard configurations to get up and running very quickly.

There are over a dozen supported configurations in these 6 repositories (also included in [access-om2/control](https://github.com/COSIMA/access-om2/tree/master/control)):

* https://github.com/COSIMA/1deg_jra55_ryf.git
* https://github.com/COSIMA/1deg_jra55_iaf.git
* https://github.com/COSIMA/025deg_jra55_ryf.git
* https://github.com/COSIMA/025deg_jra55_iaf.git
* https://github.com/COSIMA/01deg_jra55_ryf.git
* https://github.com/COSIMA/01deg_jra55_iaf.git

These include
- 3 nominal horizontal resolutions: 1° (`1deg`), 0.25° (`025deg`) and 0.1° (`01deg`)
- 2 forcing types: JRA55-do data that repeats 1 May 1990 - 30 April 1991 (`ryf`, repeat-year forcing) or 1 Jan 1958 - 31 Dec 2018 (`iaf`, interannual forcing)
- a `master` branch (for physics-only simulations) and a `master+bgc` branch (that also includes ocean and sea ice biogeochemistry) in each repository

The following steps will run the 1 degree JRA55 RYF configuration `1deg_jra55_ryf`. Analogous steps can be used for any of the others, but **the SU cost, storage and run time of the models increase dramatically at higher resolution** (roughly 0.14 kSU/model year and 100 model years/day at 1°; 7 kSU/yr and 12 yrs/day at 0.25°; 120 kSU/yr and 2 yrs/day at 0.1°; worse with high-frequency output and BGC), so **ensure that you have the computational and storage resources to support your run!**

1. Get an account on NCI and then get membership of an NCI compute project (e.g. CLEX compute projects: `w40`, `w42`, `v45` or `w97`) to charge the model SU usage to, and also projects `qv56`, `ik11` and `hh5` to access the input files and payu - apply at https://my.nci.org.au/mancini/project-search if you need to.

2. Decide on a name for your experiment, ideally one that's unique. _We'll use `1deg_jra55_ryf_demo` as an example here, but you should replace this with your own experiment name._

3. Log in to `gadi.nci.org.au` and download the experiment configuration to your home directory (since [this is backed up](http://climate-cms.wikis.unsw.edu.au/Storage))
```bash
mkdir -p ~/payu
cd ~/payu
git clone https://github.com/COSIMA/1deg_jra55_ryf.git 1deg_jra55_ryf_demo
cd 1deg_jra55_ryf_demo
```

_**Optional**: if using a branch other than `master`, check it out now. E.g. for biogeochemistry, do_
```bash
git checkout master+bgc
```

4. Check out a git branch for your experiment (same as your experiment name)
```bash
git checkout -b 1deg_jra55_ryf_demo
```

5. Model output will be saved on `/scratch` and [will be deleted if unread for 100 days](https://opus.nci.org.au/pages/viewpage.action?pageId=156434436), so it's important to copy your outputs to `/g/data` (this isn't backed up, but at least your files won't be auto-deleted). To do this automatically (but see warnings below),
- Change `SYNCDIR` in `sync_data.sh` to a path in `/g/data` you have write access to. To save confusion this should end with your experiment name (`/1deg_jra55_ryf_demo` in our case). **Double check that this directory does not already exist, otherwise you could lose data!**
- Uncomment the line `# postscript: sync_data.sh` at the end of `config.yaml`

6. Uncomment and modify the `project` and `shortpath` lines in `config.yaml` to reflect your compute project (optional if not different from default). 

7. Make whatever other configuration changes you'd like, e.g.
- run length (`restart_period` in `accessom2.nml`), timestep (`ice_ocean_timestep` in `accessom2.nml`), walltime limit (`walltime` in `config.yaml`)
- ocean diagnostic outputs (`cd ocean`, edit `diag_table_source.yaml`, run `./make_diag_table.py`; for more info see https://github.com/COSIMA/make_diag_table)
- sea ice diagnostic outputs in `ice/cice_in.nml` (`f_*` fields; 'd'=daily mean, 'm'=monthly mean, 'x'=no output)
- ocean parameters in `ocean/input.nml`
- sea ice parameters in `ice/*.nml`

8. Edit `metadata.yaml` to describe your experiment. This is important so that you and others will know what you did and why.

9. git commit your changes with an informative message: `git commit -am "initial setup for experiment to test... bla bla"`

10. load the conda environment containing `payu`
```bash
module use /g/data/hh5/public/modules
module load conda/analysis3
```

11. Run the model:
```bash
payu run
```

This uses the [payu](https://github.com/payu-org/payu) workflow management tool to prepare the run and submit it as a job to the PBS job queue. See the [Gadi User Guide](https://opus.nci.org.au/display/Help/Gadi+User+Guide) to learn more about PBS job management.

Check the status of the job (state 'Q'=waiting in queue, 'R'=running, 'E'=exiting, 'H'=held) with
```bash
uqstat -c
```
while it's running, you can get an idea of where it's up to with
```bash
grep cur_exp-datetime work/atmosphere/log/matmxx.pe00000.log
```

To kill the run early, do `qdel N`, where N is the job number (first column given by `uqstat`). If you kill the job (or it crashes), a `work` directory will be left behind after the job has disappeared from `uqstat` and you'll need to do `payu sweep` before you can run again.

When your run has finished successfully, payu puts its output in `archive/output000` (ocean output in `archive/output000/ocean`, ice output in `archive/output000/ice/OUTPUT`), and starts a new job to copy these outputs to `SYNCDIR` with `sync_data.sh`. When complete, this will also generate a `run_summary*.csv` file (best viewed in a spreadsheet program) containing a log of the runs in your experiment. payu also records a log of your experiment in the git history, including the identity of the inputs and executables used (see the files in `manifests`).

To do another run, just type `payu run` again. Or to do (say) 10 runs, type `payu run -n 10` and they'll automatically be submitted one after the other.

The outputs from each run will be in numbered subdirectories in `archive` and also in `SYNCDIR`.

Each run creates a `restart` directory in `archive` which is used as the initial condition for the next run. These restarts can accumulate and consume disk space, but only the most recent one is needed (unless you plan to restart a new experiment from an intermediate state). `tidy_restarts.py` can be used to clean them up - see `./tidy_restarts.py -h` for usage information.

See the [payu documentation](http://payu.readthedocs.io/en/latest/design.html) for more explanation of where run output is stored.

If the run is unsuccessful you can find output in `access-om2.err` and any output from the run will be in `work`. You will need to do `payu sweep` before you will be able to do another `payu run`.

**WARNING** restarts are stored on `/scratch` (so will be deleted after 100 days) and are not automatically copied to `SYNCDIR`. If you plan to continue your run in the future you'll need to store the necessary restarts somewhere safe. To copy restarts to `SYNCDIR`, first wait for all jobs to finish, tidy them with `tidy_restarts.py` (if desired - see above), then do
```bash
./sync_data.sh -r -u
```
The most recent ocean restarts will be uncollated. If you'd like them to be collated, wait for the model run to finish, check for uncollated outputs with `ls archive/restart*/ocean/*.nc.0000` and do `payu collate -d archive/restartN/ocean` for any N with uncollated restarts. When the collation job has finished (check with `uqstat` and `ls archive/restart*/ocean/*.nc.0000`) you can then sync the restarts with just 
```bash
./sync_data.sh -r
```

**ANOTHER WARNING** `sync_data.sh` won't automatically copy uncollated files to `SYNCDIR`, so may omit the most recent outputs if they haven't finished collating. To avoid auto-deletion from `/scratch`, do `./sync_data.sh` after all jobs have finished. Also, sometimes collation of MOM output fails. To detect this, wait for all jobs to finish, then check for uncollated outputs with `ls archive/output*/ocean/*.nc.0000`. If you find any, collate them with `payu collate -i N` where N is the output directory number. When the collation jobs have finished (check with `uqstat` and `ls archive/output*/ocean/*.nc.0000`), copy the collated outputs to `SYNCDIR` with `./sync_data.sh`.

## Using model output

The output data will be in NetCDF format (`.nc` files). You can inspect the metadata in `.nc` files with `ncdump -h`. The quickest way to look at it visually is `ncview`, e.g.
```bash
module load ncview
ncview archive/output123/ocean/whatever.nc &
```

To do any serious plotting or analysis, you should use the [COSIMA Cookbook](https://cosima-cookbook.readthedocs.io/en/latest/). You'll probably need to [make your own database](https://cosima-recipes.readthedocs.io/en/latest/tutorials/Make_Your_Own_Database.html#gallery-tutorials-make-your-own-database-ipynb) to access your output data copied to `SYNCDIR`.

## Downloading ACCESS-OM2 and understanding the repository layout

As the previous section showed, on Gadi only the experiment configuration needs to be downloaded to use ACCESS-OM2. This is because, by default, the configurations reference pre-existing executables and inputs. However, if you wish to dig into the details of the model, modify input or code, or set it up on a different machine, then it is necessary to download and familiarise yourself with the entire ACCESS-OM2 repository.

### Downloading the ACCESS-OM2 repository

First, to download the entire ACCESS-OM2 repository, including all of the configurations and source code:

```bash
git clone --recursive https://github.com/COSIMA/access-om2.git
```

Then, to simplify future instructions we give this directory a short name with:

```bash
cd access-om2
export ACCESS_OM2_DIR=$(pwd)
```

If you already have an existing download and would like to update to the latest version see the tutorial on [updating an experiment](Tutorials#updating-an-experiment).

### The repository layout

The project is arranged into a collection of repositories that are linked together using [git submodules](http://git-scm.com/docs/git-submodule). The access-om2 repository is the parent, with other repositories embedded within it.

```bash
cd $ACCESS_OM2_DIR
tree -L 2 -d
.
├── control
│   ├── 01deg_jra55_iaf
│   ├── 01deg_jra55_ryf
│   ├── 025deg_jra55_iaf
│   ├── 025deg_jra55_ryf
│   ├── 1deg_jra55_iaf
│   └── 1deg_jra55_ryf
├── src
│   ├── cice5
│   ├── libaccessom2
│   │   ├── datetime-fortran
│   │   ├── json-fortran
│   │   ├── oasis3-mct
│   │   ...
│   └── mom
├── test
│   └── checksums
└── tools
    ├── contrib
    └── esmgrids
```

The `control` directory contains a number of submodules, one for each standard configuration. These repositories that can be downloaded independently and used to run experiments on Gadi. The `src` directory contains a submodule for each of the dynamical models. The `libaccessom2` repository contains the file-based atmosphere YATM, the OASIS coupler and other code needed to bolt everything together.

Working with git submodules can be tricky, fortunately there is a lot of good documentation out there, for example [here](https://www.atlassian.com/blog/git/git-submodules-workflows-tips) and [here](https://blog.github.com/2016-02-01-working-with-submodules/).

If this repository layout is particularly dis(agreeable) to you for any reason, please feel free to add a comment (as others have done) on a related issue, such as [this one](https://github.com/COSIMA/access-om2/issues/42).

## Building the models

[Note: at some point in the future this approach will be superseded by a [Spack-based build method](https://forum.access-hive.org.au/t/how-to-build-access-om2-on-gadi/1545).]

The easiest way is simply
```bash
cd $ACCESS_OM2_DIR
./install.sh
```
which will build physics-only (non-BGC) executables for all model components at all resolutions (this might take ~30 min the first time, but will be faster if done again). The executables will be placed in the `$ACCESS_OM2_DIR/bin/` directory, and the `config.yaml` files in the standard `control` subdirectories will be modified to use your new executables (but note that `config.yaml` will _not_ be updated in any additional subdirectories you might have added to `control`).

The executable names include the git hash of the `src` submodule they were built from. If you have made uncommitted changes in the source submodules the filenames will also include `modified`. Before any runs it is advisable to commit your changes to the source code before running `./install.sh`, so that the run will have a traceable provenance of the executables used. Because the model components are in submodules, you need to be in the relevant `src` subdirectory to commit changes. For example, if you've made changes to MOM, you need to `cd $ACCESS_OM2_DIR/src/mom` before you do `git commit -am "an informative message explaining my updates to mom"`.

To build BGC executables, switch to the `master+bgc` branches of all the control directories
```bash
for d in $ACCESS_OM2_DIR/control/*; do cd $d; git checkout master+bgc; cd -; done
```
edit `install.sh` to have
```bash
#export mom_type=ACCESS-OM
export mom_type=ACCESS-OM-BGC
```
and run `./install.sh` again. This will again update the executables used by the control configurations.

### Running a test case

Each of the model configurations is run by [payu](https://github.com/payu-org/payu) from within its respective directory in `$ACCESS_OM2_DIR/control/`. The `config.yaml` file within each of these subdirectories gives the PBS specification for the job, including updated executable names.

To run one of these configurations, first clone the control directory to give it a unique name, e.g.
```bash
cd $ACCESS_OM2_DIR/control
git clone --no-hardlinks 1deg_jra55_ryf 1deg_jra55_ryf_demo
```
There's one small wrinkle - the `origin` remote in the original directory will be a github URL - e.g.
```bash
cd $ACCESS_OM2_DIR/control/1deg_jra55_ryf
git remote -v
```
says `origin` points to `https://github.com/COSIMA/1deg_jra55_ryf.git`. However, `origin` in your cloned directory points to the directory that was cloned, e.g. see what you get with
```bash
cd $ACCESS_OM2_DIR/control/1deg_jra55_ryf_demo
git remote -v
```
It saves confusion to make them match, e.g. with
```bash
cd $ACCESS_OM2_DIR/control/1deg_jra55_ryf_demo
git remote set-url origin https://github.com/COSIMA/1deg_jra55_ryf.git
```

You can now proceed from step 4 in the [quick start](#quick-start) instructions.

## Migration from raijin to gadi
**This is a work in progress. Instructions here are (very) incomplete!**

General gadi transition info is here: https://opus.nci.org.au/display/Help/Preparing+for+Gadi

The changes most relevant to ACCESS-OM2 are:
1. `/short` will not exist on gadi. The replacement `/scratch` is time-limited, so is not suitable for storing model inputs or executables. We have therefore moved inputs from `/short/public/access-om2/` to `/g/data/ik11/inputs/access-om2/`. To access this **you will need to be a member of project `ik11`** (apply via [mancini](https://my.nci.org.au/mancini)). **You'll also need to be a member of `ua8` for RYF or `qv56` for IAF.**
2. The openMPI and NetCDF library versions we used on raijin will not be available on gadi. We've upgraded them in new executables but **your old raijin executables will not run on gadi**.
3. The intel compilers we used on raijin will not be available on gadi.
4. There are 48 CPUs per node on the normal queue on gadi (compared to 16 on raijin), so if using the normal queue you will need this at the end of `config.yaml`:
```
platform:
    nodesize: 48
```

### Your options

#### Starting a new experiment

If you want to start a brand-new experiment, we recommend you use the latest executables and configurations, which will fix the above issues (and more).
We haven't (yet) released a version of ACCESS-OM2 suitable for gadi, but we're working on it. There are test configurations available on the `gadi-transition` and `ak-dev` branches of the JRA-do-forced IAF and RYF configurations at all three resolutions in the individual config repos. `gadi-transition` is close to the old raijin configurations so is more suitable for continuation of existing runs. `ak-dev` includes many improvements an bug fixes (see the incomplete summary in the `merge ak-dev branch` pull request, e.g. https://github.com/COSIMA/025deg_jra55_iaf/pull/4).

Not all configurations have been tested, and those that have been run have not had their output carefully checked.

The IAF configs use JRA55-do from `qv56` which is a slightly newer version (1.3.1) from that on `ua8` used in previous runs and RYF (with small differences in near-surface temperature and humidity only). You could revert to the `ua8` version for continuation runs by undoing these changes to `atmosphere/forcing.json`
https://github.com/COSIMA/025deg_jra55_iaf/commit/d19b5c86e0600f1b8d52cc35cb7dba206d53f15b#diff-cd3ba4f3a1c8dd37efc78631f27566b3
and undoing the atmosphere input changes in `config.yaml`:
https://github.com/COSIMA/025deg_jra55_iaf/commit/d19b5c86e0600f1b8d52cc35cb7dba206d53f15b#diff-259fe82e12a866f01123927480c7851b
and also replacing `/g/data1/` with `/g/data/` in these files.

To try out a config, do this on gadi:
```bash
git clone https://github.com/COSIMA/1deg_jra55_iaf.git my-test-run
cd my-test-run
git checkout gadi-transition
git checkout -b my-test-run
```
then edit `accessom2.nml`, `sync_output_to_gdata.sh`, `config.yaml`
and run with
```bash
module use /g/data/hh5/public/modules
module load conda/analysis3-unstable
payu setup
git commit -am "my test run"
payu sweep
payu run
```
with "my-test-run" being whatever name you want. You can replace `1deg_jra55_iaf` above with any of these:
```
1deg_jra55_ryf
025deg_jra55_iaf
025deg_jra55_ryf
01deg_jra55_iaf
01deg_jra55_ryf
```

If you really want to live on the bleeding edge, replace `gadi-transition` with `ak-dev` above.

#### Continuing an experiment from raijin

This is where it gets tricky. Your executables from raijin will not run on gadi due to library changes. If you want to continue a run as close as possible to your raijin experiment you'll need to recompile the versions you used so they work on gadi. Note that due to compiler changes this will not give bit-for-bit reproducibility of your previous raijin runs.

It's a bit involved: 

1. Determine the versions (i.e. git hashes) of the executables used for your raijin run. Look in the `exe` fields in `config.yaml`. These contain the git hash (at the end for yatm and before `_libaccessom2` for mom and cice), e.g. in bold (yours will probably differ):

      exe: /short/public/access-om2/bin/yatm_**b6caeab**.exe

      exe: /short/public/access-om2/bin/fms_ACCESS-OM_**50dc61e**_libaccessom2_b6caeab.x

      exe: /short/public/access-om2/bin/cice_auscom_360x300_24p_**47650cc**_libaccessom2_b6caeab.exe

Before embarking on the steps below, first check whether the changes between your versions and those on `gadi-transition` are significant enough to warrant recompiling the code. If not, just use the `gadi-transition` branch as above.

2. Download and compile access-om2 on gadi:
```bash
git clone --recursive https://github.com/COSIMA/access-om2.git
cd access-om2
git checkout gadi-transition
./install.sh
```

3. Check out the versions of the code you used on raijin, using the hashes you found in step 1 above (yours will probably differ):
```bash
cd src/libaccessom2
git checkout b6caeab
git checkout -b "recompiling b6caeab for gadi"
cd ../mom
git checkout 50dc61e
git checkout -b "recompiling 50dc61e for gadi"
cd ../cice5
git checkout 47650cc
git checkout -b "recompiling 47650cc for gadi"
```

4. Make the necessary compiler and library changes in libaccessom2, mom and cice:
- https://github.com/COSIMA/libaccessom2/compare/gadi-transition
- https://github.com/mom-ocean/MOM5/compare/gadi-transition
- https://github.com/COSIMA/cice5/compare/gadi-transition

5. Commit these changes: `cd src; for d in *; do cd $d; git commit -am "update compiler and libraries for gadi"; cd -; done`

6. Cross fingers and run `./install` again. If it works you'll have new executables in `bin`. Their names will include hashes that differ from your raijin run but match those of the commits at step 5.

7. Put the executables somewhere permanent, which is visible to the gadi compute nodes (e.g. your home directory).

8. Update `config.yaml` to point to these executables and use `/g/data/ik11/inputs/` rather than `/short/public/`, e.g.
https://github.com/COSIMA/1deg_jra55_ryf/compare/gadi-transition#diff-259fe82e12a866f01123927480c7851b
You'll also need to set PBS flags in `config.yaml` and `sync_output_to_gdata.sh`, and also define `min_thickness = 1.0` in the `&ocean_topog_nml` group in `ocean/input.nml` if it wasn't already defined there (more info [here](https://github.com/COSIMA/access-om2/issues/161)).

*Don't* update `atmosphere/forcing.json` (there are small differences between the JRA55-do v1.3 in `/g/data/ua8` and v1.3.1 in `/g/data/qv56/replicas/input4MIPs/CMIP6/OMIP/MRI/MRI-JRA55-do-1-3`).

9. Load a version of payu that works on gadi and do `payu setup`
```bash
module use /g/data/hh5/public/modules
module load conda/analysis3-unstable
payu setup
```

10. If this works, do `payu sweep` and then try a (short!) run: `payu run`


#### Further notes:
- payu v1.0.6 and later works on raijin and gadi. For the former the default location for laboratories is `/short/$PROJECT/$USER`  and for gadi it is `/scratch/$PROJECT/$USER`. payu v1.0.6 is available via the `conda/analysis3-unstable environment`. More info: http://climate-cms.wikis.unsw.edu.au/Payuongadi
```bash
module use /g/data/hh5/public/modules
module load conda/analysis3-unstable
```
- you will need to be a member of projects `hh5`, `ik11`, `qv56` and `ua8`. Apply via [mancini](https://my.nci.org.au/mancini).
- you might find useful information at https://accessdev.nci.org.au/trac/wiki/gadi
- to build from the `gadi-transition` sources, do
```bash
git clone --recursive https://github.com/COSIMA/access-om2.git
cd access-om2
git checkout gadi-transition
for d in src/*; do cd $d; git checkout gadi-transition; cd ../..; done
./install.sh
```
your executables will be in `./bin`.
