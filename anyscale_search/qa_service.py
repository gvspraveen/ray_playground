from typing import List

from llama_index import (
    load_index_from_storage, 
    ServiceContext, 
    StorageContext, 
)
from models import (
    lang_embed_model, 
    hf_predictor,
    persist_dir
)

from ray import serve
from fastapi import FastAPI

# setup prompts - specific to OpenAssistant
from llama_index.prompts.prompts import SimpleInputPrompt

# Prompt for OpenAssistant.
# Taken from https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5
query_wrapper_prompt = SimpleInputPrompt(
    "<|prompter|>{query_str}<|endoftext|><|assistant|>")


app = FastAPI()

@serve.deployment(ray_actor_options={"num_gpus": 3})
@serve.ingress(app)
class QADeployment:
    def __init__(self):
        service_context = ServiceContext.from_defaults(llm_predictor=hf_predictor, embed_model=lang_embed_model)
        # Load the vector stores that were created earlier.
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        anyscale_docs_index = load_index_from_storage(storage_context, service_context=service_context)   

        # Define Query engine
        self.anyscale_docs_index = anyscale_docs_index.as_query_engine(similarity_top_k=5, service_context=service_context)
        
    def __query__(self, question: str):        
        return self.anyscale_docs_index.query(question)
    
    @app.post("/question")
    async def query(self, question: str) -> str:
        return str(self.__query__(question))
        

# Deploy the Ray Serve application.
deployment = QADeployment.bind()