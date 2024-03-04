import os
import sys
import traci
import sumolib
import pandas as pd  
from datetime import datetime 
import numpy as np 
from sklearn.svm import SVC
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.optimizers import Adam


os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

class TrafficSimulator:
    def __init__(self, sumo_cmd):
        self.sumo_cmd = sumo_cmd
        # Start SUMO with the GUI
        traci.start([sumolib.checkBinary('sumo-gui'), '-c', self.sumo_cmd])
    
    def run_simulation(self):
        data = []
        step = 0  # Initialize a step counter to simulate a timestamp
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            vehicle_ids = traci.vehicle.getIDList()
            for veh_id in vehicle_ids:
                x, y = traci.vehicle.getPosition(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                acceleration = traci.vehicle.getAcceleration(veh_id)
                lane_id = traci.vehicle.getLaneID(veh_id)
                # Append data for each vehicle inside the loop
                data.append({
                    "timestamp": step, 
                    "vehicle_id": veh_id,
                    "x": x,
                    "y": y,
                    "speed": speed,
                    "acceleration": acceleration,
                    "lane_id": lane_id
                })
            step += 1  # Increment the step counter
        traci.close()
        df = pd.DataFrame(data)
        
        df.to_csv(f'traffic_data_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv', index=False)
        print("Simulation ended, collected data for", len(data), "vehicle instances.")
    
    def reset_simulation(self):
        traci.load(['-c', self.sumo_cmd, '--start'])
        traci.simulationStep()
    
    def get_state(self):
        vehicle_ids = traci.vehicle.getIDList()
        state_data = []
        for veh_id in vehicle_ids:
            x, y = traci.vehicle.getPosition(veh_id)
            speed = traci.vehicle.getSpeed(veh_id)
            acceleration = traci.vehicle.getAcceleration(veh_id)
            lane_id = traci.vehicle.getLaneID(veh_id)
            # Append data for each vehicle to a list
            state_data.append({
                "vehicle_id": veh_id,
                "x": x,
                "y": y,
                "speed": speed,
                "acceleration": acceleration,
                "lane_id": lane_id
            })
        state_df = pd.DataFrame(state_data)
        average_speed = state_df['speed'].mean()
        state = [average_speed]
        return state 
    
    def step_simulation(self, action):
    # Execute the action (e.g., change traffic light phase)
    # For simplicity, let's assume action is the index of the traffic light phase
        traci.trafficlight.setPhase("traffic_light_ID", action)
    
    # Advance the simulation by one step
        traci.simulationStep()
    
    # Calculate the next state and reward
        next_state = self.get_state()
        reward = -sum(next_state)  # Example reward: negative sum of cars in lanes
        done = traci.simulation.getMinExpectedNumber() == 0  # Example end condition
    
        return reward, next_state, done
    
if __name__ == '__main__':
    sumo_cmd = "osm.sumocfg"  # Ensure this path is correct and accessible
    simulator = TrafficSimulator(sumo_cmd)
    simulator.run_simulation()

class DRLAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self._build_model()
    
    def _build_model(self):
        model = Sequential()
        model.add(InputLayer(input_shape=(self.state_size,)))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
        return model
    
    def act(self, state, epsilon=0.1):
        if np.random.rand() <= epsilon:
        # Return a random action (explore)
            return np.random.randint(0, self.action_size)
        else:
        # Return the best action (exploit) based on current policy
            q_values = self.model.predict(np.array([state]))
            return np.argmax(q_values[0])

    def train(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = (reward + 0.95 * np.amax(self.model.predict(np.array([next_state]))[0]))
        target_f = self.model.predict(np.array([state]))
        target_f[0][action] = target
        self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

# Example usage
# Define the environment and agent
state_size = 10  # Example state size
action_size = 4  # Example action size
agent = DRLAgent(state_size, action_size)
simulator = TrafficSimulator(sumo_cmd='osm.sumocfg')
simulator.agent = agent

# Run simulation for a certain number of episodes
episodes = 10
simulator.run_simulation(episodes)
############ Model Integration ############

# For DQN, integrate the environment setup, action-reward mechanism, and training loop.
# For ARIMA, include steps to select model parameters based on your traffic data and perform time series forecasting.
# For SVM, implement data labeling for road changes, train the SVM model, and evaluate its performance.