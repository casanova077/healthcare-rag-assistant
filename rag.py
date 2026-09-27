from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


PDF_PATH = "documents/healthcare_rag_cardiovascular_guide.pdf"
FAISS_PATH = "faiss_index"


def load_and_split_pdf():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def create_vector_database(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_database = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_database.save_local(FAISS_PATH)

    return vector_database


def generate_answer(vector_database, question):

    results = vector_database.similarity_search(
        question,
        k=3
    )

    print("\n========== RETRIEVED INFORMATION ==========\n")

    for i, result in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(result.page_content)
        print()

    return (
        "Based on the provided document, the relevant information "
        "was retrieved successfully. See the retrieved information above."
    )


if __name__ == "__main__":

    print("Loading PDF...")

    chunks = load_and_split_pdf()

    print(f"Total chunks: {len(chunks)}")

    print("Creating vector database...")

    vector_database = create_vector_database(chunks)

    print("Vector database ready!")

    question = input("\nAsk a question about the document: ")

    answer = generate_answer(
        vector_database,
        question
    )

    print("\n========== AI ANSWER ==========\n")
    print(answer)