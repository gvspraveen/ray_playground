import ray
import random
import time
import math
from fractions import Fraction


"""
Distributed PI calculator using Montecarlo simulation. https://www.geeksforgeeks.org/estimating-value-pi-using-monte-carlo/

Each task runs for certain num_samples and calculates pi. We then average value across all tasks.

Individual Task Logic:

This task will take a 2X2 square plane and randomly generates (x,y) samples. If (x^2 + y^2 <= 1) then this
sample is inside circle.

(pi*r^2)/(4*r^2) = (area of circle)/(area of square)

So, 
pi = 4 * (area of circle)/(area of square)

Or in other words

pi = 4 * (Num of samples inside circle)/(num of samples inside square grid) 

"""

@ray.remote
def pi4_task(num_samples, delay=0.0):
    """Runs num_samples experiments, and returns the
    fraction of time it was inside the circle.
    """
    in_count = 0
    for i in range(num_samples):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            in_count += 1
    time.sleep(delay)
    return Fraction(in_count, num_samples)

SAMPLES_PER_ACTOR = 10000
DELAY_PER_ACTOR = 0.1
NUM_ACTORS = 20

# Testing single actor
# start = time.time()
# future = pi4_task.remote(SAMPLES_PER_ACTOR)
# pi4 = ray.get(future)
# end = time.time()
# dur = end - start
# print(f'Running {SAMPLES_PER_ACTOR} tests took {dur} seconds')
# pi = pi4 * 4
# print(f'{float(pi)} is off by {abs(pi-math.pi)/pi*100}%')


ray.init()
start = time.time()
print(f'Doing {NUM_ACTORS} actors')
results = []
for _ in range(NUM_ACTORS):
    results.append(pi4_task.remote(SAMPLES_PER_ACTOR, delay=DELAY_PER_ACTOR))
output = ray.get(results)
pi = sum(output)*4/len(output)
end = time.time()
dur = end - start
print(f'Running {NUM_ACTORS} actors with {SAMPLES_PER_ACTOR} samples/actor took {dur} seconds')
print(f'{float(pi)} is off by {abs(pi-math.pi)/pi*100}%')
