# Contributing

## Pull Request Process

### Creation of a new ACCESS-OM2 Config

Config branches are entirely separate from the `main` history in this repository, except for a few files in `.github` Note, you may need to be an Administrator to commit to `release-*` branches directly.

If you are creating a new branch, and don't have config stored in another repository, just branch off `main` and delete everything except `.github/workflows/pr-1-ci.yml`, `.github/workflows/pr-3-bump-tag.yml` and `.github/workflows/validate-json.yml`, then add your config.

#### If the Config is Stored in Another Repository

```bash
git remote add <config_repo> <config_repo_url>  # ex. git remote add config git@github.com/my/configs.git
git checkout <config_repo>/<config_branch> -b release-<config_name>  # checkout config from new remote + add to branch, ex. git checkout config/main -b release-1deg_abc_def
git checkout main -- .github/workflows/call-*.yml .github/workflows/validate-json.yml  #
git add .
git commit -m "Initial commit for config branch"
git push  # might require admin permissions for pushes to release-* branch
```

### Changes to ACCESS-OM2 Configs

1. Make your changes, test them, and open a PR from the `dev-*` branch to the `release-*` branch of a particular configuration.
2. Checks will run to note whether your changes break reproducibility with the current major version config tag on the target branch. For example, if you are opening a PR on the `release-1deg_jra55_iaf` branch, and the last tagged version on this branch is `release-1deg_jra55_iaf-1.2`, the checksums between the config in your PR and the checksum in the config tag are compared.
3. A comment will be posted on the PR when this is completed, notifying you whether the checksums match (meaning a minor bump to `*-1.3`), or are different (meaning a major bump to `*-3.0`).
4. Optionally, you can now modify your PR and get more reproducibility checks.
5. Finally, bump the version using the `!bump [major|minor]` command depending on the result of the reproducibility check. Additionally, if the checksums are different, the updated checksum will be automatically committed to the PR. This is a requirement before the PR will be mergable.

### Changes to the CI Infrastructure

Changes to the CI Infrastructure are made to the `main` branch in this repository. Config branches use the `call-*.yml` workflows to `workflow_call` the equivalent workflow that is on the `main` branch.

Since the logic in the CI infrastructure is quite involved, it would be a good idea to read the [README-DEV.md](./README-DEV.md).
