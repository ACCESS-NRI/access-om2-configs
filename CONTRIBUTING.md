# Contributing

## Changes to the CI Infrastructure

Changes to the CI Infrastructure are made to the `main` branch in this repository. Config branches use the `call-*.yml` workflows to `workflow_call` the equivalent workflow that is on the `main` branch.

Since the logic in the CI infrastructure is quite involved, it would be a good idea to read the [README-DEV.md](./README-DEV.md).

## Dev and Release branches

Each configuration has a `dev-*` and a `release-*` branch. They differ in the CI checks that are run when pull requests are made to update the branch. Any branch starting with either `dev-*` or  `release-*` are protected branches. You cannot (and should not) modify them directly or create new branches starting with either `dev-` or `release-`.

### Dev

The `dev-*` branch is where a configuration is updated. Temporary branches should be created and a pull request made to update the `dev-*` branch. Quality assurance (QA) CI checks are run on pull requests to `dev-*` branches, but not reproducibility checks. There is no requirement that the version be updated when changes are made to the `dev-` branch. So the `dev-` branch of a configuration allows for smaller changes that can be accumulated before a PR is made to the respective `release-*` branch.

### Release

Pull requests to the `release-*` branch should be made from the respective `dev-*` branch and are intended to create a new version of the configuration. These pull requests have CI quality assurance (QA) checks that ensure the model configuration is suitable for release. CI Model reproducibility checks are also conducted: a short test run of the configuration is checked for bitwise reproducibility. The success or otherwise of this check determines if a minor or major version bump is required.

It is expected that the version *will* be updated before the pull request can be merged. This in turn creates a new tag for that configuration branch. It can be confusing for users if there are a large number of versions of a configuration and it is of little benefit to them. For this reason the atomicity of updates to a released configuration should be minimised, i.e.  updates should be meaningful.

## Creation of a new ACCESS-OM2 Config

Config branches are entirely separate from the `main` history in this repository, except for a few files in `.github`. Note, you may need to be an Administrator to commit to `release-*` or `dev-*` branches directly.

### Brand new configuration

If you are creating a brand new configuration, and don't have the config stored in another repository, just checkout a `dev-*` branch from `main` and delete everything except `.github/workflows/ci.yml`, then add your config.

### Config is Stored in Another Repository

Create a `dev-*` branch by adding the config repository as a remote and checking out the config branch:

```bash
git remote add <config_repo> <config_repo_url>  # ex. git remote add config git@github.com/my/configs.git
git checkout <config_repo>/<config_branch> -b dev-<config_name>  # checkout config from new remote + add to branch, ex. git checkout config/main -b dev-1deg_abc_def
git checkout main -- .github/workflows/ci.yml
git add .
git commit -m "Initial commit for config branch"
git push  # might require admin permissions for pushes to dev-* branch
```

### Create a new release branch

For a brand new configuration there is no existing `release-*` branch, so one needs to be created. Follow the pull request process outlined below to update the dev branch so that it is passing QA checks. At this point create a `release-*` branch from the `dev-` branch and `git push` it to the repository:

```bash
git checkout -b release-<config_name>
git push release-<config_name>
```

