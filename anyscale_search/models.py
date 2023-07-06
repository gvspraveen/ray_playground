from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.llm_predictor import HuggingFaceLLMPredictor

from llama_index import (
    LangchainEmbedding,
)
# setup prompts - specific to OpenAssistant
from llama_index.prompts.prompts import SimpleInputPrompt

# Prompt for OpenAssistant.
# Taken from https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5
query_wrapper_prompt = SimpleInputPrompt(
    "<|prompter|>{query_str}<|endoftext|><|assistant|>")

hf_embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
            model_kwargs={"device": "cuda"},)
lang_embed_model = LangchainEmbedding(hf_embed_model)
hf_predictor = HuggingFaceLLMPredictor(
            query_wrapper_prompt=query_wrapper_prompt,
            tokenizer_name="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
            model_name="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
            device_map="auto",
        )

persist_dir="/mnt/user_storage"
