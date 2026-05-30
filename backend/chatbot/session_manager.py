# =====================================================
# chatbot/session_manager.py
# =====================================================

from backend.chatbot.chat_session import DocumentChatbot


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def create_session(
        self,
        document_id,
        document_text
    ):

        chatbot = DocumentChatbot(
            document_text
        )

        self.sessions[document_id] = chatbot

    def get_session(
        self,
        document_id
    ):

        return self.sessions.get(
            document_id
        )

    def remove_session(
        self,
        document_id
    ):

        if document_id in self.sessions:

            del self.sessions[
                document_id
            ]


# Global Manager
session_manager = SessionManager()