import ray
import time
import asyncio
import random

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


# counters = [Counter.remote() for _ in range(10)]
# results = [ray.get(c.incr.remote()) for c in counters]
# print(results)


names=["We","I","They","He","She","Jack","Jim"]	
verbs=["was","is","are","were"]
nouns=["playing a game","watching television","talking","dancing","speaking"]
@ray.remote
def generate_sentences():
   # Feel free to change the number to make the script run longer or shorter
   for i in range(100):
     a=(random.choice(names))
     b=(random.choice(verbs))
     c=(random.choice(nouns))
     return a+" ",b+" "+c
     time.sleep(1)
sentences = [generate_sentences.remote() for _ in range(15)]
print(ray.get(sentences))
