# =====================================================
# chatbot/chat_session.py
# =====================================================

from backend.chatbot.chunking import split_document
from backend.chatbot.embeddings import generate_embeddings
from backend.chatbot.vector_store import VectorStore
from backend.chatbot.retriever import retrieve_context
from backend.chatbot.llm import generate_answer


class DocumentChatbot:

    def __init__(self, document_text):

        self.document_text = document_text

        self.vector_store = VectorStore()

        self._build()

    def _build(self):

        chunks = split_document(
            self.document_text
        )

        embeddings = generate_embeddings(
            chunks
        )

        self.vector_store.build_index(
            chunks,
            embeddings
        )

    def ask(
        self,
        question,
        top_k=3
    ):

        context = retrieve_context(
            question,
            self.vector_store,
            top_k
        )

        answer = generate_answer(
            question,
            context
        )

        return answer