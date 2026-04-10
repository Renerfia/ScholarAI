from dotenv import load_dotenv
import os
import google.genai as genai
import json



def extractor():
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")

    folder_path = "data\\processed_images"
    client = genai.Client(api_key=API_KEY)
    image_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")
    ]

    extracted_texts = {}

    for image_name in image_files:
        full_path = os.path.join(folder_path, image_name)
        print(full_path)





        with open(full_path, "rb") as f:
            image_data = f.read()

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
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
                            "text": "Extract all the text from this image exactly as it appears."
                        }
                    ]
                }
            ]
        )
        extracted_texts[image_name] = response.text
        print(f"Image: {image_name}")
        print(response.text)
        print("---")
    print("Extraction is complete.")



    with open("extracted_texts.json", "w", encoding="utf-8") as f:
        json.dump(extracted_texts, f, ensure_ascii=False, indent=2)

    print("Saved to extracted_texts.json")
