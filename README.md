# Uni-Mol molecular representation

Uni-Mol offers a simple and effective SE(3) equivariant transformer architecture for pre-training molecular representations that capture 3D information. The model is trained on >200M conformations. The current model outputs a representation embedding.

This model was incorporated on 2024-07-22.Last packaged on 2025-09-05.

## Information
### Identifiers
- **Ersilia Identifier:** `eos39co`
- **Slug:** `unimol-representation`

### Domain
- **Task:** `Representation`
- **Subtask:** `Featurization`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `Fingerprint`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `512`
- **Output Consistency:** `Fixed`
- **Interpretation:** Uni-Mol representation embedding

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| dim_000 | float |  | Dimension index 0 of the Uni-Mol embedding |
| dim_001 | float |  | Dimension index 1 of the Uni-Mol embedding |
| dim_002 | float |  | Dimension index 2 of the Uni-Mol embedding |
| dim_003 | float |  | Dimension index 3 of the Uni-Mol embedding |
| dim_004 | float |  | Dimension index 4 of the Uni-Mol embedding |
| dim_005 | float |  | Dimension index 5 of the Uni-Mol embedding |
| dim_006 | float |  | Dimension index 6 of the Uni-Mol embedding |
| dim_007 | float |  | Dimension index 7 of the Uni-Mol embedding |
| dim_008 | float |  | Dimension index 8 of the Uni-Mol embedding |
| dim_009 | float |  | Dimension index 9 of the Uni-Mol embedding |

_10 of 512 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos39co](https://hub.docker.com/r/ersiliaos/eos39co)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos39co.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos39co.zip)

### Resource Consumption
- **Model Size (Mb):** `1`
- **Environment Size (Mb):** `7401`
- **Image Size (Mb):** `7169.69`

**Computational Performance (seconds):**
- 10 inputs: `31.36`
- 100 inputs: `45.61`
- 10000 inputs: `1180.63`

### References
- **Source Code**: [https://github.com/deepmodeling/Uni-Mol](https://github.com/deepmodeling/Uni-Mol)
- **Publication**: [https://openreview.net/forum?id=6K2RM6wVqKu](https://openreview.net/forum?id=6K2RM6wVqKu)
- **Publication Type:** `Preprint`
- **Publication Year:** `2024`
- **Ersilia Contributor:** [miquelduranfrigola](https://github.com/miquelduranfrigola)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [GPL-3.0-only](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos39co
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos39co
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
