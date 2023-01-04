import ray 
import subprocess
import time
import re
ray.init()




# zen_of_python = subprocess.check_output(["python", "-c", "import this"])
# corpus = zen_of_python.split()

text_file = open("sea_change.txt", "r")
data = text_file.read()
corpus = re.sub(r'[^a-zA-Z]', ' ', data)
corpus = corpus.split()


chunk = len(corpus) // num_partitions
corpus_chunks = [
    corpus[i * chunk: (i + 1) * chunk] for i in range(num_partitions)
]

@ray.remote
def map_chunks(corpus_chunk, num_partitions, delay=0.0):
    results = [list() for _ in range(num_partitions)]

    for document in corpus_chunk:
        for word in document.lower().split():
            # first_letter = word.decode("utf-8")[0]
            first_letter = word[0]
            partition_index = ord(first_letter) % num_partitions
            results[partition_index].append((word, 1))        
        # Sleep little bit between each document
        time.sleep(delay)
    return results

@ray.remote
def reduce_results(*results):
    reduce_results = dict()
    for res in results:
        for key, value in res:
            if key not in reduce_results:
                reduce_results[key] = 0
            reduce_results[key] += value

    return reduce_results


def perform_map_reduce(num_partitions, delay=0.0):
    reducer_outputs = []

    map_results = [
        map_chunks.options(num_returns=num_partitions)
        .remote(chunk, num_partitions, delay=mapper_delay)
        for chunk in corpus_chunks
    ]

    for i in range(num_partitions):
        # We can take the i-th return value from each mapper and send it to the i-th reducer         
        ith_maps_results = [map_result[i] for map_result in map_results]
        reducer_outputs.append(reduce_results.remote(*ith_maps_results))
    
    # Extract counts for each word from reducer outputs
    counts = {k: v for output in ray.get(reducer_outputs) for k, v in output.items()}

    # sort the counts
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    # Print counts
    for count in sorted_counts:
        print(f"{count[0]}: {count[1]}")
        # print(f"{count[0].decode('utf-8')}: {count[1]}")

#  NUM of PARTITIONS == NUM of MAP tasks
num_partitions = 5
mapper_delay = 0.01
perform_map_reduce(num_partitions, delay=mapper_delay)