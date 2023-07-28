from typing import List
from ray import serve
from fastapi import FastAPI
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain

app = FastAPI()

template = """
<|SYSTEM|># StableLM Tuned (Alpha version)
- You are a helpful, polite, fact-based agent for answering questions about Ray. 
- Your answers include enough detail for someone to follow through on your suggestions. 
<|USER|>

Please answer the following question using the context provided. If you don't know the answer, just say that you don't know. Base your answer on the context below. Say "I don't know" if the answer does not appear to be in the context below. 

QUESTION: {question} 
CONTEXT: 
{context}

ANSWER: <|ASSISTANT|>
"""
PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

@serve.deployment(ray_actor_options={"num_gpus": 4})
@serve.ingress(app)
class QADeployment:
    def __init__(self):
        from models import (
            hf_embed_model,
            persist_dir
        )
        self.db = FAISS.load_local(persist_dir, hf_embed_model)
        self.llm = self.llm = HuggingFacePipeline.from_model_id(
            model_id="stabilityai/stablelm-tuned-alpha-3b",
            task="text-generation",
            model_kwargs={"temperature": 0.1},
            pipeline_kwargs={"max_new_tokens": 400},
        )
        self.chain = load_qa_chain(self.llm, chain_type="stuff", prompt=PROMPT)        
        
    def __query__(self, question: str):        
        near_docs = self.db.similarity_search(question)
        print("near_docs to question: " , near_docs)
        result = self.chain({"input_documents": near_docs, "question": question})
        return result
    
    @app.post("/question")
    async def query(self, question: str):
        return self.__query__(question)

# Deploy the Ray Serve application.
deployment = QADeployment.bind()