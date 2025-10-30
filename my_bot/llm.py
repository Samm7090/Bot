from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


def get_llm(model_name: str="mistralai/mistral-small-3.1-24b-instruct:free"):
    
    llm = ChatOpenAI(
    model=model_name,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    temperature=0.7)

    return llm