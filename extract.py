from dotenv import load_dotenv
import os
import openai
import base64
import json
import time

def extractor():
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY")

    client = openai.OpenAI(
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    model = "openrouter/auto"
    folder_path = "data\\processed_images"

    image_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")
    ]

    extracted_texts = {}

    for image_name in image_files:
        full_path = os.path.join(folder_path, image_name)
        print(full_path)

        with open(full_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract all the text from this image exactly as it appears."
                        }
                    ]
                }
            ]
        )

        extracted_texts[image_name] = response.choices[0].message.content
        print(f"Image: {image_name}")
        print(response.choices[0].message.content)
        print("---")
        time.sleep(1)

    print("Extraction complete.")

    with open("extracted_texts.json", "w", encoding="utf-8") as f:
        json.dump(extracted_texts, f, ensure_ascii=False, indent=2)

    print("Saved to extracted_texts.json")



    with open("extracted_texts.json", "w", encoding="utf-8") as f:
        json.dump(extracted_texts, f, ensure_ascii=False, indent=2)

    print("Saved to extracted_texts.json")
