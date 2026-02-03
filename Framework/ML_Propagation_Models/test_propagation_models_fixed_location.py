import matplotlib.pyplot as plt
import numpy as np
from Framework import PropagationModel

# ============================================================
# Global style (same as Figure 5 — no bold)
# ============================================================
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 16,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 15,
    "axes.linewidth": 1.2,
    "grid.alpha": 0.25,
    "grid.linestyle": "--"
})


# ============================================================
# Propagation models
# ============================================================
models = [
    PropagationModel.LogShadow(std=0),
    PropagationModel.FreeSpace(fc=868),
    PropagationModel.Egli(fc=868),
    PropagationModel.OkumuraHata(fc=868),
    PropagationModel.COST231Hata(fc=868),
    PropagationModel.DecisionTree(),
    PropagationModel.RandomForest(),
    PropagationModel.XGBOOST()
]

# Distances from 250 m to 10 km
distances = list(range(250, 10250, 250))

# Dictionary to store results
results = {type(model).__name__: [] for model in models}

# ============================================================
# Compute path loss
# ============================================================
for model in models:
    model_name = type(model).__name__
    losses = []

    for distance in distances:
        try:
            rss = model.tp_to_rss(indoor=False, tp_dBm=0, d=distance, alt=60)
            losses.append(-rss)
        except Exception as e:
            print(f"Error for {model_name} at {distance} m: {e}")
            losses.append(np.nan)

    results[model_name] = losses

# ============================================================
# Plot
# ============================================================
plt.figure(figsize=(12, 8))

for model_name, losses in results.items():
    plt.plot(
        distances,
        losses,
        label=model_name,
        linewidth=2,
        marker='o',
        markersize=5
    )

plt.xlabel('Distance [m]')
plt.ylabel('Path Loss [dB]')
plt.title('Comparison of Path Loss Across Propagation Models')

plt.xticks(np.arange(0, 10001, 1000))
plt.xlim(0, 10000)
plt.ylim(60, 180)

# Legend: larger and cleaner (key fix)
plt.legend(
    loc='lower right',
    frameon=True,
    framealpha=0.9
)

plt.grid(True)
plt.tight_layout()

# ============================================================
# Save figure
# ============================================================
plt.savefig(
    "fig7_path_loss_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
