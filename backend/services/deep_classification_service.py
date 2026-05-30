# =====================================================
# DEEP DOCUMENT CLASSIFICATION SERVICE
# =====================================================

import json
import numpy as np

from PIL import Image

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    GlobalAveragePooling2D,
    Dropout,
    Dense
)

from tensorflow.keras.applications import (
    MobileNetV2,
    EfficientNetB3
)

# =====================================================
# BUILD MOBILENETV2
# =====================================================

def build_mobilenet_model():

    base_model = MobileNetV2(
        weights=None,
        include_top=False,
        input_shape=(224, 224, 3)
    )

    model = Sequential([

        base_model,

        GlobalAveragePooling2D(),

        Dropout(0.3),

        Dense(
            256,
            activation="relu"
        ),

        Dropout(0.3),

        Dense(
            16,
            activation="softmax"
        )
    ])

    return model


# =====================================================
# BUILD EFFICIENTNETB3
# =====================================================

def build_efficientnet_model():

    base_model = EfficientNetB3(
        weights=None,
        include_top=False,
        input_shape=(300, 300, 3)
    )

    model = Sequential([

        base_model,

        GlobalAveragePooling2D(),

        Dropout(0.4),

        Dense(
            256,
            activation="relu"
        ),

        Dropout(0.3),

        Dense(
            16,
            activation="softmax"
        )
    ])

    return model


# =====================================================
# LOAD LABELS
# =====================================================

with open(
    "models/MobileNetV2/document_labels.json",
    "r"
) as f:

    LABELS = json.load(f)

INDEX_TO_LABEL = {

    value: key

    for key, value in LABELS.items()

}


# =====================================================
# LOAD MODELS + WEIGHTS
# =====================================================

print("Loading MobileNetV2...")

MOBILENET_MODEL = build_mobilenet_model()

MOBILENET_MODEL.load_weights(
    "models/MobileNetV2/document_classifier.weights.h5"
)

print("MobileNetV2 Loaded")


print("Loading EfficientNetB3...")

EFFICIENTNET_MODEL = build_efficientnet_model()

EFFICIENTNET_MODEL.load_weights(
    "models/EfficientNetB3/document_classifier.weights.h5"
)

print("EfficientNetB3 Loaded")


# =====================================================
# PREPROCESS
# =====================================================

def preprocess_mobilenet(image):

    image = image.convert("RGB")

    image = image.resize((224, 224))

    image = np.array(image)

    image = image.astype("float32") / 255.0

    image = np.expand_dims(
        image,
        axis=0
    )

    return image


def preprocess_efficientnet(image):

    image = image.convert("RGB")

    image = image.resize((300, 300))

    image = np.array(image)

    image = image.astype("float32") / 255.0

    image = np.expand_dims(
        image,
        axis=0
    )

    return image


# =====================================================
# MOBILENET PREDICTION
# =====================================================

def predict_mobilenet(image):

    print("\nRUNNING MOBILENET")
    processed_image = preprocess_mobilenet(
        image
    )

    predictions = MOBILENET_MODEL.predict(
        processed_image,
        verbose=0
    )

    class_id = int(
        np.argmax(predictions)
    )

    confidence = float(
        np.max(predictions)
    )

    label = INDEX_TO_LABEL.get(
        class_id,
        "unknown"
    )

    print("\n===== MOBILENET =====")
    print("Class ID:", class_id)
    print("Label:", label)
    print("Confidence:", confidence)

    return {

        "model": "MobileNetV2",

        "label": label,

        "confidence": round(
            confidence * 100,
            2
        )
    }


# =====================================================
# EFFICIENTNET PREDICTION
# =====================================================

def predict_efficientnet(image):
    print("\nRUNNING EFFICIENTNET")
    processed_image = preprocess_efficientnet(
        image
    )

    predictions = EFFICIENTNET_MODEL.predict(
        processed_image,
        verbose=0
    )

    class_id = int(
        np.argmax(predictions)
    )

    confidence = float(
        np.max(predictions)
    )

    label = INDEX_TO_LABEL.get(
        class_id,
        "unknown"
    )
    print("\n===== EFFICIENTNET =====")
    print("Class ID:", class_id)
    print("Label:", label)
    print("Confidence:", confidence)

    return {

        "model": "EfficientNetB3",

        "label": label,

        "confidence": round(
            confidence * 100,
            2
        )
    }


# =====================================================
# BOTH RESULTS
# =====================================================

def classify_document_image(image):

    mobilenet_result = predict_mobilenet(
        image
    )

    efficientnet_result = predict_efficientnet(
        image
    )

    return {

        "mobilenet": mobilenet_result,

        "efficientnet": efficientnet_result
    }


# =====================================================
# BEST RESULT
# =====================================================

def get_best_prediction(image):

    results = classify_document_image(
        image
    )

    mobilenet_result = results[
        "mobilenet"
    ]

    efficientnet_result = results[
        "efficientnet"
    ]

    if (
        efficientnet_result["confidence"]
        >=
        mobilenet_result["confidence"]
    ):

        return efficientnet_result

    return mobilenet_result