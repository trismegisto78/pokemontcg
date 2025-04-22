# agents/random_agent.py

import random

class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def select_action(self, state):
        return random.choice(range(self.action_space.n))
