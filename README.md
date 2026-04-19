# ⚡ ScholarAI - Your Personal Study Companion

```
   ___     __  ___  __   __  _____ _   _ ___     __   __  
  / _ \   / / / _ \|  \ /  ||_ _|| \ / / __|   / /   \ \ 
 | | | | / / | | | ||  V  /   | | |  V  | (__   / /     \ \
 | |_| |/ / _| |_| || | | |   | | | |_| |/__) / /       \ \
  \___//_/ (_)\__\_\|_| |_|   |_| |_| |_|____/_/  TUTORS  \_\
```

> *"Your study notes deserve a brilliant tutor — now they have one."*

---

## 🌸 What is ScholarAI?

**ScholarAI** is an intelligent **Study Notes Tutor** powered by Google Gemini and a custom RAG (Retrieval-Augmented Generation) pipeline. Upload your PDF notes, and it becomes your personal tutor — understanding your handwriting, diagrams, math, and questions in **Bengali or English**.

### Key Features

✅ **Upload PDFs** — Upload your study notes (supports password-protected PDFs)  
✅ **Subject Organization** — Organize notes by subject for better retrieval  
✅ **Intelligent Extraction** — AI extracts text from images, handwriting, math, diagrams  
✅ **Conversation Memory** — Remembers the last 3 interactions for better context  
✅ **Bengali Support** — Asks or answers in Bengali; automatic translation  
✅ **Vector Search** — Smart semantic search finds the most relevant pages  
✅ **RAG Pipeline** — Answers based only on your notes (no hallucinations)  

---

## 🏗️ How It Works — The RAG Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTRACTION PHASE                         │
└─────────────────────────────────────────────────────────────┘

[ Your PDF ]
     │
     ▼
┌──────────────────────────┐
│ PyMuPDF: PDF → Images    │  
│ (one image per page)     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Gemma LLM: Image → Text  │  
│ (extract everything)     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Save extracted_texts.json│
└──────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    EMBEDDING PHASE                          │
└─────────────────────────────────────────────────────────────┘

[ Extracted Text ]
     │
     ▼
┌──────────────────────────┐
│ Gemini Embedding Model   │  
│ (text → 3072D vectors)   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Save embeddings.json     │
└──────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    STORAGE PHASE                            │
└─────────────────────────────────────────────────────────────┘

[ Vectors + Text ]
     │
     ▼
┌──────────────────────────────────────────┐
│ ChromaDB (persistent storage on disk)    │  
│ Organized by subject                     │
└────────────┬─────────────────────────────┘
             │
             └─→ data/vector_db/

┌─────────────────────────────────────────────────────────────┐
│                    QUERY PHASE (You Ask)                    │
└─────────────────────────────────────────────────────────────┘

[ Your Question ]
     │
     ▼
