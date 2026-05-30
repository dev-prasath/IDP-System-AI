# =====================================================
# chatbot/chatbot_service.py
# =====================================================

from backend.chatbot.chunking import split_document
from backend.chatbot.embeddings import generate_embeddings
from backend.chatbot.vector_store import VectorStore
from backend.chatbot.retriever import retrieve_context
from backend.chatbot.llm import generate_answer


def ask_question(
    document_text: str,
    question: str,
    top_k: int = 3
):
    """
    Complete RAG pipeline.
    """

    # Step 1
    chunks = split_document(document_text)

    if not chunks:
        return "No document content found."

    # Step 2
    embeddings = generate_embeddings(chunks)

    # Step 3
    vector_store = VectorStore()

    vector_store.build_index(
        chunks,
        embeddings
    )

    # Step 4
    context = retrieve_context(
        question,
        vector_store,
        top_k=top_k
    )

    # Step 5
    answer = generate_answer(
        question,
        context
    )

    return answer