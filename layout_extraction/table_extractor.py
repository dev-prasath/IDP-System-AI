# =========================================================
# layout_extraction/table_extractor.py
# SPATIAL TABLE EXTRACTION ENGINE
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import pandas as pd
from rapidfuzz import fuzz

# =========================================================
# POSSIBLE TABLE HEADERS
# =========================================================

TABLE_HEADERS = [

    "item",
    "description",
    "qty",
    "quantity",
    "price",
    "rate",
    "amount",
    "total"
]

HEADER_ALIASES = {

    "descriptions": "DESCRIPTION",

    "description": "DESCRIPTION",

    "qty": "QTY",

    "quantity": "QTY",

    "unit price": "UNIT PRICE",

    "amount": "AMOUNT",

    "total": "TOTAL"
}

# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    return str(text).strip().lower()

# =========================================================
# DETECT TABLE HEADER ROW
# =========================================================

def detect_header_row(rows):

    """
    Detect probable table header row
    using fuzzy OCR matching.
    """

    best_row_index = None

    best_match_score = 0

    try:

        # =================================================
        # ITERATE ROWS
        # =================================================

        for index, row in enumerate(rows):

            texts = [

                normalize_text(
                    item["text"]
                )

                for item in row
            ]

            row_score = 0

            matched_headers = []

            # =============================================
            # CHECK EACH OCR WORD
            # =============================================

            for text in texts:

                matched_header = fuzzy_match_header(
                    text
                )

                if matched_header:

                    row_score += 1

                    matched_headers.append(
                        matched_header
                    )

            # =============================================
            # BONUS FOR MULTIPLE HEADERS
            # =============================================

            unique_matches = len(

                set(matched_headers)
            )

            # =============================================
            # UPDATE BEST ROW
            # =============================================

            if unique_matches > best_match_score:

                best_match_score = (
                    unique_matches
                )

                best_row_index = index

        # =================================================
        # VALIDATE HEADER ROW
        # =================================================

        if best_match_score >= 2:

            print(
                "\n========== HEADER ROW DETECTED ==========\n"
            )

            print(
                f"ROW INDEX: {best_row_index}"
            )

            print(
                f"MATCH SCORE: {best_match_score}"
            )

            return best_row_index

        # =================================================
        # NO HEADER FOUND
        # =================================================

        print(
            "\nNO TABLE HEADER DETECTED\n"
        )

        return None

    except Exception as e:

        print(
            "HEADER DETECTION ERROR:",
            str(e)
        )

        return None
# =========================================================
# EXTRACT COLUMN STRUCTURE
# =========================================================

def extract_columns(header_row):

    """
    Build spatially sorted
    table columns.
    """

    columns = []

    for item in header_row:

        # =============================================
        # OCR TEXT
        # =============================================

        text = normalize_text(
            item["text"]
        )

        # =============================================
        # FUZZY HEADER MATCH
        # =============================================

        matched_header = fuzzy_match_header(
            text
        )

        # =============================================
        # SKIP UNKNOWN HEADERS
        # =============================================

        if not matched_header:
            continue

        # =============================================
        # BUILD COLUMN
        # =============================================

        columns.append({

            "header": normalize_header(
                matched_header
            ),

            "x_center": item["center_x"],

            "x_min": item["x_min"],

            "x_max": item["x_max"]
        })

    # =====================================================
    # SORT LEFT TO RIGHT
    # =====================================================

    columns = sorted(

        columns,

        key=lambda x: x["x_center"]
    )

    print(
        "\n========== DETECTED COLUMNS ==========\n"
    )

    for column in columns:

        print(column)

    return columns
# =========================================================
# FIND CLOSEST COLUMN
# =========================================================

# =========================================================
# CREATE COLUMN BOUNDARIES
# =========================================================

def create_column_boundaries(columns):

    """
    Create spatial ranges for columns.
    """

    boundaries = []

    for index, column in enumerate(columns):

        current_x = column["x_center"]

        # =============================================
        # LEFT BOUNDARY
        # =============================================

        if index == 0:

            left_boundary = 0

        else:

            previous_x = columns[
                index - 1
            ]["x_center"]

            left_boundary = (
                previous_x + current_x
            ) / 2

        # =============================================
        # RIGHT BOUNDARY
        # =============================================

        if index == len(columns) - 1:

            right_boundary = 99999

        else:

            next_x = columns[
                index + 1
            ]["x_center"]

            right_boundary = (
                current_x + next_x
            ) / 2

        boundaries.append({

            "header": column["header"],

            "left": left_boundary,

            "right": right_boundary
        })

    return boundaries
# =========================================================
# EXTRACT TABLE DATA
# =========================================================

def extract_table_data(rows):

    """
    Extract structured table
    from grouped OCR rows.
    """

    try:

        # =============================================
        # DETECT HEADER
        # =============================================

        header_index = detect_header_row(
            rows
        )

        if header_index is None:

            return []

        # =============================================
        # HEADER ROW
        # =============================================

        header_row = rows[
            header_index
        ]

        columns = extract_columns(
            header_row
        )
        boundaries = create_column_boundaries(
            columns
        )

        table_data = []

        # =============================================
        # PROCESS DATA ROWS
        # =============================================

        for row in rows[
            header_index + 1:
        ]:

            row_data = {}

            for item in row:

                header = find_column_by_position(

                    item["center_x"],

                    boundaries
                )

                if header:

                    row_data[
                        header
                    ] = item["text"]

            # =========================================
            # VALIDATE ROW
            # =========================================

            if len(row_data) >= 2:

                table_data.append(
                    row_data
                )

        return table_data

    except Exception as e:

        print(
            "TABLE EXTRACTION ERROR:",
            str(e)
        )

        return []

# =========================================================
# CONVERT TO DATAFRAME
# =========================================================

def table_to_dataframe(table_data):

    """
    Convert table JSON
    into DataFrame.
    """

    if not table_data:

        return pd.DataFrame()

    return pd.DataFrame(
        table_data
    )


# =========================================================
# FIND COLUMN USING SPATIAL RANGE
# =========================================================

def find_column_by_position(

    x_center,

    boundaries
):

    """
    Match text using
    column spatial boundaries.
    """

    for boundary in boundaries:

        if (

            boundary["left"]

            <= x_center

            <= boundary["right"]

        ):

            return boundary["header"]

    return None

# =========================================================
# NORMALIZE HEADER
# =========================================================

def normalize_header(text):

    text = normalize_text(text)

    for key, value in HEADER_ALIASES.items():

        if key in text:

            return value

    return text.upper()

# =========================================================
# FUZZY HEADER MATCH
# =========================================================

def fuzzy_match_header(text):

    """
    Match noisy OCR headers.
    """

    normalized = normalize_text(text)

    best_match = None

    best_score = 0

    for header in TABLE_HEADERS:

        score = fuzz.partial_ratio(

            normalized,
            header
        )

        if score > best_score:

            best_score = score
            best_match = header

    # =============================================
    # ACCEPT MATCH
    # =============================================

    if best_score >= 70:

        return best_match

    return None