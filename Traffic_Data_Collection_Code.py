#This code will collect traffic light data and generate it 
import os
import csv
import traci

# Path to SUMO-GUI or SUMO binary
sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"  
sumoCmd = [sumoBinary, "-c", "osm.sumocfg"]

# Traffic light features to collect
features = ['time', 'traffic_light_id', 'state']
data = []

# Initialize simulation
traci.start(sumoCmd)

# Run simulation
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for tl_id in traci.trafficlight.getIDList():
        state = traci.trafficlight.getRedYellowGreenState(tl_id)
        data.append([traci.simulation.getTime(), tl_id, state])

# Close the TraCI connection
traci.close()

# Save data to CSV
with open('sumo_traffic_lights_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(features)  # Write the header
    writer.writerows(data)

print("Traffic light data collection complete. CSV file created.")
