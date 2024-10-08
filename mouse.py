import numpy as np
import gymnasium as gym
import pygame


class Mouse(pygame.sprite.Sprite):
    def __init__(self, maze, size=20):
        super().__init__()

        # PYGAME OBJECTS
        self.maze = maze
        self.original_image = pygame.image.load('mouse.png')  # Load the mouse image
        self.image = pygame.transform.scale(self.original_image, (size, size))  # Scale the image to the desired size
        self.rect = self.image.get_rect(center=maze.start.sprites()[0].rect.center)

        self.closest = self.goal_distance()

        # OBSERVATION SHAPE EXTREMELY IMPORTANT
        self.observation_space = gym.spaces.Box(low=-1000, high=1000, shape=(6,), dtype=np.int16)

    def observe(self):
        mouse_x, mouse_y = self.rect.center
        goal_x, goal_y = self.maze.goal.sprites()[0].rect.center

        dist_x, dist_y = goal_x - mouse_x, goal_y - mouse_y

        up = self.directional_distance(0, -1, self.maze.walls)
        down = self.directional_distance(0, 1, self.maze.walls)
        left = self.directional_distance(-1, 0, self.maze.walls)
        right = self.directional_distance(1, 0, self.maze.walls)

        # RETURN OBSERVATION IN THE SAME SHAPE AS YOUR DEFINED OBSERVATION SPACE
        return [dist_x, dist_y, up, down, left, right]

    def goal_distance(self):
        """SELF EXPLANATORY"""
        mouse_x, mouse_y = self.rect.center
        goal_x, goal_y = self.maze.goal.sprites()[0].rect.center
        dist_x, dist_y = goal_x - mouse_x, goal_y - mouse_y

        return (dist_x ** 2 + dist_y ** 2) ** .5

    def directional_distance(self, dx, dy, target):
        """CHECKS COLLISION DISTANCE BY DRAWING PIXELS IN THE DIRECTION OF DX,DY"""

        distance = 0
        photon = pygame.sprite.Sprite()
        photon.image = pygame.Surface((1, 1))  # Create a 1x1 pixel surface for the photon
        photon.rect = photon.image.get_rect()
        photon.rect.center = self.rect.center  # Start at the center of the mouse

        while True:
            photon.rect.x += dx
            photon.rect.y += dy

            distance += 1
            if pygame.sprite.spritecollideany(photon, target):
                break
        return distance

    def reward(self, action, collided, done):
        """CALCULATE YOUR REWARD, RETURN INT/FLOAT"""
        if collided:
            return -5  # discourage walls

        current_distance = self.goal_distance()
        if current_distance < self.closest:
            self.closest = current_distance
            return 10  # Reward for new records

        return -1  # discourage taking a while
