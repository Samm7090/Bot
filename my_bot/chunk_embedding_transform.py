from connect_load_data import docs
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.embeddings import SentenceTransformerEmbeddings

# Converted into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
document=text_splitter.split_documents(docs)

print(f"✅ Split into {len(document)} chunks.")
print(document[0])  

# Embeddings using SentenceTransformer
embeddings=SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

# Create FAISS vector store
vectordb=FAISS.from_documents(document,embeddings)

# Test similarity search
query="Find employees in the HR department."
result=vectordb.similarity_search(query)
print(result[0].page_content)