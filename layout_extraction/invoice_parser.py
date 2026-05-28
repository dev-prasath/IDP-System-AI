# =========================================================
# layout_extraction/invoice_parser.py
# SPECIALIZED INVOICE PARSER
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import re

# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    return str(text).strip().lower()

# =========================================================
# FIND VALUE NEXT TO LABEL
# =========================================================

def find_value_after_label(

    rows,

    keywords
):

    """
    Find value positioned next
    to invoice keyword.
    """

    for row in rows:

        texts = [

            item["text"]

            for item in row
        ]

        row_text = " ".join(
            texts
        )

        normalized = normalize_text(
            row_text
        )

        for keyword in keywords:

            if keyword in normalized:

                # =====================================
                # RETURN RIGHT SIDE VALUE
                # =====================================

                for item in row:

                    item_text = normalize_text(
                        item["text"]
                    )

                    if keyword not in item_text:

                        return item["text"]

    return None

# =========================================================
# EXTRACT INVOICE DETAILS
# =========================================================

def extract_invoice_details(

    rows,

    table_data
):

    """
    Specialized invoice extraction.
    """

    invoice_data = {

        "invoice_number": None,

        "invoice_date": None,

        "due_date": None,

        "subtotal": None,

        "total_amount": None
    }

    # =====================================================
    # INVOICE NUMBER
    # =====================================================

    invoice_data[
        "invoice_number"
    ] = find_value_after_label(

        rows,

        [

            "invoice #",
            "invoice no",
            "invoice number"
        ]
    )

    # =====================================================
    # INVOICE DATE
    # =====================================================

    invoice_data[
        "invoice_date"
    ] = find_value_after_label(

        rows,

        [

            "invoice date",
            "issue date"
        ]
    )

    # =====================================================
    # DUE DATE
    # =====================================================

    invoice_data[
        "due_date"
    ] = find_value_after_label(

        rows,

        [

            "due date"
        ]
    )

    # =====================================================
    # TOTALS
    # =====================================================

    for row in rows:

        row_text = " ".join(

            item["text"]

            for item in row
        )

        normalized = normalize_text(
            row_text
        )

        amount_match = re.search(

            r'[\$€]?\s?[\d,]+\.\d{2}',

            row_text
        )

        if not amount_match:
            continue

        amount = amount_match.group()

        if "subtotal" in normalized:

            invoice_data[
                "subtotal"
            ] = amount

        elif "total" in normalized:

            invoice_data[
                "total_amount"
            ] = amount

    return invoice_data