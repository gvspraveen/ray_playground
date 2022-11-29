import ray
import time
import asyncio

ray.init()

@ray.remote
class AsyncCounter(object):
    def __init__(self) -> None:
        self.value = 0

    async def incr(self):
        await asyncio.sleep(1)
        self.value += 1
        return self.value
    
    async def get(self):
        await asyncio.sleep(1)
        return self.value

acounters = [Counter.remote() for _ in range(10)]

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
results = [loop.run_until_complete(ac.incr.remote()) for ac in acounters] 
print(results)