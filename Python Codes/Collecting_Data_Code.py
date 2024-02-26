#This code will collect data from sumo 
import os
import csv
import traci
import traci.constants as tc

# path to SUMO installation and the simulation configuration file
sumoBinary= "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "osm.sumocfg"]

# Features to collect
features = ['time', 'vehicle_id', 'x', 'y', 'speed', 'waiting_time']
data = []

# Initialize simulation
traci.start(sumoCmd)

# Run simulation
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for veh_id in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(veh_id)
        speed = traci.vehicle.getSpeed(veh_id)
        waiting_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
        data.append([traci.simulation.getTime(), veh_id, x, y, speed, waiting_time])

# Close the TraCI connection
traci.close()

# Save data to CSV
with open('sumo_output_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(features)  # Write the header
    writer.writerows(data)

print("Data collection complete. CSV file created.")
