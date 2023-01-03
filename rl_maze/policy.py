import numpy as np
import random

class Policy:

    def __init__(self, env):
        """A Policy suggests actions based on the current state.
        We do this by tracking the value of each state-action pair.
        """
        self.state_action_table = [
            [0 for _ in range(env.action_space.n)]
            for _ in range(env.observation_space.n)
        ]
        self.action_space = env.action_space

    def get_action(self, state, explore=True, epsilon=0.1):
        """Explore randomly or exploit the best value currently available."""
        if explore and random.uniform(0, 1) < epsilon:
            return self.action_space.sample()
        return np.argmax(self.state_action_table[state])

    def update_policy(self, experiences, weight=0.1, discount=0.9):
        """Updates a given policy with a list of (state, action, reward, state)
        experiences."""
        for state, action, reward, next_state in experiences:
            next_max = np.max(self.state_action_table[next_state])
            action_value = self.state_action_table[state][action]
            new_value = (1-weight) * action_value + weight * (reward + discount * next_max)
            self.state_action_table[state][action] = new_value
