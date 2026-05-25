import cv2
import numpy as np
import random


def generate_color(entity_name):

    random.seed(entity_name)

    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255)
    )


def highlight_entities(
    image,
    boxes,
    entities
):

    image_array = np.array(image).copy()

    for box_item in boxes:

        text = box_item["text"]

        points = np.array(
            box_item["box"]
        ).astype(int)

        matched_entity = None

        # Match OCR text with entities
        for entity in entities:

            entity_text = entity["text"]

            if entity_text.lower() in text.lower():

                matched_entity = entity["label"]
                break

        # =========================
        # ENTITY BOX
        # =========================

        if matched_entity:

            color = generate_color(
                matched_entity
            )

            thickness = 3

            label = matched_entity

        # =========================
        # NORMAL OCR BOX
        # =========================

        else:

            color = (180, 180, 180)

            thickness = 1

            label = None

        # Draw box
        cv2.polylines(
            image_array,
            [points],
            isClosed=True,
            color=color,
            thickness=thickness
        )

        # Draw label if entity exists
        if label:

            x = points[0][0]
            y = points[0][1] - 10

            cv2.putText(
                image_array,
                label,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    return image_array