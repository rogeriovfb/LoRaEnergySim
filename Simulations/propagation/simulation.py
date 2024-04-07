import gc
import math
import multiprocessing as mp
import os
import pickle

import pandas as pd

import SimulationProcess
from Simulations.GlobalConfig import *
from Framework import Location as loc
from Framework import PropagationModel


# The console attempts to auto-detect the width of the display area, but when that fails it defaults to 80
# characters. This behavior can be overridden with:
desired_width = 320
pd.set_option('display.width', desired_width)

gateway_location = loc.Location(x=middle, y=middle, indoor=False)

if __name__ == '__main__':
    # Load generated locations
    with open(locations_file, 'rb') as file_handler:
        locations_per_simulation = pickle.load(file_handler)
        num_of_simulations = len(locations_per_simulation)
        num_nodes = len(locations_per_simulation[0])

    # create the results directory
    os.makedirs(os.path.dirname(results_file), exist_ok=True)

    # make a dictonary to hold the results that you want to study
    # Hence, diff. simulations can have diff _results dicts.
    #_results = {
    #    'cell_size': cell_size,
    #    'adr': adr,
    #    'confirmed_messages': confirmed_messages,
    #    'num_simulations': num_of_simulations,
    #    'total_devices': num_nodes,
    #    'transmission_rate': transmission_rate_bit_per_ms,
    #    'simulation_time': simulation_time,
    #    'nodes': dict(),
    #    'gateway': dict(),
    #    'air_interface': dict(),
    #    'path_loss_variances': path_loss_variance,
    #    'payload_sizes': payload_size,
    #    'mean_energy': dict(),
    #    'std_energy': dict(),
    #    'num_of_simulations_done': 0
    #}

    _results = dict({
        'cell_size': cell_size,
        'adr': adr,
        'confirmed_messages': confirmed_messages,
        'num_simulations': num_of_simulations,
        'total_devices': num_nodes,
        'transmission_rate': transmission_rate_bit_per_ms,
        'simulation_time': simulation_time,
        'payload_sizes': payload_size,
    })

    pool = mp.Pool(math.floor(mp.cpu_count() /1))

    for n_sim in range(num_of_simulations):
        print(f'Simulation #{n_sim}')
        locations = locations_per_simulation[n_sim]
        args = []

        propagation_list = [PropagationModel.LogShadow(std=path_loss_variance),
                            #PropagationModel.COST231(fc=868),
                            PropagationModel.FreeSpace(fc=868),
                            PropagationModel.Egli(fc=868),
                            PropagationModel.OkumuraHata(fc=868),
                            PropagationModel.COST231Hata(fc=868),
                            PropagationModel.DecisionTree(),
                            PropagationModel.RandomForest(),
                            #PropagationModel.SVR(),
                            #PropagationModel.Lasso(),
                            PropagationModel.XGBOOST(),
                            #PropagationModel.NeuralNetwork(fast=True)
                            ]

        for propagation in propagation_list:
            args.append((locations, payload_size, simulation_time, gateway_location, num_nodes,
                             transmission_rate_bit_per_ms, confirmed_messages, adr, propagation))

        r_list = pool.map(func=SimulationProcess.run_helper, iterable=args)
        #r_list = [SimulationProcess.run_helper(a) for a in args]

        for _r in r_list:
            if n_sim == 0:
                _results[type(_r['propagation']).__name__] = dict()
            _results[type(_r['propagation']).__name__][n_sim] = _r
        # store the results

        pickle.dump(_results, open(results_file, "wb"))
    pool.close()
