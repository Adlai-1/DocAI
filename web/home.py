import os, sys
import hashlib
import streamlit as st
sys.path.append(os.path.abspath(os.path.dirname("rag_model")))
from rag_model.model import call_rag
from rag_model.vectorize import embed_and_save

def get_file_hash(file):
    """Compute the hash of the uploaded file."""
    file.seek(0)  # Ensure the file pointer is at the start
    file_hash = hashlib.md5(file.read()).hexdigest()
    file.seek(0)  # Reset the file pointer after reading
    return file_hash

st.title("DocAI")
st.markdown("""
An AI assistant that is able to glean valuable insight from your PDF files 
without doing it yourself!
""")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# file upload...
with st.sidebar:
    file = st.file_uploader(label="File", type=["pdf"], label_visibility="hidden", key="pdfs")

    if file:
        file_hash = get_file_hash(file)
        
        if "file_hash" not in st.session_state or st.session_state.file_hash != file_hash:
            with st.spinner("Embedding document..."):
                resp = embed_and_save(file)
            st.session_state.embedded_file = resp
            st.session_state.file_hash = file_hash
            st.toast("File successfully embedded!")

# conversations...
if text := st.chat_input("Message MakariosAI"):
    st.chat_message("user").markdown(text)
    st.session_state.messages.append({"role": "user", "content": text})
    try:
        resp = call_rag(text, st.session_state.messages)
    
        with st.chat_message("ai"):
            st.markdown(resp)
            st.session_state.messages.append({"role": "ai", "content": resp})
    
    except Exception as error:
        with st.chat_message("ai"):
            text = "Unable to generate a response, try again!"
            st.markdown(text)
            st.session_state.messages.append({"role": "ai", "content": text})
            print(error)