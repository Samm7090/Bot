from langchain_community.vectorstores import FAISS
import os

def build_faiss_vectorstore(docs: list,embeddings, save_path: str = None):
    vectordb=FAISS.from_documents(docs, embeddings)

    if save_path:
        os.makedirs(save_path, exist_ok=True)
        vectordb.save_local(save_path)
    return vectordb

# #----------------------------------------------
# save_path specifies where to store the FAISS index on disk.
# Saving the index lets you:
# Reuse it later without rebuilding from scratch.
# Load it in another session using load_faiss_from_path().
# Handle large datasets where building the index can be time-consuming.
#----------------------------------------------

def load_faiss_vectorestore(Load_path: str, embeddings,allow_dangerous_deserialization: bool = True):
    vectordb = FAISS.load_local(Load_path, embeddings, allow_dangerous_deserialization=allow_dangerous_deserialization)
    return vectordb
    