# =========================================================
# utils/highlight_entities.py
# =========================================================

import html
import re

# =========================================================
# ENTITY COLORS
# =========================================================

ENTITY_COLORS = {

    "PERSON": "#2563eb",

    "DATE": "#16a34a",

    "ORG": "#9333ea",

    "INVOICE_NO": "#dc2626",

    "AMOUNT": "#ea580c",

    "ADDRESS": "#0891b2",

    "EMAIL": "#7c3aed",

    "PHONE": "#0f766e",

    "GST_NUMBER": "#be123c",

    "PAN_NUMBER": "#1d4ed8",

    "AADHAAR_NUMBER": "#15803d"
}

# =========================================================
# HIGHLIGHT ENTITIES
# =========================================================

def highlight_entities(

    text,

    entities
):

    """
    Safely highlight entities
    without corrupting HTML.
    """

    # =====================================================
    # ESCAPE HTML FIRST
    # =====================================================

    safe_text = html.escape(text)

    # =====================================================
    # SORT ENTITIES BY LENGTH
    # LONGEST FIRST
    # =====================================================

    sorted_entities = sorted(

        entities,

        key=lambda x: len(
            x.get("text", "")
        ),

        reverse=True
    )

    # =====================================================
    # REPLACE ENTITIES
    # =====================================================

    for entity in sorted_entities:

        entity_text = entity.get(
            "text",
            ""
        ).strip()

        label = entity.get(
            "label",
            "ENTITY"
        )

        confidence = entity.get(
            "confidence",
            0
        )

        if not entity_text:

            continue

        color = ENTITY_COLORS.get(

            label,

            "#facc15"
        )

        # =================================================
        # SAFE HTML BLOCK
        # =================================================

        highlighted = f"""

<span style="
background-color:{color};
color:white;
padding:2px 6px;
border-radius:6px;
font-weight:600;
margin:2px;
display:inline-block;
">

{html.escape(entity_text)}

({confidence}%)

</span>

"""

        # =================================================
        # SAFE REGEX
        # =================================================

        pattern = re.escape(
            html.escape(entity_text)
        )

        safe_text = re.sub(

            pattern,

            highlighted,

            safe_text,

            flags=re.IGNORECASE
        )

    # =====================================================
    # FORMAT OUTPUT
    # =====================================================

    safe_text = safe_text.replace(
        "\n",
        "<br>"
    )

    return safe_text