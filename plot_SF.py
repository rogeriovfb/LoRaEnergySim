import pickle
import matplotlib.pyplot as plt

# ============================================================
# Global style configuration
# ============================================================
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 16,
    "axes.titlesize": 17,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 15,
    "axes.linewidth": 1.2,
    "grid.alpha": 0.25,
    "grid.linestyle": "--"
})

# ============================================================
# Algorithms and result files
# ============================================================
algoritmos = [
    'LogShadow', 'FreeSpace', 'Egli', 'OkumuraHata',
    'COST231Hata', 'DecisionTree', 'RandomForest', 'XGBOOST'
]

arquivos = [
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_7_False_False_propagation.p',
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_8_False_False_propagation.p',
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_9_False_False_propagation.p',
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_10_False_False_propagation.p',
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_11_False_False_propagation.p',
    'C:\\Github\\LoRaEnergySim\\Simulations\\propagation\\results\\100_10000_12_False_False_propagation.p'
]

# ============================================================
# Figure and axes
# ============================================================
fig, axs = plt.subplots(len(arquivos), figsize=(12, 14), sharex=True, sharey=True)

legend_handles = None

# ============================================================
# Plot stacked bars for each spreading factor
# ============================================================
for i, arquivo in enumerate(arquivos):
    with open(arquivo, 'rb') as f:
        dicionario = pickle.load(f)

    dados_pacotes = {
        'Collided': [],
        'Weak': [],
        'Received': []
    }

    for algoritmo in algoritmos:
        dados_air_interface = dicionario[algoritmo][0]['data_air_interface_raw']
        dados_gateway = dicionario[algoritmo][0]['data_gateway_raw']

        dados_pacotes['Received'].append(int(dados_gateway['PacketsReceived']))
        dados_pacotes['Weak'].append(int(dados_gateway['ULWeakPackets']))
        dados_pacotes['Collided'].append(int(dados_air_interface['NumberOfPacketsCollided']))

    r = range(len(algoritmos))
    bar_width = 0.8

    bar_collided = axs[i].bar(
        r,
        dados_pacotes['Collided'],
        color='lightcoral',
        width=bar_width,
        label='Collisions'
    )

    bar_weak = axs[i].bar(
        r,
        dados_pacotes['Weak'],
        bottom=dados_pacotes['Collided'],
        color='orange',
        width=bar_width,
        label='Weak Signal'
    )

    bar_received = axs[i].bar(
        r,
        dados_pacotes['Received'],
        bottom=[c + w for c, w in zip(dados_pacotes['Collided'], dados_pacotes['Weak'])],
        color='dodgerblue',
        width=bar_width,
        label='Received Packets'
    )

    if i == 0:
        legend_handles = [bar_collided, bar_weak, bar_received]

    axs[i].set_title(f'Spreading Factor {i + 7}')
    axs[i].set_xticks(r)
    axs[i].set_xticklabels(algoritmos, rotation=45, ha='right')

    totals = [
        rcv + wk + col
        for rcv, wk, col in zip(
            dados_pacotes['Received'],
            dados_pacotes['Weak'],
            dados_pacotes['Collided']
        )
    ]

    percentages = [
        (rcv / total) * 100 if total > 0 else 0
        for rcv, total in zip(dados_pacotes['Received'], totals)
    ]

    for j in range(len(algoritmos)):
        x = j
        y = totals[j] * 0.5
        axs[i].text(
            x,
            y,
            f'{percentages[j]:.1f}%',
            ha='center',
            va='center',
            fontsize=14
        )

# ============================================================
# Common labels and legend
# ============================================================
axs[-1].set_xlabel('Algorithms')
fig.text(0.04, 0.5, 'Number of Packets', va='center', rotation='vertical')

fig.legend(
    legend_handles,
    ['Collisions', 'Weak Signal', 'Received Packets'],
    loc='upper right',
    frameon=True,
    framealpha=0.9
)

# ============================================================
# Layout and save
# ============================================================
plt.subplots_adjust(
    left=0.12,
    right=0.88,
    top=0.92,
    bottom=0.08,
    hspace=0.24
)

plt.savefig(
    'fig8_packet_delivery_by_sf.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()
