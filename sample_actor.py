import ray
import time


ray.init()


@ray.remote
def squares(x):
    time.sleep(5)
    return x*x

futures = [squares.remote(i) for i in range(5)]

print(ray.get(futures))
