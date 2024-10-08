import os
import random

import pygame
from stable_baselines3 import PPO
from maze_env import MazeEnv

MODEL_NAME = 'mouse0'

# GET A DIRECTORY OF MAZES TO RANDOMLY TRAIN FROM
MAZE_SET_DIRECTORY = './mazes/basic'
all_files = os.listdir(MAZE_SET_DIRECTORY)
mazes = [os.path.join(MAZE_SET_DIRECTORY, f) for f in all_files]

env = MazeEnv(random.choice(mazes), render_mode='human')
model = PPO.load('mouse0', env)

obs, _ = env.reset()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.close()
            exit()

    action, _states = model.predict(obs)
    obs, rewards, done, _, info = env.step(action)
    env.render("human")

    if done:
        env = MazeEnv(random.choice(mazes), render_mode='human')
        obs, _ = env.reset()
        model = PPO.load('mouse0', env)

