# Check Repro Action

This action checks a downloaded checksum against a 'ground truth' checksum in a config repository.

## Inputs

| Name | Type | Description | Required | Default | Example |
| ---- | ---- | ----------- | -------- | ------- | ------- |
| checksum-location | string | Location of the checksums that will be compared against | true | N/A | `/opt/checksums` |

## Outputs

| Name | Type | Description | Example |
| ---- | ---- | ----------- | ------- |
| result | boolean | The result of the comparison between the artifact and the latest ground truth | `true` |
| ground-truth-version | string | The ground truth version compared against the input checksum | `2.1` |

## Example

```yaml
# ...
- uses: actions/checkout@v3
  with:
    ref: my-access-om2-configs

- id: check
  uses: access-nri/access-om2-configs/.github/actions/check-repro@main
  with:
    checksum-location: /tmp/checksums

- run: echo "Result of comparison was ${{ steps.check.outputs.result }} when comparing against ${{ steps.check.outputs.ground-truth-version }}.

```
