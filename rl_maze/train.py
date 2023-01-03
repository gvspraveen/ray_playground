import time
from environment import Environment
from policy import Policy
from simulation import Simulation

def train_maze_policy(env, num_episodes=100):
    policy = Policy(env)
    sim = Simulation(env)
    for _ in range(num_episodes):
        experiences = sim.rollout(policy)
        policy.update_policy(experiences)
    
    return policy

def evaluate_maze_policy(env, policy, num_episodes=50):
    sim = Simulation(env)
    cost = 0

    for _ in range(num_episodes):
        experiences = sim.rollout(policy)
        cost += len(experiences)

    # print(f"{cost / num_episodes} steps on average "
    #     f"for a total of {num_episodes} episodes.")

    return cost / num_episodes
