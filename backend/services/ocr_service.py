# =========================================================
# backend/services/ocr_service.py
# FIXED VERSION
# =========================================================

# from ocr.easyocr_engine import (
#     extract_text_and_boxes
# )

from ocr.paddle_ocr import (
    extract_text_and_boxes
)

from utils.logger import (
    log_info,
    log_error
)

# =========================================================
# OCR SERVICE
# =========================================================

def process_ocr(document_image):

    """
    Perform OCR extraction.

    Args:
        document_image:
            Preprocessed image

    Returns:
        dict:
            OCR results
    """

    try:

        log_info(
            "Starting OCR extraction"
        )

        # =================================================
        # OCR EXTRACTION
        # =================================================

        ocr_result = extract_text_and_boxes(
            document_image
        )

        # =================================================
        # VALIDATE OCR RESULT
        # =================================================

        if not ocr_result["success"]:

            return {

                "success": False,

                "message": ocr_result.get(
                    "message",
                    "OCR extraction failed"
                )
            }

        # =================================================
        # EXTRACT VALUES
        # =================================================

        extracted_text = ocr_result.get(
            "ocr_text",
            ""
        )

        boxes = ocr_result.get(
            "boxes",
            []
        )

        confidence = ocr_result.get(
            "ocr_confidence",
            0.0
        )

        log_info(
            "OCR extraction completed"
        )

        # =================================================
        # RETURN RESPONSE
        # =================================================

        return {

            "success": True,

            "ocr_text": extracted_text,

            "boxes": boxes,

            "ocr_confidence": confidence
        }

    except Exception as e:

        log_error(
            f"OCR Service Error: {str(e)}"
        )

        return {

            "success": False,

            "message": str(e)
        }