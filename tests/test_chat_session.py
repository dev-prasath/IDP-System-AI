from backend.chatbot.chat_session import DocumentChatbot

document = """
Invoice Number: INV-1001

Vendor: ABC Technologies Pvt Ltd

Amount: ₹45,000

Due Date: 10-06-2026
"""

chatbot = DocumentChatbot(document)

questions = [
    "What is the invoice amount?",
    "Who is the vendor?",
    "What is the due date?"
]

for q in questions:

    print("\nQUESTION:", q)

    print(
        "ANSWER:",
        chatbot.ask(q)
    )