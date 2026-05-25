import os

os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"

import re
import traceback

from transformers import pipeline

from nlp.regex_patterns import (
    extract_regex_entities
)

ner_pipeline = None

def load_ner_model():

    global ner_pipeline

    if ner_pipeline is None:

        print("\nLoading HuggingFace NER model...")

        ner_pipeline = pipeline(

            task="ner",

            model="dslim/bert-base-NER",

            tokenizer="dslim/bert-base-NER",

            aggregation_strategy="simple"
        )

        print("NER model loaded successfully.")

    return ner_pipeline

def clean_text(text):

    # Remove non-ascii characters
    text = re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text
    )

    # Remove extra spaces/newlines
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def is_valid_entity(text):

    if not text:

        return False

    if len(text.strip()) < 3:

        return False

    if text.isdigit():

        return False

    junk_patterns = [

        "semester",
        "subject code",
        "grade",
        "nov",
        "may",
        "page",
        "exam",
        "university"
    ]

    lower_text = text.lower()

    for pattern in junk_patterns:

        if pattern in lower_text:

            return False

    return True


def normalize_label(label):

    mapping = {

        "PER": "PERSON",

        "ORG": "ORGANIZATION",

        "LOC": "LOCATION",

        "MISC": "MISCELLANEOUS"
    }

    return mapping.get(
        label,
        label
    )

# =========================================================
# EXTRACT ENTITIES
# =========================================================

def extract_entities(text):

    try:

        # =================================================
        # INPUT VALIDATION
        # =================================================

        if text is None:

            raise ValueError(
                "Input text is None"
            )

        if not isinstance(text, str):

            raise TypeError(
                f"Expected string but got {type(text)}"
            )

        if len(text.strip()) == 0:

            print("Empty text received for NER.")

            return []

        # =================================================
        # CLEAN TEXT
        # =================================================

        text = clean_text(text)

        # =================================================
        # LIMIT VERY LARGE TEXT
        # =================================================

        MAX_TEXT_LENGTH = 4000

        if len(text) > MAX_TEXT_LENGTH:

            print(
                f"Text truncated from "
                f"{len(text)} to "
                f"{MAX_TEXT_LENGTH} characters"
            )

            text = text[:MAX_TEXT_LENGTH]

        # =================================================
        # DEBUG LOGS
        # =================================================

        print("\n========== ENTITY EXTRACTION ==========")

        print("Text Length:", len(text))

        print("\nSample Text:\n")

        print(text[:500])

        # =================================================
        # LOAD MODEL
        # =================================================

        ner_model = load_ner_model()

        # =================================================
        # RUN NER
        # =================================================

        ner_results = ner_model(text)

        print(
            f"\nNER Results Found: "
            f"{len(ner_results)}"
        )

        extracted_entities = []

        seen = set()

        # =================================================
        # PROCESS ENTITIES
        # =================================================

        for entity in ner_results:

            try:

                entity_text = entity.get(
                    "word",
                    ""
                ).strip()

                confidence = float(
                    entity.get(
                        "score",
                        0
                    )
                )

                label = normalize_label(

                    entity.get(
                        "entity_group",
                        "UNKNOWN"
                    )
                )

                # =========================================
                # CONFIDENCE FILTER
                # =========================================

                if confidence < 0.75:

                    continue

                # =========================================
                # VALIDATION FILTER
                # =========================================

                if not is_valid_entity(
                    entity_text
                ):

                    continue

                # =========================================
                # REMOVE DUPLICATES
                # =========================================

                key = (
                    label,
                    entity_text.lower()
                )

                if key in seen:

                    continue

                seen.add(key)

                # =========================================
                # FINAL ENTITY
                # =========================================

                extracted_entities.append({

                    "label": label,

                    "text": entity_text,

                    "confidence": round(
                        confidence,
                        3
                    )
                })

            except Exception as entity_error:

                print(
                    "\nError processing entity:"
                )

                print(entity_error)

                continue

        # =================================================
        # REGEX ENTITIES
        # =================================================

        try:

            regex_entities = extract_regex_entities(
                text
            )

        except Exception as regex_error:

            print(
                "\nRegex extraction failed:"
            )

            print(regex_error)

            regex_entities = []

        # =================================================
        # MERGE ENTITIES
        # =================================================

        all_entities = (

            extracted_entities

            + regex_entities
        )

        print(
            f"\nFinal Entities Extracted: "
            f"{len(all_entities)}"
        )

        return all_entities

    except Exception as e:

        print(
            "\n========== ENTITY EXTRACTION FAILED =========="
        )

        traceback.print_exc()

        return [{
            "label": "ERROR",
            "text": str(e),
            "confidence": 0.0
        }]