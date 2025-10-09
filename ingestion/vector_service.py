# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from vector_service import create_vector_db

class IngestRequest(BaseModel):
    texts: list[str]

app = FastAPI()

@app.post("/ingest")
def ingest(payload: IngestRequest):
    return create_vector_db(payload.texts)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
