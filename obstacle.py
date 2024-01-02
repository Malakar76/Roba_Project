import numpy as np


# Representation of an obstacle in the environment
class Obstacle:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max


# Check if moving the robot to a new position will make a collision with the obstacles
def detect_collision(position, move_x, move_y, obstacles, environment_size):
    px = position[0]
    py = position[1]
    new_x = px + move_x
    new_y = py + move_y

    new_x = np.clip(new_x, 0, environment_size[0])
    new_y = np.clip(new_y, 0, environment_size[1])

    for obstacle in obstacles:
        if obstacle.x_min < new_x < obstacle.x_max and obstacle.y_min < new_y < obstacle.y_max:
            return True

    return False


def compute_distance_to_obstacle(position, obstacle):
    px, py = position
    closest_x = max(obstacle.x_min, min(px, obstacle.x_max))
    closest_y = max(obstacle.y_min, min(py, obstacle.y_max))

    distance = np.hypot(px - closest_x, py - closest_y)
    return distance
