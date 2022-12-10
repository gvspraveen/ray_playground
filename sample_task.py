import ray
import time
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
def generate_sentences(num=1, delay=1):
    for _ in range(num):
        a=(random.choice(names))
        b=(random.choice(verbs))
        c=(random.choice(nouns))
        return a+" ",b+" "+c
        time.sleep(delay)
        
if __name__ == "__main__":
    sentences = [generate_sentences.remote(1, 5) for _ in range(100)]
    # print(ray.get(sentences))

