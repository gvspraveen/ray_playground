from simulation import Simulation
from policy import Policy
from environment import Environment
from train import evaluate_maze_policy
import ray

ray.init()

@ray.remote
class SimulationActor(Simulation):
    """Ray actor for a Simulation."""
    def __init__(self, env):
        super().__init__(env)


def train_maze_policy_parallel(env, num_episodes=100, num_actors=4):
    policy = Policy(env)
    actors = [SimulationActor.remote(env) for _ in range(num_actors)]
    policy_ref = ray.put(policy)

    for _ in range(num_episodes):
        experiences = [sim.rollout.remote(policy_ref) for sim in actors]
        while len(experiences) > 0:
            finished, experiences = ray.wait(experiences)
            for xp in ray.get(finished):
                policy.update_policy(xp)         
        # cost = evaluate_maze_policy(env, policy)
        # print(f"{i} episode: "
        # f"total cost = {cost}.")
    
    return policy

# Parameters to tune
maze_dimensions=(5,5)
env = Environment(maze_dimensions)
num_actors = 4 # Each actor is unit of parallelization in the implementation
episodes_per_actor = 100

# Start training
policy = train_maze_policy_parallel(env, num_episodes=episodes_per_actor, num_actors=num_actors)
# Evaluate
evaluate_maze_policy(env, policy, num_episodes=episodes_per_actor)