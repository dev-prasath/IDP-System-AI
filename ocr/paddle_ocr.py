# =========================================================
# ocr/paddle_ocr.py
# FULL UPDATED VERSION
# =========================================================

from paddleocr import PaddleOCR

import numpy as np

from PIL import Image

import cv2

# =========================================================
# LOAD OCR MODEL
# =========================================================

ocr_model = PaddleOCR(

    use_angle_cls=True,

    lang='en',

    use_gpu=False
)

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

        results = ocr_model.ocr(

            image,

            cls=True
        )

        extracted_text = []

        boxes = []

        confidence_scores = []

        # =================================================
        # DEBUG
        # =================================================

        print(
            "\n========== PADDLE OCR RESULTS ==========\n"
        )

        print(results)

        # =================================================
        # VALIDATE RESULTS
        # =================================================

        if not results:

            return {

                "success": False,

                "message": "No OCR results found",

                "ocr_text": "",

                "boxes": [],

                "ocr_confidence": 0
            }

        # =================================================
        # PROCESS OCR RESULTS
        # =================================================

        for page in results:

            if not page:
                continue

            for line in page:

                try:

                    # =====================================
                    # VALIDATE LINE
                    # =====================================

                    if len(line) < 2:
                        continue

                    polygon = line[0]

                    text = line[1][0]

                    confidence = float(
                        line[1][1]
                    )

                    # =====================================
                    # FILTER LOW CONFIDENCE
                    # =====================================

                    if confidence < 0.60:
                        continue

                    # =====================================
                    # STORE TEXT
                    # =====================================

                    extracted_text.append(
                        text
                    )

                    confidence_scores.append(
                        confidence
                    )

                    # =====================================
                    # FORMAT POLYGON
                    # =====================================

                    formatted_polygon = []

                    for point in polygon:

                        try:

                            x = int(point[0])

                            y = int(point[1])

                            formatted_polygon.append(
                                [x, y]
                            )

                        except Exception:
                            continue

                    # =====================================
                    # VALIDATE POLYGON
                    # =====================================

                    if len(formatted_polygon) < 4:
                        continue

                    # =====================================
                    # STORE BOX
                    # =====================================

                    boxes.append({

                        "text": text,

                        "confidence": round(
                            confidence * 100,
                            2
                        ),

                        "box": formatted_polygon
                    })

                except Exception as parse_error:

                    print(
                        "OCR Parse Error:",
                        parse_error
                    )

                    continue

        # =================================================
        # FINAL OCR TEXT
        # =================================================

        final_text = "\n".join(
            extracted_text
        )

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

            average_confidence = 0.0

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        return {

            "success": True,

            "ocr_text": final_text,

            "boxes": boxes,

            "ocr_confidence": average_confidence
        }

    except Exception as e:

        print(
            "PADDLE OCR ERROR:",
            str(e)
        )

        return {

            "success": False,

            "message": (
                f"OCR Processing Failed: {str(e)}"
            ),

            "ocr_text": "",

            "boxes": [],

            "ocr_confidence": 0
        }