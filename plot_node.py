import pickle
import matplotlib.pyplot as plt
import numpy as np

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
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\10_10000_7_True_True_propagation.p',
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_7_True_True_propagation.p',
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\200_10000_7_True_True_propagation.p'
]

cores = ['dodgerblue', 'orange', 'lightcoral']
legend_labels = ['Received Packets', 'Weak Signal', 'Collisions']
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, color=cores[0]),
    plt.Rectangle((0, 0), 1, 1, color=cores[1]),
    plt.Rectangle((0, 0), 1, 1, color=cores[2])
]

# ============================================================
# FIGURE 11 — Packet delivery vs. number of nodes
# ============================================================
fig11, axs = plt.subplots(len(arquivos), figsize=(12, 10), sharex=True, sharey=False)

for i, arquivo in enumerate(arquivos):
    with open(arquivo, 'rb') as f:
        dicionario = pickle.load(f)

    recebidos, weak, collided = [], [], []

    for algoritmo in algoritmos:
        dados_air = dicionario[algoritmo][0]['data_air_interface_raw']
        dados_gw = dicionario[algoritmo][0]['data_gateway_raw']

        recebidos.append(int(dados_gw['PacketsReceived']))
        weak.append(int(dados_gw['ULWeakPackets']))
        collided.append(int(dados_air['NumberOfPacketsCollided']))

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
            totals[j] * 1.05,
            f'{perc:.1f}%',
            ha='center',
            va='center',
            fontsize=13
        )

    nodes = arquivo.split("_")[-6].split("\\")[-1]
    axs[i].set_title(f'Network size: {nodes} nodes')
    axs[i].grid(axis='y')

    if i == 1:
        axs[i].set_ylabel('Number of Packets')

    limite = [50000, 500000, 999999]
    axs[i].set_ylim(0, limite[i])

# X-axis configuration
axs[-1].set_xticks(x)
axs[-1].set_xticklabels(algoritmos, rotation=45, ha='right')
axs[-1].set_xlabel('Algorithms')

# Legend inside the first subplot
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
    hspace=0.3
)

plt.savefig(
    'fig11_packet_delivery_by_network_size.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()
