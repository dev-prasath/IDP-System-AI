import cv2
import numpy as np


def preprocess_image(image):

    # Convert PIL image to numpy array
    image = np.array(image)

    # Convert RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # =========================
    # IMAGE UPSCALING
    # =========================

    scale_percent = 200

    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    image = cv2.resize(
        image,
        (width, height),
        interpolation=cv2.INTER_CUBIC
    )

    # =========================
    # GRAYSCALE
    # =========================

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # =========================
    # DENOISING
    # =========================

    filtered = cv2.bilateralFilter(
        gray,
        9,
        75,
        75
    )

    # =========================
    # ADAPTIVE THRESHOLDING
    # =========================

    thresh = cv2.adaptiveThreshold(
        filtered,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    # =========================
    # LIGHT MORPHOLOGY
    # =========================

    kernel = np.ones((1, 1), np.uint8)

    processed = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    # =========================
    # SHARPENING
    # =========================

    sharpening_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    processed = cv2.filter2D(
        processed,
        -1,
        sharpening_kernel
    )

    # =========================
    # CONVERT BACK TO RGB
    # =========================

    processed = cv2.cvtColor(
        processed,
        cv2.COLOR_GRAY2RGB
    )

    return processed