from flask import Flask, render_template, request, jsonify

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


app = Flask(__name__)

PDF_PATH = "documents/healthcare_rag_cardiovascular_guide.pdf"


# -----------------------------
# Load and prepare documents
# -----------------------------

def load_documents():

    loader = PyPDFLoader(PDF_PATH)

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


# -----------------------------
# Create vector database
# -----------------------------

print("Loading healthcare document...")

chunks = load_documents()

print(f"Loaded {len(chunks)} chunks.")

print("Creating embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_database = FAISS.from_documents(
    chunks,
    embeddings
)

print("Vector database ready!")


# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:

        return jsonify({
            "answer": "Please enter a question."
        })

    # Search relevant document chunks
    results = vector_database.similarity_search(
        question,
        k=3
    )

    # Combine retrieved information
    context = "\n\n".join(
        result.page_content
        for result in results
    )

    return jsonify({
    "answer": context
})


# -----------------------------
# Run Flask
# -----------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )