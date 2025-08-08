from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.json_converter import get_answer_from_json_string
from app.core.retriever import retrieve_chunks, build_index
from app.core.engine import evaluate_decision
from app.ingestion.load import load_content
from app.ingestion.chunk import chunk_text
from typing import List
from datetime import datetime
import os
import requests
from datetime import datetime
from fastapi import Body


app = FastAPI(
    title="CodingKrew AI",
    description="Policy Explainer AI is an intelligent, session-based insurance assistant that combines semantic document retrieval using FAISS with reasoning powered by Gemini 1.5 Flash. Users can upload multiple policy documents, ask natural language questions, and receive structured, justified decisions in real time. Each session is self-contained, allowing dynamic indexing, accurate clause referencing, and clean separation of uploaded contexts.",
    version="1.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    session_id : str

@app.get("/")
def root_main():
    return {"message": "Coding Krew is on its way"}
@app.get("/api/v1/")
def root():
    return {"message": "Coding Krew is on its way"}

def query_docs(session_id:str,questions:List[str]):
    answers = []
    try:
        for question in questions:
            relevant_chunks = retrieve_chunks(question,session_id, k=5)
            answer = evaluate_decision(question,session_id)
            answers.append(get_answer_from_json_string(answer))
        return {
            "answers": answers
        }
    except Exception as e:
        return {"error": str(e)}



@app.post("/api/v1/hackrx/run")
async def upload_docs(
    body: dict = Body(...)
):
    """
    Accepts raw JSON:
    {
        "pdf_url": "https://example.com/file.pdf"
    }
    """
    pdf_url = body.get("documents")
    questions = body.get("questions")
    if not pdf_url:
        return {"error": "pdf_url is required"}

    responses = []
    alltext_chunks = []
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    index_dir = f"session_{session_id}"

    try:
        # Download PDF
        r = requests.get(pdf_url)
        r.raise_for_status()

        # Derive filename
        filename = pdf_url.split("/")[-1]
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        # Save locally
        file_path = f"temp_uploads/{index_dir}/{filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(r.content)

        # Parse & chunk
        raw_text = load_content(file_path)
        text_chunks = chunk_text(raw_text)
        alltext_chunks.extend(text_chunks)

        responses.append({
            "url": pdf_url,
            "status": "downloaded, parsed, and added to combined index",
            "session_id": session_id
        })

        # Build index
        build_index(alltext_chunks, session_id, force_rebuild=True)

        return query_docs(session_id=session_id,questions=questions)

    except Exception as e:
        return {"error": str(e)}
