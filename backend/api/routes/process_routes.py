# =========================================================
# backend/api/routes/process_routes.py
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

from PIL import Image

import tempfile
import os

from io import BytesIO

# =========================================================
# SERVICES
# =========================================================

from backend.services.document_service import (
    process_document
)

# =========================================================
# PDF HANDLING
# =========================================================

from utils.pdf_handler import (
    pdf_to_images
)

# =========================================================
# LOGGER
# =========================================================

from utils.logger import (
    log_info,
    log_warning,
    log_error,
    log_exception
)

# =========================================================
# DATABASE
# =========================================================

from database.postgresql import (
    save_document
)

# =========================================================
# ROUTER
# =========================================================

router = APIRouter()

# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/process/health")
async def process_health():

    return {

        "success": True,

        "message": (
            "Process Routes Working"
        )
    }

# =========================================================
# PROCESS DOCUMENT ENDPOINT
# =========================================================

@router.post("/process-document")
async def process_uploaded_document(

    file: UploadFile = File(...)
):

    try:

        # =====================================================
        # VALIDATE FILE TYPE
        # =====================================================

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

        # =====================================================
        # LOG START
        # =====================================================

        log_info(
            f"Processing File: {file.filename}"
        )

        # =====================================================
        # INITIALIZE VARIABLES
        # =====================================================

        all_text = ""

        all_boxes = []

        all_entities = []

        all_tables = []

        confidence_scores = []

        total_pages = 1

        final_document_type = "Unknown"

        structured_output = {}

        # =====================================================
        # READ FILE
        # =====================================================

        file_bytes = await file.read()

        # =====================================================
        # PDF PROCESSING
        # =====================================================

        if file.content_type == "application/pdf":

            with tempfile.NamedTemporaryFile(

                delete=False,

                suffix=".pdf"

            ) as temp_pdf:

                temp_pdf.write(file_bytes)

                temp_pdf_path = temp_pdf.name

            try:

                with open(

                    temp_pdf_path,

                    "rb"

                ) as pdf_file:

                    images = pdf_to_images(
                        pdf_file
                    )

            finally:

                if os.path.exists(
                    temp_pdf_path
                ):

                    os.remove(
                        temp_pdf_path
                    )

            total_pages = len(images)

            log_info(
                f"PDF Pages Detected: {total_pages}"
            )

            # =================================================
            # PROCESS EACH PAGE
            # =================================================

            for page_index, image in enumerate(images):

                try:

                    log_info(
                        f"Processing Page: "
                        f"{page_index + 1}"
                    )

                    page_result = process_document(
                        image
                    )

                    if not page_result.get(
                        "success"
                    ):

                        log_warning(
                            f"Page {page_index + 1} "
                            f"processing failed"
                        )

                        continue

                    # =============================================
                    # OCR TEXT
                    # =============================================

                    all_text += (

                        f"\n\n===== PAGE "
                        f"{page_index + 1} =====\n\n"
                    )

                    all_text += page_result.get(
                        "ocr_text",
                        ""
                    )

                    # =============================================
                    # BOXES
                    # =============================================

                    all_boxes.extend(

                        page_result.get(
                            "boxes",
                            []
                        )
                    )

                    # =============================================
                    # ENTITIES
                    # =============================================

                    all_entities.extend(

                        page_result.get(
                            "entities",
                            []
                        )
                    )

                    # =============================================
                    # TABLES
                    # =============================================

                    all_tables.extend(

                        page_result.get(
                            "table_data",
                            []
                        )
                    )

                    # =============================================
                    # OCR CONFIDENCE
                    # =============================================

                    confidence_scores.append(

                        page_result.get(
                            "ocr_confidence",
                            0
                        )
                    )

                    # =============================================
                    # DOCUMENT TYPE
                    # =============================================

                    final_document_type = (
                        page_result.get(
                            "document_type",
                            "Unknown"
                        )
                    )

                    # =============================================
                    # STRUCTURED OUTPUT
                    # =============================================

                    structured_output.update(

                        page_result.get(
                            "structured_output",
                            {}
                        )
                    )

                except Exception as page_error:

                    log_exception(
                        page_error
                    )

                    continue

        # =====================================================
        # IMAGE PROCESSING
        # =====================================================

        else:

            image = Image.open(

                BytesIO(file_bytes)

            ).convert("RGB")

            result = process_document(
                image
            )

            if not result.get("success"):

                raise HTTPException(

                    status_code=500,

                    detail=(
                        "Image processing failed"
                    )
                )

            all_text = result.get(
                "ocr_text",
                ""
            )

            all_boxes = result.get(
                "boxes",
                []
            )

            all_entities = result.get(
                "entities",
                []
            )

            all_tables = result.get(
                "table_data",
                []
            )

            confidence_scores.append(

                result.get(
                    "ocr_confidence",
                    0
                )
            )

            final_document_type = result.get(
                "document_type",
                "Unknown"
            )

            structured_output = result.get(
                "structured_output",
                {}
            )

        # =====================================================
        # OCR CONFIDENCE
        # =====================================================

        if confidence_scores:

            overall_confidence = round(

                sum(confidence_scores)

                / len(confidence_scores),

                2
            )

        else:

            overall_confidence = 0.0

        # =====================================================
        # SAVE DOCUMENT TO DATABASE
        # =====================================================

        try:

            save_document(

                file.filename,

                final_document_type,

                all_text,

                all_entities,

                structured_output
            )

            log_info(
                "Document Saved Successfully"
            )

        except Exception as db_error:

            log_exception(
                db_error
            )

        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return {

            "success": True,

            "message": (
                "Document processed successfully"
            ),

            "file_name": file.filename,

            "document_type": final_document_type,

            "pages": total_pages,

            "ocr_confidence": overall_confidence,

            "ocr_text": all_text,

            "entities": all_entities,

            "structured_output": structured_output,

            "boxes": all_boxes,

            "table_data": all_tables
        }

    except HTTPException as http_error:

        log_error(
            str(http_error.detail)
        )

        raise http_error

    except Exception as e:

        log_exception(e)

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )