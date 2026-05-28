# =========================================================
# layout_extraction/layout_parser.py
# MASTER LAYOUT INTELLIGENCE ENGINE
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from layout_extraction.spatial_grouping import (
    group_boxes_into_rows
)

from layout_extraction.key_value_extractor import (
    extract_key_value_pairs
)

from layout_extraction.table_extractor import (
    extract_table_data
)

from layout_extraction.invoice_parser import (
    extract_invoice_details
)

from layout_extraction.table_postprocessor import (
    clean_table_data
)

# =========================================================
# DOCUMENT TYPE RULES
# =========================================================

KEY_VALUE_DOCUMENTS = [

    "id card",
    "aadhaar",
    "pan",
    "passport"
]

TABLE_DOCUMENTS = [

    "invoice",
    "receipt",
    "bank statement"
]

# =========================================================
# MAIN LAYOUT PARSER
# =========================================================

def parse_document_layout(

    boxes,

    document_type="unknown"
):

    """
    Main spatial layout parser.
    """

    try:

        # =============================================
        # NORMALIZE TYPE
        # =============================================

        document_type = str(
            document_type
        ).lower()

        # =============================================
        # GROUP ROWS
        # =============================================

        rows = group_boxes_into_rows(
            boxes
        )

        # =============================================
        # BASE RESPONSE
        # =============================================

        layout_result = {

            "rows": rows,

            "key_value_data": {},

            "table_data": [],

            "layout_type": "unknown"
        }

        # =============================================
        # KEY VALUE EXTRACTION
        # =============================================

        if any(

            doc_type in document_type

            for doc_type in KEY_VALUE_DOCUMENTS
        ):

            key_value_data = (
                extract_key_value_pairs(
                    rows
                )
            )

            layout_result[
                "key_value_data"
            ] = key_value_data

            layout_result[
                "layout_type"
            ] = "key_value"

            invoice_details = (
                extract_invoice_details(

                    rows,

                    table_data
                )
            )

            layout_result[
                "invoice_details"
            ] = invoice_details

        # =============================================
        # TABLE EXTRACTION
        # =============================================

        elif any(

            doc_type in document_type

            for doc_type in TABLE_DOCUMENTS
        ):

            table_data = (
                extract_table_data(
                    rows
                )
            )

            processed_table = clean_table_data(
                table_data
            )

            table_data = processed_table.get(
                "cleaned_table",
                []
            )

            summary_data = processed_table.get(
                "summary_data",
                {}
            )

            layout_result[
                "summary_data"
            ] = summary_data

            layout_result[
                "table_data"
            ] = table_data

            layout_result[
                "layout_type"
            ] = "table"

        # =============================================
        # MIXED EXTRACTION
        # =============================================

        else:

            key_value_data = (
                extract_key_value_pairs(
                    rows
                )
            )

            table_data = (
                extract_table_data(
                    rows
                )
            )

            layout_result[
                "key_value_data"
            ] = key_value_data

            layout_result[
                "table_data"
            ] = table_data

            layout_result[
                "layout_type"
            ] = "mixed"

        return layout_result

    except Exception as e:

        print(
            "LAYOUT PARSER ERROR:",
            str(e)
        )

        return {

            "rows": [],

            "key_value_data": {},

            "table_data": [],

            "layout_type": "unknown"
        }