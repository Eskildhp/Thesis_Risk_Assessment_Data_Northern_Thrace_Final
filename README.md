# A GIS Framework for Risk Management of Immovable Cultural Heritage in Northern Thrace

This repository contains the supporting material for the master's thesis A GIS Framework for Risk Management of Immovable Cultural Heritage: A Case Study in Northern Thrace (Southern Bulgaria). The study assesses relative archaeological risk in Northern Thrace based on environmental hazards and the vulnerability of the archaeological sites. The hazards include seismic hazard, flooding, wildfire, landslide susceptibility and soil erosion. Asset vulnerability is also included. The archaeological sites were first grouped based on similar environmental conditions. The AHP criterion weights were applied to each cluster. The resulting criterion weights are combined with standardized risk variables using Weighted Linear Combination (WLC). The risk scores are evaluated using Getis-Ord Gi\* hot spot analysis. The robustness of the model is evaluated using One-at-a-Time (OAT) sensitivity analysis and Monte Carlo uncertainty analysis.

Repository contents

The repository contains supporting material used to document the analytical workflow of the thesis, including:

* The archaeological site master dataset (public version)
* Scripts and documentation for the environmental data 
* Environmental clustering data and visualizations
* Cluster-specific AHP matrices, evidence and calculations
* Risk assessment data and WLC results
* Getis-Ord Gi\* hotspot analysis data and documentation
* OAT sensitivity analysis data, scripts and results
* Monte Carlo uncertainty analysis data, scripts and results
* Documentation describing the procedures and files

The source datasets are specified in the thesis and documentation. In cases where third-party datasets may not be distributed, the source and access information or derived analytical data are provided.

### Analytical workflow

The main analytical steps are:

1. Preparation of the environmental and archaeological data
2. Environmental clustering
3. Cluster-specific Analytic Hierarchy Process (AHP)
4. Weighted Linear Combination (WLC)
5. Getis-Ord Gi\* hot spot analysis
6. One-at-a-Time (OAT) sensitivity analysis
7. Monte Carlo uncertainty analysis

### Repository structure

The repository follows the main steps of the workflow.

```text
Thesis\_Risk\_Assessment\_Data\_Northern\_Thrace/
├── README.md
├── LICENSE
├── .gitignore
│
├── data/
│   ├── README.md
│   └── Sites\_master.csv
│
├── data\_acquisition/
│   ├── README.md
│   └── scripts/
│       └── Copernicus\_DEM\_download.ps1
│
├── clustering/
│   ├── README.md
│   ├── ward\_clustering\_ruslog.py
│   ├── Cluster\_matrix\_Ruslog.csv
│   ├── results/
│   └── visualization/
│
├── AHP/
│   ├── README.md
│   ├── matrices/
│   ├── evidence/
│   └── results/
│
├── risk\_assessment/
│   ├── README.md
│   └── results/
│
├── hotspot\_analysis/
│   ├── README.md
│   └── results/
│       └── Getis\_Ord\_Gi\_site\_results.csv
│
├── sensitivity\_analysis/
│   ├── README.md
│   ├── inputs/
│   ├── scripts/
│   └── results/
│
└── uncertainty\_analysis/
    ├── README.md
    ├── inputs/
    ├── scripts/
    └── results/
```

Each analytical folder contains its own README with more detailed information about the procedure, files and outputs.

### Data

The `data/` folder contains the public site-level master dataset used in the thesis workflow.

`Sites\_master.csv` contains archaeological, descriptive, environmental and analytical attributes for the 250 archaeological sites included in the final analysis.

Precise site coordinates are not included in the public dataset.

### Data acquisition

The `data\_acquisition/` folder has the documentation and scripts for external environmental datasets.

A PowerShell script was used to identify and download Copernicus DEM tiles for the study area through the Copernicus Data Space Ecosystem.

Some third-party environmental datasets are not included in the repository. These are subject to the terms and conditions of the respective data providers.

### Environmental spatial clustering

