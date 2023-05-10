import ray
from ray import serve
from starlette.requests import Request
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from custom_embeddings import open_api_key, FAISS_INDEX_PATH
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from typing import List, Optional, Any

# Inspiration
# https://python.langchain.com/en/latest/modules/chains/index_examples/vector_db_qa.html
# https://www.anyscale.com/blog/building-a-self-hosted-question-answering-service-using-langchain-ray

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

@serve.deployment(ray_actor_options={"num_gpus": 1})
class KnowledgeBase:
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)
        self.db = FAISS.load_local(FAISS_INDEX_PATH, self.embeddings)
        self.llm = self.llm = HuggingFacePipeline.from_model_id(
            model_id="stabilityai/stablelm-tuned-alpha-3b",
            task="text-generation",
            model_kwargs={"temperature": 0.1},
        )
        self.chain = load_qa_chain(self.llm, chain_type="stuff", prompt=PROMPT)

    def ask(self, question):
        near_docs = self.db.similarity_search(question)
        result = self.chain({"input_documents": near_docs, "question": question})
        return result["output_text"]

    async def __call__(self, request: Request) -> List[str]:
        return self.ask(request.query_params["question"])

deployment = KnowledgeBase.bind()