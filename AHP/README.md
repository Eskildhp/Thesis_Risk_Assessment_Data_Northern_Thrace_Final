# Cluster-Specific Analytic Hierarchy Process (AHP)

This folder contains the Analytic Hierarchy Process (AHP) calculations, supporting evidence and criterion weights used in the risk assessment for Northern Thrace, Bulgaria as well as the separate global AHP model used in the comparison.

A separate AHP model was created for each of the three separate clusters identified during the spatial clustering. This allowed the importance to reflect the different environmental characteristics of each cluster and then apply the weights to the sites inside the respective clusters.

## Criteria

Six criteria were included in the AHP:

* Seismic hazard
* Wildfire hazard
* Flood hazard
* Soil erosion
* Landslide susceptibility
* Asset vulnerability

The environmental criteria include the natural hazards and environmental processes that may affect the sites. Asset vulnerability represents characteristics of the sites that may influence their susceptibility to damage. The seismic criterion uses the final score derived from five equally weighted components: peak ground acceleration (PGA), epicentre density, magnitude, focal depth and fault distance.

## Pairwise comparison procedure

Pairwise comparisons were performed separately for each cluster. A global AHP pairwise comparison matrix was also implemented.

The relative importance of each pair of criteria was evaluated using the Saaty nine point comparison scale. A value of `1` represents equal importance. Larger values indicate increasing preference for one criterion over another and corresponding reciprocal values were used for the opposite comparisons.

The pairwise judgments were made by the author, using evidence from the distribution and level of the final criterion scores in each cluster. The cluster evidence and separate global AHP evidence worksheets are in the `evidence/` directory.

The completed pairwise comparison matrices are in the `matrices/` directory.

## Criterion weight calculation

For each cluster, the pairwise comparison values were normalized by column. The mean for each row was then used as the criterion weight.

The resulting criterion weights were then used in the Weighted Linear Combination (WLC).

The final criterion weights are:

|Criterion|Cluster 1|Cluster 2|Cluster 3|
|-|-:|-:|-:|
|Seismic|0.293856|0.247528|0.145637|
|Wildfire|0.293856|0.146483|0.130486|
|Flood|0.030634|0.037219|0.040181|
|Soil erosion|0.088094|0.037219|0.130486|
|Landslide|0.123895|0.450247|0.483126|
|Asset vulnerability|0.169665|0.081303|0.070085|

## Consistency assessment

The internal consistency of each pairwise comparison matrix was evaluated using the estimated maximum eigenvalue (`λmax`), Consistency Index (`CI`), and Consistency Ratio (`CR`).

For the six-criterion matrices, the Consistency Index was calculated as:

`CI = (λmax - n) / (n - 1)`

where `n = 6`.

The Consistency Ratio was calculated as:

`CR = CI / RI`

A Random Index (`RI`) value of `1.24` was used for the matrices with six criterion.

A Consistency Ratio below `0.10` was considered acceptable (Saaty, 1980).

|Cluster|λmax|CI|CR|Consistency|
|-|-:|-:|-:|-|
|Cluster 1|6.461791|0.092358|0.074482|Acceptable|
|Cluster 2|6.526162|0.105232|0.084865|Acceptable|
|Cluster 3|6.299859|0.059972|0.048364|Acceptable|

All of the clusters have values within the acceptable range for the CR.

## Global AHP comparison

A single AHP matrix was also applied to all 250 sites for a comparison with the cluster-specific AHP approach. It uses the same six standardized criteria and the same missing-value weight process as the final risk assessment. The global weights do not replace the cluster-specific weights used for the final `WLC_RISK3` results.

|Criterion|Global weight|
|-|-:|
|Seismic|0.269764|
|Wildfire|0.255876|
|Flood|0.039157|
|Soil erosion|0.058735|
|Landslide|0.255876|
|Asset vulnerability|0.120593|

For the global matrix, `λmax = 6.311816`, `CI = 0.062363`, and `CR = 0.050293`. The matrix is in `matrices/Thrace_AHP_ALL.xlsx`; its evidence is in `evidence/AHP_Global_Evidence_Worksheet.xlsx`. The global weights and consistency results are also provided in `results/AHP_global_summary.csv`. The resulting site-level global scores and classes are documented with the risk assessment outputs.

## Folder structure

```text
AHP/
├── README.md
├── matrices/
│   ├── Thrace_AHP_C1.xlsx
│   ├── Thrace_AHP_C2.xlsx
│   ├── Thrace_AHP_C3.xlsx
│   └── Thrace_AHP_ALL.xlsx
├── evidence/
│   ├── AHP_Pairwise_Evidence_Worksheet.xlsx
│   └── AHP_Global_Evidence_Worksheet.xlsx
└── results/
    ├── AHP_cluster_summary.csv
    └── AHP_global_summary.csv
```


## File descriptions

### `matrices/`

The `matrices/` directory contains the completed Excel workbooks for the three cluster-specific AHP calculations and the global AHP comparison:

* `Thrace_AHP_C1.xlsx` — Cluster 1
* `Thrace_AHP_C2.xlsx` — Cluster 2
* `Thrace_AHP_C3.xlsx` — Cluster 3
* `Thrace_AHP_ALL.xlsx` — Global comparison

Each workbook contains the pairwise comparison matrix and the calculations used to derive:

* normalized comparison values;
* criterion weights;
* weighted sum values;
* consistency vectors;
* `λmax`;
* `CI`; and
* `CR`.

The workbooks were developed from an Excel AHP template provided by A. Agapiou through personal communication in March 2026, which were modified and completed.

### `evidence/`

The `evidence/` directory contains:

* `AHP_Pairwise_Evidence_Worksheet.xlsx` — cluster-specific pairwise comparison evidence
* `AHP_Global_Evidence_Worksheet.xlsx` — global pairwise comparison evidence

The workbooks contain the evidence used to assign the pairwise comparison values. The calculations use the final dataset of 250 sites, including the mean scores, the number of high scores and their overlap with high asset vulnerability. The same pairwise comparison values are used in the final matrices.

It records information used to compare the relative importance of the six criteria and provides supporting documentation for the judgments used in the final AHP matrices.

### `results/`

The `results/` directory contains:

* `AHP_cluster_summary.csv` — final weights and consistency statistics for Clusters 1–3
* `AHP_global_summary.csv` — weights and consistency statistics for the global AHP comparison

These files are summaries of the criterion weights and consistency statistics, and are machine-readable.

Values in the CSVs are rounded to six decimal places for readability. The Excel workbooks have the formulas and calculations.

## Relationship to the risk assessment

The criterion weights were applied to the archaeological sites according to the cluster.

For each site, the standardized criterion scores were multiplied by the corresponding AHP weights and combined using Weighted Linear Combination (WLC).



