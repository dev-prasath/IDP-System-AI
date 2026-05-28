# =========================================================
# nlp/regex_extractor.py
# CENTRALIZED REGEX ENTITY EXTRACTION ENGINE
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import re

# =========================================================
# REGEX PATTERNS
# =========================================================

REGEX_PATTERNS = {

    "EMAIL": [

        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    ],

    "PHONE": [

        r'(?:\+91[\-\s]?)?[6-9]\d{9}'
    ],

    "AADHAAR": [

        r'\d{4}\s\d{4}\s\d{4}'
    ],

    "PAN": [

        r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    ],

    "GST": [

        r'\d{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{3}'
    ],

    "INVOICE_NUMBER": [

        r'(?:Invoice\s*(?:No|Number|#)?\s*[:\-]?\s*)([A-Z0-9\-\/]+)'
    ],

    "DATE": [

        r'\d{2}/\d{2}/\d{4}',
        r'\d{2}-\d{2}-\d{4}',
        r'\d{4}-\d{2}-\d{2}'
    ],

    "AMOUNT": [

        r'₹\s?[\d,]+(?:\.\d{2})?',
        r'Rs\.?\s?[\d,]+(?:\.\d{2})?',
        r'[\d,]+\.\d{2}'
    ]
}

# =========================================================
# CLEAN ENTITY TEXT
# =========================================================

def clean_entity_text(text):

    text = str(text)

    text = text.strip()

    return text

# =========================================================
# EXTRACT REGEX ENTITIES
# =========================================================

def extract_regex_entities(text):

    """
    Extract entities using regex.
    """

    entities = []

    try:

        if not text:

            return entities

        # =================================================
        # ITERATE LABELS
        # =================================================

        for label, patterns in REGEX_PATTERNS.items():

            for pattern in patterns:

                matches = re.finditer(

                    pattern,

                    text,

                    re.IGNORECASE
                )

                for match in matches:

                    # =====================================
                    # HANDLE GROUPS
                    # =====================================

                    if match.groups():

                        entity_text = match.group(1)

                    else:

                        entity_text = match.group()

                    entity_text = clean_entity_text(
                        entity_text
                    )

                    # =====================================
                    # VALIDATE
                    # =====================================

                    if len(entity_text) == 0:

                        continue

                    # =====================================
                    # BUILD ENTITY
                    # =====================================

                    entity = {

                        "text": entity_text,

                        "label": label,

                        "start": match.start(),

                        "end": match.end(),

                        "confidence": 98.0,

                        "source": "regex"
                    }

                    entities.append(entity)

        return entities

    except Exception as e:

        print(
            f"Regex Extraction Error: {str(e)}"
        )

        return []