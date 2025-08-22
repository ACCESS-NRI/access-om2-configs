
## Integrating with COSIMA cookbook

Here's how you can automatically copy your model output to `/g/data3/` to make it available for analysis via the [COSIMA Cookbook](http://cosima-cookbook.readthedocs.io/en/latest).

You will need write access to `/g/data3/hh5/tmp/cosima/`, or at least to the subdirectory you use - talk to the CMS team about this; it is controlled by FACLs.

**This example is for `1deg_jra55_ryf`; you'll need to make the obvious changes for other models.**

First check the existing directories in `/g/data3/hh5/tmp/cosima/access-om2/` and **create a new one** with a **new, unique name**, e.g.
```
mkdir /g/data3/hh5/tmp/cosima/access-om2/1deg_jra55_ryf_spinupN/
```
For clarity it's best if this name matches your git branch (see previous section).

Now edit ``$ACCESS_OM_DIR/control/1deg_jra55_ryf/sync_output_to_gdata.sh`` to set ``GDATADIR`` to the directory in `g/data3` you created above, e.g.
```
GDATADIR=/g/data3/hh5/tmp/cosima/access-om2/1deg_jra55_ryf_spinupN/
```
and also set an appropriate project for the PBS -P flag.
**WARNING: it is crucial that ``GDATADIR`` is the new, empty directory you created above! If it is already exists you may overwrite output and restarts from previous experiments** (see [here](https://github.com/OceansAus/access-om2/issues/59)). **PLEASE DOUBLE-CHECK!**

Finally, edit `$ACCESS_OM_DIR/control/1deg_jra55_ryf/config.yaml` to uncomment the line 
```
postscript: sync_output_to_gdata.sh
``` 
This will run `sync_output_to_gdata.sh` after each run, automatically rsynching collated output from all previous runs to `/g/data3/hh5/tmp/cosima/access-om2/1deg_jra55_ryf_spinupN/`, where COSIMA Cookbook can find it and add it to the cookbook database.

In python, you then need to use `build_index` to update the cookbook index to see your new runs:
```{python}
import cosima_cookbook as cc
cc.build_index()
```
The `/g/data3` directory you created above (e.g. `1deg_jra55_ryf_spinupN`) will be the experiment's name in the COSIMA Cookbook, i.e. in the list returned by `cc.get_experiments(configuration)`, where `configuration` is the parent directory name (e.g. `access-om2`):
```{python}
configuration = 'access-om2'
expts = cc.get_experiments(configuration)
```
For further COSIMA Cookbook usage instructions and examples see <http://cosima-cookbook.readthedocs.io/en/latest>.
