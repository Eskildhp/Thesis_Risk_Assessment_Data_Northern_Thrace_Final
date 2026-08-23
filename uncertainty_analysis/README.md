# Monte Carlo Uncertainty Analysis

This folder contains the Monte Carlo uncertainty analysis used to evaluate the effect of uncertainty in the AHP criterion weights in the WLC risk results.

The analysis is performed separately for the 3 clusters used.

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

The WLC score is recalculated for every Monte Carlo simulation run using the perturbed criterion weights.

In cases where a criterion is not available for a site the criterion is omitted and the remaining weights are renormalized:

`WLC = Σ(wj × xj) / Σ(wj for available criteria)`

where:

* `wj` is the cluster-specific AHP weight for criterion `j`
* `xj` is the standardized site score for criterion `j`

### Intentional N/A values

The script differentiates between documented non-applicable values from intentional missing data.

The following cases are treated as intentional N/A values:

* `RUSLE\_SCR` is omitted when `Rusle\_MTH` is `Urban excl.`, `Coastal excl.`, or `Other excl.`
* `ELSUS\_SCR` is omitted when `ELSUS\_MTH` is `NoData>400m`
* `ASSET\_SCR` is omitted when `Material\_general` is `Unknown / Not specified`

For these cases, the remaining AHP weights are renormalized for that site.

Unexpected missing criterion values are recorded in `00\_Data\_Quality.csv` and stop the analysis from running.

### Baseline validation

Before the Monte Carlo simulations are run, the script recalculates the baseline WLC score for each site using the original cluster-specific AHP weights.

The calculated baseline is compared with the existing ArcGIS WLC field:

`WLC\_RISK2`

The comparison uses a tolerance of:

`1e-5`

If any site differs from the ArcGIS baseline by more than this tolerance, the analysis stops and the differences are recorded in `01A\_Baseline\_Validation.csv`.

### Risk classification

The baseline and simulated WLC scores use the same five risk classes as the main risk assessment:

|Risk class|WLC score|
|-|-|
|Very Low|1–<2|
|Low|2–<4|
|Moderate|4–<6|
|High|6–<8|
|Very High|8–9|

### Uncertainty measures

For each archaeological site, the simulation results are summarized using:

* Mean simulated WLC score
* Population standard deviation
* Coefficient of variation
* Minimum simulated WLC score
* Maximum simulated WLC score
* Difference between the Monte Carlo mean and baseline WLC
* Risk class of the Monte Carlo mean
* Percentage of simulations remaining in the baseline risk class

Classification stability is calculated as the percentage of the 1,000 simulations where a site remains in its original baseline risk class.

The results also record the number and percentage of simulations where each site falls in each of the 5 risk classes.

### Convergence checks

Simulation convergence is checked after:

* 100 iterations
* 250 iterations
* 500 iterations
* 750 iterations
* 1,000 iterations

At each checkpoint, the site-level Monte Carlo means and standard deviations are compared with the previous checkpoint.

The output records the mean and maximum absolute changes in these values between checkpoints.

### Folder structure

&#x20;   uncertainty\_analysis/
    ├── README.md
    ├── inputs/
    │   └── Sites\_uncertainty\_input.csv
    ├── results/
    │   ├── 00\_Data\_Quality.csv
    │   ├── 01\_Baseline\_Weights.csv
    │   ├── 01A\_Baseline\_Validation.csv
    │   ├── 02\_MC\_Iteration\_Weights.csv
    │   ├── 03\_MC\_Site\_Summary.csv
    │   ├── 04\_MC\_Cluster\_Summary.csv
    │   ├── 05\_MC\_Convergence.csv
    │   ├── 06\_Top\_20\_Uncertain\_Sites.csv
    │   └── Run\_Log.txt
    └── scripts/
        └── Thrace\_AHP\_Monte\_Carlo.py


### Input file

### `Sites\_uncertainty\_input.csv`

The input table contains the site identifiers, cluster assignments, standardized criterion scores, fields used to identify intentional N/A values, and the existing ArcGIS WLC score used for baseline validation.

The `\_MTH` fields are method/status fields used to document how criterion values were assigned or why a value is unavailable.

|Field|Description|
|-|-|
|`Rusle\_MTH`|Method/status field for the RUSLE soil erosion score, including documented exclusions|
|`ELSUS\_MTH`|Method/status field for the ELSUS landslide susceptibility score, including sites where no valid cell was available within 400 m|
|`Material\_general`|General material/physical typology used to identify sites where an Asset Vulnerability score could not be assigned|
|`WLC\_RISK2`|Existing ArcGIS WLC result used to validate the recalculated baseline before the simulations begin|

Precise archaeological site coordinates are not included.

The script also reads the three AHP workbooks from:

`../AHP/matrices/`

These are:

* `Thrace\_AHP\_C1.xlsx`
* `Thrace\_AHP\_C2.xlsx`
* `Thrace\_AHP\_C3.xlsx`

### Output files

### `00\_Data\_Quality.csv`

Records sites with intentional N/A criteria or unexpected missing criterion values and documents the reason for each exclusion.

### `01\_Baseline\_Weights.csv`

Contains the baseline AHP criterion weights and consistency statistics for the 3 clusters.

### `01A\_Baseline\_Validation.csv`

Compares the baseline WLC recalculated by the script with the existing ArcGIS `WLC\_RISK2` value for each site.

### `02\_MC\_Iteration\_Weights.csv`

Contains the 6 normalized criterion weights generated for each Monte Carlo iteration and cluster.

This file contains 3,000 sets of simulated criterion weights based on 1,000 simulations for each of the 3 clusters .

### `03\_MC\_Site\_Summary.csv`

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

### `04\_MC\_Cluster\_Summary.csv`

Summarizes the site-level Monte Carlo results by cluster.

The file includes cluster summaries including:

* Baseline and Monte Carlo mean WLC
* Absolute change from baseline
* Standard deviation
* Coefficient of variation
* Classification stability
* Number of sites where Monte Carlo mean risk class is different from the baseline class

### `05\_MC\_Convergence.csv`

Records changes in the site-level Monte Carlo means and standard deviations between the successive convergence checkpoints.

### `06\_Top\_20\_Uncertain\_Sites.csv`

Contains the 20 sites with the highest coefficient of variation in the Monte Carlo results.

Precise site coordinates are not included in the public version.

### `Run\_Log.txt`

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

&#x20;   python -m pip install openpyxl


## Running the script

From the repository root, run:

&#x20;   python uncertainty\_analysis/scripts/Thrace\_AHP\_Monte\_Carlo.py


The script reads the AHP matrices and uncertainty input table from their repository locations and writes the output files to:

`uncertainty\_analysis/results/`

## Reproducibility

The Monte Carlo analysis uses the fixed random seed `20260813`.

Running the script with the same input files, AHP matrices, and Python implementation will reproduce the same sequence of simulated weight perturbations.

