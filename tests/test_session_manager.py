# test_session_manager.py

from backend.chatbot.session_manager import (
    session_manager
)

document_text = """
Invoice Number: INV-1001

Vendor: ABC Technologies

Amount: ₹45,000

Due Date: 10-06-2026
"""

session_manager.create_session(
    "doc1",
    document_text
)

chatbot = session_manager.get_session(
    "doc1"
)

answer = chatbot.ask(
    "What is the invoice amount?"
)

print(answer)