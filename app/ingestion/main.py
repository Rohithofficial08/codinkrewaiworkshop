from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.retriever import retrieve_chunks, build_index
from app.core.engine import evaluate_decision
from app.ingestion.load import load_content
from app.ingestion.chunk import chunk_text
from typing import List
from datetime import datetime
import os

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
def root():
    return {"message": "Coding Krew is on its way"}

@app.post("/query")
def query_docs(request: QueryRequest):
    session_id = request.session_id
    try:
        relevant_chunks = retrieve_chunks(request.query,session_id, k=5)
        answer = evaluate_decision(request.query,session_id)
        print("Query received:", request.query)
        print("Chunks retrieved:", relevant_chunks)
        print("Answer returned:", answer)
        return {
            "query": request.query,
            "response": answer,
            "retrieved_clauses": relevant_chunks
        }
    except Exception as e:
        return {"error": str(e)}



@app.post("/upload_docs")
async def upload_docs(uploaded_files: List[UploadFile] = File(...)):
    responses = []
    alltext_chunks = []
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    index_dir = f"session_{session_id}"

    try:
        for uploaded_file in uploaded_files:
            contents = await uploaded_file.read()
            file_path = f"temp_uploads/{index_dir}/{uploaded_file.filename}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(contents)

            raw_text = load_content(file_path)
            text_chunks = chunk_text(raw_text)
            alltext_chunks.extend(text_chunks)

            responses.append({
                "filename": uploaded_file.filename,
                "status": "parsed and added to combined index" ,
                "session_id": session_id 
            })

        build_index(alltext_chunks, session_id, force_rebuild=True)

        return {
            "status": "success",
            "indexed_files": responses,
            "session_id": session_id ,
            "message": "All uploaded documents parsed and indexed into a single index."
        }

    except Exception as e:
        return {"error": str(e)}

