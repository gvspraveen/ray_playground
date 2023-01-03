from discrete_space import DiscreteSpace

class Environment:
    def __init__(self, obs_space=(5, 5)):
        self.obs_x, self.obs_y = obs_space
        self.seeker, self.goal = (0, 0), (self.obs_y-1, self.obs_x-1)
        self.info = {'seeker': self.seeker, 'goal': self.goal}

        self.action_space = DiscreteSpace(4)
        self.observation_space = DiscreteSpace(self.obs_y*self.obs_x)

    def reset(self):
        """Reset seeker position and return observations."""
        self.seeker = (0, 0)

        return self.get_observation()

    def get_reward(self):
        """Reward finding the goal"""
        return 1 if self.seeker == self.goal else 0

    def get_observation(self):
        """Encode the seeker position as integer"""
        return self.obs_y * self.seeker[0] + self.seeker[1]

    def is_done(self):
        """We're done if we found the goal"""
        return self.seeker == self.goal

    def step(self, action):
        """Take a step in a direction and return all available information."""
        if action == 0:  # move down
            self.seeker = (min(self.seeker[0] + 1, self.obs_y-1), self.seeker[1])
        elif action == 1:  # move left
            self.seeker = (self.seeker[0], max(self.seeker[1] - 1, 0))
        elif action == 2:  # move up
            self.seeker = (max(self.seeker[0] - 1, 0), self.seeker[1])
        elif action == 3:  # move right
            self.seeker = (self.seeker[0], min(self.seeker[1] + 1, self.obs_x-1))
        else:
            raise ValueError("Invalid action")

        obs = self.get_observation()
        rew = self.get_reward()
        done = self.is_done()
        return obs, rew, done, self.info

    def render(self, *args, **kwargs):
        grid = [['| ' for _ in range(self.obs_x)] + ["|\n"] for _ in range(self.obs_y)]
        grid[self.goal[0]][self.goal[1]] = '|G'
        grid[self.seeker[0]][self.seeker[1]] = '|S'
        print(''.join([''.join(grid_row) for grid_row in grid]))