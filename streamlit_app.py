import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG QnA App", layout="centered")

st.title("📄 RAG-based Document QnA")
st.write("Upload PDF or TXT files and ask questions using Ollama + FAISS")


# Upload Section
st.header("📤 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

if uploaded_file is not None:
    if st.button("Upload & Index"):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue())
        }

        with st.spinner("Uploading and indexing document..."):
            response = requests.post(
                f"{FASTAPI_URL}/upload",
                files=files
            )

        if response.status_code == 200:
            st.success("Document uploaded and indexed successfully!")
        else:
            st.error("Failed to upload document")

# QnA Section
st.header("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking... "):
            response = requests.post(
                f"{FASTAPI_URL}/ask",
                params={"question": question}
            )

        if response.status_code == 200:
            data = response.json()

            st.subheader("💡 Answer")
            st.write(data["answer"])

            st.subheader("📊 Similarity Scores")
            st.write(data["similarity_scores"])
        else:
            st.error("Error getting answer")
