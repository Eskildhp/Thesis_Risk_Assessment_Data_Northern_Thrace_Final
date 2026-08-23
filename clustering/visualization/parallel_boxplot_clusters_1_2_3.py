from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ================================================================
# FILE PATHS
# ================================================================

Visualization_folder = Path(__file__).resolve().parent
Project_folder = Visualization_folder.parent

Input_file = (
    Project_folder
    / "results"
    / "sites_with_candidate_clusters.csv"
)

Output_folder = Visualization_folder

Output_PNG = Output_folder / "parallel_boxplot_clusters_1_2_3.png"
Output_PDF = Output_folder / "parallel_boxplot_clusters_1_2_3.pdf"
Output_means = Output_folder / "parallel_boxplot_cluster_means.csv"


# ================================================================
# PLOT SETUP
# ================================================================

Cluster_field = "Cluster_3"
Clusters = [1, 2, 3]

Pair_weight = 1 / np.sqrt(2)

Plot_variables = [
    {"label": "Elevation", "source": "C_DEM", "scale_factor": 1.0},
    {"label": "Slope", "source": "C_Slope", "scale_factor": 1.0},
    {
        "label": "North–south aspect\ncomponent",
        "source": "C_Acos",
        "scale_factor": Pair_weight,
    },
    {
        "label": "East–west aspect\ncomponent",
        "source": "C_Asin",
        "scale_factor": Pair_weight,
    },
    {
        "label": "Log-transformed\nestimated soil loss",
        "source": "C_RusLog",
        "scale_factor": 1.0,
    },
    {
        "label": "Distance to the modelled\nflood zone",
        "source": "C_FlDist",
        "scale_factor": Pair_weight,
    },
]

Cluster_colors = {
    1: "#F17C7E",
    2: "#A0E875",
    3: "#77D2F0",
}

Cluster_markers = {
    1: "o",
    2: "s",
    3: "^",
}

def prepare_plot_data():
    """Prepare the site data used in the cluster visualisation."""

    if not Input_file.exists():
        raise FileNotFoundError(f"Input file not found: {Input_file}")

    site_data = pd.read_csv(Input_file)

    required_fields = [
        Cluster_field,
        *[variable["source"] for variable in Plot_variables]
    ]

    missing_fields = [
        field for field in required_fields
        if field not in site_data.columns
    ]

    if missing_fields:
        raise ValueError(f"Missing fields: {missing_fields}")

    site_data[Cluster_field] = pd.to_numeric(
        site_data[Cluster_field],
        errors="coerce"
    )

    # Restore weighted variables to the standardized scale used in the plot
    for variable in Plot_variables:
        source = variable["source"]
        plot_field = f"Z_{source}"

        site_data[source] = pd.to_numeric(
            site_data[source],
            errors="coerce"
        )

        site_data[plot_field] = (
            site_data[source] / variable["scale_factor"]
        )

        variable["plot_field"] = plot_field

    fields_to_check = [
        Cluster_field,
        *[variable["plot_field"] for variable in Plot_variables]
    ]

    if site_data[fields_to_check].isna().any().any():
        raise ValueError("Missing or nonnumeric plotting values found.")

    site_data[Cluster_field] = site_data[Cluster_field].astype(int)

    return site_data

def calculate_cluster_means(site_data):
    """Calculate the mean environmental values for each cluster."""

    mean_rows = []

    for cluster in Clusters:
        cluster_sites = site_data[
            site_data[Cluster_field] == cluster
        ]

        for variable in Plot_variables:
            mean_rows.append({
                "Cluster": cluster,
                "Variable": variable["label"].replace("\n", " "),
                "Mean_standardized_value": cluster_sites[
                    variable["plot_field"]
                ].mean(),
                "Number_of_sites": len(cluster_sites)
            })

    return pd.DataFrame(mean_rows)

def create_parallel_boxplot(site_data, cluster_means):
    """Create the parallel box plot of the environmental cluster profiles."""

    Output_folder.mkdir(parents=True, exist_ok=True)

    plot_fields = [
        variable["plot_field"] for variable in Plot_variables
    ]

    labels = [
        variable["label"] for variable in Plot_variables
    ]

    box_data = [
        site_data[field].to_numpy() for field in plot_fields
    ]

    y_positions = np.arange(1, len(Plot_variables) + 1)

    fig, ax = plt.subplots(figsize=(12, 7.5))

    ax.boxplot(
        box_data,
        positions=y_positions,
        orientation="horizontal",
        widths=0.45,
        patch_artist=True,
        manage_ticks=False,
        medianprops={"linewidth": 1.4, "color": "black"},
        boxprops={
            "facecolor": "white",
            "edgecolor": "0.35",
            "linewidth": 1.0
        },
        whiskerprops={"color": "0.35", "linewidth": 1.0},
        capprops={"color": "0.35", "linewidth": 1.0},
        flierprops={
            "marker": "+",
            "markersize": 5,
            "markeredgecolor": "0.35",
            "linestyle": "none"
        }
    )

    site_counts = (
        site_data[Cluster_field]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    for cluster in Clusters:
        mean_values = []

        for variable in Plot_variables:
            variable_name = variable["label"].replace("\n", " ")

            mean_value = cluster_means.loc[
                (cluster_means["Cluster"] == cluster)
                & (cluster_means["Variable"] == variable_name),
                "Mean_standardized_value"
            ].iloc[0]

            mean_values.append(mean_value)

        ax.plot(
            mean_values,
            y_positions,
            marker=Cluster_markers[cluster],
            markersize=7,
            linewidth=1.5,
            color=Cluster_colors[cluster],
            markerfacecolor=Cluster_colors[cluster],
            markeredgecolor="0.25",
            label=f"Cluster {cluster} (n={site_counts[cluster]})",
            zorder=3
        )

    ax.axvline(
        0,
        color="0.45",
        linestyle="--",
        linewidth=1.0,
        zorder=0
    )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()

    ax.set_xlabel("Standardized value (z-score)")
    ax.set_title(
        "Parallel box plot of standardized environmental "
        "characteristics by cluster"
    )

    ax.grid(axis="x", linestyle=":", linewidth=0.7, alpha=0.55)

    ax.legend(
        title="Final environmental cluster",
        loc="best",
        frameon=True
    )

    fig.tight_layout()

    fig.savefig(Output_PNG, dpi=300, bbox_inches="tight")
    fig.savefig(Output_PDF, bbox_inches="tight")

    plt.show()

def main():
    """Run the cluster visualisation workflow."""

    site_data = prepare_plot_data()

    cluster_means = calculate_cluster_means(site_data)
    cluster_means.to_csv(Output_means, index=False)

    create_parallel_boxplot(site_data, cluster_means)

    print("Cluster visualisation complete.")
    print(f"Mean values saved to: {Output_means}")
    print(f"PNG saved to: {Output_PNG}")
    print(f"PDF saved to: {Output_PDF}")

if __name__ == "__main__":
    main()