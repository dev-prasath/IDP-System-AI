from backend.chatbot.chunking import split_document

sample_text = ""

for i in range(1, 31):
    sample_text += f"""
    Invoice Number: INV-{i}
    Vendor: ABC Technologies
    Amount: ₹{i*1000}
    Due Date: 10-06-2026

    """

chunks = split_document(sample_text)

print(f"\nTotal Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\n{'='*50}")
    print(f"CHUNK {i+1}")
    print(f"{'='*50}")
    print(chunk)