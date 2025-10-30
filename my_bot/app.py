import streamlit as st
import os
from pathlib import Path
from rag_chain import build_rag_chain


# Import helper functions
from embeddings import sentence_transformer_embedding as get_sentence_transformer_embeddings
from vectorestore import load_faiss_vectorestore as load_faiss_from_path



st.set_page_config(page_title="MySQL → LangChain → FAISS — Query", layout="wide")


st.title("💬 Ask your database (read-only mode)")
st.markdown(
"This app uses a pre-built FAISS index to answer questions. Type your prompt below.\n\n"
"If the index or embeddings are missing, you’ll see a warning instead of automatic creation."
)


# Configuration
INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./faiss_index")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


# Try loading embeddings
try:
    embeddings = get_sentence_transformer_embeddings(model_name=EMBEDDING_MODEL)
except Exception as e:
    st.error(f"Failed to initialize embeddings: {e}")
    st.stop()


# Try loading FAISS index
index_folder = Path(INDEX_PATH)
if not index_folder.exists():
    st.warning(f"⚠️ FAISS index folder not found at: {INDEX_PATH}. Please build it first.")
    st.stop()


try:
    vectordb = load_faiss_from_path(INDEX_PATH, embeddings)
    st.success(f"✅ Loaded FAISS index from {INDEX_PATH}")
except Exception as e:
    st.error(f"❌ Failed to load FAISS index: {e}")
    st.stop()

#--------RetrivalQA------------------
# Build the RAG chain (LLM + Retriever)

# qa_chain = build_rag_chain(vectordb)
# st.info("🤖 LLM chain initialized successfully — ready for queries!")
#------------------------------------

#---------Retrival_chain-------------
from retrival_chain import to_pass_retriver,create_retrival_chain
retriver=to_pass_retriver(vectordb)
retrival_chain=create_retrival_chain(retriver)
#-------------------------------------

# Prompt input
prompt = st.text_input("Ask your question (e.g., 'Find employees in HR')")


if st.button("Search"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        try:
            #-----------without llm---------------
            # with st.spinner("Searching in the FAISS index..."):
            #     results = vectordb.similarity_search(prompt, k=5)
            #-------------------------------------

            #-----------RetrivalQA----------------
            # with st.spinner("Querying AI via RAG chain..."):
            #     response = qa_chain(prompt)
            #-------------------------------------

            #-----------Retrival Chain------------
            from retrival_chain import query_answer
            with st.spinner("Querying AI via RAG chain..."):
                response = query_answer(retrival_chain,prompt)


            # if not results:
            #     st.info("No results found for that query.")
            # else:
            #     st.markdown("---")
            #     st.subheader("Top results")
            # for i, r in enumerate(results, start=1):
            #     st.markdown(f"**Result {i}**")
            #     content = getattr(r, 'page_content', str(r))
            #     st.write(content)
            #     if hasattr(r, 'metadata') and r.metadata:
            #         st.caption(str(r.metadata))
            st.markdown("---")
            st.subheader("### 🧠 AI Answer")
            # st.write(response["result"])  (for RetrivalQA)
            st.write(response["answer"])

            #The Retrived Context lets the user see what pieces of text (chunks) from your vector database were used by the LLM to answer the query.
            
            #-------------RetrivalQA----------------
            # st.markdown("---")
            # st.subheader("### 📄 Retrieved Context")
            # for i, doc in enumerate(response["source_documents"], start=1):
            #     st.markdown(f"**Source {i}:**")
            #     st.write(doc.page_content[:300] + "...")
            
            #-------------Retrival Chain-------------
            st.markdown("---")
            st.markdown("### 📄 Retrieved Context")
            for i, doc in enumerate(response["context"], start=1):
                st.write(f"**Source {i}:** {doc.page_content[:300]}...")

        except Exception as e:
            st.exception(e)


# Footer
st.markdown("---")
st.caption(
"Read-only mode: This app only queries an existing FAISS index.\n"
"To rebuild or update the index, use your backend pipeline or CLI tools outside Streamlit."
)