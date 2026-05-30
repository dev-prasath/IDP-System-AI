# =====================================================
# chatbot/llm.py
# =====================================================

import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment."
    )

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(
    question: str,
    context_chunks: list
):
    """
    Generate answer from retrieved chunks.
    """

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a document assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
reply:

"Information not found in the document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = model.generate_content(
        prompt
    )

    return response.text.strip()