from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
# from langchain_community.llms import Ollama
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import httpx
from fastapi.responses import PlainTextResponse, JSONResponse




load_dotenv()

# Ensure LangChain/OpenAI client talks to OpenRouter:
# os.environ.setdefault("OPENAI_API_BASE")


OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# Api
app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)
#---------
# OpenAI 
# add_routes(
#     app,
#     ChatOpenAI(),
#     path="/openai"
# )


prompt1=ChatPromptTemplate.from_template("Write me the essay on{topic} with 100 words")

llm = ChatOpenAI(
    model="mistralai/mistral-small-3.1-24b-instruct:free",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

add_routes(
    app,
    prompt1|llm,
    path="/essay"
)

#-------------------
# Open Source
# ollama
# llm=Ollama(model="gemma:latest")

# prompt2=ChatPromptTemplate.from_template("write me essay on {topic} with 100 words")

# add_routes(
#     app,
#     prompt2| llm,
#     path="/essay"
# )
# -------------------

# --- NEW: Plain text wrapper (Ollama-style output) ---
@app.post("/essay/plain")
async def essay_plain(request: Request):
    """Return only plain essay text."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://127.0.0.1:8000/essay/invoke", json=body, timeout=60)

    try:
        payload = resp.json()
    except Exception:
        return PlainTextResponse(resp.text, status_code=resp.status_code)

    # Robust extraction
    essay = None
    if "output" in payload and "content" in payload["output"]:
        essay = payload["output"]["content"]

    if essay:
        return PlainTextResponse(essay, status_code=200)
    else:
        # fallback if content is missing
        return JSONResponse(payload, status_code=resp.status_code)
