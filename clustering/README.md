# Environmental Ward Hierarchical Clustering

This folder contains the Python workflow and related data used to group the archaeological sites according to similarities in their environmental characteristics. The analysis uses Ward hierarchical clustering and Euclidean distance. Other solutions of 3-7 clusters are compared using the silhouette scores. The solution with the highest silhouette score is automatically identified and exported with the profiles of the resulting clusters.

## Folder structure

```text
clustering/
├── README.md
├── ward_clustering_ruslog.py
├── Cluster_matrix_Ruslog.csv
├── results/
│   ├── best_cluster_profiles.csv
│   ├── best_silhouette_clusters.csv
│   ├── candidate_cluster_profiles.csv
│   ├── cluster_evaluation.csv
│   ├── sites_with_candidate_clusters.csv
│   ├── ward_dendrogram_full.png
│   └── ward_dendrogram_truncated.png
└── visualization/
    ├── parallel_boxplot_clusters_1_2_3.py
    ├── parallel_boxplot_clusters_1_2_3.png
    ├── parallel_boxplot_clusters_1_2_3.pdf
    └── parallel_boxplot_cluster_means.csv
```

## Input data

The clustering script reads:

```text
Cluster_matrix_Ruslog.csv
```

The table contains the site identifier, site name and environmental variables for the clustering analysis.

The final clustering model uses the following fields:

|Field|Description|
|-|-|
|`C_DEM`|Standardized/scaled elevation variable|
|`C_Slope`|Standardized/scaled slope variable|
|`C_Acos`|North–south aspect component|
|`C_Asin`|East–west aspect component|
|`C_RusLog`|Log-transformed estimated soil-loss variable|
|`C_FlDist`|Standardized/scaled distance to the modelled flood zone|
|`C_x`|Transformed spatial x variable used in clustering|
|`C_y`|Transformed spatial y variable used in clustering|

The final model uses the log-transformed RUSLE variable rather than the original RUSLE values. Distance to the modelled flood zone is maintained. Flood depth is excluded from the final clustering model.

### Spatial data note

`C_x` and `C_y` are transformed spatial variables used to introduce a spatial component into the clustering analysis. They are not raw archaeological site coordinates. Raw x/y coordinates of archaeological sites are not included in the public repository.

## Data validation

Before clustering is performed, the script checks that:

* all required fields are present;
* site IDs are not missing;
* site IDs are not duplicated;
* the environmental variables can be interpreted as numeric values; and
* the environmental variables contain no missing values.

The analysis stops if these requirements are not met.

## Clustering procedure

The analysis follows the following main steps:

1. Read the clustering matrix.
2. Validate the required site and environmental data.
3. Extract the eight variables used in the final model.
4. Perform Ward hierarchical clustering using Euclidean distance.
5. Produce full and truncated dendrograms.
6. Generate candidate solutions containing 3, 4, 5, 6, and 7 clusters.
7. Calculate the silhouette score for each candidate solution.
8. Record the size of the smallest, largest and mean cluster for each solution.
9. Add all candidate cluster assignments to the site table.
10. Calculate the mean environmental profile of each cluster.
11. Select the solution with the highest silhouette score.
12. Export the results to the `results/` folder.

## Cluster solution evaluation

The script tests:

```text
3
4
5
6
7
```

clusters.

For each cluster solution, `cluster_evaluation.csv` records:

* `Requested_k`
* `Actual_clusters`
* `Silhouette_score`
* `Smallest_cluster`
* `Largest_cluster`
* `Mean_cluster_size`

The evaluation table is sorted from the highest to the lowest silhouette score. The first row is therefore used to identify the preferred cluster solution.

## Outputs

### `cluster_evaluation.csv`

Summary of the silhouette score and cluster-size statistics for every tested cluster solution.

### `sites_with_candidate_clusters.csv`

Site-level table containing the clustering variables and assignments for all tested solutions:

```text
Cluster_3
Cluster_4
Cluster_5
Cluster_6
Cluster_7
```

### `candidate_cluster_profiles.csv`

Mean environmental profile and number of sites for each cluster in every tested cluster solution.

### `best_silhouette_clusters.csv`

Site identifiers, site names, and cluster assignments for the candidate solution with the highest silhouette score.

The selected assignment is stored as:

```text
Cluster_best_silhouette
```

### `best_cluster_profiles.csv`

Mean environmental characteristics and number of sites for the clusters belonging to the highest-silhouette solution.

### `ward_dendrogram_full.png`

Full Ward hierarchical clustering dendrogram showing the overall hierarchical structure.

### `ward_dendrogram_truncated.png`

Truncated dendrogram showing the final 20 merged groups of the hierarchy.



## Cluster visualization

The final three-cluster solution is visualized using:

```text
visualization/parallel_boxplot_clusters_1_2_3.py
```

The visualization script reads:

```text
results/sites_with_candidate_clusters.csv
```

The script creates a parallel box plot comparing the standardized environmental characteristics of Clusters 1-3. The background box plots show the overall distribution of each environmental variable across all sites. The connected colored lines and markers show the mean environmental profile of each cluster.

The plotted variables are:

* elevation
* slope
* north-south aspect component
* east-west aspect component
* log-transformed estimated soil loss
* distance to the modelled flood zone

The transformed spatial variables `C_x` and `C_y` are used in the clustering analysis but are not shown in the environmental profile figure.

The weighting adjustment applied to the paired aspect variables and flood distance variable in the clustering matrix is reversed for the visualization so that these variables are displayed on the standardized scale. The RUSLE variable remains log-transformed.

The visualization script creates the following files in the `visualization/` folder:

### `parallel_boxplot_clusters_1_2_3.png`

