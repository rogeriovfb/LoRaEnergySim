import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

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
# Algorithms and input files
# ============================================================
algoritmos = [
    'LogShadow', 'FreeSpace', 'Egli', 'OkumuraHata',
    'COST231Hata', 'DecisionTree', 'RandomForest', 'XGBOOST'
]

arquivos = [
    'C:\\GitHub\\LoRaEnergySim\\Simulations\\propagation\\results\\100_100_7_True_True_propagation.p',
    'C:\\GitHub\\LoRaEnergySim\\Simulations\\propagation\\results\\100_1000_7_True_True_propagation.p',
    'C:\\GitHub\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_7_True_True_propagation.p'
]

cores = ['dodgerblue', 'orange', 'lightcoral']

# ============================================================
# FIGURE 9 — Packet delivery vs. cell size
# ============================================================
fig9, axs = plt.subplots(len(arquivos), figsize=(12, 10), sharex=True, sharey=True)

legend_labels = ['Received Packets', 'Weak Signal', 'Collisions']
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color=cores[0]),
    plt.Rectangle((0, 0), 1, 1, color=cores[1]),
    plt.Rectangle((0, 0), 1, 1, color=cores[2])
]

energia_total_por_algoritmo = {}

for i, arquivo in enumerate(arquivos):
    with open(arquivo, 'rb') as f:
        dicionario = pickle.load(f)

    recebidos, weak, collided = [], [], []

    for algoritmo in algoritmos:
        dados_air = dicionario[algoritmo][0]['data_air_interface_raw']
        dados_gw = dicionario[algoritmo][0]['data_gateway_raw']
        dados_nos = dicionario[algoritmo][0]['data_nodes_raw']

        recebidos.append(int(dados_gw['PacketsReceived']))
        weak.append(int(dados_gw['ULWeakPackets']))
        collided.append(int(dados_air['NumberOfPacketsCollided']))

        if i == 2:
            energia_total_por_algoritmo.setdefault(algoritmo, [])
            energia_total_por_algoritmo[algoritmo].append(
                sum(dados_nos['TotalEnergy']) / 1000
            )

    x = np.arange(len(algoritmos))
    width = 0.75

    axs[i].bar(x, collided, width, color=cores[2])
    axs[i].bar(x, weak, width, bottom=collided, color=cores[1])
    axs[i].bar(
        x,
        recebidos,
        width,
        bottom=[c + w for c, w in zip(collided, weak)],
        color=cores[0]
    )

    totals = [r + w + c for r, w, c in zip(recebidos, weak, collided)]
    percentages = [(r / t) * 100 if t > 0 else 0 for r, t in zip(recebidos, totals)]

    for j, perc in enumerate(percentages):
        axs[i].text(
            j,
            totals[j] * 0.9,
            f'{perc:.1f}%',
            ha='center',
            va='bottom',
            fontsize=13
        )

    cell_size = arquivo.split('_')[1]
    axs[i].set_title(f'Cell size: {cell_size} × {cell_size}')
    if i == 1:
        axs[i].set_ylabel('Number of Packets')
    axs[i].grid(axis='y')

axs[-1].set_xticks(x)
axs[-1].set_xticklabels(algoritmos, rotation=45, ha='right')
axs[-1].set_xlabel('Algorithms')

axs[0].legend(
    legend_handles,
    legend_labels,
    loc='upper left',
    frameon=True,
    framealpha=0.9
)

plt.subplots_adjust(
    left=0.1,
    right=0.9,
    top=0.9,
    bottom=0.12,
    hspace=0.25
)

plt.savefig(
    'fig9_packet_delivery_by_cell_size.png',
    dpi=300,
    bbox_inches='tight'
)

# ============================================================
# FIGURE 10 — Total energy consumption
# ============================================================
fig10 = plt.figure(figsize=(11, 6))

for algoritmo in algoritmos:
    total_energy = sum(energia_total_por_algoritmo[algoritmo])
    plt.bar(algoritmo, total_energy, color='dodgerblue')
    plt.text(
        algoritmo,
        total_energy * 1.0,
        f'{int(total_energy)} J',
        ha='center',
        va='bottom',
        fontsize=13
    )

plt.xlabel('Algorithms')
plt.ylabel('Total Energy Consumed by All Nodes [J]')
plt.grid(axis='y')
plt.xticks(rotation=45, ha='right')

plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f'{int(x)}')
)

plt.subplots_adjust(
    left=0.1,
    right=0.95,
    top=0.9,
    bottom=0.2,
    hspace=0.25
)

plt.savefig(
    'fig10_total_energy_consumption.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()
