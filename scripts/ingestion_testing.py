from app.ingestion.load import load_content
from app.ingestion.chunk import chunk_text
import os

file_path = "data\docs\BAJHLIP23020V012223.pdf"

text = load_content(file_path)
chunks = chunk_text(text)

print(f"Loaded {len(chunks)} chunks:")
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i+1} ---\n{chunk}")
