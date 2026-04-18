from pathlib import Path
import chromadb
import json

extracted_texts_path = Path("data/json_files/extracted_texts.json")
embeddings_path = Path("data/json_files/embeddings.json")

# Function to load the ChromaDB collection
def load_collection():
    db_path = Path("data/vector_db")
    client = chromadb.PersistentClient(path=str(db_path))
    collection = client.get_or_create_collection("notes")
    return collection

# Main function to store embeddings and texts in the vector database
def store(subject_name):
    collection = load_collection()
    print("Collection name:", collection.name)

    # Check if extracted texts and embeddings exist before proceeding
    if not extracted_texts_path.exists() or extracted_texts_path.stat().st_size == 0:
        print("No extracted texts found. Run extractor first.")
        return
    
    if not embeddings_path.exists() or embeddings_path.stat().st_size == 0:
        print("No embeddings found. Run embed first.")
        return
    


    with open(extracted_texts_path, "r", encoding="utf-8") as f:
        extracted_texts = json.load(f)
    with open(embeddings_path, "r", encoding="utf-8") as f:
        embeddings = json.load(f)

    # Store each embedding and its corresponding text in the vector database
    for image_name in extracted_texts.keys():
        collection.upsert(
            ids=[f"{subject_name}_{image_name}"],
            embeddings=[embeddings[image_name]],
            documents=[extracted_texts[image_name]]
        )
        print(f"Stored: {image_name}")

    print(f"Total stored: {collection.count()}")

    # Cleanup: Clear JSON files and processed images after storing
    try:
        with open(extracted_texts_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        with open(embeddings_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        print("Cleared JSON files.")

        data_processed_images = Path("data/processed_images")
        if data_processed_images.exists():
            for file in data_processed_images.iterdir():
                if file.is_file():
                    file.unlink()
        print("Cleared processed images.")

    except Exception as e:
        print(f"Cleanup error: {e}")
        
    
    