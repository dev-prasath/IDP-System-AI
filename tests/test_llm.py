from backend.chatbot.llm import generate_answer

chunks = [
    """
    Invoice Number: INV-1001

    Vendor: ABC Technologies Pvt Ltd

    Amount: ₹45,000

    Due Date: 10-06-2026
    """
]

question = "What is the invoice amount?"

answer = generate_answer(
    question,
    chunks
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)