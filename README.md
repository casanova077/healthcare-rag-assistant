# Healthcare RAG Assistant

A small Flask application that answers questions by retrieving relevant passages from a cardiovascular health PDF. It uses LangChain for PDF loading and text splitting, Hugging Face embeddings, and FAISS similarity search.

> **Medical safety:** This is an educational demonstration only. It is not medical advice, a diagnostic tool, or a substitute for a qualified healthcare professional. Do not use it for urgent or personal medical decisions.

## Features

- Browser-based question and answer interface
- Retrieval from `documents/healthcare_rag_cardiovascular_guide.pdf`
- Sentence Transformer embeddings with `sentence-transformers/all-MiniLM-L6-v2`
- FAISS similarity search over the document's text chunks
- Command-line indexing and retrieval workflow in `rag.py`

## Requirements

- Python 3.10 or newer
- Internet access the first time the Hugging Face embedding model is downloaded
- The source PDF in the `documents/` directory

## Setup

From the project directory, create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the web app

Start Flask with:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in a browser. The application loads and splits the PDF and builds the in-memory FAISS index when it starts, so the first launch may take a little longer.

## Run the command-line workflow

To create a local FAISS index and query it from the terminal:

```powershell
python rag.py
```

The generated index is written to `faiss_index/`. The current web app builds its own index at startup rather than loading this saved index.

## Project structure

```text
.
├── app.py                    # Flask web application
├── rag.py                    # Command-line indexing and retrieval workflow
├── documents/                # Source healthcare PDF
├── faiss_index/              # Generated FAISS files
├── static/                   # CSS and browser JavaScript
├── templates/                # Flask HTML template
├── requirements.txt          # Python dependencies
└── .gitignore                # Local and generated files excluded from Git
```

## Configuration and security

The current application does not require an API key. Keep local secrets in `.env`, never commit them, and rotate any key that may already have been exposed or committed. Do not upload private patient or health information to this demonstration.

## Troubleshooting

- If the embedding model fails to load, check your internet connection and confirm that the virtual environment is active.
- If the PDF cannot be found, verify that its filename and location match `documents/healthcare_rag_cardiovascular_guide.pdf`.
- If FAISS installation fails on your platform, use a supported Python version and consult the FAISS package installation guidance for that platform.
