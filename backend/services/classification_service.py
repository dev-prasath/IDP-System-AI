# =========================================================
# backend/services/classification_service.py
# FULL UPDATED VERSION
# HYBRID TEXT DOCUMENT CLASSIFIER
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from utils.logger import (
    log_info,
    log_warning,
    log_error
)

# =========================================================
# KEYWORD DATABASE
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
    "subtotal",
    "cgst",
    "sgst",
    "igst",
    "tax",
    "vendor",
    "qty",
    "rate"
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
    "professional summary",
    "internship",
    "technical skills",
    "career objective",
    "work experience",
    "resume",
    "curriculum vitae"
]

ID_CARD_KEYWORDS = [

    "government of india",
    "date of birth",
    "aadhaar",
    "passport",
    "driving licence",
    "id number",
    "gender",
    "uidai",
    "dob",
    "identity"
]

MEDICAL_KEYWORDS = [

    "patient",
    "diagnosis",
    "prescription",
    "hospital",
    "doctor",
    "blood pressure",
    "medical report",
    "medicine",
    "clinical",
    "symptoms",
    "treatment"
]

REPORT_KEYWORDS = [

    "analysis",
    "summary",
    "findings",
    "conclusion",
    "report",
    "research",
    "observations",
    "results",
    "methodology"
]

LETTER_KEYWORDS = [

    "dear sir",
    "regards",
    "sincerely",
    "subject",
    "letter",
    "respected sir"
]

# =========================================================
# SCORE CALCULATOR
# =========================================================

def calculate_score(
    text,
    keywords
):

    """
    Calculate keyword match score.
    """

    score = 0

    matched_keywords = []

    for keyword in keywords:

        if keyword in text:

            score += 1

            matched_keywords.append(
                keyword
            )

    return score, matched_keywords

# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    if text is None:

        return ""

    text = str(text)

    text = text.lower()

    text = text.replace(
        "\n",
        " "
    )

    text = text.replace(
        "\t",
        " "
    )

    return text.strip()

# =========================================================
# DOCUMENT CLASSIFIER
# =========================================================

def classify_document(text):

    """
    Hybrid text-based
    document classifier.

    Args:
        text (str)

    Returns:
        str:
            Document type
    """

    try:

        log_info(
            "Starting text classification"
        )

        # =================================================
        # VALIDATION
        # =================================================

        if text is None:

            return "Unknown"

        text = normalize_text(
            text
        )

        if len(text.strip()) == 0:

            return "Unknown"

        # =================================================
        # LIMIT HUGE TEXT
        # =================================================

        MAX_TEXT_LENGTH = 10000

        if len(text) > MAX_TEXT_LENGTH:

            text = text[
                :MAX_TEXT_LENGTH
            ]

        # =================================================
        # CALCULATE SCORES
        # =================================================

        scores = {}

        matched = {}

        invoice_score, invoice_matches = (
            calculate_score(
                text,
                INVOICE_KEYWORDS
            )
        )

        scores["Invoice"] = (
            invoice_score
        )

        matched["Invoice"] = (
            invoice_matches
        )

        # =================================================

        resume_score, resume_matches = (
            calculate_score(
                text,
                RESUME_KEYWORDS
            )
        )

        scores["Resume"] = (
            resume_score
        )

        matched["Resume"] = (
            resume_matches
        )

        # =================================================

        id_score, id_matches = (
            calculate_score(
                text,
                ID_CARD_KEYWORDS
            )
        )

        scores["ID Card"] = (
            id_score
        )

        matched["ID Card"] = (
            id_matches
        )

        # =================================================

        medical_score, medical_matches = (
            calculate_score(
                text,
                MEDICAL_KEYWORDS
            )
        )

        scores["Medical Document"] = (
            medical_score
        )

        matched["Medical Document"] = (
            medical_matches
        )

        # =================================================

        report_score, report_matches = (
            calculate_score(
                text,
                REPORT_KEYWORDS
            )
        )

        scores["Report"] = (
            report_score
        )

        matched["Report"] = (
            report_matches
        )

        # =================================================

        letter_score, letter_matches = (
            calculate_score(
                text,
                LETTER_KEYWORDS
            )
        )

        scores["Letter"] = (
            letter_score
        )

        matched["Letter"] = (
            letter_matches
        )

        # =================================================
        # DEBUG SCORES
        # =================================================

        print(
            "\n========== TEXT CLASSIFIER =========="
        )

        print(
            "\nDOCUMENT SCORES:\n"
        )

        for doc_type, score in scores.items():

            print(
                f"{doc_type}: {score}"
            )

            print(
                f"Matched Keywords: "
                f"{matched[doc_type]}"
            )

            print()

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
                "Low confidence classification"
            )

            return "Unknown"

        # =================================================
        # FINAL RESULT
        # =================================================

        log_info(
            f"Text classified as "
            f"{document_type}"
        )

        print(
            f"\nFINAL CLASSIFICATION: "
            f"{document_type}"
        )

        print(
            f"SCORE: {max_score}"
        )

        return document_type

    except Exception as e:

        log_error(
            f"Classification Error: {str(e)}"
        )

        return "Unknown"