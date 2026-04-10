

def embed():
    import google.genai as genai
    from dotenv import load_dotenv
    import os
    load_dotenv()

    import google.genai as genai
    import json
    import time
    API_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=API_KEY)

    with open("extracted_texts.json", "r", encoding="utf-8") as f:
        extracted_texts = json.load(f)

    embeddings = {} # Dictionary to store embeddings for each image

    for image_name, text in extracted_texts.items():
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        
        embeddings[image_name] = response.embeddings[0].values
        print(f"Embedded: {image_name}")
        time.sleep(1)
        #save the embeddings to a json file
        with open("embeddings.json", "w", encoding="utf-8") as f:
            json.dump(
                {name: list(vector) for name, vector in embeddings.items()}, #converts embeddings to lists for json serialization
                f
            )
            print(f"Saved embedding for {image_name} to embeddings.json")

    print("Done!")
    print(f"Total embedded: {len(embeddings)}")



    print("Embeddings saved!")