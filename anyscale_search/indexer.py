from anyscale_docs_crawler import scrape_urls
from models import (
    hf_embed_model, 
    hf_predictor, 
    lang_embed_model,
    persist_dir
)

from llama_index import Document
from llama_index import SimpleWebPageReader

import ray
from ray.data import ActorPoolStrategy

from typing import Dict, List

# Inspired by https://www.anyscale.com/blog/build-and-scale-a-powerful-query-engine-with-llamaindex-ray
# https://gist.github.com/amogkam/8d2f10c8f6e2cba96673ada6c69311a9

# Step 1: Logic for parsing the web pages into llama_index documents.
def parse_urls(url_row: Dict[str, str]) -> Dict[str, Document]:
    url = url_row["path"]
    documents = SimpleWebPageReader(html_to_text=True).load_data([url])
    return [{"doc": doc} for doc in documents]


# Step 2: Convert the loaded documents into llama_index Nodes. This will split the documents into chunks.
from llama_index.node_parser import SimpleNodeParser
from llama_index.data_structs import Node

def convert_documents_into_nodes(documents: Dict[str, Document]) -> Dict[str, Node]:
    parser = SimpleNodeParser()
    document = documents["doc"]
    nodes = parser.get_nodes_from_documents([document])
    return [{"node": node} for node in nodes]


# Step 3: Embed each node using a local embedding model.
class EmbedNodes:
    def __init__(self):
        self.embedding_model = hf_embed_model
    
    def __call__(self, node_batch: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        nodes = node_batch["node"]
        text = [node.text for node in nodes]
        embeddings = self.embedding_model.embed_documents(text)
        assert len(nodes) == len(embeddings)

        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding
        return {"embedded_nodes": nodes}



if __name__ == "__main__":

    # Processing Logic Begins here
        
    urls = list(scrape_urls())
    # documents = SimpleWebPageReader(html_to_text=True).load_data(urls[0:1])
    # print(documents[0])

    all_urls = [{"path": url} for url in urls]

    # Create the Ray Dataset pipeline
    ds = ray.data.from_items(all_urls)
    ds = ds.limit(25)

    # Parallel process the urls and parse webpage and create Documents
    loaded_ds = ds.flat_map(parse_urls)

    # Convert Documents into llama Nodes
    nodes_ds = loaded_ds.flat_map(convert_documents_into_nodes)
    nodes_ds.show(limit=1)


    # Use `map_batches` to specify a batch size to maximize GPU utilization.
    # We define `EmbedNodes` as a class instead of a function so we only initialize the embedding model once. 
    # This state can be reused for multiple batches.
    embedded_nodes_ds = nodes_ds.map_batches(
        EmbedNodes, 
        batch_size=32, 
        # Use 1 GPU per actor.
        num_gpus=1,
        # There are 3 GPUs in the cluster. Each actor uses 1 GPU. So we want 3 total actors.
        # Set the size of the ActorPool to the number of GPUs in the cluster.
        compute=ActorPoolStrategy(size=3), 
        )

    # Trigger execution and collect all the embedded nodes.
    anyscale_docs_nodes = []
    for row in embedded_nodes_ds.iter_rows():
        node = row["embedded_nodes"]
        assert node.embedding is not None
        anyscale_docs_nodes.append(node)

    # Step 6: Store the embedded nodes in a local vector store, and persist to disk.
    from llama_index import VectorStoreIndex, ServiceContext

    print("Storing Anyscale Documentation embeddings in vector index.")
    service_context = ServiceContext.from_defaults(llm_predictor=hf_predictor, embed_model=lang_embed_model)

    # https://gpt-index.readthedocs.io/en/latest/how_to/index/usage_pattern.html
    docs_index = VectorStoreIndex(nodes=anyscale_docs_nodes, service_context=service_context)
    docs_index.storage_context.persist(persist_dir=persist_dir)

    print("Vector index successfully Saved. Ready for serving.")
