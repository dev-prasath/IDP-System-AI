# =========================================================
# table_service.py
# =========================================================

import pandas as pd


# =========================================================
# SORT BOXES
# =========================================================

def sort_boxes(boxes):

    return sorted(
        boxes,
        key=lambda x: (
            x["box"][0][1],
            x["box"][0][0]
        )
    )


# =========================================================
# GROUP INTO ROWS
# =========================================================

def group_rows(
    boxes,
    row_tolerance=20
):

    rows = []

    current_row = []

    previous_y = None

    for item in boxes:

        y = item["box"][0][1]

        if previous_y is None:

            current_row.append(item)

            previous_y = y

            continue

        if abs(y - previous_y) <= row_tolerance:

            current_row.append(item)

        else:

            rows.append(current_row)

            current_row = [item]

        previous_y = y

    if current_row:

        rows.append(current_row)

    return rows


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if not text:

        return ""

    return (
        str(text)
        .replace("\n", " ")
        .replace("|", "")
        .strip()
    )


# =========================================================
# EXTRACT TABLE
# =========================================================

def extract_table_data(boxes):

    try:

        if not boxes:

            return []

        # =============================================
        # SORT
        # =============================================

        sorted_boxes = sort_boxes(boxes)

        # =============================================
        # GROUP ROWS
        # =============================================

        grouped_rows = group_rows(sorted_boxes)

        table_data = []

        max_columns = 0

        # =============================================
        # BUILD ROWS
        # =============================================

        for row in grouped_rows:

            sorted_row = sorted(
                row,
                key=lambda x: x["box"][0][0]
            )

            row_values = []

            for cell in sorted_row:

                text = clean_text(
                    cell.get("text", "")
                )

                # ignore noisy short values

                if len(text) == 0:

                    continue

                row_values.append(text)

            if len(row_values) >= 2:

                max_columns = max(
                    max_columns,
                    len(row_values)
                )

                table_data.append(row_values)

        # =============================================
        # NORMALIZE ROW LENGTHS
        # =============================================

        normalized_rows = []

        for row in table_data:

            while len(row) < max_columns:

                row.append("")

            normalized_rows.append(row)

        # =============================================
        # DATAFRAME
        # =============================================

        columns = [
            f"Column_{i+1}"
            for i in range(max_columns)
        ]

        df = pd.DataFrame(
            normalized_rows,
            columns=columns
        )

        # =============================================
        # REMOVE EMPTY ROWS
        # =============================================

        df = df.dropna(
            how="all"
        )

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        print(
            f"Table Extraction Error: {e}"
        )

        return []