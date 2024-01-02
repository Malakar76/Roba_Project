import copy
import numpy as np
from obstacle import compute_distance_to_obstacle, detect_collision


# Class to represent a particle
class Particle:
    # Initialize the particles with random positions and equal weights
    def __init__(self, environment_size=0):
        self.position = np.random.uniform(0, environment_size, 2)
        self.weight = 1

    def __str__(self):
        return f"Position: {self.position}, Weight: {self.weight}"

    def __copy__(self):
        new_instance = Particle()
        new_instance.weight = self.weight
        new_instance.position = self.position
        return new_instance

    # Move a particle based on the given movement
    def move_particle(self, move_x, move_y, obstacles, environment_size):
        if not (detect_collision(self.position, move_x, move_y, obstacles, environment_size)):
            self.position += [move_x, move_y]
            self.position = np.clip(self.position, [0, 0], environment_size)

    # Calculate the predicted distance from a particle to the nearest obstacle.
    def calculate_predicted_distance(self, obstacles):
        closest_distance = float('inf')

        for obstacle in obstacles:
            distance = compute_distance_to_obstacle(self.position, obstacle)
            closest_distance = min(distance, closest_distance)

        return closest_distance

    # Update the weight of the particle based on sensor data and predicted distances
    def update_weight(self, obstacles, sensor_data):
        self.weight = np.exp(-np.abs(self.calculate_predicted_distance(obstacles) - sensor_data))


# Update a table of particle
def update_weights(particles, obstacles, sensor_data):
    weights = 0
    for particle in particles:
        particle.update_weight(obstacles, sensor_data)
        weights += particle.weight
    for particle in particles:
        particle.weight = particle.weight / weights


# Resample the particles based on their weights.
def resample_particles(particles):
    weight = 0
    weights = []
    new_particles = []
    for particle in particles:
        weight += particle.weight
        weights.append(particle.weight)
    indices = np.random.choice(len(particles), size=len(particles), p=weights)
    for i in indices:
        new_particles.append(copy.copy(particles[i]))
    for particle in new_particles:
        particle.weight = 1
    return new_particles


# Estimate the robot's position based on the weighted average of the particle positions.
def estimate_robot_position(particles):
    total_weight = 0
    x = 0
    y = 0
    for particle in particles:
        total_weight += particle.weight
        x += particle.position[0] * particle.weight
        y += particle.position[1] * particle.weight
    x /= total_weight
    y /= total_weight
    return x, y
