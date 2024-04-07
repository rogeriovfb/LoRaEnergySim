import numpy as np


############### SIMULATION SPECIFIC PARAMETERS ###############
start_with_fixed_sf = True
start_sf = 7

scaling_factor = 1
transmission_rate_id = str(scaling_factor)
transmission_rate_bit_per_ms = scaling_factor*(12*8)/(60*60*1000)  # 12*8 bits per hour (1 typical packet per hour)
simulation_time = 24 * 60 * 60 * 1000 * 30/scaling_factor
cell_size = 10000
adr = True
confirmed_messages = True

#payload_sizes = [12]
#path_loss_variances = [7.9]  # [0, 5, 7.8, 15, 20]

payload_size = 12
path_loss_variance = 0

MAC_IMPROVEMENT = False
num_locations = 10000
num_of_simulations = 1
locations_file = "locations/"+"{}_locations_{}_sim.pkl".format(num_locations, num_of_simulations)
results_file = "results/{}_{}_{}_{}_propagation.p".format(num_locations, payload_size, adr, confirmed_messages,)

############### SIMULATION SPECIFIC PARAMETERS ###############

############### DEFAULT PARAMETERS ###############
LOG_ENABLED = True
MAX_DELAY_BEFORE_SLEEP_MS = 500
PRINT_ENABLED = True
MAX_DELAY_START_PER_NODE_MS = np.round(simulation_time / 10)
track_changes = True
middle = np.round(cell_size / 2)
load_prev_simulation_results = True

############### DEFAULT PARAMETERS ###############
