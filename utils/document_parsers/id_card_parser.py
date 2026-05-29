# =========================================================
# utils/document_parsers/id_card_parser.py
# SMART ID CARD PARSER
# =========================================================

import re


# =========================================================
# GET ENTITY
# =========================================================

def get_entity(
    entities,
    label
):

    for entity in entities:

        if entity.get("label") == label:

            return entity.get("text")

    return None


# =========================================================
# PARSE ID CARD
# =========================================================

def parse_id_card(
    ocr_text,
    entities
):

    # =====================================================
    # ENTITY EXTRACTION
    # =====================================================

    person_name = get_entity(
        entities,
        "PERSON"
    )

    aadhaar_number = get_entity(
        entities,
        "AADHAAR"
    )

    pan_number = get_entity(
        entities,
        "PAN"
    )

    passport_number = get_entity(
        entities,
        "PASSPORT"
    )

    # =====================================================
    # DATE OF BIRTH
    # =====================================================

    date_of_birth = None

    # Format:
    # DOB : 04/27/1985

    dob_match = re.search(

        r"DOB\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})",

        ocr_text,

        re.IGNORECASE
    )

    if dob_match:

        date_of_birth = dob_match.group(1)

    # Format:
    # Year of Birth : 1987

    if not date_of_birth:

        yob_match = re.search(

            r"Year\s+of\s+Birth\s*[:\-]?\s*(\d{4})",

            ocr_text,

            re.IGNORECASE
        )

        if yob_match:

            date_of_birth = yob_match.group(1)

    # Fallback to extracted DATE entity

    if not date_of_birth:

        date_of_birth = get_entity(
            entities,
            "DATE"
        )

    # =====================================================
    # NAME FALLBACK
    # =====================================================

    if not person_name:

        lines = ocr_text.split("\n")

        blacklist = [

            "government",
            "india",
            "aadhaar",
            "authority",
            "dob",
            "male",
            "female",
            "sex",
            "eyes",
            "driver",
            "license",
            "licence",
            "class",
            "iss",
            "yr",
            "father",
            "mother",
            "husband",
            "wife",
            "birth",
            "year of birth"
        ]

        candidates = []

        for line in lines:

            line = line.strip()

            if not line:

                continue

            lower_line = line.lower()

            # Skip blacklist words

            if any(

                word in lower_line

                for word in blacklist
            ):

                continue

            # Skip numeric lines

            if any(

                char.isdigit()

                for char in line
            ):

                continue

            # Skip very short lines

            if len(line) < 3:

                continue

            candidates.append(line)

        if candidates:

            person_name = candidates[0]

    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    parsed_id_card = {

        "person_name":
            person_name,

        "aadhaar_number":
            aadhaar_number,

        "pan_number":
            pan_number,

        "passport_number":
            passport_number,

        "date_of_birth":
            date_of_birth
    }

    return parsed_id_card