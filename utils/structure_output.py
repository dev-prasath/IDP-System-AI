# =========================================================
# utils/structure_output.py
# ENTERPRISE STRUCTURED OUTPUT ENGINE
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import re

# =========================================================
# SAFE VALUE
# =========================================================

def safe_value(value):

    if value is None:

        return None

    value = str(value).strip()

    if len(value) == 0:

        return None

    return value

# =========================================================
# ENTITY FILTER
# =========================================================

def filter_entities_by_label(
    entities,
    label
):

    return [

        entity

        for entity in entities

        if entity.get(
            "label",
            ""
        ).upper() == label.upper()
    ]

# =========================================================
# BEST ENTITY
# =========================================================

def get_best_entity(
    entities,
    label
):

    filtered = filter_entities_by_label(
        entities,
        label
    )

    if not filtered:

        return None

    # Highest confidence first
    filtered = sorted(

        filtered,

        key=lambda x: (

            x.get(
                "confidence",
                0
            ),

            x.get(
                "source",
                ""
            ) == "regex"
        ),

        reverse=True
    )

    return filtered[0]

# =========================================================
# EXTRACT ENTITY TEXTS
# =========================================================

def extract_entity_texts(
    entities,
    label
):

    filtered = filter_entities_by_label(
        entities,
        label
    )

    values = []

    seen = set()

    for entity in filtered:

        text = safe_value(

            entity.get(
                "text"
            )
        )

        if not text:

            continue

        key = text.lower()

        if key in seen:

            continue

        seen.add(key)

        values.append(text)

    return values

# =========================================================
# DETECT TOTAL AMOUNT
# =========================================================

def detect_total_amount(entities):

    amounts = filter_entities_by_label(
        entities,
        "AMOUNT"
    )

    if not amounts:

        return None

    best_amount = None

    best_score = -1

    for amount in amounts:

        text = str(

            amount.get(
                "text",
                ""
            )
        )

        confidence = amount.get(
            "confidence",
            0
        )

        score = confidence

        lower = text.lower()

        # Prefer total-like amounts
        keywords = [

            "total",
            "grand",
            "final",
            "net"
        ]

        for keyword in keywords:

            if keyword in lower:

                score += 20

        # Prefer larger amounts
        numbers = re.findall(

            r'[\d,.]+',

            text
        )

        if numbers:

            try:

                value = float(

                    numbers[0].replace(
                        ",",
                        ""
                    )
                )

                score += value / 1000

            except Exception:

                pass

        if score > best_score:

            best_score = score

            best_amount = text

    return best_amount

# =========================================================
# INVOICE DETAILS
# =========================================================

def build_invoice_details(entities):

    invoice_entity = get_best_entity(
        entities,
        "INVOICE_NUMBER"
    )

    gst_entity = get_best_entity(
        entities,
        "GST"
    )

    org_entity = get_best_entity(
        entities,
        "ORGANIZATION"
    )

    date_entity = get_best_entity(
        entities,
        "DATE"
    )

    return {

        "invoice_number":

            safe_value(

                invoice_entity.get("text")

                if invoice_entity else None
            ),

        "total_amount":

            detect_total_amount(
                entities
            ),

        "gst_number":

            safe_value(

                gst_entity.get("text")

                if gst_entity else None
            ),

        "vendor":

            safe_value(

                org_entity.get("text")

                if org_entity else None
            ),

        "invoice_date":

            safe_value(

                date_entity.get("text")

                if date_entity else None
            )
    }

# =========================================================
# RESUME DETAILS
# =========================================================

def build_resume_details(entities):

    person = get_best_entity(
        entities,
        "PERSON"
    )

    email = get_best_entity(
        entities,
        "EMAIL"
    )

    phone = get_best_entity(
        entities,
        "PHONE"
    )

    return {

        "candidate_name":

            safe_value(

                person.get("text")

                if person else None
            ),

        "email":

            safe_value(

                email.get("text")

                if email else None
            ),

        "phone":

            safe_value(

                phone.get("text")

                if phone else None
            ),

        "skills":

            extract_entity_texts(
                entities,
                "SKILL"
            )
    }

# =========================================================
# ID DETAILS
# =========================================================

def build_id_details(entities):

    person = get_best_entity(
        entities,
        "PERSON"
    )

    aadhaar = get_best_entity(
        entities,
        "AADHAAR"
    )

    pan = get_best_entity(
        entities,
        "PAN"
    )

    passport = get_best_entity(
        entities,
        "PASSPORT"
    )

    date = get_best_entity(
        entities,
        "DATE"
    )

    return {

        "person_name":

            safe_value(

                person.get("text")

                if person else None
            ),

        "aadhaar_number":

            safe_value(

                aadhaar.get("text")

                if aadhaar else None
            ),

        "pan_number":

            safe_value(

                pan.get("text")

                if pan else None
            ),

        "passport_number":

            safe_value(

                passport.get("text")

                if passport else None
            ),

        "date":

            safe_value(

                date.get("text")

                if date else None
            )
    }

# =========================================================
# MAIN STRUCTURE ENGINE
# =========================================================

def structure_entities(
    document_type,
    entities
):

    document_type = str(
        document_type
    ).lower()

    structured_data = {

        "document_type": document_type,

        "persons":

            extract_entity_texts(
                entities,
                "PERSON"
            ),

        "organizations":

            extract_entity_texts(
                entities,
                "ORGANIZATION"
            ),

        "dates":

            extract_entity_texts(
                entities,
                "DATE"
            ),

        "locations":

            extract_entity_texts(
                entities,
                "LOCATION"
            ),

        "emails":

            extract_entity_texts(
                entities,
                "EMAIL"
            ),

        "phones":

            extract_entity_texts(
                entities,
                "PHONE"
            ),

        "amounts":

            extract_entity_texts(
                entities,
                "AMOUNT"
            ),

        "invoice_numbers":

            extract_entity_texts(
                entities,
                "INVOICE_NUMBER"
            ),

        "aadhaar_numbers":

            extract_entity_texts(
                entities,
                "AADHAAR"
            ),

        "pan_numbers":

            extract_entity_texts(
                entities,
                "PAN"
            ),

        "gst_numbers":

            extract_entity_texts(
                entities,
                "GST"
            ),

        "passport_numbers":

            extract_entity_texts(
                entities,
                "PASSPORT"
            ),

        "skills":

            extract_entity_texts(
                entities,
                "SKILL"
            )
    }

    # =====================================================
    # DOCUMENT-SPECIFIC STRUCTURES
    # =====================================================

    if "invoice" in document_type:

        structured_data[
            "invoice_details"
        ] = build_invoice_details(
            entities
        )

    elif "resume" in document_type:

        structured_data[
            "candidate_details"
        ] = build_resume_details(
            entities
        )

    elif "id" in document_type:

        structured_data[
            "id_details"
        ] = build_id_details(
            entities
        )

    # =====================================================
    # ENTITY SUMMARY
    # =====================================================

    structured_data[
        "entity_summary"
    ] = {

        "total_entities": len(
            entities
        ),

        "total_persons": len(
            structured_data["persons"]
        ),

        "total_organizations": len(
            structured_data["organizations"]
        ),

        "total_dates": len(
            structured_data["dates"]
        ),

        "total_emails": len(
            structured_data["emails"]
        ),

        "total_phones": len(
            structured_data["phones"]
        ),

        "total_amounts": len(
            structured_data["amounts"]
        )
    }

    return structured_data