# =========================================================
# layout_extraction/table_postprocessor.py
# TABLE CLEANING + ROW MERGING
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import re

# =========================================================
# SUMMARY KEYWORDS
# =========================================================

SUMMARY_KEYWORDS = [

    "subtotal",
    "tax",
    "total",
    "balance",
    "due"
]

# =========================================================
# CHECK SUMMARY ROW
# =========================================================

def is_summary_row(row):

    row_text = " ".join(

        str(value)

        for value in row.values()
    ).lower()

    return any(

        keyword in row_text

        for keyword in SUMMARY_KEYWORDS
    )

# =========================================================
# CHECK MULTILINE DESCRIPTION
# =========================================================

def is_description_continuation(row):

    """
    Detect continuation rows.
    """

    keys = list(row.keys())

    # =============================================
    # ONLY DESCRIPTION PRESENT
    # =============================================

    if len(keys) == 1:

        return True

    return False

# =========================================================
# MERGE MULTILINE ROWS
# =========================================================

def merge_multiline_rows(table_data):

    """
    Merge wrapped descriptions.
    """

    merged_rows = []

    current_row = None

    for row in table_data:

        # =============================================
        # CONTINUATION ROW
        # =============================================

        if is_description_continuation(
            row
        ):

            if current_row:

                description_key = None

                for key in current_row.keys():

                    if "DESC" in key.upper():

                        description_key = key
                        break

                if description_key:

                    continuation_text = list(

                        row.values()

                    )[0]

                    current_row[
                        description_key
                    ] += (

                        " " +

                        continuation_text
                    )

            continue

        # =============================================
        # NEW MAIN ROW
        # =============================================

        if current_row:

            merged_rows.append(
                current_row
            )

        current_row = row

    # =============================================
    # FINAL ROW
    # =============================================

    if current_row:

        merged_rows.append(
            current_row
        )

    return merged_rows

# =========================================================
# EXTRACT SUMMARY ROWS
# =========================================================

def extract_summary_rows(table_data):

    """
    Separate totals from line items.
    """

    cleaned_table = []

    summary_data = {}

    for row in table_data:

        if is_summary_row(row):

            row_text = " ".join(

                str(value)

                for value in row.values()
            ).lower()

            amount = None

            for value in row.values():

                if re.search(

                    r'[\$€]?\s?[\d,]+\.\d{2}',

                    str(value)
                ):

                    amount = value
                    break

            # =========================================
            # MAP SUMMARY FIELD
            # =========================================

            if "subtotal" in row_text:

                summary_data[
                    "subtotal"
                ] = amount

            elif "tax" in row_text:

                summary_data[
                    "tax"
                ] = amount

            elif "total" in row_text:

                summary_data[
                    "total"
                ] = amount

            elif "balance" in row_text:

                summary_data[
                    "balance_due"
                ] = amount

        else:

            cleaned_table.append(
                row
            )

    return cleaned_table, summary_data

# =========================================================
# MAIN CLEANER
# =========================================================

def clean_table_data(table_data):

    """
    Full table postprocessing.
    """

    # =============================================
    # MERGE MULTILINE ROWS
    # =============================================

    merged_table = merge_multiline_rows(
        table_data
    )

    # =============================================
    # EXTRACT SUMMARY
    # =============================================

    cleaned_table, summary_data = (
        extract_summary_rows(
            merged_table
        )
    )

    return {

        "cleaned_table":
            cleaned_table,

        "summary_data":
            summary_data
    }