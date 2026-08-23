from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from sklearn.metrics import silhouette_score


# ================================================================
# FILE PATHS AND VARIABLES
# ================================================================

Project_folder = Path(__file__).resolve().parent

# This is the CSV shown in Windows as "Cluster_matrix_Ruslog"
# with file type "Microsoft Excel Comma Separated Values".
Input_file = Project_folder / "Cluster_matrix_Ruslog.csv"

Output_folder = Project_folder / "results"

site_ID_field = "Site_ID"
site_name_field = "Site"

# Variables used in the final clustering model:
# - log-transformed RUSLE
# - flood distance retained
# - flood depth excluded
Clustering_variables = [
    "C_DEM",
    "C_Slope",
    "C_Acos",
    "C_Asin",
    "C_RusLog",
    "C_FlDist",
    "C_x",
    "C_y",
]

Cluster_numbers = range(3, 8)


# ================================================================
# FUNCTIONS
# ================================================================

def validate_data(data, id_field, name_field, cluster_fields):
    """Check that the site data is valid for the Ward hierarchical clustering analysis."""

    required_fields = [id_field, name_field] + cluster_fields
    missing_fields = [
        field for field in required_fields
        if field not in data.columns
    ]

    if missing_fields:
        raise ValueError(f"Missing fields: {missing_fields}")
    
    # Convert the environmental variables used in Ward clustering to numeric values
    clean_data = data.copy()
    clean_data[cluster_fields] = clean_data[cluster_fields].apply(
        pd.to_numeric, errors="coerce"
    )

    if clean_data[id_field].isna().any():
        raise ValueError("Missing site IDs found.")

    if clean_data[id_field].duplicated().any():
        raise ValueError("Duplicate site IDs found.")

    if clean_data[cluster_fields].isna().any().any():
        raise ValueError("Missing or nonnumeric environmental values found.")

    return clean_data


def make_dendrograms(ward_linkage, output_folder):
    """Create full and truncated dendrograms from the Ward clustering."""

    # Full dendrogram showing the complete clustering structure
    plt.figure(figsize=(18, 10))
    dendrogram(ward_linkage, no_labels=True)
    plt.title("Ward Hierarchical Clustering")
    plt.xlabel("Archaeological sites")
    plt.ylabel("Ward linkage distance")
    plt.tight_layout()
    plt.savefig(
        output_folder / "ward_dendrogram_full.png",
        dpi=300
    )
    plt.close()

    # Truncated dendrogram showing the final 20 merged groups
    plt.figure(figsize=(14, 9))
    dendrogram(
        ward_linkage,
        truncate_mode="lastp",
        p=20,
        show_leaf_counts=True,
        show_contracted=True
    )
    plt.title("Ward Hierarchical Clustering - Final Merges")
    plt.xlabel("Final branches or merged groups")
    plt.ylabel("Ward linkage distance")
    plt.tight_layout()
    plt.savefig(
        output_folder / "ward_dendrogram_truncated.png",
        dpi=300
    )
    plt.close()


def evaluate_clusters(environmental_data, ward_clusters):
    """Compare the tested Ward cluster solutions using silhouette scores."""

    cluster_evaluation = []
    cluster_solutions = {}

    for k in Cluster_numbers:
        labels = fcluster(
            ward_clusters,
            k,
            criterion="maxclust"
        )

        cluster_solutions[k] = labels
        site_counts = pd.Series(labels).value_counts()

        silhouette_value = silhouette_score(
            environmental_data,
            labels,
            metric="euclidean"
        )

        cluster_evaluation.append({
            "Requested_k": k,
            "Actual_clusters": len(np.unique(labels)),
            "Silhouette_score": silhouette_value,
            "Smallest_cluster": int(site_counts.min()),
            "Largest_cluster": int(site_counts.max()),
            "Mean_cluster_size": float(site_counts.mean())
        })

    evaluation_results = pd.DataFrame(cluster_evaluation)
    evaluation_results = evaluation_results.sort_values(
        "Silhouette_score",
        ascending=False
    ).reset_index(drop=True)

    return evaluation_results, cluster_solutions


