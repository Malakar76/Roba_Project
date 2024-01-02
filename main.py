import pygame
import random
from obstacle import *
from Model import *
from Particle import *


def main():
    # Initialize the Pygame library
    pygame.init()
    # Set up the display window
    screen = pygame.display.set_mode((400, 400))
    # Initialize the clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Define the environment size and number of particles
    environment_size = (400, 400)
    num_particles = 2000
    move_x, move_y = 0, 0
    # Create a list of obstacles in the environment
    obstacles = [
        Obstacle(70, 50, 310, 100),
        Obstacle(130, 120, 180, 180),
        Obstacle(70, 220, 200, 240),
        Obstacle(250, 260, 350, 350),
        Obstacle(30,320, 200, 360)
    ]

    # Initialize particles in the environment and position of the robot
    particles = [Particle(environment_size) for _ in range(num_particles)]
    i = random.randint(0, num_particles)
    while detect_collision(particles[i].position, 0, 0, obstacles, environment_size):
        i = random.randint(1, num_particles)
    model = Model(particles[i].position[0], particles[i].position[1])

    # Draw the obstacles on the screen
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 0, 255), (
            obstacle.x_min, obstacle.y_min, obstacle.x_max - obstacle.x_min, obstacle.y_max - obstacle.y_min))

    # Draw the particles on the screen
    for particle in particles:
        pygame.draw.circle(screen, (255, 0, 0), (int(particle.position[0]), int(particle.position[1])), 2)

    # Draw the robot
    pygame.draw.circle(screen, (0, 255, 0), (int(model.position[0]), int(model.position[1])), 2)

    # Update the display
    pygame.display.flip()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle key presses for particle movement
            keys = pygame.key.get_pressed()
            move_x, move_y = 0, 0
            if keys[pygame.K_LEFT]:
                move_x = -1
            if keys[pygame.K_RIGHT]:
                move_x = 1
            if keys[pygame.K_UP]:
                move_y = -1
            if keys[pygame.K_DOWN]:
                move_y = 1

        # Check for collisions and update particle/robot positions if there is no collision
        if not detect_collision(model.position, move_x, move_y, obstacles, environment_size):
            model.move_robot(move_x, move_y)
            for particle in particles:
                particle.move_particle(move_x, move_y, obstacles, environment_size)

        # Update sensor data and particle weights based on the new positions
        sensor_data = model.sensor_data_computation(obstacles)
        update_weights(particles, obstacles, sensor_data)

        # Resample the particles and estimate the position of the robot
        particles = resample_particles(particles)
        estimated_position = estimate_robot_position(particles)

        # Clear the screen for the new frame
        screen.fill((0, 0, 0))

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 0, 255), (
                obstacle.x_min, obstacle.y_min, obstacle.x_max - obstacle.x_min, obstacle.y_max - obstacle.y_min))

        # Draw particles
        for particle in particles:
            pygame.draw.circle(screen, (255, 0, 0), (int(particle.position[0]), int(particle.position[1])), 2)

        # Draw the estimated position of the robot
        pygame.draw.circle(screen, (0, 255, 255), (int(estimated_position[0]), int(estimated_position[1])), 5)

        # Draw the robot
        pygame.draw.circle(screen, (0, 255, 0), (int(model.position[0]), int(model.position[1])), 5)

        # Update the display and control the frame rate
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
