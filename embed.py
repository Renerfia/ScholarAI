
import google.genai as genai
from dotenv import load_dotenv
import os
load_dotenv()
from pathlib import Path 
import json
import time


def embed():
    
    json_path = Path("data/json_files")
    extracted_texts_file = json_path / "extracted_texts.json"
    embeddings_file = json_path / "embeddings.json"
    API_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=API_KEY)
    

    with open(extracted_texts_file, "r", encoding="utf-8") as f:
        extracted_texts = json.load(f)

    embeddings = {} # Dictionary to store embeddings for each image

    for image_name, text in extracted_texts.items():
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        
        embeddings[image_name] = response.embeddings[0].values
        print(f"Embedded: {image_name}")
        time.sleep(4)
    
    #save all embeddings to json file once
    with open(embeddings_file, "w", encoding="utf-8") as f:
        json.dump(
            {name: list(vector) for name, vector in embeddings.items()}, #converts embeddings to lists for json serialization
            f
        )
        print(f"Saved all embeddings to embeddings.json")

    print("Done!")
    print(f"Total embedded: {len(embeddings)}")



    print("Embeddings saved!")
    