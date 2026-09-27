# Public Site Dataset

This folder contains the results for the 250 archaeological sites included in the study. The table contains information on the sites and construction materials, exposure values, standardized criterion scores, cluster assignments and the final results. The precise coordinates of the archaeological sites are not included.

### File

`Sites_master.csv`

### Dataset contents

The dataset contains fields relating to:

* Site identification and broad geographic reference
* Construction material and exposure
* The five standardized seismic components and final seismic score
* Standardized hazard and vulnerability scores
* Environmental cluster assignment
* Final weighted linear combination (WLC) risk score and class
* One-at-a-Time (OAT) sensitivity results
* Monte Carlo uncertainty results
* Getis-Ord Gi* hot-spot analysis results
* Global AHP comparison results

The field names are the same as those used in the final site database, except for the OAT field `SUM_Changed_Num_1` which is shown here as `SUM_Changed_Num`.

### Archaeological and geographic information

|Field|Description|
|-|-|
|`Site_ID`|Unique identifier assigned to each site|
|`Site`|Standardized site name|
|`Region`|Administrative region (*oblast*) where the site is located|
|`Location`|Closest nearby settlement or geographic reference|
|`Material_general`|General site construction material|
|`Exposure_class`|Classification of site exposure|

The chronology and site type fields are in the internal database, but are not included in the public results table.

### Environmental variables

The master table contains environmental values used in the clustering, risk assessment as well as supporting data.

|Field|Description|
|-|-|
|`DEM_`|Elevation value in the environmental dataset|
|`Slope_`|Terrain slope|
|`Aspect_cos_`|Cosine-transformed aspect|
|`Aspect_sin_`|Sine-transformed aspect|
|`FL_Dist`|Flood related distance variable|
|`FL_Depth`|Flood depth variable|
|`rusle_cluster`|RUSLE soil erosion value for the environmental workflow|
|`rusle_log`|Log-transformed RUSLE value converted using a logarithm. See also Rusle_MTH|
|`Final_FWI`|Final Fire Weather Index value used in the analysis|
|`ELSUS`|Landslide susceptibility value|
|`PGA`|Peak ground acceleration value used for the seismic criterion|
|`Lithology`|Lithological classification for context|
|`CLC_code`|CORINE Land Cover code|
|`CLC_text`|CORINE Land Cover class description|

### Seismic criterion

The seismic criterion is calculated from five factors: PGA, epicentre density, magnitude, focal depth and fault distance. The values for each factor were standardized to a 1, 3, 5, 7 and 9 scale. All five factors were given the same weight when calculating the seismic score.

|Field|Description|
|-|-|
|`PGA_SC`|Peak ground acceleration score|
|`DEN_SC`|Earthquake epicentre density score|
|`MAG_SC`|Earthquake magnitude score|
|`DEP_SC`|Earthquake focal depth score; shallower depths receive higher scores|
|`FLT_SC`|Fault-distance score; shorter distances receive higher scores|
|`SEIS_AVG`|Mean of the five standardized seismic component scores|
|`SEIS_SCR`|Final seismic criterion score after reclassifying `SEIS_AVG`|

### Standardized risk and final model fields

|Field|Description|
|-|-|
|`FLOOD_SCR`|Standardized flood hazard score|
|`FWI_SCR`|Standardized fire-weather danger score|
|`ELSUS_SCR`|Standardized landslide susceptibility score|
|`RUSLE_SCR`|Standardized soil erosion score|
|`ASSET_SCR`|Standardized asset vulnerability score|
|`Cluster_3`|Final environmental cluster assigned using Ward hierarchical clustering|
|`WLC_RISK3`|Final cluster-specific WLC risk score|
|`RISK_CL3`|Final cluster-specific risk class|

The `FWI_SCR` field shows fire-weather danger and not actual fires. `RUSLE_SCR` is missing for 77 sites and `ELSUS_SCR` for 21 sites. Empty cells are missing values and do not mean a score of zero. Where a criterion was missing, it was left out of the risk calculation and the remaining weights were adjusted to sum to 1.

### OAT sensitivity output

|Field|Description|
|-|-|
|`SUM_Changed_Num`|Number of OAT scenarios where the site changed risk class. A value of 0 means the risk class did not change|

### Monte Carlo uncertainty outputs

The dataset shows Monte Carlo results for each site.

|Field|Description|
|-|-|
|`MC_MEAN3`|Mean simulated WLC risk score|
|`MC_SD3`|Standard deviation of simulated WLC risk scores|
|`MC_CV3`|Coefficient of variation of simulated WLC risk scores, expressed as a percentage|
|`MC_MIN3`|Minimum simulated WLC risk score|
|`MC_MAX3`|Maximum simulated WLC risk score|
|`MC_STAB3`|Percentage of simulations where the site stayed in the baseline risk class|

### Hotspot analysis outputs

|Field|Description|
|-|-|
|`Gi_Bin_3`|Getis-Ord Gi* significance level from the final analysis|
|`GiZScore`|Getis-Ord Gi* z-score|
|`GiPValue`|Getis-Ord Gi* p-value|
|`gi_class`|final classification as a hotspot, cold spot or not significant|

### Global AHP comparison outputs

|Field|Description|
|-|-|
|`ALL_RISK`|Risk score using the global AHP weights|
|`ALL_CLASS`|Risk class using the global AHP weights|
|`RISK_DIFF`|Difference between cluster-specific AHP and global AHP scores (`WLC_RISK3` minus `ALL_RISK`)|
|`ABS_DIFF`|Absolute value of `RISK_DIFF`|
|`CLASS_SHIFT`|Change in risk class between `RISK_CL3` and `ALL_CLASS`; positive values show a higher risk class with the cluster-specific AHP|

### Data preparation

The public dataset uses the final site master table, but the precise archaeological site coordinates have been removed:

* `X_coordinate`
* `Y_coordinate`

`Region` and `Location` provide general geographic information. `Location` is the nearest settlement or geographic reference, not the precise location of the archaeological site.

### Repository files

`Sites_master.csv` is the main public results table for the 250 sites. It does not contain all of the environmental and chronological fields from the internal database. The files used for each analysis are described in the relevant analysis folders.

* `clustering/` contains the variables and results from the environmental clustering
* `risk_assessment/` contains the results from the final WLC risk assessment
* `sensitivity_analysis/` contains the results from the OAT sensitivity analysis
* `uncertainty_analysis/` contains the results from the Monte Carlo uncertainty analysis
* `hotspot_analysis/` contains the results from the Getis-Ord Gi* analysis

### Repository structure

```text
data/
├── README.md
└── Sites_master.csv
```

### Data use

The dataset supports the results presented in the thesis. The methods, data sources and individual analyses are described in the thesis and the relevant repository folders. Continuous values have been rounded in the public dataset.

Precise archaeological site coordinates are not included in the public repository.
