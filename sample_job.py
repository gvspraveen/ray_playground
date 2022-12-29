import ray
import time
import random

ray.init()

names=["We","I","They","He","She","Jack","Jim"]	
verbs=["was","is","are","were"]
nouns=["playing a game","watching television","talking","dancing","speaking"]
def generator():
    a=(random.choice(names))
    b=(random.choice(verbs))
    c=(random.choice(nouns))
    return a+" ",b+" "+c        

@ray.remote
def sentence_task(sentences_per_tasks=1, delay=1):
    sentences = []
    for _ in range(sentences_per_tasks):
        sentences.append(generator())
        time.sleep(delay)
    print(sentences)
    return sentences

num_tasks = 100
sentences_per_tasks = 5
task_delay = 0.5

futures = [sentence_task.remote(sentences_per_tasks, task_delay) for _ in range(num_tasks)]
sentences = ray.get(futures)
print(sentences)