def calculate_environmental_profiles(
    site_data, environmental_fields, cluster_field
):
    """Calculate the mean environmental profile of each cluster."""

    mean_profiles = (
        site_data.groupby(cluster_field)[environmental_fields]
        .mean()
        .reset_index()
    )

    site_counts = (
        site_data.groupby(cluster_field)
        .size()
        .rename("Number_of_sites")
        .reset_index()
    )

    return site_counts.merge(mean_profiles, on=cluster_field)

def calculate_candidate_profiles(site_data, environmental_fields):
    """Calculate environmental profiles for each tested cluster solution."""

    profile_tables = []

    for k in Cluster_numbers:
        cluster_field = f"Cluster_{k}"

        profiles = calculate_environmental_profiles(
            site_data[[cluster_field, *environmental_fields]],
            environmental_fields,
            cluster_field
        )

        profiles = profiles.rename(columns={cluster_field: "Cluster"})
        profiles.insert(0, "Number_of_clusters", k)
        profile_tables.append(profiles)

    candidate_profiles = pd.concat(profile_tables, ignore_index=True)

    return candidate_profiles.sort_values(
        ["Number_of_clusters", "Cluster"]
    ).reset_index(drop=True)


# ================================================================
# MAIN PROGRAM
# ================================================================

def main():
    """Run the Ward hierarchical clustering analysis."""

    if not Input_file.exists():
        raise FileNotFoundError(f"Input file not found: {Input_file}")

    Output_folder.mkdir(parents=True, exist_ok=True)

    site_data = pd.read_csv(
        Input_file,
        dtype={site_ID_field: str}
    )

    site_data = validate_data(
        site_data,
        site_ID_field,
        site_name_field,
        Clustering_variables
    )

    environmental_data = site_data[Clustering_variables].to_numpy(dtype=float)

    # Perform Ward hierarchical clustering on the environmental variables
    ward_clusters = linkage(
        environmental_data,
        method="ward",
        metric="euclidean",
        optimal_ordering=True
    )

    make_dendrograms(
        ward_clusters,
        Output_folder
    )

    evaluation_results, cluster_solutions = evaluate_clusters(
        environmental_data,
        ward_clusters
    )

    output_sites = site_data[
        [site_ID_field, site_name_field, *Clustering_variables]
    ].copy()

    # Calculate mean standardized profiles for every tested grouping.
    for k, labels in cluster_solutions.items():
        output_sites[f"Cluster_{k}"] = labels

    candidate_profiles = calculate_candidate_profiles(
        output_sites,
        Clustering_variables
    )

    evaluation_results.to_csv(
        Output_folder / "cluster_evaluation.csv",
        index=False
    )

    output_sites.to_csv(
        Output_folder / "sites_with_candidate_clusters.csv",
        index=False
    )

    candidate_profiles.to_csv(
        Output_folder / "candidate_cluster_profiles.csv",
        index=False
    )

    # Select the cluster solution with the highest silhouette score
    best_cluster_number = int(
        evaluation_results.iloc[0]["Requested_k"]
    )

    best_cluster_field = f"Cluster_{best_cluster_number}"

    best_clusters = output_sites[
        [site_ID_field, site_name_field, best_cluster_field]
    ].copy()

    best_clusters = best_clusters.rename(
        columns={best_cluster_field: "Cluster_best_silhouette"}
    )

    best_clusters.to_csv(
        Output_folder / "best_silhouette_clusters.csv",
        index=False
    )

    best_profiles = calculate_environmental_profiles(
        output_sites[
            [best_cluster_field, *Clustering_variables]
        ].copy(),
        Clustering_variables,
        best_cluster_field
    )

    best_profiles.to_csv(
        Output_folder / "best_cluster_profiles.csv",
        index=False
    )

    print("\nWard clustering completed")
    print(f"Sites: {len(site_data)}")
    print(f"Variables: {len(Clustering_variables)}")
    print("\nCluster evaluation:")
    print(evaluation_results.to_string(index=False))
    print(f"\nHighest silhouette score: {best_cluster_number} clusters")
    print(f"\nResults saved to: {Output_folder}")


if __name__ == "__main__":
    main()
