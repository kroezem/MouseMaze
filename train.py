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

while True:
    env = MazeEnv(random.choice(mazes))
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log='./logs')  # STARTS A FRESH MODEL
    # model = PPO.load(MODEL_NAME, env) #LOADS EXISTING MODEL

    model.learn(total_timesteps=10_000, reset_num_timesteps=False, tb_log_name=f'{MODEL_NAME}_{env.name}')
    print('*****SAVING*****')
    model.save(MODEL_NAME)
