import ray
import time

ray.init('auto')

@ray.remote(num_cpus=0)
class Controller:
    def __init__(self):
        self._work = []
    async def wait():
        pass
    
    async def stop():
        pass

@ray.remote(num_cpus=2)
def tasks(i):
    print(f"Executing task {i}")
    time.sleep(120)
    print(f"Task {i} finished")
    
obj = [tasks.remote(i) for i in range(1000)]

while True:
    print(f"Node number: {len(ray.nodes())}")
    time.sleep(5)