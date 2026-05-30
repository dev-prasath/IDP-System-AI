# =====================================================
# chatbot/embeddings.py
# =====================================================

from sentence_transformers import SentenceTransformer

# Load once when application starts
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_embeddings(chunks):
    """
    Generate embeddings for text chunks.

    Parameters
    ----------
    chunks : list

    Returns
    -------
    embeddings
    """

    if not chunks:
        return []

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings