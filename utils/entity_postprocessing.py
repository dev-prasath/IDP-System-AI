import re

# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.title()

# =========================================================
# NORMALIZE DATE
# =========================================================

def normalize_date(text):

    text = text.replace(".", "/")
    text = text.replace("-", "/")

    return text

# =========================================================
# PROCESS ENTITIES
# =========================================================

def process_entities(entities):

    processed_entities = []

    seen = set()

    for entity in entities:

        label = entity["label"]

        text = entity["text"]

        confidence = entity.get(
            "confidence",
            0
        )

        # =============================================
        # NORMALIZE TEXT
        # =============================================

        text = normalize_text(text)

        # =============================================
        # NORMALIZE DATE
        # =============================================

        if label == "DATE":

            text = normalize_date(text)

        # =============================================
        # REMOVE DUPLICATES
        # =============================================

        key = (label, text)

        if key in seen:
            continue

        seen.add(key)

        # =============================================
        # FINAL ENTITY
        # =============================================

        processed_entities.append({

            "label": label,

            "text": text,

            "confidence": confidence
        })

    return processed_entities