For the CI workflows to work correctly the `release-` branch needs to have a version set, and a reproducibility checksum committed. There is a convenience workflow for this purpose: [Generate Initial Checksums](https://github.com/ACCESS-NRI/access-om2-configs/actions/workflows/generate-initial-checksums.yml). Click the "Run workflow" menu, fill in the fields and push the green "Run workflow" button.

Once the workflow is completed there should be a new commit on the `release-*` branch, and a [tag](https://github.com/ACCESS-NRI/access-om2-configs/tags) for the specified version.

Once the `release-*` branch has been updated those changes need to be merged **back** into the `dev-*` branch. This step is only necessary when the `release-*` branch is updated independently of the `dev-*` branch.

## Pull Request Process

### Update dev config

1. Make your changes, test them, and open a PR from a feature/change branch (or fork) to the `dev-*` branch of a particular configuration.
2. QA checks will run to ensure the configuration meets criteria for a released configuration, and to ensure consistency of released configurations.
3. [Fix the problems identified in the QA checks](#common-changes-required), commit and push to the PR branch.
4. Once all checks pass the pull request branch can be merged.
5. Consider making a PR to the equivalent `release-*` branch.

Note: If this is a brand new configuration and there is no existing `release-*` branch you will [need to create one first](#create-a-new-release-branch).

### Update release config

1. Open a PR from the `dev-*` branch of a particular configuration to the equivalent `release-*` branch
2. QA checks will run to ensure the configuration meets criteria for a released configuration, and to ensure consistency of released configurations.
3. Checks will also run to test if changes break reproducibility with the current major version config tag on the target branch. For example, if you are opening a PR on the `release-1deg_jra55_iaf` branch, and the last tagged version on this branch is `release-1deg_jra55_iaf-1.2`, the checksums between the config in your PR and the checksum in the config tag are compared.
4. A comment will be posted on the PR when this is completed, notifying you whether the checksums match (in this example meaning a minor bump to `*-1.3`), or are different (meaning a major bump to `*-2.0`).
5. Optionally, you can now modify your PR and get more reproducibility checks. Particularly in the case where bitwise reproducibility should be retained this is an opportunity to modify the configuration to enable this.
6. Bump the version using the `!bump [major|minor]` command depending on the result of the reproducibility check. Additionally, if the checksums are different, the updated checksum will be automatically committed to the PR. Bumping the version in some way is a requirement before the PR will be mergable.
7. Merge the PR

### Common Changes Required

#### Required metadata

The following fields must be set in `metadata.yaml`:

##### version

Use the existing `release-*` version. If there isn't an existing version set to `null`.

##### realm

```yaml
realm:
    - ocean
    - seaIce
    - ocnBgchm # Only include this for BGC models
```

##### nominal resolution

Choose the appropriate value for the resolution used:

| Config resolution | Nominal Resolution |
| -- | -- |
| 1&deg; | 100 km |
| 0.25&deg; | 25 km |
| 0.1&deg; | 10 km |

These are sourced from [the CMIP6 controlled vocabulary](https://github.com/WCRP-CMIP/CMIP6_CVs/blob/main/CMIP6_nominal_resolution.json). If your resolution differs from those listed you will need to make a pull request to add it to this documentation and the QA checks.

##### keywords

We have a "controlled vocabulary of keywords to prevent a proliferation of synonyms that mean the same thing, and to make it easy to populate these fields:

| Topic | Keywords (mutually exclusive) |
|--|--|
| Spatial extent | `global`, `regional` |
| Forcing product | `JRA55`, `ERA5` |
| Forcing mode | `repeat-year`, `ryf`, `repeat-decade`, `rdf`, `interannual`, `iaf` |
| Model | `access-om2`, `access-om2-025`, `access-om2-01` |

##### reference

An appropriate scientific reference for the configuration. For ACCESS-OM2 this should be `https://doi.org/10.5194/gmd-13-401-2020` if there is no more appropriate reference.

##### license

This is the license that will apply to the model outputs for an experiment. This should be set to the [SPDX identifier](https://spdx.org/licenses/) for [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (`CC-BY-4.0`) to alleviate users from the burden of choosing a license, and to ensure model outputs have a permissive license for reuse to encourage open and shareable science.

##### url

This is a bit tricky. Ideally this should be a URL to the GitHub (or similar) repository of the configuration *for the experiment being run*. So if we include this and require it to be filled then it should either be the URL pointing at the branch being modified, or a placeholder. Either way it should include a comment that it should be updated to reference the experiment being run.

##### model

Should be either `access-om2` or `access-om2-bgc`.

#### Configuration settings

##### restart_period

This is checked to make sure a shorter run time hasn't been set during testing and forgotten to set back to the proper value. As it is difficult to create a general heuristic the values have been hard-coded to those shown below:

| Config resolution | `restart_period`|
| -- | -- |
| 1&deg; | `5, 0, 0` |
| 1&deg; BGC | `5, 0, 0` |
| 0.25&deg; | `2, 0, 0` |
| 0.25&deg; BGC | `1, 0, 0` |
| 0.1&deg; | `0, 3, 0` |
| 0.1&deg; BGC | `0, 1, 0` |

The values shown are what is required for the namelist variable `restart_period` in the `accessom2.nml` namelist file.

If you need to set it to a different value for a released configuration this will need to be changed in the CI checking code.

##### restart_freq

This governs how what model restart files are retained.

The requirement is simply that a date-based frequency be used so that restarts are saved in a reliable manner. Typical values are `1YS` or `5YS` for 0.1&deg; models, and `5YS` to `20YS` for 1&deg;. See the [payu documentation](https://payu.readthedocs.io/en/latest/config.html#model) for a detailed description of the meaning of the time units in `restart_freq`.

##### sync

This should not be enabled by default. Nor should `path` be set to a real path. Ideally set `path` to `null`:

```yaml
sync:
    enable: false
    path: null
```

Users should enable this, and set the `path` themselves, as there is no safe default for this.

##### userscript

The `sync` userscript should be set to the correct path so that daily ice data will be concatenated, which saves a great deal of space. This will only work when syncing is enabled.

```yaml
userscripts:
    sync: /g/data/vk83/apps/om2-scripts/concatenate_ice/concat_ice_daily.sh
```
