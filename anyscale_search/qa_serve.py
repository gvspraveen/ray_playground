from ray import serve
from fastapi import FastAPI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import openai
import os


# Create Open API key here : https://app.endpoints.anyscale.com/
open_api_key = os.getenv('OPEN_API_KEY')

system_content = """
Please answer the following question using the context provided. If you don't know the answer, just say that you don't know. Your task is to generate answers to question from the given context. 
"""

query_template = """
Question: {question}, context: {context}
"""

app = FastAPI()
@serve.deployment(ray_actor_options={"num_gpus": 1})
@serve.ingress(app)
class QADeployment:
    def __init__(self):
        from models import (
            hf_embed_model,
            persist_dir
        )
        self.db = FAISS.load_local(persist_dir, hf_embed_model)
        
    def __query__(self, question: str):        
        near_docs = self.db.similarity_search(question)
        print("near_docs to question: " , near_docs)
        chat_completion = openai.ChatCompletion.create(
            api_base = "https://api.endpoints.anyscale.com/v1",
            model="meta-llama/Llama-2-7b-chat-hf",
            messages=[{"role": "system", "content": "You are a helpful assistant"}, 
                    {"role": "user", "content": question}],
            temperature=0.9
         )   
        return chat_completion
    
    @app.post("/question")
    async def query(self, question: str):
        return self.__query__(question)

# Deploy the Ray Serve application.
deployment = QADeployment.bind()