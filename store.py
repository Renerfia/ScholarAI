import chromadb
import json
def load_collection():
    db_path = "data\\vector_db"
    client = chromadb.PersistentClient(path=db_path)

    collection = client.get_or_create_collection("notes")
    return collection

def store(subject_name):
    collection = load_collection()  
    print("Collection created!")
    print("Collection name:", collection.name)

    with open("embeddings.json", "r", encoding="utf-8") as f:
        embeddings = json.load(f)
    with open("extracted_texts.json", "r", encoding="utf-8") as f:
        extracted_texts = json.load(f)

    for image_name in extracted_texts.keys():
        collection.add(
            ids=[f"{subject_name}_{image_name}"],
            embeddings=[embeddings[image_name]],
            documents=[extracted_texts[image_name]]
        )
        print(f"Added {image_name} to collection.")
    print("All done!")
    print(f"Total stored: {collection.count()}")