# =====================================================
# IMPORTS
# =====================================================

import json
import numpy as np

from PIL import Image

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    GlobalAveragePooling2D
)
from tensorflow.keras.models import Sequential

# =====================================================
# PATHS
# =====================================================

WEIGHTS_PATH = r"E:\Data_Science\Guvi_Capstone Project\Intelligent Document Processing System\models\document_classifier.weights.h5"

LABEL_PATH = r"E:\Data_Science\Guvi_Capstone Project\Intelligent Document Processing System\models\document_labels.json"

# =====================================================
# LOAD LABELS
# =====================================================

with open(LABEL_PATH, "r") as f:

    labels = json.load(f)

print("✅ Labels loaded")

# =====================================================
# REBUILD MODEL ARCHITECTURE
# =====================================================

print("Building MobileNetV2 architecture...")

base_model = MobileNetV2(

    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)

)

base_model.trainable = False

model = Sequential([

    base_model,

    GlobalAveragePooling2D(),

    Dropout(0.3),

    Dense(256, activation="relu"),

    Dropout(0.3),

    Dense(16, activation="softmax")

])

# =====================================================
# LOAD WEIGHTS
# =====================================================

print("Loading weights...")

model.load_weights(WEIGHTS_PATH)

print("✅ Weights loaded successfully!")

# =====================================================
# IMAGE PREPROCESSING
# =====================================================

def preprocess_image(image):

    image = image.resize((224, 224))

    image = np.array(image)

    image = image.astype("float32") / 255.0

    image = np.expand_dims(image, axis=0)

    return image

# =====================================================
# CLASSIFIER
# =====================================================

def classify_document(image):

    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)

    predicted_index = int(np.argmax(predictions))

    confidence = float(np.max(predictions)) * 100

    # Reverse label mapping
    index_to_label = {

        value: key

        for key, value in labels.items()

    }

    predicted_label = index_to_label[predicted_index]

    return {

        "document_type": predicted_label,

        "confidence": round(confidence, 2)

    }