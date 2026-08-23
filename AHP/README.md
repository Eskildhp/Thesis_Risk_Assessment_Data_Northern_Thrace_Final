# Cluster-Specific Analytic Hierarchy Process (AHP)

This folder contains the Analytic Hierarchy Process (AHP) calculations, supporting evidence and final criterion weights used in the risk assessment for Northern Thrace, Bulgaria.

A separate AHP model was created for each of the three separate clusters identified during the spatial clustering. This allowed the importance to reflect the different environmental characteristics of each cluster and then apply the weights to the sites inside the respective clusters.

## Criteria

Six criteria were included in the AHP:

* Seismic hazard
* Wildfire hazard
* Flood hazard
* Soil erosion
* Landslide susceptibility
* Asset vulnerability

The environmental criteria represent different natural hazards or environmental processes that may affect sites. Asset vulnerability represents characteristics of the sites that may influence their susceptibility to damage.

## Pairwise comparison procedure

Pairwise comparisons were performed separately for each cluster.

The relative importance of each pair of criteria was evaluated using the Saaty nine point comparison scale. A value of `1` represents equal importance. Larger values indicate increasing preference for one criterion over another and corresponding reciprocal values were used for the opposite comparisons.

The pairwise judgments were made by the author supported by the evidence in each cluster documented in the AHP Comparison Evidence worksheet which includes information on the distribution and severity of the hazard and vulnerability criteria within each environmental cluster.

The completed pairwise comparison matrices are in the `matrices/` directory.

## Criterion weight calculation

The pairwise comparison values were normalized by column in each cluster table. The criterion weight was calculated as the mean of the normalized row.

The resulting criterion weights were then used in the Weighted Linear Combination (WLC).

The final criterion weights are:

|Criterion|Cluster 1|Cluster 2|Cluster 3|
|-|-:|-:|-:|
|Seismic|0.293856|0.267511|0.220447|
|Wildfire|0.293856|0.148696|0.107842|
|Flood|0.030634|0.037835|0.038169|
|Soil erosion|0.088094|0.037835|0.107842|
|Landslide|0.123895|0.425959|0.461066|
|Asset vulnerability|0.169665|0.082164|0.064633|

## Consistency assessment

The internal consistency of each pairwise comparison matrix was evaluated using the maximum eigenvalue (`λmax`), Consistency Index (`CI`), and Consistency Ratio (`CR`).

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
|Cluster 2|6.372847|0.074569|0.060137|Acceptable|
|Cluster 3|6.468224|0.093645|0.075520|Acceptable|

All of the clusters have values within the acceptable range for the CR.

## Folder structure

AHP/
    ├── README.md
    ├── matrices/
    │   ├── Thrace\_AHP\_C1.xlsx
    │   ├── Thrace\_AHP\_C2.xlsx
    │   └── Thrace\_AHP\_C3.xlsx
    ├── evidence/
    │   └── AHP\_Pairwise\_Evidence\_Worksheet.xlsx
    └── results/
        └── AHP\_cluster\_summary.csv


## File descriptions

### `matrices/`

The `matrices/` directory contains the completed Excel workbook for the AHP calculations for the three calculations:

* `Thrace_AHP_C1.xlsx` — Cluster 1
* `Thrace_AHP_C2.xlsx` — Cluster 2
* `Thrace_AHP_C3.xlsx` — Cluster 3

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

`AHP_Pairwise_Evidence_Worksheet.xlsx`

This workbook documents the evidence considered when assigning the pairwise comparison values.

It records information used to compare the relative importance of the six criteria and provides supporting documentation for the judgments used in the final AHP matrices.

### `results/`

The `results/` directory contains:

`AHP_cluster_summary.csv`

This file provides a machine-readable summary of the final criterion weights and consistency statistics for all three clusters.

Values in the CSV are rounded to six decimal places for readability. The Excel workbooks have the formulas and calculations.

## Relationship to the risk assessment

The criterion weights were applied to the archaeological sites according to the cluster.

For each site, the standardized criterion scores were multiplied by the corresponding AHP weights and combined using Weighted Linear Combination (WLC).



