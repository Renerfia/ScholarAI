import streamlit as st
from query import query
from extract import extractor
from pdf_to_image import pdf_to_image
from embed import embed
from store import store, load_collection

st.title("Study Notes Tutor")
if "history" not in st.session_state:
    st.session_state["history"] = []

question = st.text_input("Ask a question about your study notes:")
if st.button("Ask"):
    if question.strip() != "":
        history = ""
        for item in st.session_state["history"][-5:]: #include last 5 interactions in the history
            history += f"User: {item['question']}\nAnswer: {item['answer']}\n\n"
        with st.spinner("Thinking..."):
            answer = query(question, history)
        st.session_state["history"].append({
            "question": question,
            "answer": answer
        })
for item in reversed(st.session_state["history"]):
    st.write("**You:**", item["question"])
    st.write("**Answer:**")
    st.write(item["answer"])
    st.write("---")


#sidebar
with st.sidebar:
    st.title("Train AI from your PDF Notes")
    folder_path = st.text_input("Enter the path to your PDF file:") #streamlit doesn't support folder upload, so we will use file uploader for now. User can upload one pdf at a time.
    subject = st.text_input("Enter the subject of your notes (e.g. Math, Physics):(It's crucial!)")
    if st.button("Extract"):
        if folder_path is not None:
            with st.spinner("Extracting text from pdf..."):
                pdf_to_image(folder_path) #convert pdf to images
            with st.spinner("Extracting text from images..."):
                extractor() #extract text from images
            with st.spinner("Embedding text into vector database..."):
                embed() #embed the extracted text into vector database
            with st.spinner("Storing embedded vectors in chromadb..."):
                store(subject) #store the embedded vectors in chromadb

            st.success("Extraction complete! You can now ask questions about your notes.")