300 dpi PNG version of the environmental cluster profile figure.

### `parallel_boxplot_clusters_1_2_3.pdf`

PDF version of the environmental cluster profile figure.

### `parallel_boxplot_cluster_means.csv`

Mean standardized value and number of sites for each plotted environmental variable and cluster.

## Running the scripts

The Ward clustering script and input CSV should remain in the same `clustering/` folder.

From a terminal opened in this folder, run:

```bash
python ward_clustering_ruslog.py
```

The script automatically identifies its own folder and creates the `results/` directory if it does not already exist.

After the clustering results have been generated, open a terminal in the `visualization/` folder and run:

```bash
python parallel_boxplot_clusters_1_2_3.py
```

The visualization script reads `results/sites_with_candidate_clusters.csv` and saves the PNG, PDF and cluster-mean CSV outputs in the `visualization/` folder.

## Python dependencies

The script uses:

* Python `pathlib`
* NumPy
* Pandas
* Matplotlib
* SciPy
* scikit-learn

The external packages can be installed using:

```bash
pip install numpy pandas matplotlib scipy scikit-learn
```

## Software documentation

The Python workflow used the Python standard library and the official NumPy, Pandas, Matplotlib, SciPy and scikit-learn packages. The documentation listed below was used as reference when developing the script.

|Package|Functionality used in the script|Use in this analysis|Official documentation|
|-|-|-|-|
|Python `pathlib`|`Path`, `resolve()`, `parent`, `exists()`, `mkdir()`|Defines file locations for the Python script, checks that the input file exists, and creates the results folder.|[Python pathlib documentation](https://docs.python.org/3/library/pathlib.html)|
|pandas|`read_csv()` and `DataFrame.to_csv()`|Reads the clustering input matrix and exports the tables as CSV files.|[pandas I/O documentation](https://pandas.pydata.org/docs/user_guide/io.html)|
|pandas|`DataFrame.groupby()`|Groups sites according to their assigned cluster so that cluster sizes and mean environmental profiles can be calculated.|[pandas DataFrame.groupby documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)|
|pandas|`DataFrame.merge()`|Combines the number of sites in each cluster with the calculated mean environmental profiles.|[pandas merge documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)|
|pandas|`concat()`|Combines the environmental profile tables produced for the different cluster solutions.|[pandas concat documentation](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)|
|NumPy|`unique()`|Counts the number of unique cluster labels returned for each tested cluster solution.|[NumPy unique documentation](https://numpy.org/doc/stable/reference/generated/numpy.unique.html)|
|SciPy|`scipy.cluster.hierarchy.linkage()`|Performs hierarchical agglomerative clustering using Ward's method and Euclidean distance.|[SciPy linkage documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html)|
|SciPy|`scipy.cluster.hierarchy.fcluster()`|Converts the hierarchical clustering into separate cluster solutions containing 3-7 clusters.|[SciPy fcluster documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html)|
|SciPy|`scipy.cluster.hierarchy.dendrogram()`|Produces the full and truncated dendrograms from the hierarchical clustering result.|[SciPy dendrogram documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html)|
|scikit-learn|`sklearn.metrics.silhouette_score()`|Calculates the mean silhouette coefficient for each cluster solution so the alternatives can be compared.|[scikit-learn silhouette_score documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)|
|Matplotlib|`pyplot.figure()` and `pyplot.savefig()`|Creates the dendrogram figures and exports them as PNG files.|[Matplotlib figure documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html) and [Matplotlib savefig documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)|
|NumPy|`sqrt()` and `arange()`|Defines the paired-variable scale adjustment and the plotting positions used in the cluster visualization.|[NumPy mathematical functions](https://numpy.org/doc/stable/reference/routines.math.html) and [NumPy arange documentation](https://numpy.org/doc/stable/reference/generated/numpy.arange.html)|
|pandas|`to_numeric()`, `isna()`, and `value_counts()`|Validates the plotting fields, checks for missing values and counts the number of sites in each final cluster.|[pandas to_numeric documentation](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html), [pandas isna documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html), and [pandas value_counts documentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)|
|Matplotlib|`Axes.boxplot()`, `Axes.plot()`, and `savefig()`|Creates the parallel box plot, adds the mean environmental profile of each cluster and exports the visualization as PNG and PDF.|[Matplotlib boxplot documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html), [Matplotlib plot documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html), and [Matplotlib savefig documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)|

These sources describe the software implementation of the workflow. The academic support for Ward hierarchical clustering, Euclidean distance and silhouette analysis is listed under methodological references.

## Methodological references

The clustering methodology and evaluation of alternative cluster solutions are based on the following sources:

* Ward, J. H., Jr. (1963). Hierarchical grouping to optimize an objective function. *Journal of the American Statistical Association, 58*(301), 236-244. https://doi.org/10.1080/01621459.1963.10500845
* Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics, 20*, 53-65. https://doi.org/10.1016/0377-0427(87)90125-7

Ward (1963) is the basis for the hierarchical grouping procedure. Observations are successively combined into separate groups while minimizing the increase in variation within the clusters at each stage. Rousseeuw (1987) is the support for the silhouette coefficient used here to compare the alternative cluster solutions.

## Reproducibility and data availability

The repository contains the clustering script, transformed clustering variables, cluster solutions, evaluation results, cluster profiles, dendrograms and environmental cluster visualization outputs. Raw archaeological site coordinates are not included. The spatial variables included in the clustering matrix (`C_x` and `C_y`) are transformed analytical variables rather than raw geographic coordinates.

The files in `results/` and `visualization/` are outputs generated from the clustering and visualization workflows and are included to make the analytical results readable without requiring the scripts to be rerun.

