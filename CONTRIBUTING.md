# Contributing

## Pull Request Process

### Creation of a new ACCESS-OM2 Config

Config branches are entirely separate from the `main` history in this repository, save for a few files in `.github`. Note, you may need to be an Administrator to commit to `release-*` branches directly.

#### If the Config is Stored in Another Repository

1. Add the repository that houses the config as an upstream remote. Let's call this upstream `config`, and assume that the config is stored on the `main` branch. Let's also call the config `1deg_abc_def`.
2. Checkout the config from one repo to this one. Run `git checkout <upstream>/<config_branch> -b release-<config_name>`. In our example, this would be `git checkout config/main -b release-1deg_abc_def`.
3. Checkout the new branch. Run `git checkout release-<config_name>`. This would be `git checkout release-1deg_abc_def`.
4. Copy across the required workflow files from the `main` branch. Run `git checkout main -- .github/workflows/call-*.yml .github/workflows/validate-json.yml`.
5. Commit and push the config branch. Due to branch protection rules, you may need to be an Administrator of the repository to commit directly to a `release-*` branch.

#### If the Config is Local or New

1. Branch off `main` and delete everything except for `.github/workflows/call-*.yml` and `.github/workflows/validate-json.yml`.
2. Add and commit your config files onto this branch.
3. Commit and push the config branch. Due to branch protection rules, you may need to be an Administrator of the repository to commit directly to a `release-*` branch.

### Changes to ACCESS-OM2 Configs

1. Make your changes, test them, and open a PR from the `dev-*` branch to the `release-*` branch of a particular configuration.
2. Checks will run to note whether your changes break reproducibility with the current major version config tag on the target branch. For example, if you are opening a PR on the `release-1deg_jra55_iaf` branch, and the last tagged version on this branch is `release-1deg_jra55_iaf-1.2`, the checksums between the config in your PR and the checksum in the config tag are compared.
3. A comment will be posted on the PR when this is completed, notifying you whether the checksums match (meaning a minor bump to `*-1.3`), or are different (meaning a major bump to `*-3.0`).
4. Optionally, you can now modify your PR and get more reproducibility checks.
5. Finally, bump the version using the `!bump [major|minor]` command depending on the result of the reproducibility check. Additionally, if the checksums are different, the updated checksum will be automatically committed to the PR. This is a requirement before the PR will be mergable.

### Changes to the CI Infrastructure

Changes to the CI Infrastructure are made to the `main` branch in this repository. Config branches use the `call-*.yml` workflows to `workflow_call` the equivalent workflow that is on the `main` branch.

Since the logic in the CI infrastructure is quite involved, it would be a good idea to read the [README-DEV.md](./README-DEV.md).
