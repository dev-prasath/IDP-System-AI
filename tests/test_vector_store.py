from backend.chatbot.chunking import split_document
from backend.chatbot.embeddings import generate_embeddings
from backend.chatbot.vector_store import VectorStore

text = """
Invoice Number INV-1001

Vendor ABC Technologies Pvt Ltd

Amount ₹45000

Due Date 10-06-2026

This invoice is for software development services.
""" * 10

chunks = split_document(text)

embeddings = generate_embeddings(chunks)

store = VectorStore()

store.build_index(
    chunks,
    embeddings
)

print("Index Created Successfully")

print(f"Stored Chunks: {len(chunks)}")