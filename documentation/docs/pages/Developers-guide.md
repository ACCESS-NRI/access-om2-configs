
## Building models individually

This section describes how to build each of the ACCESS-OM2 component model individually. Since this is a time consuming process it has been automated by the [`install.sh`](Getting-started#Building-the-models) script.

In addition [pytest](https://docs.pytest.org) can be used to run the build tests - a successful run of these tests will result in the creation of all model executables.

On NCI you can load pytest with:
```{bash}
module use ~access/modules
module load pythonlib/pytest
```

Then run the build test:
```{bash}
python -m pytest test/test_build.py
```

If you really want to build the models individually, first download the model source code and change into the ACCESS-OM2 top-level directory:

```{bash}
cd /short/${PROJECT}/${USER}
git clone --recursive https://github.com/COSIMA/access-om2.git
cd access-om2
export ACCESS_OM_DIR=$(pwd)
```

Now start by compiling libaccessom2 because it is needed by the other models:

```{bash}
cd $ACCESS_OM_DIR/src/libaccessom2
./build_on_raijin.sh
```

This step invokes CMake which is used by the libaccessom2 build system. The CMake configuration file contains a reference to the OasisMCT repository and starts by downloading code from there. It also downloads a couple of other libraries such as [datetime-fortran](https://github.com/nicjhan/datetime-fortran.git) and [json-fortran](https://github.com/jacobwilliams/json-fortran.git).

Check that the YATM executable exists to determine whether the build was successful:

```
ls $ACCESS_OM_DIR/src/libaccessom2/build/bin/yatm.exe
```


Before the MOM and CICE builds, it is required to specify the libaccessom2 path by:

```{bash}
export LIBACCESSOM2_ROOT=$ACCESS_OM_DIR/src/libaccessom2/
```

Now build MOM:

```{bash}
cd $ACCESS_OM_DIR/src/mom/exp
./MOM_compile.csh --type ACCESS-OM --platform nci
```


Check that MOM the executable exists:
```{bash}
ls $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
```

Unfortunately the CICE build is resolution dependent, so we need to do three separate builds, one each for 1, 1/4 and 1/10th degree:

```{bash}
cd $ACCESS_OM_DIR/src/cice5
make 1deg
make 025deg
make 01deg
```

Check that CICE executables exist:
```{bash}
ls $ACCESS_OM_DIR/src/cice5/build_auscom_*/cice_*.exe
```

## Installing new executables

Once new executables have been created they need to be renamed and copied to the correct directory. Once again the [`install.sh`](Getting-started#Building-the-models) script does this for you so is preferable.

First copy and rename mppnccombine:
```{bash}
mkdir -p $ACCESS_OM_DIR/bin
cp $ACCESS_OM_DIR/src/mom/bin/mppnccombine.nci $ACCESS_OM_DIR/bin/mppnccombine
```

Now for the model executables. The convention is that the executable is suffixed with `_<git commit hash>` where `<git commit hash>` is the first eight characters of the commit hash of the code that was compiled to create the executable. This value can be found, for example for MOM, with:

```{bash}
cp $ACCESS_OM_DIR/src/mom/
git rev-parse --short=8 HEAD
```

So the following set of commands would copy the MOM executable into the correct location with the correct name:

```{bash}
cd $ACCESS_OM_DIR/src/mom/
HASH=$(git rev-parse --short=8 HEAD)
cp exec/nci/ACCESS-OM/fms_ACCESS-OM.x $ACCESS_OM_DIR/bin/fms_ACCESS-OM_${HASH}.x
```

These new executable names also need to match those used in the experiment configuration file `config.yaml`. For example it should be a line like:

```
exe: fms_ACCESS-OM_${HASH}.x
```

## Contributing changes to the ACCESS-OM2 repository

**CAUTION: OUT OF DATE!** SEE [ISSUE 42](https://github.com/COSIMA/access-om2/issues/42#issuecomment-346602379)

Each of the ACCESS-OM2 model configurations are in separate repositories.

To contribute changes to a model configuration follow these steps:


### 1. Create GitHub account

If you do not already have an account on GitHub, [follow the instructions to create one](https://help.github.com/articles/signing-up-for-a-new-github-account/).

### 2. Fork repository

Navigate to the GitHub page for the model configuration to which you wish to contribute, and [fork it](https://help.github.com/articles/fork-a-repo/).

### 3. Clone repository

Navigate to the GitHub page for the fork made above and [clone it](https://help.github.com/articles/cloning-a-repository/).

Add the original COSIMA model configuration repository that was forked **from** as a remote. In this case it is called upstream:

    git remote add upstream <url>

### 4. Run and test configuration

Create a new branch for each experiment and check it out, e.g.

    git branch expt
    git checkout expt

where 'expt' is a descriptive name you give for this configuration. Run the model as you would normally with payu run logging enabled (i.e. put 'runlog: True' at the end of config.yaml). It might be necessary to use hashexe.sh to alter the path to the executable when there are code updates.

### 5. Contributing changes back

When the model is at a point where changes need to be contributed back it is necessary to create a new branch with a clean commit history. The recommended steps are:

Checkout the master branch and get latest updates:

    git checkout master
    git pull

Create a new branch, e.g.

    git branch clean
    git checkout clean

Determine which files have changed in the expt branch compared to the master branch

    git diff expt master

Get updated files from the expt branch into the clean branch, do this for each file: 

    git checkout expt <file>
    git add <file>

Commit changes to the clean branch. 

    git commit -m "Commit message"

Depending on changes and what users wish to do one commit for all the changes may suffice, or separate commits after each changed file is staged (the "add" command).

Push clean branch back to forked repo

    git push origin clean

Issue a [pull request from the clean branch on your fork back to the upstream repo](https://help.github.com/articles/creating-a-pull-request-from-a-fork/).

Please remember that these commits will be to a shared model configuration which should be suitable for anyone to use. For this reason please do not commit anything that uses hard-coded paths to files, or references specific project IDs. In particular be very careful when committing `config.yaml` files. Any changes should be of universal benefit, not specific to one configuration.

## Testing

ACCESS-OM2 tests can be found in the `test/` directory. Many of these are run routinely by and results can be found on the [ACCESS-OM2 Jenkins page](https://accessdev.nci.org.au/jenkins/job/ACCESS-OM2/). 

During development it is often necessary to check that the model reproduces historical results bit-for-bit. This can be done by running the reproducibility tests. The simple way to do this is run:
```
python -m pytest test/test_bit_reproducibility.py
```
However this is very slow because each test run uses qsub to queue a job. It is much quicker to run the tests within an interactive session, e.g. 

```
qsub -I -P e14 -v DISPLAY -q expressbw -l ncpus=252,mem=500Gb,walltime=5:00:00
cd $ACCESS_OM_DIR
python -m pytest test/test_bit_reproducibility.py
```

In this case the test runs are done directly within the interactive session.

## Understanding the model log output

The component models of ACCESS-OM2 create a myriad of log files. This section attempts to categorise and explain these.
