# =========================================================
# backend/services/classification_service.py
# ADVANCED VERSION
# =========================================================

from utils.logger import (
    log_info,
    log_warning
)

# =========================================================
# KEYWORDS
# =========================================================

INVOICE_KEYWORDS = [

    "invoice",
    "gst",
    "bill to",
    "invoice number",
    "tax invoice",
    "total amount",
    "amount due",
    "purchase order",
    "subtotal"
]

RESUME_KEYWORDS = [

    "skills",
    "experience",
    "education",
    "projects",
    "certifications",
    "linkedin",
    "github",
    "portfolio",
    "professional summary"
]

ID_CARD_KEYWORDS = [

    "government of india",
    "date of birth",
    "aadhaar",
    "passport",
    "driving licence",
    "id number",
    "gender"
]

MEDICAL_KEYWORDS = [

    "patient",
    "diagnosis",
    "prescription",
    "hospital",
    "doctor",
    "blood pressure",
    "medical report"
]

REPORT_KEYWORDS = [

    "analysis",
    "summary",
    "findings",
    "conclusion",
    "report"
]

# =========================================================
# SCORE DOCUMENT TYPE
# =========================================================

def calculate_score(

    text,
    keywords
):

    """
    Calculate keyword match score.
    """

    score = 0

    for keyword in keywords:

        if keyword in text:

            score += 1

    return score

# =========================================================
# DOCUMENT CLASSIFICATION
# =========================================================

def classify_document(text):

    """
    Intelligent document classifier.

    Args:
        text (str):
            OCR extracted text

    Returns:
        str:
            Document type
    """

    try:

        log_info(
            "Starting document classification"
        )

        text = text.lower()

        # =================================================
        # CALCULATE SCORES
        # =================================================

        scores = {

            "Invoice": calculate_score(
                text,
                INVOICE_KEYWORDS
            ),

            "Resume": calculate_score(
                text,
                RESUME_KEYWORDS
            ),

            "ID Card": calculate_score(
                text,
                ID_CARD_KEYWORDS
            ),

            "Medical Document": calculate_score(
                text,
                MEDICAL_KEYWORDS
            ),

            "Report": calculate_score(
                text,
                REPORT_KEYWORDS
            )
        }

        # =================================================
        # FIND BEST MATCH
        # =================================================

        document_type = max(

            scores,

            key=scores.get
        )

        max_score = scores[
            document_type
        ]

        # =================================================
        # LOW CONFIDENCE
        # =================================================

        if max_score == 0:

            log_warning(
                "Could not confidently classify document"
            )

            return "Unknown"

        log_info(
            f"Document classified as "
            f"{document_type}"
        )

        return document_type

    except Exception as e:

        log_warning(
            f"Classification Error: {str(e)}"
        )

        return "Unknown"