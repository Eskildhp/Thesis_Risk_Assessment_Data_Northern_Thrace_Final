# Weighted Linear Combination (WLC) Risk Assessment

This folder contains the final site-level results of the Weighted Linear Combination (WLC) used to calculate relative risk for the study area.

The WLC combines the six standardized hazard and vulnerability criteria using the cluster-specific criterion weights derived through the Analytic Hierarchy Process (AHP).

## Method

Each archaeological site was assigned to one of the three clusters that were identified during the environmental spatial clustering step.

Separate AHP criterion weights were calculated for each cluster. These weights are documented in the [`AHP/`](../AHP/) directory.

For each site, the standardized criterion scores were multiplied by the corresponding AHP weights for the cluster the site is assigned to and combined to calculate the final WLC risk score.

The general calculation is:

`WLC = Σ(wj × xj)`

where:

* `wj` is the AHP weight assigned to criterion `j` for the site's environmental cluster
* `xj` is the standardized score of criterion `j`

When a criterion value not available for a site, the calculation was based on the available criteria and the remaining weights were renormalized:

`WLC = Σ(wj × xj) / Σ(wj for valid criteria)`

This keeps a missing criterion from lowering the final score for the site.

The WLC calculation was performed in ArcGIS Pro using the **Calculate Field** tool.

## Criteria

Six standardized criteria were included in the WLC:

* Seismic hazard
* Flood hazard
* Wildfire hazard
* Landslide susceptibility
* Soil erosion
* Asset vulnerability

The standardized criterion scores and cluster-specific AHP weights were used for the final risk calculation.

## Risk classification

The final WLC scores were classified using the following ranges:

|Risk class|WLC score|
|-|-|
|Very Low|1–<2|
|Low|2–<4|
|Moderate|4–<6|
|High|6–<8|
|Very High|8–9|

## Cluster-specific weights

The WLC uses a different set of criterion weights depending on the environmental cluster assigned to each site.

The full AHP matrices, supporting evidence, and final weights are available in:

`../AHP/`

A machine-readable summary of the weights is provided in:

`../AHP/results/AHP_cluster_summary.csv`

## Output file

The `results/` directory contains:

`WLC_site_results.csv`

This file contains the site-level standardized criterion scores and final WLC results used in the risk assessment.

### Fields

|Field|Description|
|-|-|
|`Site_ID`|Unique identifier for the archaeological site|
|`Site`|Site name|
|`Cluster_3`|Environmental cluster assigned during Ward hierarchical clustering|
|`SEIS_SCR`|Standardized seismic hazard score|
|`FLOOD_SCR`|Standardized flood hazard score|
|`FWI_SCR`|Standardized wildfire hazard score|
|`ELSUS_SCR`|Standardized landslide susceptibility score|
|`RUSLE_SCR`|Standardized soil erosion score|
|`ASSET_SCR`|Standardized asset vulnerability score|
|`WLC_RISK`|Final cluster-weighted WLC risk score|
|`RISK_CLASS`|Final categorical risk classification|

## Folder structure

risk\_assessment/
    ├── README.md
    └── results/
        └── WLC\_site\_results.csv


## Relationship to the analytical workflow

The WLC stage follows the environmental clustering and AHP stages of the analysis:

Environmental clustering
            ↓
    Cluster-specific AHP
            ↓
    Standardized criterion scores
            ↓
    Weighted Linear Combination
            ↓
    Final site risk score
            ↓
    Risk classification

The resulting `WLC_RISK` values were subsequently used in later analytical stages, including the uncertainty analysis.

## Data availability

The public results file contains the site names, identifiers, cluster assignments, standardized criterion scores and calculated risk results.

Precise site coordinates are not included in this repository.

