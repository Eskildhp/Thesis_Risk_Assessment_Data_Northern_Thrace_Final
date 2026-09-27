# AHP Sensitivity Analysis

This folder contains the OAT sensitivity analysis for the three environmental clusters. The analysis tests how changes to the AHP pairwise comparisons affect the criterion weights, consistency, WLC risk scores and risk classes.

The analysis uses the final `SEIS_SCR` values and the final AHP matrices in `../AHP/matrices/`. The baseline WLC scores and classes are `WLC_RISK3` and `RISK_CL3` in `../data/Sites_master.csv`.

## Method

The script reads the AHP matrix for each cluster and calculates the criterion weights by normalizing the columns and taking the mean of each row.

Each pairwise comparison is then moved one level up and one level down on the Saaty scale where possible. The reciprocal value is changed at the same time.

For each change, the script recalculates:

* criterion weights
* maximum eigenvalue (`λmax`)
* Consistency Index (`CI`)
* Consistency Ratio (`CR`)
* WLC risk scores
* Site risk classes

Only matrices with `CR < 0.10` are used.

There are 90 runs in total, 30 for each cluster. All 90 matrices have a `CR < 0.10`. 

The site-level results contain 7,500 rows, with 30 runs for each of the 250 sites. Fifteen sites change risk class in at least one run. These results agree with `SUM_Changed_Num` in `../data/Sites_master.csv`.

## Saaty comparison scale

The script uses the following Saaty scale:

`1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, 6, 7, 8, 9`

Each pairwise comparison is changed by one step in each direction where possible.

## WLC recalculation

The analysis uses six criteria:

* Seismic hazard
* Wildfire hazard
* Flood hazard
* Soil erosion
* Landslide susceptibility
* Asset vulnerability

The changed weights were then used to calculate the WLC risk scores for that run. Not all sites have scores for all six criteria. Where a score is missing, it is excluded from the calculation and the weights for the criteria that are present are adjusted to sum to 1:

`WLC = Σ(wj × xj) / Σ(wj for available criteria)`

where:

* `wj` is the AHP weight for criterion `j`
* `xj` is the standardized score for criterion `j`

## Missing

Some missing criterion values are expected from the original data:

* `RUSLE_SCR` is omitted when `Rusle_MTH` is `Urban excl.`, `Coastal excl.`, or `Other excl.`
* `ELSUS_SCR` is omitted when `ELSUS_MTH` is `NoData>400m`
* `ASSET_SCR` is omitted when `Material_general` is `Unknown / Not specified`

For these sites, the other weights are adjusted to sum to 1.

Any other missing criterion value is recorded in `00_Data_Quality.csv` and stop the analysis.

## Risk classification

The recalculated WLC scores use the same five risk classes as the main risk assessment:

|Risk class|WLC score|
|-|-|
|Very Low|1–<2|
|Low|2–<4|
|Moderate|4–<6|
|High|6–<8|
|Very High|8–9|

## Sensitivity measures

The analysis records changes in the risk classes and the Overall Change Rate (OCR).

### Site class changes

For each run, the script records:

* Number of sites that change risk class
* Percentage of sites that change risk class

### Overall Change Rate (OCR)

The script also calculates the Overall Change Rate (OCR) adapted from Chen et al. (2013).

The Overall Change Rate (OCR) is adapted from Chen et al. (2013). Their method compares changes in the number of raster cells in each class. Here, the calculation uses the number of archaeological sites in each risk class before and after each change to a pairwise comparison.

## Folder structure

    sensitivity_analysis/
    ├── README.md
    ├── inputs/
    │   └── Sites_sensitivity_input.csv
    ├── results/
    │   ├── 00_Data_Quality.csv
    │   ├── 01_Baseline_Weights.csv
    │   ├── 02_Pairwise_Sensitivity_Runs.csv
    │   ├── 03_Site_Level_Sensitivity.csv
    │   ├── 04_Criterion_Sensitivity_Summary.csv
    │   └── Run_Log.txt
    └── scripts/
        └── Thrace_AHP_Sensitivity.py

## Input file

### `Sites_sensitivity_input.csv`

This is the input file for the sensitivity analysis. It has the site ID, cluster and the six criterion scores for each site. It also has the fields needed to account for missing values.

`SEIS_SCR` is the seismic score used in the final analysis. It combines PGA, epicentre density, magnitude, focal depth and fault distance. A score is available for all 250 sites.

The `_MTH` fields show how the RUSLE and ELSUS values were handled. `Rusle_MTH` identifies the RUSLE exclusions and `ELSUS_MTH` identifies sites where ELSUS NoData was more than 400 m from the site. `Material_general` is used for sites where asset vulnerability could not be scored.

|Field|Description|
|-|-|
|`Rusle_MTH`|Method/status for the RUSLE score and exclusions|
|`ELSUS_MTH`|Method/status for ELSUS, including sites with no valid cell within 400 m|
|`Material_general`|General construction material used for the asset vulnerability score|

Precise archaeological site coordinates are not included.

The script also reads the three AHP matrices from:

`../AHP/matrices/`

These are:

* `Thrace_AHP_C1.xlsx`
* `Thrace_AHP_C2.xlsx`
* `Thrace_AHP_C3.xlsx`

## Output files

### `00_Data_Quality.csv`

Records sites with intentional N/A criteria or missing criterion values and documents the reason for each Lists the sites with missing criteria and the reason why the value is missing.

### `01_Baseline_Weights.csv`

Contains the original AHP weights and consistency results for each cluster.

### `02_Pairwise_Sensitivity_Runs.csv`

Contains the results from the 90 changes to the pairwise comparisons, including:

* Baseline and perturbed Saaty values
* Changed criterion weights
* Baseline and alternative CR
* Number and percentage of sites changing risk class
* OCR
* Number of sites in each risk class before and after the change

### `03_Site_Level_Sensitivity.csv`

Contains the results for each site and each sensitivity run, including:

* Baseline and recalculated WLC scores
* Baseline and recalculated risk classes
* Whether the site changed risk class
* Criteria excluded due to missing values
* Weight sums before and after perturbation

Precise archaeological site coordinates are not included.

### `04_Criterion_Sensitivity_Summary.csv`

Summarizes the results for each cluster and criterion, including:

* Number of valid runs
* Mean and maximum OCR
* Mean and maximum percentage of sites changing risk class

### `Run_Log.txt`

Records the number of sites, original CR values, number of runs and the number of accepted and rejected matrices.

## Requirements

The script requires:

* Python 3
* `openpyxl`

Install `openpyxl` with:

    python -m pip install openpyxl

## Running the script

From the repository root or the script directory, run:

    python sensitivity_analysis/scripts/Thrace_AHP_Sensitivity.py

The script reads the AHP matrices and input file and saves the results in:

`sensitivity_analysis/results/`

## Methodology source

Chen, Y., Yu, J., & Khan, S. (2013). The spatial framework for weight sensitivity analysis in AHP-based multi-criteria decision making. *Environmental Modelling & Software, 48*, 129–140. https://doi.org/10.1016/j.envsoft.2013.06.010
