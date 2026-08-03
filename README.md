# NaFM Natural Product Embeddings

NaFM is a scaffold-aware graph foundation model that turns a natural-product SMILES into a 1024-dimensional embedding. Pretrained on the COCONUT natural-product database via contrastive and masked-graph learning, it captures scaffold and side-chain information useful for taxonomy classification, genome mining, and virtual screening. The embedding is a general-purpose featurizer specialised for natural-product chemical space.

This model was incorporated on 2026-08-03.Last packaged on 2026-08-03.

## Information
### Identifiers
- **Ersilia Identifier:** `eos6pj2`
- **Slug:** `nafm-embeddings`

### Domain
- **Task:** `Representation`
- **Subtask:** `Featurization`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `Descriptor`, `Embedding`, `Natural product`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `1024`
- **Output Consistency:** `Fixed`
- **Interpretation:** 1024-dimensional scaffold-aware embedding specialised for natural-product chemical space

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| feat_0000 | float |  | NaFM scaffold-aware natural-product embedding dimension 0 |
| feat_0001 | float |  | NaFM scaffold-aware natural-product embedding dimension 1 |
| feat_0002 | float |  | NaFM scaffold-aware natural-product embedding dimension 2 |
| feat_0003 | float |  | NaFM scaffold-aware natural-product embedding dimension 3 |
| feat_0004 | float |  | NaFM scaffold-aware natural-product embedding dimension 4 |
| feat_0005 | float |  | NaFM scaffold-aware natural-product embedding dimension 5 |
| feat_0006 | float |  | NaFM scaffold-aware natural-product embedding dimension 6 |
| feat_0007 | float |  | NaFM scaffold-aware natural-product embedding dimension 7 |
| feat_0008 | float |  | NaFM scaffold-aware natural-product embedding dimension 8 |
| feat_0009 | float |  | NaFM scaffold-aware natural-product embedding dimension 9 |

_10 of 1024 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos6pj2](https://hub.docker.com/r/ersiliaos/eos6pj2)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos6pj2.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos6pj2.zip)

### Resource Consumption
- **Model Size (Mb):** `305`
- **Environment Size (Mb):** `1315`
- **Image Size (Mb):** `1930.09`

**Computational Performance (seconds):**
- 10 inputs: `35.46`
- 100 inputs: `25.49`
- 10000 inputs: `252.91`

### References
- **Source Code**: [https://github.com/TomAIDD/NaFM-Official](https://github.com/TomAIDD/NaFM-Official)
- **Publication**: [https://doi.org/10.1038/s42256-026-01226-8](https://doi.org/10.1038/s42256-026-01226-8)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2026`
- **Ersilia Contributor:** [TiagoJanela](https://github.com/TiagoJanela)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [MIT](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos6pj2
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos6pj2
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
