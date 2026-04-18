# This module handles querying the vector database and generating responses using AI models

# Import necessary libraries
import google.genai as genai
import chromadb
import os 
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
from pathlib import Path

# Define the main query function
def query(question, history):
    # Load API keys from environment variables
    API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Initialize ChromaDB client for vector database
    client_db = chromadb.PersistentClient(path=str(Path("data") / "vector_db"))
    # Get or create the collection for notes
    collection = client_db.get_or_create_collection("notes")
    
    # Initialize Gemini AI client
    client_ai = genai.Client(api_key=API_KEY)
    # Initialize Groq client for LLM
    groq_client = Groq(api_key=GROQ_API_KEY)
    
    # Translate the question to Bengali using Groq
    translation_response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": f"Translate this to proper Bengali script only, no explanation: {question}"
        }
    ],
        max_tokens=200
    )
    
    # Extract the translated question
    translated_question = translation_response.choices[0].message.content

    # Define the embedding model
    embedding_model = "gemini-embedding-001"
    # Generate embedding for the translated question
    question_embedding = client_ai.models.embed_content(
        model=embedding_model,
        contents=translated_question
    )

    # Extract the embedding values
    embedded_question = question_embedding.embeddings[0].values

    # Determine number of results to retrieve
    n_results = min(5, collection.count())
    # Query the vector database for similar documents
    query_results = collection.query(
        query_embeddings=[embedded_question],
        n_results=n_results
    )

    # Check if any documents were retrieved
    if not query_results['documents'][0]:
        # No documents found
        retrieved_texts = "No relevant notes found."
    # If documents found, join them
    else:
        # Join the retrieved documents
        retrieved_texts = "\n\n".join(query_results['documents'][0])
        # Truncate to fit within token limits
        retrieved_texts = retrieved_texts[:10000]  # Truncate to fit within token limits
    
    # Try to generate response using Groq
    try:
        # Construct the prompt for the LLM
        prompt = f"""
            You are an assistant that can only answer from the notes provided below.

            Important instructions:
            - Only say what is in the notes, do not make anything up
            - If the notes contain questions, give them exactly as they appear
            - If the answer is not in the notes, just say "This information is not in the notes"
            - Always answer in the same language the user asked in (Bengali or English)
            - Write math equations in LaTeX format

            Notes:
            {retrieved_texts}

            Conversation History:
            {history}

            Question: {question}

            Remember: Only answer from the notes above, nothing else.
            """
        # Generate the final response
        final_response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )
        
        # Return the response content
        return final_response.choices[0].message.content
    
    # Handle any exceptions
    except Exception as e:
        # Return error message
        return f"Error: {str(e)}"