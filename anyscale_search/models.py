from langchain.embeddings import HuggingFaceEmbeddings

hf_embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
            model_kwargs={"device": "cuda"},)
persist_dir="/mnt/user_storage"
