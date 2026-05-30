from backend.chatbot.chunking import split_document
from backend.chatbot.embeddings import generate_embeddings
from backend.chatbot.vector_store import VectorStore
from backend.chatbot.retriever import retrieve_context

document = """
Invoice Number: INV-1001

Vendor: ABC Technologies Pvt Ltd

Amount: ₹45,000

Due Date: 10-06-2026

This invoice was generated for software development services.

Contact Email: accounts@abctech.com

Phone: +91 9876543210
"""

# Chunk
chunks = split_document(document)

# Embeddings
embeddings = generate_embeddings(chunks)

# Build Index
store = VectorStore()

store.build_index(
    chunks,
    embeddings
)

# Ask Question
question = "What is the invoice amount?"

results = retrieve_context(
    question,
    store
)

print("\nQUESTION:")
print(question)

print("\nRETRIEVED CONTEXT:")

for i, chunk in enumerate(results, start=1):
    print(f"\nChunk {i}")
    print(chunk)