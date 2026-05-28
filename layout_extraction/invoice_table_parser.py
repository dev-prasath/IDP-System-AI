# =========================================================
# SMART INVOICE TABLE PARSER
# SAFE VERSION
# =========================================================

import re

# =========================================================
# PARSE INVOICE TABLE
# =========================================================

def parse_invoice_table(rows):

    """
    Convert OCR rows into
    structured invoice table.
    """

    parsed_rows = []

    # =====================================================
    # VALIDATION
    # =====================================================

    if rows is None:

        return []

    if not isinstance(rows, list):

        return []

    # =====================================================
    # PROCESS ROWS
    # =====================================================

    for row in rows:

        try:

            # =============================================
            # HANDLE DIFFERENT ROW TYPES
            # =============================================

            if isinstance(row, dict):

                row_text = " ".join(

                    str(value)

                    for value in row.values()
                )

            elif isinstance(row, list):

                row_text = " ".join(

                    str(item)

                    for item in row
                )

            else:

                row_text = str(row)

            row_text = row_text.strip()

            if len(row_text) == 0:

                continue

            # =============================================
            # EXTRACT AMOUNTS
            # =============================================

            amounts = re.findall(

                r"\$?\d+(?:,\d+)?(?:\.\d+)?",

                row_text
            )

            # =============================================
            # QUANTITY
            # =============================================

            qty_match = re.search(

                r"\b\d+\b",

                row_text
            )

            quantity = (

                qty_match.group()

                if qty_match

                else ""
            )

            # =============================================
            # DESCRIPTION
            # =============================================

            description = re.sub(

                r"\$?\d+(?:,\d+)?(?:\.\d+)?",

                "",

                row_text
            ).strip()

            # =============================================
            # SKIP EMPTY
            # =============================================

            if len(description) == 0:

                continue

            # =============================================
            # FINAL ROW
            # =============================================

            parsed_rows.append({

                "description": description,

                "quantity": quantity,

                "amounts": amounts
            })

        except Exception as row_error:

            print(
                f"Invoice Row Error: {row_error}"
            )

            continue

    return parsed_rows