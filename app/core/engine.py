import google.generativeai as genai
import yaml
import json
from app.core.retriever import retrieve_chunks

with open("config/config.yaml") as f:
    cfg = yaml.safe_load(f)

genai.configure(api_key=cfg["gemini_api_key"])

model = genai.GenerativeModel("gemini-1.5-flash")

COT = """
You are a claims evaluation assistant. You are provided with:
- A customer query
- Retrieved policy document clauses

Your job is to:
1. Identify the important fields from the query (e.g., age, procedure, location, policy duration).
2. Think step-by-step to determine if the policy covers this case.
3. Reference specific clauses to justify your reasoning.
4. Give a structured JSON response with:
    - decision ("approved" or "rejected")
    - amount (if any)
    - justification

---

Query:
{query}

Retrieved Clauses:
{clauses}

---

⚠️ DO NOT return markdown, explanations, or extra text.
✅ Just return valid JSON. No triple backticks.
"""

def evaluate_decision(query, session_id):
    retrieved_chunks = retrieve_chunks(query,session_id)
    clauses = "\n\n".join(retrieved_chunks)
    prompt = COT.format(query=query, clauses=clauses)
    response = model.generate_content(prompt)
    #raw_output = 
    return response.candidates[0].content.parts[0].text

    # try:
    #     parsed_output = json.loads(raw_output)
    #     return {
    #         "query": query,
    #         "response": parsed_output,
    #         "retrieved_clauses": retrieved_chunks
    #     }
    # except json.JSONDecodeError:
    #     return {
    #         "query": query,
    #         "response": {"error": "Invalid JSON response from Gemini", "raw": raw_output},
    #         "retrieved_clauses": retrieved_chunks
    #     }
    
    
    
#