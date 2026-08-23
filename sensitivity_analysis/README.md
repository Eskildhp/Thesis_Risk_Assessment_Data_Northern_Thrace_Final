# AHP Sensitivity Analysis

This folder contains the OAT sensitivity analysis used to evaluate how changes in the cluster-specific AHP pairwise comparisons affect the criterion weights, consistency, WLC risk scores and the final risk classes. The analysis was performed individually for the 3 clusters.  

## Method

The script reads the AHP pairwise comparison matrix for the cluster and reproduces the baseline criterion weights using column normalization and the mean of each normalized row.

Each pairwise comparison is changed by one level on the Saaty comparison scale in both directions where possible. The reciprocal comparison is updated automatically.

After each change, the script recalculates:

* criterion weights
* maximum eigenvalue (`λmax`)
* Consistency Index (`CI`)
* Consistency Ratio (`CR`)
* WLC risk scores
* Site risk classes

The alternative matrices are only used for the sensitivity analysis when `CR < 0.10`.

The procedure produces 90 sensitivity runs.

## Saaty comparison scale

The script uses the Saaty comparison sequence:

`1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, 6, 7, 8, 9`

Each comparison is moved by one level at a time.

## WLC recalculation

The six criteria used in the sensitivity analysis are:

* Seismic hazard
* Wildfire hazard
* Flood hazard
* Soil erosion
* Landslide susceptibility
* Asset vulnerability

The WLC score is recalculated in each sensitivity run using the alternative AHP weights.

In cases where a criterion is not available for a site, the criterion is not included and the remaining weights are renormalized:

`WLC = Σ(wj × xj) / Σ(wj for available criteria)`

where:

* `wj` is the cluster-specific AHP weight for criterion `j`
* `xj` is the standardized site score for criterion `j`

## Intentional N/A values

The script differentiates between documented non-applicable values from unexpected missing data.

The following cases are treated as intentional N/A values:

* `RUSLE_SCR` is omitted when `Rusle_MTH` is `Urban excl.`, `Coastal excl.`, or `Other excl.`
* `ELSUS_SCR` is omitted when `ELSUS_MTH` is `NoData>400m`
* `ASSET_SCR` is omitted when `Material_general` is `Unknown / Not specified`

In these cases, the remaining AHP weights are renormalized for that site.

Unexpected missing criterion values are recorded in `00_Data_Quality.csv` and stop the analysis.

## Risk classification

Recalculated WLC scores are assigned to the same 5 risk classes used in the main risk assessment:

|Risk class|WLC score|
|-|-|
|Very Low|1–<2|
|Low|2–<4|
|Moderate|4–<6|
|High|6–<8|
|Very High|8–9|

## Sensitivity measures

Two main forms of change are recorded.

### Site class changes

For each sensitivity run, the script records:

* Number of sites that change risk class
* Percentage of sites that change risk class

### Overall Change Rate (OCR)

The script also calculates the Overall Change Rate (OCR) adapted from Chen et al. (2013).

The original method compares changes in raster cell counts between classes. The calculation is adapted to compare the number of archaeological sites in each risk class before and after each pairwise comparison change.

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

The input table contains the site identifiers, environmental cluster assignments, standardized criterion scores and the supporting fields needed to identify the intentional N/A values.

The _MTH fields are method/status fields used to document how criterion values were assigned or why a value is not available. Rusle_MTH records cases where the RUSLE soil-erosion criterion was excluded, while ELSUS_MTH records the treatment of landslide-susceptibility NoData values. Material_general is used to identify sites where an Asset Vulnerability score could not be assigned.

|Field|Description|
|-|-|
|`Rusle_MTH`|Method/status field for the RUSLE soil erosion score, including documented exclusions|
|`ELSUS_MTH`|Method/status field for the ELSUS landslide susceptibility score, including sites where no valid cell was available within 400 m|
|`Material_general`|General material/physical typology used to identify sites where an Asset Vulnerability score could not be assigned|

Precise archaeological site coordinates are not included.

The script also reads the three AHP workbooks from:

`../AHP/matrices/`

These are:

* `Thrace_AHP_C1.xlsx`
* `Thrace_AHP_C2.xlsx`
* `Thrace_AHP_C3.xlsx`

## Output files

### `00_Data_Quality.csv`

Records sites with intentional N/A criteria or missing criterion values and documents the reason for each exclusion.

### `01_Baseline_Weights.csv`

Contains the baseline AHP criterion weights and consistency statistics for the 3 clusters.

### `02_Pairwise_Sensitivity_Runs.csv`

Contains the results for each pairwise comparison change including:

* Baseline and perturbed Saaty values
* Alternative criterion weights
* Baseline and alternative CR
* Number and percentage of sites changing class
* OCR
* Baseline and alternative risk-class counts

### `03_Site_Level_Sensitivity.csv`

Contains the results for each accepted sensitivity run including:

* Baseline and alternative WLC scores
* Baseline and alternative risk classes
* Whether the site changed class
* Criteria excluded as intentional N/A values
* Weight sums before and after perturbation

Precise site coordinates are not included in the public version.

### `04_Criterion_Sensitivity_Summary.csv`

Summarizes the sensitivity results by cluster and criterion using:

* Number of valid runs
* Mean and maximum OCR
* Mean and maximum percentage of sites changing risk class

### `Run_Log.txt`

Provides a concise record of the analysis run, including the number of sites, baseline CR values, number of sensitivity runs and the number of accepted and rejected matrices.

## Requirements

The script requires:

* Python 3
* `openpyxl`

Install `openpyxl` with:

    python -m pip install openpyxl

## Running the script

From the repository root or the script directory, run:

    python sensitivity_analysis/scripts/Thrace_AHP_Sensitivity.py

The script reads the required AHP workbooks and sensitivity input table from the repository locations and writes the resulting files to:

`sensitivity_analysis/results/`

## Methodology source

Chen, Y., Yu, J., & Khan, S. (2013). The spatial framework for weight sensitivity analysis in AHP-based multi-criteria decision making. *Environmental Modelling & Software, 48*, 129–140. https://doi.org/10.1016/j.envsoft.2013.06.010
