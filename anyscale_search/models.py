from langchain.embeddings import HuggingFaceEmbeddings

# Prompt for OpenAssistant.
# Taken from https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5
# query_wrapper_prompt = SimpleInputPrompt(
#     "<|prompter|>{query_str}<|endoftext|><|assistant|>")

hf_embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
            model_kwargs={"device": "cuda"},)
persist_dir="/mnt/user_storage"
