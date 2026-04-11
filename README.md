# ⚡ AI PDF Review Assistant

```
   ___  _     ____  ____  _____     __   __  
  / _ \| |   |  _ \|  _ \| ____|   / /   \ \ 
 | | | | |   | |_) | |_) |  _|    / /     \ \
 | |_| | |___| __/|  _ <| |___   / /       \ \
  \__\_\_____|_|   |_| \_\_____|/_/  REVIEW  \_\
```

> *"Knowledge locked in pages... until now."*

---

## 🌸 What is this?

**AI PDF Review Assistant** is an intelligent document analysis system powered by Google Gemini and a custom RAG (Retrieval-Augmented Generation) pipeline. Feed it your PDFs — it reads them, understands them, and answers your questions like a brilliant study partner who never sleeps.

Ask in **Bengali or English**. Get answers with **full LaTeX math rendering**. It remembers the conversation. It finds exactly what you need.

---

## ⚔️ The Pipeline — How It Works

```
  [ Your PDF ]
       │
       ▼
  ┌─────────────────────────────┐
  │  PyMuPDF converts each      │
  │  page → image               │
  └────────────┬────────────────┘
               │
               ▼
  ┌─────────────────────────────┐
  │  Gemini Vision reads every  │
  │  image — Bengali, math,     │
  │  diagrams, handwriting      │
  └────────────┬────────────────┘
               │
               ▼
  ┌─────────────────────────────┐
  │  Gemini Embedding converts  │
  │  text → vectors (3072D)     │
  └────────────┬────────────────┘
               │
               ▼
  ┌─────────────────────────────┐
  │  ChromaDB stores vectors    │
  │  on disk permanently        │
  └────────────┬────────────────┘
               │
       [ You ask a question ]
               │
               ▼
  ┌─────────────────────────────┐
  │  Your question → embedded   │
  │  → ChromaDB finds closest   │
  │  matching pages             │
  └────────────┬────────────────┘
               │
               ▼
  ┌─────────────────────────────┐
  │  Gemini answers using only  │
  │  YOUR notes as context      │
  └─────────────────────────────┘
```

---

## 🚀 How to Use

**1.** Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
OPENROUTER_API_KEY=your_api_key_here
```

**2.** Get your free Gemini API key and Openrouter API key from: https://aistudio.google.com/apikey and https://openrouter.ai/workspaces/default/keys

**3.** Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**4.** Install all dependencies:
```bash
pip install -r requirements.txt
```

**5.** Launch the app:
```bash
streamlit run app.py
```
**6.**Before asking anything, insert your local pdf file's full path on the sidebar and click "Extract"

**7.** Done — start asking! ⚡

---

## 📁 Project Structure

```

When you click the "Extract" button the program will take every image of every pages in the pdf file and send them to the AI model.
This process works gradually.

Then the AI model reads them and generates description from every pages. Most likely what they includes. 

After that these text description converted into vector and stored in a vectordb in data folder(inside app local folder).

When you ask question, it turns your question into vector and finds several relevant matches in the database. It being stored as retrieved_text

Finally the program sends the retrieved text and the original question and also the history to the main AI model(Gemini Model). The model sees them answers accordingly.

ai-pdf-review-assistant/
│
├── app.py               # Streamlit UI
├── extract.py           # Image → text extraction via Gemini
├── embed.py             # Text → vector embeddings
├── store.py             # Store vectors in ChromaDB
├── query.py             # Question answering pipeline
│
├── data/
│   └── vector_db/       # ChromaDB persistent storage
│
├── extracted_texts.json
├── embeddings.json
├── .env                 # Your API key goes here
├── requirements.txt
└── README.md
```

---

## 🗡️ Tech Stack

```
Language      →  Python
UI            →  Streamlit
Vector DB     →  ChromaDB
PDF Parser    →  PyMuPDF (fitz)
AI Model      →  Google Gemini (vision + embedding + generation)
```

---

## 📜 License

```
Copyright 2026 Renerfia

Licensed under the Apache License, Version 2.0
```

---

<div align="center">

*Built with obsession. Powered by Gemini and Openrouter. Forged in Python.*

⭐ Star this repo if it helped you. It was made for educational purpose

</div>
