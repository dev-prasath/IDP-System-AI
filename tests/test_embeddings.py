# test_embeddings.py

from backend.chatbot.chunking import split_document
from backend.chatbot.embeddings import generate_embeddings

text = """
Invoice Number INV-1001

Vendor ABC Technologies

Amount ₹45000

Due Date 10-06-2026
""" * 10

chunks = split_document(text)

vectors = generate_embeddings(chunks)

print(f"Chunks: {len(chunks)}")

print(f"Embeddings Shape: {vectors.shape}")

print(vectors[0][:10])