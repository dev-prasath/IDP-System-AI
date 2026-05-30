# =====================================================
# chatbot/retriever.py
# =====================================================

from backend.chatbot.embeddings import embedding_model


def retrieve_context(
    query: str,
    vector_store,
    top_k: int = 3
):
    """
    Retrieve most relevant chunks
    for a user question.
    """

    query_embedding = embedding_model.encode(
        query,
        convert_to_numpy=True
    )

    results = vector_store.search(
        query_embedding,
        top_k=top_k
    )

    return results