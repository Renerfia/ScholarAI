import google.genai as genai
import chromadb
import os 
from dotenv import load_dotenv
load_dotenv()

def query(question,history):
    API_KEY = os.getenv("GEMINI_API_KEY")
    client_db = chromadb.PersistentClient(path="data\\vector_db")
    collection = client_db.get_or_create_collection("notes")
    model = "gemini-2.5-flash-lite"

    client_ai = genai.Client(api_key=API_KEY)

    #question = "নোটগুলো থেকে আমাকে কিছু গুরুত্বপূর্ণ অনুশীলন দিন।" #test by asking question

    embedding_model ="gemini-embedding-001"
    question_embedding = client_ai.models.embed_content(
        model=embedding_model,
        contents=question) #it returns a vector

    embedded_question = question_embedding.embeddings[0].values

    query_results = collection.query(
        query_embeddings=[embedded_question],
        n_results=10
    )

    print(query_results)

    retrieved_texts =f"\n\n".join(query_results['documents'][0]) #retrieves the documents from the query results
    try:
        final_response = client_ai.models.generate_content(
            model=model,
            contents=f"""
                Answer the question based on the notes below.
                your main work is to find question in the notes and send to the user if asked.
                also solve them if asked.
                Format any math equations in LaTeX.
                Always speak in Bangla

                Notes:{retrieved_texts}

                History of previous questions and answers:
                {history}

                User Question: {question}
            """
        )
        return final_response.text

    
    except Exception as e:
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            import time
            time.sleep(10) #wait for 5 seconds before retrying
