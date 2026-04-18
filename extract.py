import google.genai as genai
import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def extractor():
    
    model = "gemini-2.5-flash-lite"

    folder_path = Path("data/processed_images")

    image_files = [
        f for f in folder_path.iterdir()
        if f.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]

    # load existing progress
    if Path("extracted_texts.json").exists():
        with open("extracted_texts.json", "r", encoding="utf-8") as f:
            extracted_texts = json.load(f)
        print(f"Resuming: {len(extracted_texts)} images already done")
    else:
        extracted_texts = {}

    for image_path in image_files:

        if image_path.name in extracted_texts:
            print(f"Skipping {image_path.name} (already done)")
            continue

        print(f"Processing: {image_path.name}")

        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            API_KEY = os.getenv("GEMINI_API_KEY")  # ensure we're using the primary key for new requests
            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model=model,
                contents=[
                    {
                        "parts": [
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_data
                                }
                            },
                            {
                                "text": "Extract all text from this image exactly as it appears. It can be Bengali, English or math equations."
                            }
                        ]
                    }
                ]
            )

            extracted_texts[image_path.name] = response.text
            print(f"Done: {image_path.name}")

            # autosave after every image
            with open("extracted_texts.json", "w", encoding="utf-8") as f:
                json.dump(extracted_texts, f, ensure_ascii=False, indent=2)

        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                print("Rate limited! Waiting 60 seconds...")
                time.sleep(60)
                API_KEY = os.getenv("GEMINI_API_KEY_2")  # switch to backup key
                client = genai.Client(api_key=API_KEY)
                print("Switched to backup API key, resuming...")
            elif "400" in error_str:
                print(f"Bad request for {image_path.name} — skipping")
            elif "401" in error_str:
                print("Invalid API key!")
                break
            else:
                print(f"Error: {error_str}")

        finally:
            time.sleep(5)

    print(f"Extraction complete! Total: {len(extracted_texts)}")

if __name__ == "__main__":
    extractor()