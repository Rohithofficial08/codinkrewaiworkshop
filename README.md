# CodingKrew AI - Bajaj Finserv Hackathon Submission

## 🚀 Overview

CodingKrew AI is a smart document reasoning system built for the **Bajaj Finserv Hackathon**. It allows users to upload one or more insurance policy documents and then ask natural language questions about them. The system uses **FAISS for semantic retrieval** and **Gemini 1.5 Flash for reasoning**, returning structured decisions in JSON format.

> ⚠️ Although I can't participate in the hackathon because my team isn't eligible, a project is still a project, and sarcasm is my coping mechanism. 😎

---

## 🎯 Problem Statement

In real-world insurance settings, understanding the clauses and conditions of policy documents is time-consuming and error-prone. This project solves that by:

* Parsing uploaded policy documents
* Semantically retrieving relevant clauses
* Generating smart, justified decisions

Problem Statement : [HackRx6.0](https://hackrx.in/#problem-statement)

---

## ✅ Features

* **Multi-file Upload**: Upload one or more `.pdf` or `.docx` files
* **Session-wise Indexing**: Each session gets its own FAISS index and metadata folder
* **Semantic Clause Search**: Questions retrieve the most relevant document chunks
* **Structured Decision Output**: Gemini responds with a JSON decision object
* **Streamlit Frontend**: Easy-to-use UI for upload and querying

---

## 🧠 Tech Stack

| Component     | Tech/Tool                       | Version                      |
| ------------- | ------------------------------- | ---------------------------- |
| Backend       | FastAPI                         | 0.110.0                      |
| Embedding     | SentenceTransformers (MiniLM)   | sentence-transformers==2.2.2 |
| Vector Search | FAISS                           | faiss-cpu==1.7.4             |
| LLM           | Gemini 1.5 Flash (Google AI)    | gemini-1.5-flash             |
| Frontend      | Streamlit                       | 1.33.0                       |
| Data Storage  | Session-wise folders in `/data` | -                            |

---

## 🧩 Version Breakdown

### ✅ Version 1 (V1)

* Single document upload
* Static FAISS index location
* Basic query interface with Gemini output

### 🔁 Version 2 (V2)

* Multi-document upload in one session
* Dynamic FAISS index creation (`session_<timestamp>`) for isolation
* Stored session ID used during querying
* Fully integrated frontend with upload → query loop

---

## 🗂️ Folder Structure

```
project/
├── app/
│   ├── core/
│   │   ├── engine.py        # Gemini prompting logic
│   │   ├── retriever.py     # FAISS index building & querying
│   │   └── embedder.py      # Text embeddings
│   ├── ingestion/
│   │   ├── load.py          # Load content from files
│   │   └── chunk.py         # Chunk raw text
│   └── main.py              # FastAPI app
├── ui/
│   └── app.py               # Streamlit interface
├── data/
│   └── session_<id>/index/  # Saved FAISS index + chunks
├── config/
│   └── config.yaml          # API keys and settings
```
Mermaid Diagram : [CodingKrewAI](CodingKrewAI.svg)
---

## 🔍 Sample Output

**Query**: *"Is cataract surgery covered?"*

**Output JSON**:

```json
{
  "decision": "rejected",
  "amount": null,
  "justification": "The provided policy clauses do not contain any information regarding coverage for cataract."
}
```

**Referenced Clauses**:

* Clause 1: "We cover maternity-related hospitalization expenses..."
* Clause 2: "Air ambulance service is provided in emergency..."

---

## 🚰 How It Works

1. **Upload Endpoint** (`/upload_docs`) parses and chunks all uploaded files
2. **Text is embedded** and stored in a FAISS index saved under `/data/session_<timestamp>/`
3. **Query Endpoint** (`/query`) takes user query + session ID, retrieves relevant clauses, and forwards them to Gemini
4. **Gemini generates** a JSON-based decision with reasoning and references

---

## 💡 Future Improvements

* Multi-user login & session history
* Highlighting relevant source lines in UI
* Exportable reports (PDF/JSON)
* Analytics dashboard for policy trends

---



