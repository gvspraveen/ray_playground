import ray
import time
import random

ray.init()

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

sentences = [generate_sentences.remote(1, 5) for _ in range(100)]
# print(ray.get(sentences))
