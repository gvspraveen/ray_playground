## A simple distributed maze app using Reinforcement learning inspired by [Learning Ray tutorial](https://github.com/maxpumperla/learning_ray/blob/main/notebooks/ch_03_core_app.ipynb)

### Files

1. environment -> A container for maze game. Sets up the maze dimensions, start & end positions, methods to move seeker in the maze
2. policy -> A simple policy which determines next action from current state. Also has a learning method which updates weights
3. simulation -> Takes a environment and policy. Executes the game till goal state is reached. Returns all the steps taken from start to finish
4. train -> Helper methods to evaluate the policy (calculates average number of steps taken to achieve goal for each iteration of game)
5. train_parallel -> Utilizes Ray actorst to perform distributed training of policy simulatenously through multiple actors.

### How to run

- Open train_parallel.py
- Update parameters at end of file (maze size, number of parallel actors, etc)
- Run `python train_parallel.py`
