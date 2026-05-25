# =========================================================
# EASYOCR ENGINE
# =========================================================

from email.mime import image

import easyocr
import numpy as np
from PIL import Image
import cv2

reader = None


def load_easyocr():

    global reader

    if reader is None:

        reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    return reader

# =========================================================
# OCR EXTRACTION
# =========================================================

def extract_text_and_boxes(image):

    try:

        # =================================================
        # IMAGE CONVERSION
        # =================================================

        if isinstance(image, Image.Image):

            image = np.array(image)

        # =================================================
        # HANDLE GRAYSCALE
        # =================================================

        if len(image.shape) == 2:

            image = cv2.cvtColor(
                image,
                cv2.COLOR_GRAY2RGB
            )

        # =================================================
        # OCR
        # =================================================

        ocr_reader = load_easyocr()

        results = ocr_reader.readtext(image)

        extracted_text = []
        boxes = []
        confidence_scores = []

        # =================================================
        # DEBUG
        # =================================================

        print("\n================ OCR RESULTS ================\n")
        print(results)

        # =================================================
        # PARSE RESULTS
        # =================================================

        for result in results:

            try:

                # =========================================
                # SAFELY HANDLE DIFFERENT OUTPUT FORMATS
                # =========================================

                if not isinstance(result, (list, tuple)):

                    continue

                if len(result) < 3:

                    continue

                bbox = result[0]
                text = result[1]
                confidence = result[2]

                # =========================================
                # VALIDATE TYPES
                # =========================================

                if not isinstance(bbox, (list, tuple)):

                    continue

                if not isinstance(text, str):

                    text = str(text)

                try:

                    confidence = float(confidence)

                except Exception:

                    confidence = 0.0

                # =========================================
                # STORE TEXT
                # =========================================

                extracted_text.append(text)

                confidence_scores.append(confidence)

                # =========================================
                # FORMAT BOX
                # =========================================

                formatted_points = []

                for point in bbox:

                    try:

                        x = int(point[0])
                        y = int(point[1])

                        formatted_points.append([x, y])

                    except Exception:

                        continue

                formatted_box = {
                    "text": text,
                    "confidence": round(
                        confidence * 100,
                        2
                    ),
                    "box": formatted_points
                }

                boxes.append(formatted_box)

            except Exception as parse_error:

                print(
                    "OCR Parsing Error:",
                    parse_error
                )

                print(
                    "Problematic Result:",
                    result
                )

                continue

        # =================================================
        # FINAL TEXT
        # =================================================

        final_text = "\n".join(extracted_text)

        # =================================================
        # OCR CONFIDENCE
        # =================================================

        if confidence_scores:

            average_confidence = round(
                (
                    sum(confidence_scores)
                    / len(confidence_scores)
                ) * 100,
                2
            )

        else:

            average_confidence = 0

        # =================================================
        # RETURN
        # =================================================

        return {
            "success": True,
            "ocr_text": final_text,
            "boxes": boxes,
            "ocr_confidence": average_confidence
        }

    except Exception as e:

        print(
            "OCR ENGINE ERROR:",
            str(e)
        )

        return {
            "success": False,
            "message": str(e),
            "ocr_text": "",
            "boxes": [],
            "ocr_confidence": 0
        }