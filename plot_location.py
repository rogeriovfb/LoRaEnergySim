import matplotlib.pyplot as plt
import pickle
import numpy as np
import math
from matplotlib.ticker import MaxNLocator

# ============================================================
# Global style configuration
# ============================================================
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 15,
    "axes.titlesize": 16,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 14,
    "axes.linewidth": 1.2,
    "grid.alpha": 0.3,
    "grid.linestyle": "--"
})

# ============================================================
# Load location data
# ============================================================
file_location_10 = "G:\\Meu Drive\\Mestrado\\DISSERTAÇÃO\\DADOS SIMULAÇÃO\\Locations\\10_locations_1_sim_10000_cell.pkl"
location_10 = pickle.load(open(file_location_10, "rb"))

file_location_100 = "G:\\Meu Drive\\Mestrado\\DISSERTAÇÃO\\DADOS SIMULAÇÃO\\Locations\\100_locations_1_sim_10000_cell.pkl"
location_100 = pickle.load(open(file_location_100, "rb"))

# ============================================================
# Plot function
# ============================================================
def plot_nodes(locations, filename):
    num_nodes = len(locations)

    x_values = [loc.x for loc in locations]
    y_values = [loc.y for loc in locations]
    altitudes = [loc.alt for loc in locations]

    distances = [
        np.sqrt((loc.x - 5000) ** 2 + (loc.y - 5000) ** 2)
        for loc in locations
    ]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # --------------------------------------------------------
    # Subplot 1 — Node spatial distribution
    # --------------------------------------------------------
    axs[0].scatter(x_values, y_values, s=20, color='dodgerblue', label='Nodes')
    axs[0].scatter(5000, 5000, color='red', marker='*', s=250, label='Gateway')

    axs[0].set_title(f'Network with {num_nodes} Nodes')
    axs[0].set_xlabel('X Coordinate [m]')
    axs[0].set_ylabel('Y Coordinate [m]')
    axs[0].set_xlim(0, 10000)
    axs[0].set_ylim(0, 10000)
    axs[0].grid(True)
    axs[0].legend(loc='upper right', frameon=True, framealpha=0.9)

    # --------------------------------------------------------
    # Subplot 2 — Distance to gateway
    # --------------------------------------------------------
    num_bins = math.ceil((max(distances) - min(distances)) / 1000)

    axs[1].hist(
        distances,
        bins=num_bins,
        color='orange',
        alpha=0.8,
        edgecolor='black'
    )

    axs[1].set_title('Distance to Gateway')
    axs[1].set_xlabel('Distance [m]')
    axs[1].set_ylabel('Frequency')
    axs[1].grid(True)
    axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))

    # --------------------------------------------------------
    # Subplot 3 — Altitude distribution
    # --------------------------------------------------------
    axs[2].hist(
        altitudes,
        bins=10,
        color='lightcoral',
        alpha=0.8,
        edgecolor='black'
    )

    axs[2].set_title('Node Altitude Distribution')
    axs[2].set_xlabel('Altitude [m]')
    axs[2].set_ylabel('Number of Nodes')
    axs[2].grid(True)

    # --------------------------------------------------------
    # Layout and save
    # --------------------------------------------------------
    plt.subplots_adjust(
        left=0.06,
        right=0.98,
        top=0.9,
        bottom=0.15,
        wspace=0.25
    )

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()

# ============================================================
# Generate figures
# ============================================================
plot_nodes(location_10[0], 'fig6_node_distribution_10_nodes.png')
plot_nodes(location_100[0], 'fig6_node_distribution_100_nodes.png')
