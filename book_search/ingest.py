from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import ray
import numpy as np
import time
import os
from custom_embeddings import open_api_key, FAISS_INDEX_PATH


# Inspiration 
# https://github.com/hwchase17/notion-qa/blob/master/ingest.py
# https://www.anyscale.com/blog/building-a-self-hosted-question-answering-service-using-langchain-ray

# Here we load in the markdown data.
ps = list(Path("book_search/").glob("**/*.md"))
# ps = list(Path("/mnt/user_storage/highlights/").glob("**/*.md"))
db_shards = 8

def extract_docs(ps):
    docs = []
    sources = []
    for p in ps:
        try:
            with open(p, 'rb') as f:
                data = f.read()
                data = data.decode('utf-8', 'ignore')
                docs.append(data)
                sources.append({"source": str(p)})

        except UnicodeDecodeError as e:
            print(f'Error decoding file: {e}')
        # with open(p) as f:
            
        #     docs.append(f.read())
        # sources.append({"source": str(p)})

    return docs, sources


def chunk_docs(docs, sources):
    # Text Splitter
    # Here we split the documents, as needed, into smaller chunks.
    # We do this due to the context limits of the LLMs.
    text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
    return text_splitter.create_documents(docs, metadatas=sources)


@ray.remote(num_gpus=1)
def process_shard(shard): 
    embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)
    # embeddings = CustomHuggingFaceEmbeddings(default_hf_embedding)
    result = FAISS.from_documents(shard, embeddings)
    return result

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
    db.save_local(FAISS_INDEX_PATH)
process_docs()

