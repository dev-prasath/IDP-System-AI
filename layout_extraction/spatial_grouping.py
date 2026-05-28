# =========================================================
# layout_extraction/spatial_grouping.py
# SPATIAL LAYOUT GROUPING ENGINE
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from layout_extraction.coordinate_utils import (
    enrich_ocr_boxes,
    sort_boxes
)

# =========================================================
# GROUP BOXES INTO ROWS
# =========================================================

def group_boxes_into_rows(

    boxes,

    y_threshold=25
):

    """
    Group OCR boxes into rows
    using Y-coordinate similarity.

    Args:
        boxes (list)

    Returns:
        list:
            Grouped rows
    """

    try:

        # =============================================
        # ENRICH BOXES
        # =============================================

        enriched_boxes = enrich_ocr_boxes(
            boxes
        )

        # =============================================
        # SORT NATURALLY
        # =============================================

        enriched_boxes = sort_boxes(
            enriched_boxes
        )

        rows = []

        # =============================================
        # GROUPING LOGIC
        # =============================================

        for current_box in enriched_boxes:

            added_to_row = False

            current_y = current_box[
                "center_y"
            ]

            # =========================================
            # TRY TO MATCH EXISTING ROW
            # =========================================

            for row in rows:

                row_y = row[0][
                    "center_y"
                ]

                if abs(
                    current_y - row_y
                ) <= y_threshold:

                    row.append(
                        current_box
                    )

                    added_to_row = True

                    break

            # =========================================
            # CREATE NEW ROW
            # =========================================

            if not added_to_row:

                rows.append([
                    current_box
                ])

        # =============================================
        # SORT EACH ROW LEFT TO RIGHT
        # =============================================

        final_rows = []

        for row in rows:

            sorted_row = sorted(

                row,

                key=lambda x: x["x_min"]
            )

            final_rows.append(
                sorted_row
            )

        return final_rows

    except Exception as e:

        print(
            "ROW GROUPING ERROR:",
            str(e)
        )

        return []

# =========================================================
# CONVERT ROWS TO TEXT
# =========================================================

def rows_to_text(rows):

    """
    Convert grouped rows
    into readable text.

    Args:
        rows (list)

    Returns:
        list
    """

    formatted_rows = []

    for row in rows:

        row_text = " | ".join(

            item["text"]

            for item in row
        )

        formatted_rows.append(
            row_text
        )

    return formatted_rows

# =========================================================
# DEBUG PRINT ROWS
# =========================================================

def print_grouped_rows(rows):

    """
    Debug grouped OCR rows.
    """

    print(
        "\n========== GROUPED ROWS ==========\n"
    )

    for index, row in enumerate(rows):

        texts = [

            item["text"]

            for item in row
        ]

        print(
            f"ROW {index + 1}:",
            texts
        )