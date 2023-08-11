from langchain.embeddings import HuggingFaceEmbeddings


persist_dir="/mnt/user_storage"

model_name = "sentence-transformers/all-MiniLM-L6-v2"
hf_embed_model = HuggingFaceEmbeddings(model_name=model_name, 
            model_kwargs={"device": "cuda"},)
