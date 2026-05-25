from paddleocr import PaddleOCR
import numpy as np

# Initialize OCR model
ocr_model = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    use_gpu=False
)


def extract_text_and_boxes(image):

    try:

        image = np.array(image)

        results = ocr_model.ocr(
            image,
            cls=True
        )

        extracted_text = []
        boxes = []
        confidence_scores = []

        if results and results[0]:

            for line in results[0]:

                box = line[0]
                text = line[1][0]
                score = float(line[1][1])

                # Filter low-confidence OCR
                if score > 0.60:

                    extracted_text.append(text)

                    confidence_scores.append(score)

                    boxes.append({
                        "text": text,
                        "confidence": round(score, 3),
                        "box": box
                    })

        # =========================================
        # OVERALL OCR CONFIDENCE
        # =========================================

        if confidence_scores:

            average_confidence = round(
                (sum(confidence_scores) / len(confidence_scores)) * 100,
                2
            )

        else:

            average_confidence = 0.0

        return (
            " ".join(extracted_text),
            boxes,
            average_confidence
        )

    except Exception as e:

        raise Exception(
            f"OCR Processing Failed: {str(e)}"
        )