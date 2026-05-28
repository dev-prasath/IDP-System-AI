# =========================================================
# nlp/hybrid_entity_engine.py
# ENTERPRISE HYBRID ENTITY FUSION ENGINE
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from copy import deepcopy

# =========================================================
# LOGGER
# =========================================================

from utils.logger import (
    log_info,
    log_exception
)

# =========================================================
# SAFE STRING
# =========================================================

def safe_string(value):

    if value is None:

        return ""

    return str(value).strip()

# =========================================================
# CREATE ENTITY
# =========================================================

def create_entity(
    label,
    text,
    confidence=0.90,
    source="hybrid"
):

    return {

        "label": label.upper(),

        "text": safe_string(text),

        "confidence": float(confidence),

        "source": source
    }

# =========================================================
# DEDUPLICATE ENTITIES
# =========================================================

def deduplicate_entities(entities):

    unique = {}

    for entity in entities:

        label = safe_string(
            entity.get("label")
        ).upper()

        text = safe_string(
            entity.get("text")
        ).lower()

        key = (label, text)

        if key not in unique:

            unique[key] = entity

        else:

            existing_confidence = unique[
                key
            ].get(
                "confidence",
                0
            )

            new_confidence = entity.get(
                "confidence",
                0
            )

            if new_confidence > existing_confidence:

                unique[key] = entity

    return list(unique.values())

# =========================================================
# LAYOUT FIELD CONVERSION
# =========================================================

def convert_layout_fields(
    layout_fields
):

    entities = []

    try:

        if not isinstance(
            layout_fields,
            dict
        ):

            return []

        mapping = {

            "name": "PERSON",

            "dob": "DATE",

            "aadhaar_number": "AADHAAR",

            "pan_number": "PAN",

            "gst_number": "GST",

            "invoice_number": "INVOICE_NUMBER",

            "vendor": "ORGANIZATION"
        }

        for key, value in layout_fields.items():

            value = safe_string(value)

            if len(value) == 0:

                continue

            label = mapping.get(

                key.lower(),

                key.upper()
            )

            entities.append(

                create_entity(

                    label=label,

                    text=value,

                    confidence=0.93,

                    source="layout"
                )
            )

        return entities

    except Exception as e:

        log_exception(
            f"Layout conversion failed: {str(e)}"
        )

        return []

# =========================================================
# TABLE ENTITY EXTRACTION
# =========================================================

def extract_table_entities(
    table_data
):

    entities = []

    try:

        if not isinstance(
            table_data,
            list
        ):

            return []

        for row in table_data:

            if not isinstance(
                row,
                dict
            ):

                continue

            for key, value in row.items():

                key_lower = safe_string(
                    key
                ).lower()

                value = safe_string(value)

                if len(value) == 0:

                    continue

                # =========================================
                # AMOUNT
                # =========================================

                if key_lower in [

                    "amount",
                    "total",
                    "price",
                    "unit price"
                ]:

                    entities.append(

                        create_entity(

                            label="AMOUNT",

                            text=value,

                            confidence=0.91,

                            source="table"
                        )
                    )

                # =========================================
                # ITEM
                # =========================================

                elif key_lower in [

                    "item",
                    "description"
                ]:

                    entities.append(

                        create_entity(

                            label="ITEM",

                            text=value,

                            confidence=0.85,

                            source="table"
                        )
                    )

        return entities

    except Exception as e:

        log_exception(
            f"Table entity extraction failed: {str(e)}"
        )

        return []

# =========================================================
# PRIORITY BOOSTING
# =========================================================

def apply_priority_boosting(entities):

    boosted = deepcopy(entities)

    for entity in boosted:

        source = entity.get(
            "source",
            ""
        )

        confidence = entity.get(
            "confidence",
            0
        )

        # =============================================
        # REGEX PRIORITY
        # =============================================

        if source == "regex":

            confidence += 0.03

        # =============================================
        # LAYOUT PRIORITY
        # =============================================

        elif source == "layout":

            confidence += 0.02

        # =============================================
        # TABLE PRIORITY
        # =============================================

        elif source == "table":

            confidence += 0.01

        entity["confidence"] = round(

            min(confidence, 0.99),

            4
        )

    return boosted

# =========================================================
# MAIN HYBRID ENGINE
# =========================================================

def process_hybrid_entities(

    nlp_entities,

    layout_fields=None,

    table_data=None,

    document_type="unknown"
):

    try:

        log_info(
            "Starting hybrid entity fusion"
        )

        # =================================================
        # BASE ENTITIES
        # =================================================

        final_entities = []

        # =================================================
        # NLP ENTITIES
        # =================================================

        if nlp_entities:

            final_entities.extend(
                nlp_entities
            )

        # =================================================
        # LAYOUT ENTITIES
        # =================================================

        layout_entities = convert_layout_fields(
            layout_fields
        )

        final_entities.extend(
            layout_entities
        )

        # =================================================
        # TABLE ENTITIES
        # =================================================

        table_entities = extract_table_entities(
            table_data
        )

        final_entities.extend(
            table_entities
        )

        # =================================================
        # CONFIDENCE BOOSTING
        # =================================================

        final_entities = apply_priority_boosting(
            final_entities
        )

        # =================================================
        # DEDUPLICATION
        # =================================================

        final_entities = deduplicate_entities(
            final_entities
        )

        # =================================================
        # SORT
        # =================================================

        final_entities = sorted(

            final_entities,

            key=lambda x: (

                x.get(
                    "confidence",
                    0
                )
            ),

            reverse=True
        )

        # =================================================
        # DEBUG OUTPUT
        # =================================================

        print(
            "\n========== HYBRID ENGINE ==========\n"
        )

        print(
            f"FINAL HYBRID ENTITIES: "
            f"{len(final_entities)}"
        )

        for entity in final_entities[:20]:

            print(entity)

        log_info(
            f"Hybrid fusion completed "
            f"with {len(final_entities)} entities"
        )

        return {

            "success": True,

            "entities": final_entities
        }

    except Exception as e:

        log_exception(
            f"Hybrid engine failed: {str(e)}"
        )

        return {

            "success": False,

            "entities": []
        }