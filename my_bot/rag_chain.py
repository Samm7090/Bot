from langchain.chains import RetrievalQA
from llm import get_llm

def build_rag_chain(vectordb, model_name="mistralai/mistral-7b-instruct"):

    """
    Build a Retrieval-Augmented Generation (RAG) chain using FAISS + LLM.
    """
    llm = get_llm(model_name=model_name)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff",
        return_source_documents=True
    )
    return qa_chain