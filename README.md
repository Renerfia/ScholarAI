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
```

**2.** Get your free Gemini API key from: https://aistudio.google.com/apikey

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

**6.** Use the **Extractor** first from the sidebar to process your PDFs before asking questions.

**7.** Done — start asking! ⚡

---

## 📁 Project Structure

```
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

*Built with obsession. Powered by Gemini. Forged in Python.*

⭐ Star this repo if it helped you

</div>
