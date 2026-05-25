# =========================================================
# backend/routes/process_routes.py
# =========================================================

from fastapi import APIRouter, UploadFile, File
from PIL import Image
import tempfile
import os
from io import BytesIO

# =========================================================
# SERVICES
# =========================================================

from backend.services.document_service import process_document

# =========================================================
# PDF HANDLING
# =========================================================

from utils.pdf_handler import pdf_to_images

# =========================================================
# backend/routes/process_routes.py
# UPDATE IMPORTS
# =========================================================

from backend.schemas.response_schema import (
    ProcessResponseSchema
)



# =========================================================
# RESTORE ORIGINAL IMPORTS
# =========================================================

from ocr.easyocr_engine import (
    extract_text_and_boxes
)

from preprocessing.image_processing import (
    preprocess_image
)

from utils.pdf_handler import (
    pdf_to_images
)

from nlp.entity_extractor import (
    extract_entities
)

from utils.entity_postprocessing import (
    process_entities
)

from utils.structure_output import (
    structure_entities
)

# from documentClassifier.classifier import (
#     classify_document
# )
# =========================================================
# ROUTER
# =========================================================

router = APIRouter()

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

            return {
                "success": False,
                "message": "Unsupported file type"
            }

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

            with open(temp_pdf_path, "rb") as pdf_file:

                images = pdf_to_images(pdf_file)

            os.remove(temp_pdf_path)

            total_pages = len(images)

            # =================================================
            # PROCESS EACH PAGE
            # =================================================

            for page_index, image in enumerate(images):

                try:

                    page_result = process_document(
                        image
                    )

                    if not page_result["success"]:

                        continue

                    all_text += (
                        f"\n\n===== PAGE {page_index + 1} =====\n\n"
                    )

                    all_text += page_result[
                        "ocr_text"
                    ]

                    all_boxes.extend(
                        page_result["boxes"]
                    )

                    all_entities.extend(
                        page_result["entities"]
                    )

                    all_tables.extend(
                        page_result.get(
                            "table_data",
                            []
                        )
                    )

                    confidence_scores.append(
                        page_result[
                            "ocr_confidence"
                        ]
                    )

                    final_document_type = (
                        page_result[
                            "document_type"
                        ]
                    )

                    structured_output.update(
                        page_result[
                            "structured_output"
                        ]
                    )

                except Exception as page_error:

                    print(
                        f"PDF PAGE ERROR: {page_error}"
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

            if not result["success"]:

                return result

            all_text = result["ocr_text"]

            all_boxes = result["boxes"]

            all_entities = result["entities"]

            all_tables = result.get(
                "table_data",
                []
            )

            confidence_scores.append(
                result["ocr_confidence"]
            )

            final_document_type = result[
                "document_type"
            ]

            structured_output = result[
                "structured_output"
            ]

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
        # FINAL RESPONSE
        # =====================================================

        return {

            "success": True,

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

    except Exception as e:

        print(
            "PROCESS DOCUMENT ERROR:",
            str(e)
        )

        return {

            "success": False,

            "message": str(e)
        }