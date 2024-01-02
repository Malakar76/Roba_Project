import numpy as np
from obstacle import compute_distance_to_obstacle


# Model used to define the robot
class Model:
    def __init__(self, pos_x, pos_y):
        self.position = [pos_x, pos_y]

    # Function to move the robot
    def move_robot(self, move_x, move_y, move_noise=0.1):
        self.position[0] += np.random.normal(move_x, move_noise)
        self.position[1] += np.random.normal(move_y, move_noise)

    # Function to compute the sensor minimum distance with an obstacle (rectangle)
    def sensor_data_computation(self, obstacles, sensor_noise=0.5):
        distance = [compute_distance_to_obstacle(self.position, obstacle) for obstacle in obstacles]
        min_distance = min(distance) if distance else float('inf')
        return np.random.normal(min_distance, sensor_noise)
