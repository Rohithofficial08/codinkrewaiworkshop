import streamlit as st
import requests
import json
from datetime import datetime
import os

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CodingKrewAI", layout="wide")
st.title("🧠 Coding Krew AI - Your Own Policy Explainer")
st.markdown("Upload your policy documents and ask any question about them.")

# Upload section
st.subheader("📤 Upload Document")
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Uploading and indexing..."):
       response = requests.post(f"{API_URL}/upload_docs",files=[("uploaded_files", (uploaded_file.name, uploaded_file.getvalue()))]  # ✅ Send as list of tuples
)

    if response.status_code == 200:
        data = response.json()
        #st.write("📥 Raw Response:", data)
        st.success(data.get("message", "Upload succeeded!"))

        session_id = data.get("session_id")
        st.session_state["session_id"] = session_id
        st.info(f"🔑 Session ID saved: `{session_id}`")
    else:
        st.error(response.json().get("error", "Upload failed."))

st.markdown("---")

# Query section
st.subheader("🔍 Ask a Question")
query = st.text_input("Enter your query in plain English")

if st.button("Submit Query") and query:
    session_id = st.session_state.get("session_id")

    if not session_id:
        st.error("❗ No documents uploaded yet. Please upload first.")
    else:
        with st.spinner("Thinking with Gemini..."):
            response = requests.post(
                f"{API_URL}/query",
                json={"query": query, "session_id": session_id}
            )

        if response.status_code == 200:
            result = response.json()

            if "error" in result:
                st.error("❌ Error: " + result["error"])
            else:
                st.success(" AI Answer:")
                st.markdown(f"**Q:** {result.get('query')}")

                # JSON answer
                response_text = result.get("response", "")
                try:
                    parsed = json.loads(response_text)
                    st.json(parsed)
                except json.JSONDecodeError:
                    st.markdown("**A (raw):**")
                    st.code(response_text, language="json")

                # Clauses
                st.markdown("### 🔎 Referenced Clauses:")
                for i, clause in enumerate(result.get("retrieved_clauses", [])):
                    st.markdown(f"**Clause {i+1}:**")
                    st.code(clause, language="text")
        else:
            try:
                st.error(" Server Error: " + response.json().get("error", "Unknown error"))
            except:
                st.error(" Unknown Error occurred.")

st.markdown(
    """
    <div style='position: fixed; bottom: 10px; right: 15px; color: #888; font-size: 0.75em;'>
         Trinetra AI
    </div>
    """,
    unsafe_allow_html=True
)

