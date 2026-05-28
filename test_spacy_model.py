# =========================================================
# TEST_SPACY_MODEL.py
# FULL TESTING SCRIPT
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import spacy

# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = r"E:\Data_Science\Guvi_Capstone Project\Intelligent Document Processing System\models\spaCy"
# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading spaCy model...\n")

nlp = spacy.load(
    MODEL_PATH
)

print("spaCy model loaded successfully!")

# =========================================================
# TEST TEXTS
# =========================================================

test_samples = [

    """
    Invoice Number: INV-2026-101

    GST Number: 33ABCDE1234F1Z5

    Total Amount: ₹45,000

    Contact:
    support@testcompany.com
    +91 9876543210
    """,

    """
    John Doe

    Python Developer

    Skills:
    Python, TensorFlow, NLP, OpenCV

    Email:
    johndoe@gmail.com

    Phone:
    9876543210
    """
]

# =========================================================
# RUN TESTS
# =========================================================

for index, text in enumerate(test_samples):

    print(
        f"\n========== TEST {index + 1} =========="
    )

    doc = nlp(text)

    if len(doc.ents) == 0:

        print(
            "\nNo entities detected."
        )

    else:

        print(
            "\nDetected Entities:\n"
        )

        for ent in doc.ents:

            print(

                f"TEXT: {ent.text}"

                f"\nLABEL: {ent.label_}"

                f"\n"
            )

print(
    "\n========== TESTING COMPLETED =========="
)