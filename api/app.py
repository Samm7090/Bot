from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

#Api
app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

# OpenAI 
# add_routes(
#     app,
#     ChatOpenAI(),
#     path="/openai"
# )

# model=ChatOpenAI()
# prompt1=ChatPromptTemplate.from_template("Write me the poem on{topic} with 100 words")

# add_routes(
#     app,
#     prompt1|model,
#     path="/poem"
# )

# Open Source
#ollama
llm=Ollama(model="gemma:latest")

prompt2=ChatPromptTemplate.from_template("write me essay on {topic} with 100 words")

add_routes(
    app,
    prompt2| llm,
    path="/essay"
)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)