## Reproducible Model tests

These pytests are used for reproducibility checks in the `repro-ci` workflows. Code from these tests is adapted from COSIMAS's access-om2 
reproducibility [tests](https://github.com/COSIMA/access-om2/blob/master/test/test_bit_reproducibility.py).

### How to run tests manually

1. First clone test code which is on the `main` branch of `access-om2-configs` repository
```
git clone https://github.com/ACCESS-NRI/access-om2-configs/ test-code
```

2. Checkout an experiment
```sh
git clone https://github.com/ACCESS-NRI/accessom2-configs/ <experiment>
cd <experiment>
git checkout <branch/tag>
```

3. Run Pytests
```sh
pytest <path/to/test-code>/test
```

The output directory for pytests output defaults to `/scratch/$PROJECT/$USER/test-model-repro` and contains the following sub-directories:
- `control` - contains copies of the model configuration used for each experiment in the tests.
- `lab` - contains `payu` model output directories containing `work` and `archive` sub-directories.

This output directory also contains output generated in pytests, e.g.
the `CHECKSUM` file.

To set pytest output code to a different folder, use `--output-path` command flag, for example:

```sh
pytest <path/to/test-code>/test --output-path /some/other/path/for/output
```

By default, the control directory, e.g. the model configuration to test, is the current working directory. This can be set similarly to above by using the 
`--control-path` command flag.

The path containing the checksum file to check against can also be set using
`--checksum-path` command flag. The default is the `testing/checksum/CHECKSUM`
file which is stored in the control directory.

To run only fast tests, use `-k fast`, e.g.

```sh
pytest <path/to/test-code>/test -m fast
```

Alternatively to not run tests marked slow, use `-m "not slow"`
```sh
pytest <path/to/test-code>/test -m "not slow"
```