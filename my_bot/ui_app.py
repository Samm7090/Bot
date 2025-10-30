import streamlit as st
import os
from pathlib import Path
from rag_chain import build_rag_chain

# Import helper functions
from embeddings import sentence_transformer_embedding as get_sentence_transformer_embeddings
from vectorestore import load_faiss_vectorestore as load_faiss_from_path

st.set_page_config(page_title="MySQL → LangChain → FAISS — Query", layout="wide")

st.title("💬 Welcome to HR Bot")
st.write("👋 Hi, I'm Siri! How can I help you today?")
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

# --------Retrival_chain-------------
from retrival_chain import to_pass_retriver, create_retrival_chain
retriver = to_pass_retriver(vectordb)
retrival_chain = create_retrival_chain(retriver)
# -----------------------------------

# ---------------------------
# Session state init
# ---------------------------
if "history" not in st.session_state:
    # history is list of dicts: {"role": "user"|"assistant", "text": "..."}
    st.session_state.history = []


# ---------------------------
# Sidebar: New chat, Search chat
# ---------------------------
with st.sidebar:
    st.header("💬 Chat controls")

    # New chat button: clears conversation history
    if st.button("🔄 New chat"):
        st.session_state.history = []
        st.success("Started a new chat (history cleared).")

    st.markdown("---")
    st.subheader("Search chat")
    search_query = st.text_input("Search messages", placeholder="Type to filter history...", key="sidebar_search")

    st.markdown("---")
    st.caption("Read-only: this UI queries an existing FAISS index. Build/refresh index outside Streamlit.")

    st.markdown("### History preview")
    if not st.session_state.history:
        st.write("_No conversation yet._")
    else:
        # If there's a search query, filter messages; otherwise show latest 10 messages
        def message_matches(q, msg):
            return q.lower() in msg.get("text", "").lower()

        if search_query and search_query.strip():
            matched = [m for m in st.session_state.history if message_matches(search_query, m)]
            if not matched:
                st.info("No messages matched your search.")
            else:
                for m in matched:
                    role = m.get("role", "user")
                    text = m.get("text", "")
                    if role == "user":
                        st.markdown(f"**You:** {text}")
                    else:
                        st.markdown(f"**AI:** {text}")
                    st.divider()
        else:
            # show last 10 messages (newest first)
            snippet = st.session_state.history[-10:]
            for m in snippet:
                role = m.get("role", "user")
                text = m.get("text", "")
                if role == "user":
                    st.markdown(f"**You:** {text}")
                else:
                    st.markdown(f"**AI:** {text}")
                st.divider()


# Prompt input
prompt = st.text_input("Ask your question (e.g., 'Find employees in HR')")

if st.button("Search"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        try:
            # Append user message to history
            st.session_state.history.append({"role": "user", "text": prompt})

            #-----------Retrival Chain------------
            from retrival_chain import query_answer
            with st.spinner("Querying AI via RAG chain..."):
                response = query_answer(retrival_chain, prompt)

            st.markdown("---")
            st.subheader("### 🧠 AI Answer")

            assistant_text = ""
            try:
                assistant_text = response["answer"]
            except Exception:
                if isinstance(response, dict):
                    assistant_text = response.get("result") or response.get("output") or str(response)
                else:
                    assistant_text = str(response)

            st.write(assistant_text)

            # Append assistant message to history
            st.session_state.history.append({"role": "assistant", "text": assistant_text})

            #The Retrieved Context lets the user see what pieces of text (chunks) from your vector database were used by the LLM to answer the query.
            st.markdown("---")
            st.markdown("### 📄 Retrieved Context")
            context_items = response.get("context") if isinstance(response, dict) else None
            if context_items:
                for i, doc in enumerate(context_items, start=1):
                    st.write(f"**Source {i}:** {doc.page_content[:300]}...")
            else:
                st.write("_No retrieved context available._")

        except Exception as e:
            st.exception(e)

# Footer
st.markdown("---")
st.caption(
    "Read-only mode: this app only queries an existing FAISS index.\n"
    "To rebuild or update the index, use your backend pipeline or CLI tools outside Streamlit."
)
