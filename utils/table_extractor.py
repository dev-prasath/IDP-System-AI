from collections import defaultdict


def extract_table(boxes):

    rows = defaultdict(list)

    # Group boxes by Y-coordinate
    for item in boxes:

        text = item["text"]

        x = item["box"][0][0]
        y = item["box"][0][1]

        row_key = round(y / 20) * 20

        rows[row_key].append(
            (x, text)
        )

    structured_rows = []

    # Sort rows
    for row in sorted(rows.keys()):

        row_items = sorted(
            rows[row],
            key=lambda x: x[0]
        )

        structured_rows.append(
            [item[1] for item in row_items]
        )

    return structured_rows