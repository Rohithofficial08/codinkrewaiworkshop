from app.ingestion.load import load_content
from app.ingestion.chunk import chunk_text
from app.core.retriever import build_index

file_path = "data/docs/sample_policy.pdf"
text = load_content(file_path)
chunks = chunk_text(text)
build_index(chunks, force_rebuild=True)