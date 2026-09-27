# Monte Carlo Uncertainty Analysis

This folder contains the Monte Carlo uncertainty analysis used to evaluate the effect of uncertainty in the AHP criterion weights in the WLC risk results.

The analysis is performed separately for the 3 clusters used.

The input uses the final five-component `SEIS_SCR` values and the final cluster-specific AHP matrices in `../AHP/matrices/`. The recalculated baseline risk scores and classes correspond to `WLC_RISK3` and `RISK_CL3` in `../data/Sites_master.csv`.

### Method

The script reads the AHP pairwise comparison matrix for each cluster and reproduces the baseline criterion weights using column normalization and the mean of each normalized row.

The script performs 1,000 Monte Carlo simulations for each cluster.

During each simulation each baseline AHP weight is varied by a random value within ±10% of the original value using a uniform distribution.

The perturbed weights are then normalized so that the six criterion weights total 1.

The resulting weights are used to recalculate the WLC risk score for each site in its cluster.

A fixed random seed (`20260813`) is used so that the simulation results can be reproduced.

### Criteria

Six criteria are included in the uncertainty analysis:

* Seismic hazard
* Wildfire hazard
* Flood hazard
* Soil erosion
* Landslide susceptibility
* Asset vulnerability

### WLC recalculation

Each Monte Carlo run gives a new set of weights. These are used to calculate the WLC scores for that run.

Some sites do not have values for all six criteria. If a value is missing, the WLC is calculated from the criteria that have values:

`WLC = Σ(wj × xj) / Σ(wj for available criteria)`

where:

* `wj` AHP weight for criterion `j`
* `xj` site score for criterion `j`

### Missing values

Some values are missing due to the way the original environmental data were handled:

The following cases are treated as intentional N/A values:

* `RUSLE_SCR` is not used when `Rusle_MTH` is `Urban excl.`, `Coastal excl.`, or `Other excl.`
* `ELSUS_SCR` is not used when `ELSUS_MTH` is `NoData>400m`
* `ASSET_SCR` is not used when `Material_general` is `Unknown / Not specified`

For these sites, the WLC calculation uses the criteria that are available.

Unexpected missing criterion values are recorded in `00_Data_Quality.csv` and stop the analysis from running.

### Baseline validation

Before the Monte Carlo simulations are run, the script recalculates the baseline WLC score for each site using the original cluster-specific AHP weights.

The calculated baseline is compared with the existing ArcGIS WLC field:

`WLC_RISK3`

The comparison uses a tolerance of:

`1e-5`

If the difference is greater than this tolerance, the analysis stops. The site and the difference are saved in `01A_Baseline_Validation.csv`.


### Risk classification

The baseline and simulated WLC scores are classified using the same ranges:

|Risk class|WLC score|
|-|-|
|Very Low|1–<2|
|Low|2–<4|
|Moderate|4–<6|
|High|6–<8|
|Very High|8–9|

### Uncertainty measures

The 1,000 simulations give a range of results for each archaeological site. For each site, the following were calculated:

* Mean WLC
* Standard deviation
* Coefficient of variation
* Lowest WLC score
* Highest WLC score
* Difference between the Monte Carlo mean and baseline WLC
* Risk class of the Monte Carlo mean
* Percentage of runs where the site stays in the baseline risk class

The percentage in the original risk class is used to show class stability.

Of the 250 sites, 225 do not change risk class in any of the 1,000 runs. The other 25 change at least once. The values can be checked against the `MC_*` fields in `../data/Sites_master.csv`.

The results also show how often each site is assigned to each of the five risk classes.

### Convergence checks

The simulation was checked at five points to see whether the results had stabilized:

* 100 runs
* 250 runs 
* 500 runs
* 750 runs
* 1,000 runs

At each checkpoint, the site-level Monte Carlo means and standard deviations are compared with the previous checkpoint.

The output records the mean and maximum absolute changes in these values between checkpoints.

### Folder structure

