import os

import numpy as np
import pygame
import gymnasium as gym

from maze import Maze
from mouse import Mouse


class MazeEnv(gym.Env):
    def __init__(self, map_file, render_mode="rgb_array"):
        super(MazeEnv, self).__init__()
        self.name = os.path.basename(map_file).split('.')[0]

        # GAME OBJECTS
        self.maze = Maze(map_file)
        self.mouse = Mouse(self.maze)

        # DEFINING THESE SPACES IS EXTREMELY IMPORTANT
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.int8)
        self.observation_space = self.mouse.observation_space

        # SETTING UP PYGAME
        pygame.init()
        if render_mode == 'human':
            self.screen = pygame.display.set_mode((802, 802))
            pygame.display.set_caption("Maze Gym Environment")
            self.clock = pygame.time.Clock()

    def reset(self, seed=None, options=None):
        """RESETS ENV BACK TO BASE STATE"""
        self.mouse = Mouse(self.maze)
        observation = self.mouse.observe()

        # ALWAYS NEEDS TO RETURN: observation, infos
        return observation, {}

    def step(self, action):
        """THIS IS WHERE ALL THE WORK IS ACTUALLY DONE"""

        collided = False
        self.mouse.rect.x += action[0]
        if pygame.sprite.spritecollide(self.mouse, self.maze.walls, False):
            collided = True
            self.mouse.rect.x -= action[0]

        self.mouse.rect.y += action[1]
        if pygame.sprite.spritecollide(self.mouse, self.maze.walls, False):
            collided = True
            self.mouse.rect.y -= action[1]

        # CHECK IF REACHED GOAL
        done = pygame.sprite.spritecollide(self.mouse, self.maze.goal, False)

        obs = self.mouse.observe()
        reward = self.mouse.reward(action, collided, done)

        # ALWAYS NEEDS TO RETURN: observation, reward, termination, truncation, infos
        return obs, reward, done, False, {}

    def render(self, mode='human'):
        """THIS RENDERS PYGAME, DONT RUN DURING TRAINING"""
        if mode == 'human':
            self.screen.fill((0, 0, 0))
            self.maze.draw(self.screen)
            self.screen.blit(self.mouse.image, self.mouse.rect)
            pygame.display.flip()
            self.clock.tick(120)

        elif mode == 'rgb_array':
            return pygame.surfarray.array3d(pygame.display.get_surface()).transpose(1, 0, 2)

    def close(self):
        pygame.quit()
