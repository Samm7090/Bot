from db_conn import get_sqlalchemy_engine
from loader import load_sql_data
from chunk_splitter import split_load_data
from embeddings import sentence_transformer_embedding
from vectorestore import build_faiss_vectorstore

def load_chunk_embed_build(query: str="Select * from employees",engine=None, model_name: str='all-MiniLM-L6-v2', chunk_size: int=1000, chunk_overlap: int=200, save_path: str= None):
    if engine is None:
        engine = get_sqlalchemy_engine()

    docs = load_sql_data(query, engine)
    chunk = split_load_data(docs,chunk_size, chunk_overlap)
    embedding = sentence_transformer_embedding(model_name=model_name)
    vectordb = build_faiss_vectorstore(chunk, embedding, save_path="faiss_index")
    return vectordb

if __name__ == "__main__":

    engine = get_sqlalchemy_engine()

    vectordb = load_chunk_embed_build(engine=engine, save_path="./faiss_index")

    results = vectordb.similarity_search("Find employee in HR department", k=2)

    if results:
        print(results[0].page_content)
    else:
        print("No results returned.")