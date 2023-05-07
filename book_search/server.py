import ray
from ray import serve
from starlette.requests import Request
from langchain.embeddings import OpenAIEmbeddings
from custom_embeddings import open_api_key, FAISS_INDEX_PATH
from langchain.vectorstores import FAISS

@serve.deployment(ray_actor_options={"num_gpus": 1})
class KnowledgeBase:
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)
        self.db = FAISS.load_local(FAISS_INDEX_PATH, self.embeddings)