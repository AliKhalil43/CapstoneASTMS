#This code will collect data for vehicle waiting times at traffic lights

import os
import csv
import traci

sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"  
sumoCmd = [sumoBinary, "-c", "osm.sumocfg"]

# Initialize data collection
data = []
features = ['time_step', 'traffic_light_id', 'vehicle_id', 'waiting_time']

# Start simulation
traci.start(sumoCmd)

# Run simulation
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    # Get list of traffic lights
    traffic_lights = traci.trafficlight.getIDList()
    for tl in traffic_lights:
        # Get controlled lanes by this traffic light and find vehicles in those lanes
        controlled_lanes = traci.trafficlight.getControlledLanes(tl)
        for lane in controlled_lanes:
            vehicles = traci.lane.getLastStepVehicleIDs(lane)
            for vehicle in vehicles:
                # Get vehicle waiting time
                waiting_time = traci.vehicle.getWaitingTime(vehicle)
                # Record data if the vehicle is waiting
                if waiting_time > 0:
                    data.append([traci.simulation.getTime(), tl, vehicle, waiting_time])

# Close the TraCI connection
traci.close()

# Save data to CSV
with open('vehicle_waiting_times_at_traffic_lights.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(features)  # Write the header
    writer.writerows(data)

print("Vehicle waiting times at traffic lights data collection complete. CSV file created.")
