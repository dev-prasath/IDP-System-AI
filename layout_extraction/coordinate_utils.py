# =========================================================
# layout_extraction/coordinate_utils.py
# OCR BOX COORDINATE UTILITIES
# =========================================================

# =========================================================
# GET BOX DIMENSIONS
# =========================================================

def get_box_dimensions(box):

    """
    Extract spatial coordinates from OCR polygon.

    Args:
        box (list):
            OCR polygon points

    Returns:
        dict:
            Spatial coordinates
    """

    try:

        if not box or len(box) < 4:

            return None

        x_coords = [point[0] for point in box]
        y_coords = [point[1] for point in box]

        x_min = min(x_coords)
        y_min = min(y_coords)

        x_max = max(x_coords)
        y_max = max(y_coords)

        width = x_max - x_min
        height = y_max - y_min

        center_x = x_min + (width / 2)
        center_y = y_min + (height / 2)

        return {

            "x_min": x_min,
            "y_min": y_min,

            "x_max": x_max,
            "y_max": y_max,

            "width": width,
            "height": height,

            "center_x": center_x,
            "center_y": center_y
        }

    except Exception:

        return None

# =========================================================
# ENRICH OCR BOXES
# =========================================================

def enrich_ocr_boxes(boxes):

    """
    Add spatial metadata to OCR boxes.

    Args:
        boxes (list)

    Returns:
        list
    """

    enriched_boxes = []

    for item in boxes:

        try:

            polygon = item.get("box", [])

            dimensions = get_box_dimensions(
                polygon
            )

            if dimensions is None:
                continue

            enriched_item = {

                "text": item.get(
                    "text",
                    ""
                ),

                "confidence": item.get(
                    "confidence",
                    0
                ),

                "box": polygon,

                **dimensions
            }

            enriched_boxes.append(
                enriched_item
            )

        except Exception:
            continue

    return enriched_boxes

# =========================================================
# SORT BOXES TOP TO BOTTOM
# =========================================================

def sort_boxes(boxes):

    """
    Sort OCR boxes naturally.

    Returns:
        list
    """

    return sorted(

        boxes,

        key=lambda b: (

            b["y_min"],
            b["x_min"]
        )
    )