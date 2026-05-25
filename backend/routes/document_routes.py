# =========================================================
# backend/routes/document_routes.py
# =========================================================

from fastapi import APIRouter

from database.postgresql import (
    fetch_documents,
    update_document_title
)

router = APIRouter()

# =========================================================
# FETCH DOCUMENTS
# =========================================================

@router.get("/documents")
async def get_documents():

    documents = fetch_documents()

    return {

        "success": True,

        "documents": documents
    }

# =========================================================
# UPDATE DOCUMENT TITLE
# =========================================================

@router.put("/documents/{doc_id}")
async def update_title(

    doc_id: int,
    title: str
):

    update_document_title(
        doc_id,
        title
    )

    return {

        "success": True,

        "message": (
            "Document title updated"
        )
    }