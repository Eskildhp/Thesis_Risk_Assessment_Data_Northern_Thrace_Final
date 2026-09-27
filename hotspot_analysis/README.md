# Getis-Ord Gi* Hotspot Analysis

This folder contains the results from the Getis-Ord Gi* hot spot analysis. The analysis was carried out in ArcGIS Pro using the final cluster-specific WLC risk score (`WLC_RISK3`).

### Method

Getis-Ord Gi* was used to identify statistically significant hotspots and cold spots in the WLC risk scores. Positive z-scores show clustering of high risk values and negative z-scores show clustering of low risk values.

The analysis used:

* 8 nearest neighbors
* Euclidean distance

The sites are not evenly distributed across the study area. Eight nearest neighbors were therefore used instead of a fixed distance. The distance-band analysis did not show a clear peak.

### Output

`results/Getis_Ord_Gi_site_results.csv`

This file has the Getis-Ord Gi* results for the 250 sites. `Site_ID` can be used to link it to `data/Sites_master.csv`.

The file has the site name and ID, WLC risk score and the Gi* results.

The fields are:

|Field|Description|
|-|-|
|`Site_ID`|Archaeological site identifier|
|`Site`|Archaeological site name|
|`WLC_RISK3`|WLC risk score used in the Gi* analysis|
|`GiZScore`|Gi* z-score|
|`GiPValue`|Gi* p-value|
|`Gi_Bin_3`|Gi* category from ArcGIS Pro|
|`gi_class`|Hotspot, cold spot or not significant and the confidence level|

`WLC_RISK` and `Gi_Bin` are from an earlier risk calculation and are not used here. `gi_class` was updated from the final `Gi_Bin_3`.

### Interpretation

Positive Gi* values show areas where high risk scores cluster together, while negative values show areas where low risk scores cluster together. Hotspots and cold spots are shown at 90%, 95% and 99% confidence levels. Other sites are not significant.

### Relationship to the thesis

These results are presented in Chapter 5 as a table and a map showing the distribution of hotspots and cold spots.

### Data availability

The CSV does not contain the archaeological site coordinates.

### Repository structure

```text
hotspot_analysis/
├── README.md
└── results/
    └── Getis_Ord_Gi_site_results.csv
```

