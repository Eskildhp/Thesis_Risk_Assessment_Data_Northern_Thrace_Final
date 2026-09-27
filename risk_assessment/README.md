# Weighted Linear Combination (WLC) Risk Assessment

This folder has the final WLC results and the comparison with the global AHP.

## Method

The risk score was calculated separately for the three environmental clusters. Each cluster uses its own AHP weights, which are in the [`AHP/`](../AHP/) directory.

For each site, the six criterion scores were weighted according to its cluster and then added to calculate
 `WLC_RISK3`.

The calculation is:

`WLC = Σ(wj × xj)`

where:

* `wj` is the AHP weight for criterion `j` 
* `xj` is the standardized score for criterion `j`

Not every site has a value for all six criteria. Where a value is missing, that criterion is omitted and the weights for the other criteria are recalculated to sum to 1:

`WLC = Σ(wj × xj) / Σ(wj for valid criteria)`

Missing values are therefore not counted as zero.

The WLC was calculated in ArcGIS Pro with **Calculate Field**.

## Criteria

Six standardized criteria were included in the WLC:

* Seismic hazard
* Flood hazard
* Wildfire hazard
* Landslide susceptibility
* Soil erosion
* Asset vulnerability

`SEIS_SCR` is the seismic score calculated from five components: peak ground acceleration (PGA), epicentre density, magnitude, focal depth and fault distance.

## Risk classification

The final WLC scores were divided into five risk classes:

|Risk class|WLC score|
|-|-|
|Very Low|1–<2|
|Low|2–<4|
|Moderate|4–<6|
|High|6–<8|
|Very High|8–9|

## Cluster-specific weights

A separate set of AHP weights was used for each environmental cluster. The AHP matrices, evidence used for the pairwise comparisons and final weights are in:

`../AHP/`

The summary of the final weights is in:

`../AHP/results/AHP_cluster_summary.csv`

## Output file

The `results/WLC_site_results.csv` file contains the criterion scores and WLC results for all 250 sites and the results from the global AHP comparison.

### Fields

The fields are:

|Field|Description|
|-|-|
|`Site_ID`|Unique identifier for the archaeological site|
|`Site`|Site name|
|`Cluster_3`|Environmental cluster|
|`SEIS_SCR`|Seismic hazard|
|`FLOOD_SCR`|Flood hazard|
|`FWI_SCR`|Fire-weather danger score|
|`ELSUS_SCR`|Landslide susceptibility|
|`RUSLE_SCR`|Soil erosion|
|`ASSET_SCR`|Asset vulnerability|
|`WLC_RISK3`|WLC risk score|
|`RISK_CL3`|Risk class|
|`ALL_RISK`|Risk score from the global AHP|
|`ALL_CLASS`|Risk class from the global AHP|
|`RISK_DIFF`|Difference between `WLC_RISK3` and `ALL_RISK`|
|`ABS_DIFF`|Absolute value of `RISK_DIFF`|
|`CLASS_SHIFT`|Change in risk class between `RISK_CL3` and `ALL_CLASS`. Positive values show a higher class with the cluster-specific AHP|

`RUSLE_SCR` has no value for 77 sites and `ELSUS_SCR` has no value for 21 sites. Missing values are left blank. They are not zero values. Where a value is missing, it is excluded from the calculation and the other weights are recalculated to total 1.


## Global AHP comparison

A global AHP was also used to compare the results. One set of weights was applied across the whole study area. The cluster-specific AHP uses a separate set of weights for each cluster. The criterion scores and risk class ranges were the same for both calculations.

The global AHP weights are in:
`../AHP/results/AHP_global_summary.csv` 

The global AHP matrix is in:

and `../AHP/matrices/Thrace_AHP_ALL.xlsx`.

The global AHP gives the same risk class for 197 sites. The other 53 sites change by one class. This was only used as a comparison with the final `WLC_RISK3` results. 

## Folder structure

```text
risk_assessment/
    ├── README.md
    └── results/
        └── WLC_site_results.csv
```

## Relationship to the analytical workflow

The WLC follows the environmental clustering and AHP:

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

`WLC_RISK3` was then used in the sensitivity, uncertainty and Getis-Ord Gi* analyses.

## Data availability

The public file contains the site ID and name, cluster, criterion scores and WLC results. The continuous values are rounded to six decimal places. Precise archaeological site coordinates are not included.
