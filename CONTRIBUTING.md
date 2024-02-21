# Contributing

## Pull Request Process

### Changes to ACCESS-OM2 Configs

1. Make your changes, test them, and open a PR to either the `release-*` or `dev-*` branch of a particular configuration.
2. Checks will run to note whether your changes break reproducibility with the current major version config tag on the target branch. For example, if you are opening a PR on the `release-1deg_jra55_iaf` branch, and the last tagged version on this branch is `release-1deg_jra55_iaf-1.2`, the checksums between the config in your PR and the checksum in the config tag are compared.
3. A comment will be posted on the PR when this is completed, notifying you whether the checksums match (meaning a minor bump to `*-1.3`), or are different (meaning a major bump to `*-3.0`).
4. Optionally, you can now modify your PR and get more reproducibility checks.
5. Finally, bump the version using the `!bump [major|minor]` command depending on the result of the reproducibility check. Additionally, if the checksums are different, the updated checksum will be automatically committed to the PR. This is a requirement before the PR will be mergable.

### Changes to the CI Infrastructure

Changes to the CI Infrastructure are made to the `main` branch in this repository. Since the logic in the CI infrastructure is quite involved, it would be a good idea to read the [README-DEV.md](./README-DEV.md).