```text
uncertainty_analysis/
    ├── README.md
    ├── inputs/
    │   └── Sites_uncertainty_input.csv
    ├── results/
    │   ├── 00_Data_Quality.csv
    │   ├── 01_Baseline_Weights.csv
    │   ├── 01A_Baseline_Validation.csv
    │   ├── 02_MC_Iteration_Weights.csv
    │   ├── 03_MC_Site_Summary.csv
    │   ├── 04_MC_Cluster_Summary.csv
    │   ├── 05_MC_Convergence.csv
    │   ├── 06_Top_20_Uncertain_Sites.csv
    │   └── Run_Log.txt
    └── scripts/
        └── Thrace_AHP_Monte_Carlo.py
```

### Input file

### `Sites_uncertainty_input.csv`

This file has the data used for the Monte Carlo analysis. It contains the site ID, cluster, criterion scores and the original `WLC_RISK3` score. The original WLC score is used to check the calculation before running the simulations.

The `_MTH` fields show why some RUSLE and ELSUS values are missing.

|Field|Description|
|-|-|
|`Rusle_MTH`|Status field for the RUSLE soil erosion score, including documented exclusions|
|`ELSUS_MTH`|Status field for the ELSUS landslide susceptibility score, including sites where no valid cell was available within 400 m|
|`Material_general`|Material/typology used for asset vulnerability|
|`WLC_RISK3`|WLC risk score used to validate the recalculated baseline before the simulations begin|

The public file does not contain site coordinates.

The script also uses the three AHP matrices in:

`../AHP/matrices/`

These are:

* `Thrace_AHP_C1.xlsx`
* `Thrace_AHP_C2.xlsx`
* `Thrace_AHP_C3.xlsx`

### Output files

### `00_Data_Quality.csv`

Lists sites with missing criterion values and the reason for the missing value.

### `01_Baseline_Weights.csv`

Shows the AHP weights and consistency results for the three clusters.### `01A_Baseline_Validation.csv`

### `01A_Baseline_Validation.csv`

Compares the baseline WLC recalculated by the script with the final ArcGIS `WLC_RISK3` value for each site.

### `02_MC_Iteration_Weights.csv`

Contains the 6 normalized criterion weights generated for each Monte Carlo iteration and cluster.

This file contains 3,000 sets of simulated criterion weights based on 1,000 simulations for each of the 3 clusters.

### `03_MC_Site_Summary.csv`

Contains the site-level uncertainty results, including:

* Baseline WLC and risk class
* Monte Carlo mean WLC
* Monte Carlo standard deviation
* Coefficient of variation
* Minimum and maximum simulated WLC
* Mean difference from the baseline WLC
* Monte Carlo mean risk class
* Baseline-class stability
* Counts and percentages for each simulated risk class

Precise site coordinates are not included in the public version.

### `04_MC_Cluster_Summary.csv`

Summarizes the site-level Monte Carlo results by cluster.

The file includes cluster summaries including:

* Baseline and Monte Carlo mean WLC
* Absolute change from baseline
* Standard deviation
* Coefficient of variation
* Classification stability
* Number of sites where Monte Carlo mean risk class is different from the baseline class

### `05_MC_Convergence.csv`

Records changes in the site-level Monte Carlo means and standard deviations between the successive convergence checkpoints.

### `06_Top_20_Uncertain_Sites.csv`

Contains the 20 sites with the highest coefficient of variation in the Monte Carlo results.

Precise site coordinates are not included in the public version.

### `Run_Log.txt`

Provides a record of the analysis run, including:

* Number of simulations per cluster
* Weight perturbation range
* Random seed
* Baseline validation settings
* Number of baseline mismatches
* Number of sites in each cluster
* Output files produced

## Requirements

The script requires:

* Python 3
* `openpyxl`

Install `openpyxl` with:

```bash
python -m pip install openpyxl
```

## Running the script

Run the script from the repository root:
```bash
python uncertainty_analysis/scripts/Thrace_AHP_Monte_Carlo.py
```

The results are saved in:

`uncertainty_analysis/results/`

## Reproducibility

`20260813` is used as the random seed, making it possible for the simulation to be repeated with the same inputs files.

