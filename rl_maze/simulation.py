from environment import Environment
import time

class Simulation:
    def __init__(self, env):
        self.env = env

    def rollout(self, policy, render=False, explore=True, epsilon=0.1, delay=0.0):
        experiences = []
        state = self.env.reset()
        done = False
        while not done:
            next_action = policy.get_action(state, explore=explore, epsilon=epsilon)
            next_state, reward, done, info = self.env.step(next_action)
            experiences.append([state, next_action, reward, next_state])
            state = next_state
            if render:
                time.sleep(0.01)
                self.env.render()

        time.sleep(delay)
        return experiences


# Test
# environment = Environment(obs_space=(3,3))
# policy = Policy(environment)
# sim = Simulation(environment)
# sim.rollout(render=True, policy, explore=True, epsilon=1.0)
