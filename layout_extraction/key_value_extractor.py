# =========================================================
# layout_extraction/key_value_extractor.py
# KEY VALUE LAYOUT EXTRACTION
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import re

# =========================================================
# FIELD KEYWORDS
# =========================================================

FIELD_MAPPING = {

    "name": [

        "name"
    ],

    "dob": [

        "dob",
        "date of birth",
        "birth"
    ],

    "gender": [

        "gender",
        "male",
        "female"
    ],

    "aadhaar_number": [

        "aadhaar",
        "uid",
        "uidai"
    ]
}

# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    text = str(text).lower()

    text = text.strip()

    return text

# =========================================================
# FIND FIELD NAME
# =========================================================

def detect_field(text):

    normalized = normalize_text(
        text
    )

    for field, keywords in FIELD_MAPPING.items():

        for keyword in keywords:

            if keyword in normalized:

                return field

    return None

# =========================================================
# CLEAN VALUE
# =========================================================

def clean_value(value):

    value = str(value)

    value = value.replace(
        ":",
        ""
    )

    value = value.strip()

    return value

# =========================================================
# EXTRACT KEY VALUE PAIRS
# =========================================================

def extract_key_value_pairs(rows):

    """
    Extract structured fields
    from grouped OCR rows.
    """

    structured_data = {}

    try:

        for row in rows:

            # =============================================
            # EXTRACT ROW TEXTS
            # =============================================

            texts = [

                item["text"]

                for item in row
            ]

            row_text = " ".join(
                texts
            )

            normalized_row = normalize_text(
                row_text
            )

            # =============================================
            # NAME DETECTION
            # =============================================

            if (
                len(texts) == 1
                and len(row_text.split()) >= 2
                and "government" not in normalized_row
            ):

                probable_name = row_text.strip()

                if "name" not in structured_data:

                    structured_data[
                        "name"
                    ] = probable_name

            # =============================================
            # DOB
            # =============================================

            if "dob" in normalized_row:

                dob_match = re.search(

                    r'\d{2}/\d{2}/\d{4}',

                    row_text
                )

                if dob_match:

                    structured_data[
                        "dob"
                    ] = dob_match.group()

            # =============================================
            # GENDER
            # =============================================

            gender_match = re.search(

                r'(male|female)',

                normalized_row,

                re.IGNORECASE
            )

            if gender_match:

                gender = gender_match.group()

                structured_data[
                    "gender"
                ] = gender.capitalize()

            # =============================================
            # AADHAAR NUMBER
            # =============================================

            aadhaar_match = re.search(

                r'\d{4}\s\d{4}\s\d{4}',

                row_text
            )

            if aadhaar_match:

                structured_data[
                    "aadhaar_number"
                ] = aadhaar_match.group()

        return structured_data

    except Exception as e:

        print(
            "KEY VALUE EXTRACTION ERROR:",
            str(e)
        )

        return {}