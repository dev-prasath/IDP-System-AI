# =========================================================
# backend/api/routes/document_routes.py
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

# =========================================================
# DATABASE
# =========================================================

from database.postgresql import (
    fetch_documents,
    update_document_title,
    fetch_document_by_id,
    save_document
)

# =========================================================
# DOCUMENT PIPELINE
# =========================================================

from backend.services.document_service import (
    process_document
)

# =========================================================
# LOGGER
# =========================================================

from utils.logger import (
    log_info,
    log_error,
    log_exception
)

# =========================================================
# ROUTER
# =========================================================

router = APIRouter()

# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/documents/health")
async def document_health():

    return {

        "success": True,

        "message": (
            "Document Routes Working"
        )
    }

# =========================================================
# PROCESS DOCUMENT
# =========================================================

@router.post("/process-document")
async def process_uploaded_document(

    file: UploadFile = File(...)
):

    try:

        # =================================================
        # VALIDATE FILE
        # =================================================

        allowed_types = [

            "image/png",
            "image/jpeg",
            "application/pdf"
        ]

        if file.content_type not in allowed_types:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Unsupported file type"
                )
            )

        # =================================================
        # LOG
        # =================================================

        log_info(
            f"Processing File: {file.filename}"
        )

        # =================================================
        # PROCESS DOCUMENT
        # =================================================

        result = process_document(
            file.file
        )

        # =================================================
        # VALIDATE RESULT
        # =================================================

        if not result.get("success"):

            raise HTTPException(

                status_code=500,

                detail=(
                    "Document processing failed"
                )
            )

        # =================================================
        # EXTRACT RESULT DATA
        # =================================================

        document_type = result.get(
            "document_type",
            "Unknown"
        )

        ocr_text = result.get(
            "ocr_text",
            ""
        )

        entities = result.get(
            "entities",
            []
        )

        structured_output = result.get(
            "structured_output",
            {}
        )

        # =================================================
        # SAVE TO DATABASE
        # =================================================

        try:

            save_document(

                file.filename,

                document_type,

                ocr_text,

                entities,

                structured_output
            )

            log_info(
                "Document saved to database"
            )

        except Exception as db_error:

            log_exception(db_error)

        # =================================================
        # RETURN RESULT
        # =================================================

        return {

            "success": True,

            "message": (
                "Document processed successfully"
            ),

            "data": result
        }

    except HTTPException as http_error:

        log_error(str(http_error.detail))

        raise http_error

    except Exception as e:

        log_exception(e)

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )

# =========================================================
# FETCH ALL DOCUMENTS
# =========================================================

@router.get("/documents")
async def get_documents():

    try:

        documents = fetch_documents()

        return {

            "success": True,

            "count": len(documents),

            "documents": documents
        }

    except Exception as e:

        log_exception(e)

        raise HTTPException(

            status_code=500,

            detail=(
                "Failed to fetch documents"
            )
        )

# =========================================================
# FETCH SINGLE DOCUMENT
# =========================================================

@router.get("/documents/{doc_id}")
async def get_single_document(

    doc_id: int
):

    try:

        document = fetch_document_by_id(
            doc_id
        )

        if not document:

            raise HTTPException(

                status_code=404,

                detail=(
                    "Document not found"
                )
            )

        return {

            "success": True,

            "document": document
        }

    except HTTPException as http_error:

        raise http_error

    except Exception as e:

        log_exception(e)

        raise HTTPException(

            status_code=500,

            detail=(
                "Failed to fetch document"
            )
        )

# =========================================================
# UPDATE DOCUMENT TITLE
# =========================================================

@router.put("/documents/{doc_id}")
async def update_title(

    doc_id: int,
    title: str
):

    try:

        update_document_title(

            doc_id,

            title
        )

        log_info(
            f"Document {doc_id} updated"
        )

        return {

            "success": True,

            "message": (
                "Document title updated"
            )
        }

    except Exception as e:

        log_exception(e)

        raise HTTPException(

            status_code=500,

            detail=(
                "Failed to update title"
            )
        )

# =========================================================
# DELETE DOCUMENT
# =========================================================

@router.delete("/documents/{doc_id}")
async def delete_document(

    doc_id: int
):

    try:

        # Optional:
        # Implement delete_document_by_id()

        return {

            "success": True,

            "message": (
                "Delete endpoint ready"
            )
        }

    except Exception as e:

        log_exception(e)

        raise HTTPException(

            status_code=500,

            detail=(
                "Failed to delete document"
            )
        )