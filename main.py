import os
import traci
import traci.constants as tc
import subprocess
import time

# Set the path to your SUMO installation
sumo_bin = "/opt/homebrew/bin/sumo"
sumo_cmd = [sumo_bin, "-c", "/opt/homebrew/bin/sumo/scenario/file.sumocfg"]

# Start SUMO as a subprocess
sumo_process = subprocess.Popen(sumo_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Connect to the running simulation using TraCI
traci.start(sumo_cmd)

# Add a couple of vehicles to the simulation
traci.vehicle.add("vehicle_1", "route_0", typeID="car")
traci.vehicle.add("vehicle_2", "route_0", typeID="car")

# Simulation loop
for step in range(100):  # Replace with the desired number of simulation steps
    # Perform simulation steps
    traci.simulationStep()

    # Access simulation data using TraCI functions
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getPosition(vehicle_id)
        print(f"Vehicle {vehicle_id}: Position {vehicle_position}")

    time.sleep(1)  # Optional: Add a delay to slow down the simulation loop

# Finish simulation
traci.close()
sumo_process.terminate()
