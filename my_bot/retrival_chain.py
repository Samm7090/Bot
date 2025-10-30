from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

# Define a custom prompt template

prompt=ChatPromptTemplate.from_template("""
Answer the following questions based only on the provided context.
Think step by step before provided a detailed answer.
<context>
{context}
</context>

Question: {input}
""")

#---------------------
"Create document chain first from create stuff document chain"
#---------------------
from langchain.chains.combine_documents import create_stuff_documents_chain

llm=get_llm()
documnet_chain=create_stuff_documents_chain(llm=llm,prompt=prompt)

#---------------------
"Create retriver and we will call rectiver in app.py instead of call vectoredb in this file"
#---------------------
def to_pass_retriver(vectordb):
    retriver=vectordb.as_retriever()
    return retriver

#---------------------
"Create a retrival chain using the document chain and retriver"
#---------------------
from langchain.chains import create_retrieval_chain
def create_retrival_chain(retriver):
    retrival_chain=create_retrieval_chain(retriver,documnet_chain)
    return retrival_chain

#---------------------
"function to invoke query"
#---------------------
def query_answer(retrival_chain,prompt:str):
    response=retrival_chain.invoke({"input":prompt})
    return response