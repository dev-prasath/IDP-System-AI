from backend.chatbot.chatbot_service import ask_question

document_text = """
Invoice Number: INV-1001

Vendor: ABC Technologies Pvt Ltd

Amount: ₹45,000

Due Date: 10-06-2026

Contact Email:
accounts@abctech.com

Phone:
9876543210
"""

questions = [
    "What is the invoice amount?",
    "Who is the vendor?",
    "What is the invoice number?",
    "What is the due date?"
]

for question in questions:

    answer = ask_question(
        document_text,
        question
    )

    print("\n" + "="*50)
    print("QUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)