┌──────────────────────────┐
│ Groq LLM: Translate to   │  
│ Bengali (if needed)      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Gemini: Embed question   │  
│ (same 3072D space)       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ ChromaDB: Vector search  │  
│ (find top 5 matches)     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│ Gemini: Generate answer using:           │  
│ • Retrieved page content                 │
│ • Your original question                 │
│ • Conversation history (last 3)          │
└──────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key ([get free key](https://aistudio.google.com/apikey))
- Groq API key ([get free key](https://console.groq.com/keys))

### Step 1: Clone & Setup
```bash
cd /path/to/ScholarAI
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### Step 2: Create `.env` file
```env
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Launch
```bash
streamlit run app.py
```

### Step 5: Use ScholarAI
1. **Sidebar**: Enter full path to your PDF file
2. **Sidebar**: Enter subject name (e.g., "Math", "Physics", "Bengali")
3. **Sidebar** (optional): Check "password authentication" if PDF is encrypted
4. **Click "Extract"** — AI will extract text from all pages
5. **Main Area**: Start asking questions!

Example questions:
- "What is the formula for kinetic energy?"
- "আমার নোটে সাইন ফাংশনের ডেফিনিশন কী?" (Bengali)
- "Explain this diagram from page 3"

---

## 📁 Project Structure

```
ScholarAI/
│
├── app.py                  # Streamlit UI (main entry point)
│
├── extract.py              # Step 1: Extract text from PDF images
│                           #   - Uses Gemma LLM for extraction
│                           #   - Saves to extracted_texts.json
│
├── embed.py                # Step 2: Convert text to embeddings
│                           #   - Uses Gemini Embedding model
│                           #   - Saves to embeddings.json
│
├── store.py                # Step 3: Store in ChromaDB
│                           #   - Organizes by subject
│                           #   - Persistent storage
│
├── query.py                # Step 4: Answer questions
│                           #   - Vector search + Gemini generation
│                           #   - Bengali translation with Groq
│
├── pdf_to_image.py         # Convert PDF pages to images
│                           #   - Supports password-protected PDFs
│
├── data/
│   ├── json_files/         # Intermediate files
│   │   ├── extracted_texts.json
│   │   └── embeddings.json
│   ├── processed_images/   # PDF pages as images
│   └── vector_db/          # ChromaDB storage
│
├── thumbnail_images/       # Preview images
│
├── requirements.txt        # Python dependencies
├── .env                    # Your API keys (create this!)
└── README.md              # This file
```

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.9+ |
| **UI Framework** | Streamlit |
| **Vector Database** | ChromaDB |
| **PDF Processing** | PyMuPDF (fitz) |
| **Text Extraction** | Gemma LLM (via Google GenAI) |
| **Embeddings** | Google Gemini Embedding API |
| **Answer Generation** | Google Gemini API |
| **Translation** | Groq LLM (Llama 3.1) |

---

## ⚙️ How to Use Each Module

### Extract Text from PDFs
```python
from extract import extractor

# After uploading PDF and converting to images
extractor()  # Creates extracted_texts.json
```

### Generate Embeddings
```python
from embed import embed

# Convert extracted text to vectors
embed()  # Creates embeddings.json
```

### Store in Vector Database
```python
from store import store

# Save vectors in ChromaDB
store("Math")  # "Math" is the subject
```

### Query Your Notes
```python
from query import query

answer = query("What is a derivative?", history="")
print(answer)
```

---

## 🎯 Use Cases

📚 **Study Preparation** — Upload lecture notes, ask the AI tutor  
🔍 **Note Review** — Quickly search across all your notes  
❓ **Concept Clarification** — Ask questions about anything in your notes  
📝 **Exam Practice** — Quiz yourself on your own materials  
🌐 **Multilingual Learning** — Study in Bengali or English  

---

## 📊 Performance Notes

- **First-time extraction**: Depends on PDF size (10-50 sec per page typical)
- **Queries**: Usually respond within 5-10 seconds
- **Storage**: ~1KB per page for embeddings + text
- **Memory**: Requires ~2GB RAM for typical use

---

## 🐛 Troubleshooting

**Error: "GEMINI_API_KEY not found"**
- Create `.env` file in project root with your API key

**Error: "PDF is encrypted"**
- Check "password authentication" checkbox and enter the password

**Extraction is slow**
- Normal for large PDFs. The AI is carefully reading every page.
- You can stop and resume — already processed images are skipped

**"No embeddings found" error**
- Run extraction first, then embedding, then storage (in order)

---

## 📜 License

```
Copyright 2026 Renerfia
Licensed under the Apache License, Version 2.0
```

---

## 💡 Future Improvements

- [ ] Support for multiple PDF uploads in one session
- [ ] Export notes to study cards (Anki format)
- [ ] Multi-language support for more languages
- [ ] Voice input/output for studying hands-free
- [ ] Better math equation rendering
- [ ] Web interface for cloud deployment

---

<div align="center">

**ScholarAI** — Turning static PDFs into intelligent tutors.

*Built with obsession. Powered by Google Gemini & Groq. Forged in Python.*

⭐ If ScholarAI helped you ace your studies, give this repo a star!

Made for educational purposes with ❤️

</div>
