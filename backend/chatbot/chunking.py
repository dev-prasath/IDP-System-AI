# =====================================================
# chatbot/chunking.py
# =====================================================

from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_document(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    """
    Split OCR text into smaller chunks
    for embedding and retrieval.

    Parameters
    ----------
    text : str
        OCR extracted text

    chunk_size : int
        Size of each chunk

    chunk_overlap : int
        Overlap between chunks

    Returns
    -------
    list
        List of text chunks
    """

    if not text:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_text(text)

    return chunks