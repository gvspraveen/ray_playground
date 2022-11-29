import ray
import time
import asyncio

ray.init()

@ray.remote
class Counter(object):
    def __init__(self):
        self.value = 0

    def incr(self):
        self.value += 1
        return self.value

    def getvalue(self):
        return self.value


counters = [Counter.remote() for _ in range(10)]
# results = [ray.get(c.incr.remote()) for c in counters]
# print(results)