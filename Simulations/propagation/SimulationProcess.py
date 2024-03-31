import simpy

from Framework import PropagationModel
from Framework.AirInterface import AirInterface
from Framework.EnergyProfile import EnergyProfile
from Framework.Gateway import Gateway
from Framework.LoRaParameters import LoRaParameters
from Framework.Node import Node
from Framework.SNRModel import SNRModel
from Simulations.GlobalConfig import *

import time


tx_power_mW = {2: 91.8, 5: 95.9, 8: 101.6, 11: 120.8, 14: 146.5}
rx_measurements = {'pre_mW': 8.2, 'pre_ms': 3.4, 'rx_lna_on_mW': 39,
                   'rx_lna_off_mW': 34,
                   'post_mW': 8.3, 'post_ms': 10.7}

def run_helper(args):
    return run(*args)


def run(locs, p_size, sim_time, gateway_location, num_nodes, transmission_rate, confirmed_messages, adr, propagation_model):
    start_time = time.time()

    sim_env = simpy.Environment()
    gateway = Gateway(sim_env, gateway_location, max_snr_adr=True, avg_snr_adr=False)
    nodes = []
    air_interface = AirInterface(gateway, propagation_model, SNRModel(), sim_env)
    for node_id in range(num_nodes):
        energy_profile = EnergyProfile(5.7e-3, 15, tx_power_mW,
                                       rx_power=rx_measurements)
        _sf = np.random.choice(LoRaParameters.SPREADING_FACTORS)
        if start_with_fixed_sf:
            _sf = start_sf
        lora_param = LoRaParameters(freq=np.random.choice(LoRaParameters.DEFAULT_CHANNELS),
                                    sf=_sf,
                                    bw=125, cr=5, crc_enabled=1, de_enabled=0, header_implicit_mode=0, tp=14)
        node = Node(node_id, energy_profile, lora_param, sleep_time=(8 * p_size / transmission_rate),
                    process_time=5,
                    adr=adr,
                    location=locs[node_id],
                    base_station=gateway, env=sim_env, payload_size=p_size, air_interface=air_interface,
                    confirmed_messages=confirmed_messages)
        nodes.append(node)
        sim_env.process(node.run())

    sim_env.run(until=sim_time)

    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))
    # Simulation is done.
    # process data

    mean_energy_per_bit_list = list()
    for n in nodes:
        mean_energy_per_bit_list.append(n.energy_per_bit())

    data_nodes_raw = Node.get_simulation_data_frame(nodes)
    data_gateway_raw = gateway.get_simulation_data(0)
    data_air_interface_raw = air_interface.get_simulation_data(0)

    # eff_en = data_mean_nodes['TotalEnergy'][sigma] / (p_size*data_mean_nodes['UniquePackets'][sigma])
    # print('Eb {} for Size:{} and Sigma:{}'.format(eff_en, p_size, sigma))

    return {
        'propagation': propagation_model,
        'simulation_time': end_time - start_time,
        'mean_energy_all_nodes_per_bit': mean_energy_per_bit_list,
        'data_nodes_raw': data_nodes_raw,
        'data_gateway_raw': data_gateway_raw,
        'data_air_interface_raw':data_air_interface_raw
    }
