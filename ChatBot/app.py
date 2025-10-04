# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain_core.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2="true"
LANGSMITH_API_KEY=os.getenv("LANGSMITH_API_KEY")


## Prompt template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("human","Question: {question}")
    ]
)

## Streamlit framework

st.title("Langchain Demo with OPENAI API")
input_text=st.text_input("Search the topic you want")


## Ollama LLAma2 LLM

llm=Ollama(model="gemma:latest")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser


if input_text:
    st.write(chain.invoke({'question':input_text}))