The `clustering/` folder has the Ward hierarchical clustering workflow that was used to group sites according to similar environmental characteristics.

The folder includes:

* The clustering matrix
* The Ward hierarchical clustering Python script
* Cluster solutions containing 3-7 clusters
* Silhouette score and cluster-size evaluation
* Environmental profiles of the potential (candidate) and selected clusters
* Ward dendrograms (full and truncated)
* A parallel boxplot with the environmental characteristics of the final cluster solution (3 clusters)

Detailed information is found in `clustering/README.md`.

### Analytic Hierarchy Process

The `AHP/` folder has the 3 cluster-specific AHP models used to derive the criterion weights.

It includes:

* The pairwise comparison matrices for Clusters 1, 2 and 3
* The evidence used to support the pairwise comparisons
* Calculated criterion weights
* Consistency calculations and summary results

Detailed information is provided in `AHP/README.md`.

### Risk assessment

The `risk\_assessment/` folder contains the final site-level Weighted Linear Combination results.

The results include the standardized criterion scores, cluster assignment, final WLC archaeological risk score and categorical risk classification for each archaeological site.

Detailed information is provided in `risk\_assessment/README.md`.

### Getis-Ord Gi\* hot spot analysis

The `hotspot\_analysis/` folder contains the site-level results from the Getis-Ord Gi\* analysis. The analysis was used to identify statistically significant hotspots and cold spots based on the final WLC risk scores. The process was implemented in ArcGIS Pro using eight nearest neighbors and Euclidean distance. The public results include the site identifiers, risk scores, Getis-Ord Gi\* statistics and significance classifications. Precise archaeological site coordinates are not included.

Detailed information is found in `hotspot\_analysis/README.md`.

### OAT sensitivity analysis

The `sensitivity\_analysis/` folder has the One-at-a-Time sensitivity data and analysis for evaluating how changes in individual AHP pairwise comparisons influence the archaeological risk.

The pairwise comparisons were changed by one level on the Saaty scale and the remaining comparisons were kept unchanged. Criterion weights, consistency ratios, WLC scores and risk classifications were recalculated after each perturbation. This was implemented for each cluster.

In this folder: analysis script, data, baseline weights, pairwise sensitivity runs and sensitivity results

Detailed information is found in `sensitivity\_analysis/README.md`.

### Monte Carlo uncertainty analysis

The `uncertainty\_analysis/` folder has the Monte Carlo analysis used to evaluate uncertainty related to the cluster-specific AHP criterion weights. Each baseline criterion weight was changed by ±10% and the resulting weights were normalized to total one. The WLC risk scores were recalculated for 1,000 simulations per cluster. The outputs include baseline validation, simulation weights, site-level uncertainty statistics, cluster summaries, convergence results and classification stability.

Detailed information is found in `uncertainty\_analysis/README.md`.

### Data availability

The repository has derived data, scripts, supporting tables and documentation.

Environmental and spatial data is sourced from external providers including Copernicus, the European Commission Joint Research Centre, EFEHR, EMSC, EMODnet and other European data providers. Original datasets are subject to the terms and conditions of the respective providers.

Precise site coordinates are not in the public repository. Transformed or derived spatial variables are supplied when required for the analyses. For example, `C\_x` and `C\_y` in the environmental clustering data are transformed variables and are not to be interpreted as original site coordinates.

### Reproducibility

The purpose of the repository is for the workflow and supporting results of the thesis to be available for use. The GIS data preparation and spatial analysis were primarily implemented in ArcGIS Pro. Python was used for clustering, sensitivity analysis, Monte Carlo uncertainty analysis and some supporting data processing tasks. A Windows PowerShell script was used for the Copernicus DEM data acquisition.

Individual folders contain README files that describe the data and analytical procedures.

### Thesis

*A GIS Framework for Risk Management of Immovable Cultural Heritage: A Case Study in Northern Thrace (Southern Bulgaria)*

Master's thesis  
Digital Heritage and Landscape Archaeology  
Department of History and Archaeology  
University of Cyprus  
2026

