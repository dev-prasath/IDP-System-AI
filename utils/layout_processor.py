# =========================================================
# IMPORTS
# =========================================================

import cv2
import numpy as np

# =========================================================
# SORT OCR BOXES
# =========================================================

def sort_boxes(boxes):

    """
    Sort OCR boxes top-to-bottom
    and left-to-right.
    """

    boxes = sorted(
        boxes,
        key=lambda x: (
            x["box"][0][1],
            x["box"][0][0]
        )
    )

    return boxes

# =========================================================
# RECONSTRUCT TEXT
# =========================================================

def reconstruct_text(boxes):

    """
    Rebuild OCR text into readable layout.
    """

    sorted_boxes = sort_boxes(boxes)

    lines = []

    current_line = []
    current_y = None

    threshold = 20

    for item in sorted_boxes:

        text = item["text"]

        y = item["box"][0][1]

        if current_y is None:

            current_y = y

        # Same line
        if abs(y - current_y) < threshold:

            current_line.append(text)

        else:

            lines.append(
                " ".join(current_line)
            )

            current_line = [text]

            current_y = y

    # Last line
    if current_line:

        lines.append(
            " ".join(current_line)
        )

    return "\n".join(lines)

# =========================================================
# TEXT REGION VISUALIZATION
# =========================================================

def generate_text_region_visualization(image):

    """
    Detect probable text regions
    and draw bounding boxes.
    """

    try:

        visualization = image.copy()

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2GRAY
        )

        thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY_INV
            + cv2.THRESH_OTSU
        )[1]

        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (15, 5)
        )

        dilated = cv2.dilate(
            thresh,
            kernel,
            iterations=1
        )

        contours, _ = cv2.findContours(
            dilated,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            if w > 40 and h > 10:

                cv2.rectangle(
                    visualization,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

        return visualization

    except Exception:

        return image

# =========================================================
# OCR VISUALIZATION
# =========================================================

def generate_ocr_visualization(
    image,
    boxes
):

    """
    Draw OCR bounding polygons.
    """

    try:

        visualization = image.copy()

        for item in boxes:

            try:

                points = np.array(
                    item["box"]
                ).astype(int)

                cv2.polylines(
                    visualization,
                    [points],
                    isClosed=True,
                    color=(0, 255, 0),
                    thickness=2
                )

            except Exception:

                continue

        return visualization

    except Exception:

        return image