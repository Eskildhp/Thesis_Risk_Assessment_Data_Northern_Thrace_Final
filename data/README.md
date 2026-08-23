# Public Site Dataset

The folder has the public version of the archaeological site master table containing archaeological descriptions, environmental variables, standardized criterion scores, cluster assignments, final risk results and some analytical outputs for the 250 sites in the dataset.

### File

`Sites\_master.csv`

### Dataset contents

The dataset contains fields relating to:

* Site identification and spatial reference
* Archaeological chronology and site classification
* Construction material and exposure
* Cultural heritage status
* Environmental variables for the analysis
* Standardized hazard and vulnerability scores
* Cluster assignment
* Final weighted linear combination (WLC) risk score and risk class
* Monte Carlo uncertainty data
* Getis-Ord Gi\* hot-spot analysis data

The field names correspond to the database used in the analyses.

### Archaeological and geographic information

|Field|Description|
|-|-|
|`Site\_ID`|Unique identifier assigned to each site|
|`Site`|Standardized site name|
|`Region`|Administrative region (*oblast*) where the site is located|
|`Location`|Closest nearby settlement or geographic reference|
|`Material\_general`|General site construction material used|
|`Exposure\_class`|Classification of the site exposure|
|`Exposure\_tx`|Text description corresponding to the exposure classification|
|`Int\_Status`|International cultural heritage status information (where applicable)|
|`Nat\_Status`|National cultural heritage status information (where applicable)|

Chronological information is stored in period fields. A site may have evidence from more than one chronological phase. In these cases the associated `\_class` fields record the site classification used for that period. Chronological fields include: Paleolithic, Neolithic, Chalcolithic, Bronze Age, Iron Age, Roman, Early Byzantine, First Bulgarian Empire and Second Bulgarian Empire.

### Environmental variables

The master table contains environmental values used in the clustering, risk assessment as well as supporting data.

|Field|Description|
|-|-|
|`DEM\_`|Elevation value in the environmental dataset|
|`Slope\_`|Terrain slope|
|`Aspect\_cos\_`|Cosine-transformed aspect|
|`Aspect\_sin\_`|Sine-transformed aspect|
|`FL\_Dist`|Flood related distance variable|
|`FL\_Depth`|Flood depth variable|
|`rusle\_cluster`|RUSLE soil erosion value for the environmental workflow|
|`rusle\_log`|Log-transformed RUSLE variable used in the environmental workflow; interpretation should be read together with Rusle_MTH|
|`Final\_FWI`|Final Fire Weather Index value used in the analysis|
|`ELSUS`|Landslide susceptibility value|
|`PGA`|Peak ground acceleration value used for the seismic criterion|
|`Lithology`|Lithological classification for context|
|`CLC\_code`|CORINE Land Cover code|
|`CLC\_text`|CORINE Land Cover class description|

### Standardized risk fields

|Field|Description|
|-|-|
|`SEIS\_SCR`|Standardized seismic hazard score|
|`FLOOD\_SCR`|Standardized flood hazard score|
|`FWI\_SCR`|Standardized wildfire hazard score|
|`ELSUS\_SCR`|Standardized landslide susceptibility score|
|`RUSLE\_SCR`|Standardized soil erosion score|
|`ASSET\_SCR`|Standardized vulnerability score|
|`Cluster\_3`|Final environmental cluster assigned using Ward hierarchical clustering|
|`WLC\_RISK2`|Final weighted linear combination risk score|
|`RISK\_CLASS2`|Final risk class|

### Method and status fields

Several fields record how environmental values were assigned or handled during the data preparation, including NoData or nearest-valid-value procedures.

|Field|Description|
|-|-|
|`Rusle\_MTH`|Method or status information for the RUSLE soil erosion criterion|
|`FWI\_MTH`|Method or status information for the Fire Weather Index criterion|
|`FWI\_DIST`|Distance to the substituted FWI value where nearest-valid-value handling was needed|
|`ELSUS\_MTH`|Method or status information for the ELSUS landslide susceptibility criterion|
|`ELSUS\_DIST`|Distance to the nearest valid ELSUS value used to determine direct, nearest-value, or NoData status|



### Monte Carlo uncertainty outputs

The dataset contains selected site-level outputs from the Monte Carlo uncertainty analysis.

|Field|Description|
|-|-|
|`MC\_Mean\_WLC`|Mean WLC risk score across the Monte Carlo simulations|
|`MC\_SD`|Standard deviation of the simulated WLC risk scores|
|`MC\_CV\_Pct`|Coefficient of Variation (CV) calculated from the simulated WLC scores|
|`MC\_Min\_WLC`|Minimum simulated WLC risk score|
|`MC\_Max\_WLC`|Maximum simulated WLC risk score|
|`Baseline\_Class\_Stability\_Pct`|Percentage of simulations where the site stayed in the baseline risk class|

### Hot-spot analysis outputs

|Field|Description|
|-|-|
|`Gi\_Bin`|Getis-Ord Gi\* significance bin |
|`gi\_class`|Text interpretation of the corresponding hotspot, cold-spot or non-significant classification|

### Data sanitization

The public dataset is derived from the final internal site master table but without the precise archaeological site coordinates.

The following spatial fields are excluded from the public version:

* `X\_coordinate`
* `Y\_coordinate`

`Region` and `Location` are included only as broader geographic reference fields. `Location` identifies the closest nearby settlement or geographic reference and should not be interpreted as the precise position of the archaeological site.

### Relationship to the repository

`Sites\_master.csv` is the central public site-level dataset in the repository.

More specialized files are located in the analysis folders:

* `clustering/` contains the transformed variables and outputs used for environmental clustering
* `risk\_assessment/` contains the final WLC risk assessment outputs
* `sensitivity\_analysis/inputs/` contains the fields required for the One-at-a-Time sensitivity analysis
* `uncertainty\_analysis/inputs/` contains the fields required for the Monte Carlo uncertainty analysis

The files are derived from the same site database but are limited to the variables required for each analytical step.

### Repository structure

```text
data/
├── README.md
└── Sites\_master.csv
```

### Data use

The dataset is provided as supporting material for the thesis and should be used with the methodology, data-source documentation and analysis descriptions in the thesis and repository.

Precise archaeological site coordinates are not included in the public repository.

