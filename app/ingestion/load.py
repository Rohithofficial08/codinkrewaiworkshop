import os
import fitz #PyMuPDF
import docx

def load_content(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only .pdf and .docx are supported.")

def extract_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

#print(load_content("data\\docs\\EDLHLGA23009V012223.pdf"))
