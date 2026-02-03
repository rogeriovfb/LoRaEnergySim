import matplotlib.pyplot as plt
import pickle


# ============================================================
# Global style
# ============================================================
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "grid.alpha": 0.3,
    "grid.linestyle": "--"
})


# Função para obter o tempo de simulação de um determinado algoritmo nos resultados
def get_simulation_time(key, results):
    return results[key][0]['simulation_time']


# Carregar os resultados de cada arquivo pickle
file_1 = 'G:\\Meu Drive\\Mestrado\\DISSERTAÇÃO\\DADOS SIMULAÇÃO\\Ensaio Tempo de Processamento\\1_12_False_False_propagation.p'
results_1 = pickle.load(open(file_1, "rb"))

file_10 = 'G:\\Meu Drive\\Mestrado\\DISSERTAÇÃO\\DADOS SIMULAÇÃO\\Ensaio Tempo de Processamento\\10_12_False_False_propagation.p'
results_10 = pickle.load(open(file_10, "rb"))

file_100 = 'G:\\Meu Drive\\Mestrado\\DISSERTAÇÃO\\DADOS SIMULAÇÃO\\Ensaio Tempo de Processamento\\100_12_False_False_propagation.p'
results_100 = pickle.load(open(file_100, "rb"))


# Dados de RMSE para cada algoritmo
algoritmos = [
    'LogShadow', 'FreeSpace', 'Egli', 'OkumuraHata', 'COST231Hata',
    'DecisionTree', 'RandomForest', 'SVR', 'Lasso', 'XGBOOST', 'NeuralNetwork'
]

rmse = [9.78, 40.90, 15.32, 10.74, 12.63, 7.05, 6.78, 8.12, 9.41, 6.79, 7.83]


# Dados de tempos de simulação
dados = {
    '1 node': {alg: get_simulation_time(alg, results_1) for alg in algoritmos},
    '10 nodes': {alg: get_simulation_time(alg, results_10) for alg in algoritmos},
    '100 nodes': {alg: get_simulation_time(alg, results_100) for alg in algoritmos}
}


# ============================================================
# Figura 1 – Processing Time
# ============================================================
fig1, axs1 = plt.subplots(3, 1, figsize=(11, 13), sharex=True)

for i, (condicao, tempos) in enumerate(dados.items()):
    valores = [tempos[alg] for alg in algoritmos]
    bars = axs1[i].bar(algoritmos, valores, color=plt.cm.Set3.colors)

    axs1[i].set_title(
        f'Processing Time Comparison under Condition: {condicao}'
    )
    axs1[i].grid(True)

    # Rótulos numéricos (mantidos, mas com offset)
    for bar in bars:
        height = bar.get_height()
        axs1[i].text(
            bar.get_x() + bar.get_width() / 2,
            height * 1.01,               # pequeno afastamento
            f'{height:.1f}',
            ha='center',
            va='bottom',
            fontsize=11
        )

    axs1[i].set_ylim(0, max(valores) * 1.15)
    axs1[i].locator_params(axis='y', nbins=8)

    if i == 1:
        axs1[i].set_ylabel('Processing Time [s]')

axs1[-1].set_xlabel('Algorithms')
plt.setp(axs1[-1].get_xticklabels(), rotation=45, ha='right')

plt.subplots_adjust(hspace=0.15)


# ============================================================
# Figura 2 – RMSE × Processing Time
# ============================================================
fig2, axs2 = plt.subplots(3, 1, figsize=(11, 13), sharex=True)

for i, (condicao, tempos) in enumerate(dados.items()):
    metric_values = [rmse[j] * tempos[alg] for j, alg in enumerate(algoritmos)]
    bars = axs2[i].bar(algoritmos, metric_values, color=plt.cm.Set3.colors)

    axs2[i].set_title(
        f'RMSE × Processing Time under Condition: {condicao}'
    )
    axs2[i].grid(True)

    # Rótulos numéricos (mantidos)
    for bar in bars:
        height = bar.get_height()
        axs2[i].text(
            bar.get_x() + bar.get_width() / 2,
            height * 1.01,
            f'{height:.1f}',
            ha='center',
            va='bottom',
            fontsize=11
        )

    axs2[i].set_ylim(0, max(metric_values) * 1.15)
    axs2[i].locator_params(axis='y', nbins=8)

    if i == 1:
        axs2[i].set_ylabel('RMSE × Processing Time')

axs2[-1].set_xlabel('Algorithms')
plt.setp(axs2[-1].get_xticklabels(), rotation=45, ha='right')

plt.subplots_adjust(hspace=0.15)

fig1.savefig(
    "fig5_processing_time_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
