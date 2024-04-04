import os
import pickle

from Simulations.GlobalConfig import locations_file, num_locations, num_of_simulations, cell_size
from Framework.Location import Location

locations_per_simulation = list()


for num_sim in range(num_of_simulations):
    locations = list()
    for i in range(num_locations):
        locations.append(Location(min=0, max=cell_size, alt_min=10, alt_max=60, indoor=False))
    locations_per_simulation.append(locations)


os.makedirs(os.path.dirname(locations_file), exist_ok=True)
with open(locations_file, 'wb') as f:
    pickle.dump(locations_per_simulation, f)

# just to test the code
# with open('locations_10000_locations_1000_sim.pkl', 'rb') as filehandler:
#     print(pickle.load(filehandler))
