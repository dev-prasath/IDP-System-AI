# =====================================================
# IMPORTS
# =====================================================

import json
import numpy as np

from PIL import Image

import tensorflow as tf

from tensorflow.keras.applications import EfficientNetB3

from tensorflow.keras.layers import (
    Dense,
    Dropout,
    GlobalAveragePooling2D
)

# =====================================================
# PATHS
# =====================================================

WEIGHTS_PATH = (
    r"models\EfficientNetB3\document_classifier.weights.h5"
)

LABEL_PATH = (
    r"models\EfficientNetB3\document_labels.json"
)

# =====================================================
# LOAD LABELS
# =====================================================

with open(LABEL_PATH, "r") as f:

    labels = json.load(f)

print("✅ Labels loaded")

# =====================================================
# REVERSE LABEL MAPPING
# =====================================================

index_to_label = {

    value: key

    for key, value in labels.items()

}

# =====================================================
# BUILD EFFICIENTNETB3 MODEL
# =====================================================

print("Building EfficientNetB3 architecture...")

base_model = EfficientNetB3(

    weights="imagenet",

    include_top=False,

    input_shape=(300, 300, 3)

)

base_model.trainable = False

# =====================================================
# FUNCTIONAL MODEL
# =====================================================

inputs = tf.keras.Input(
    shape=(300, 300, 3)
)

x = base_model(
    inputs,
    training=False
)

x = GlobalAveragePooling2D()(x)

x = Dropout(0.4)(x)

x = Dense(
    256,
    activation="relu"
)(x)

x = Dropout(0.3)(x)

outputs = Dense(
    len(labels),
    activation="softmax"
)(x)

model = tf.keras.Model(
    inputs,
    outputs
)

# =====================================================
# BUILD MODEL
# =====================================================

print("Building model layers...")

dummy_input = np.zeros(
    (1, 300, 300, 3),
    dtype=np.float32
)

model(dummy_input)

print("✅ Model built successfully!")

# =====================================================
# LOAD WEIGHTS
# =====================================================

print("Loading model weights...")

model.load_weights(
    WEIGHTS_PATH
)

print("✅ EfficientNetB3 weights loaded successfully!")

# =====================================================
# IMAGE PREPROCESSING
# =====================================================

def preprocess_image(image):

    # RGB conversion
    image = image.convert("RGB")

    # Resize for EfficientNetB3
    image = image.resize((300, 300))

    # Convert to numpy
    image = np.array(image)

    # Normalize
    image = image.astype("float32") / 255.0

    # Add batch dimension
    image = np.expand_dims(
        image,
        axis=0
    )

    return image

# =====================================================
# DOCUMENT CLASSIFIER
# =====================================================

def classify_document(image):

    try:

        processed_image = preprocess_image(image)

        predictions = model.predict(

            processed_image,

            verbose=0

        )

        predicted_index = int(

            np.argmax(predictions)

        )

        confidence = float(

            np.max(predictions)

        ) * 100

        predicted_label = index_to_label[

            predicted_index

        ]

        return {

            "document_type": predicted_label,

            "confidence": round(
                confidence,
                2
            ),

            "success": True
        }

    except Exception as e:

        return {

            "document_type": "unknown",

            "confidence": 0,

            "success": False,

            "error": str(e)
        }