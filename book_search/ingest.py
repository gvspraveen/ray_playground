from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import ray
import numpy as np
import time
from langchain.embeddings.base import Embeddings
from typing import List
from sentence_transformers import SentenceTransformer


# Source : https://github.com/hwchase17/notion-qa/blob/master/ingest.py
# https://docs.google.com/document/d/1hph_cknMborgUsDI55p0mvQKyphqUZmvD8B75UOvweg/edit#

# Here we load in the markdown data.
ps = list(Path("book_search/").glob("**/*.md"))
db_shards = 8

def extract_docs(ps):
    docs = []
    sources = []
    for p in ps:
        with open(p) as f:
            docs.append(f.read())
        sources.append({"source": str(p)})

    return docs, sources


def chunk_docs(docs, sources):
    # Text Splitter
    # Here we split the documents, as needed, into smaller chunks.
    # We do this due to the context limits of the LLMs.
    text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
    return text_splitter.create_documents(docs, metadatas=sources)


@ray.remote(num_gpus=1)
def process_shard(shard): 
    embeddings = OpenAIEmbeddings(openai_api_key="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")
    result = FAISS.from_documents(shard, embeddings)
    return result

class LocalHuggingFaceEmbeddings(Embeddings):
    def __init__(self, model_id): 
        # Should use the GPU by default
        self.model = SentenceTransformer(model_id)
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using a locally running
           Hugging Face Sentence Transformer model
        Args:
            texts: The list of texts to embed.
        Returns:
            List of embeddings, one for each text.
        """
        embeddings =self.model.encode(texts)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a query using a locally running HF 
        Sentence trnsformer. 
        Args:
            text: The text to embed.
        Returns:
            Embeddings for the text.
        """
        embedding = self.model.encode(text)
        return list(map(float, embedding))

def process_docs():
    print(f'Loading chunks into vector store ... using {db_shards} shards') 
    st = time.time()
    docs, sources = extract_docs(ps)
    chunks = chunk_docs(docs, sources)
    shards = np.array_split(chunks, db_shards)
    futures = [process_shard.remote(shards[i]) for i in range(db_shards)]
    results = ray.get(futures)
    et = time.time() - st
    print(f'Shard processing complete. Time taken: {et} seconds.')


    st = time.time()
    print('Merging shards ...')
    # Straight serial merge of others into results[0]
    db = results[0]
    for i in range(1,db_shards):
        db.merge_from(results[i])
    et = time.time() - st
    print(f'Merged in {et} seconds.') 

process_docs()

