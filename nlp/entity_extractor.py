# =========================================================
# nlp/entity_extractor.py
# ENTERPRISE HYBRID ENTITY EXTRACTION ENGINE
# spaCy + Regex + Basic NLP
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import os
import re
import traceback
import spacy

os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"

# =========================================================
# REGEX EXTRACTION
# =========================================================

from nlp.regex_patterns import (
    extract_regex_entities
)

# =========================================================
# LOGGER
# =========================================================

from utils.logger import (
    log_info,
    log_error,
    log_exception
)

# =========================================================
# SPACY MODEL PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SPACY_MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "spaCy"
)

# =========================================================
# LOAD SPACY MODEL
# =========================================================

nlp = None

def load_spacy_model():

    global nlp

    try:

        if nlp is None:

            log_info(
                f"Loading spaCy model from: "
                f"{SPACY_MODEL_PATH}"
            )

            nlp = spacy.load(
                SPACY_MODEL_PATH
            )

            log_info(
                "spaCy model loaded successfully"
            )

        return nlp

    except Exception as e:

        log_exception(
            f"Failed to load spaCy model: {str(e)}"
        )

        return None

# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if text is None:

        return ""

    text = str(text)

    # Remove non-ascii
    text = re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# =========================================================
# CLEAN ENTITY TEXT
# =========================================================

def clean_entity_text(text):

    if text is None:

        return ""

    text = str(text)

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# =========================================================
# VALIDATE ENTITY
# =========================================================

def is_valid_entity(text):

    if not text:

        return False

    text = str(text).strip()

    if len(text) < 2:

        return False

    junk_words = [

        "invoice",
        "page",
        "copy",
        "original",
        "university",
        "semester",
        "subject",
        "grade",
        "exam",
        "signature",
        "authorized",
        "customer copy"
    ]

    lower_text = text.lower()

    if lower_text in junk_words:

        return False

    return True

# =========================================================
# NORMALIZE LABEL
# =========================================================

def normalize_label(label):

    label = str(label).upper().strip()

    mapping = {

        "PER": "PERSON",
        "PERSON_NAME": "PERSON",

        "ORG": "ORGANIZATION",
        "COMPANY": "ORGANIZATION",
        "VENDOR": "ORGANIZATION",

        "LOC": "LOCATION",
        "GPE": "LOCATION",

        "MAIL": "EMAIL",
        "MOBILE": "PHONE",
        "CONTACT": "PHONE",

        "INVOICE_NO": "INVOICE_NUMBER",
        "INVOICE_NUM": "INVOICE_NUMBER",
        "BILL_NO": "INVOICE_NUMBER",

        "GST_NUMBER": "GST",
        "PAN_NUMBER": "PAN",

        "TOTAL": "AMOUNT",
        "TOTAL_AMOUNT": "AMOUNT"
    }

    return mapping.get(
        label,
        label
    )

# =========================================================
# CREATE ENTITY
# =========================================================

def create_entity(
    label,
    text,
    confidence=0.90,
    source="unknown",
    start=0,
    end=0
):

    return {

        "label": normalize_label(label),

        "text": clean_entity_text(text),

        "confidence": round(
            float(confidence),
            4
        ),

        "source": source,

        "start": int(start),

        "end": int(end)
    }

# =========================================================
# DEDUPLICATE ENTITIES
# =========================================================

def deduplicate_entities(entities):

    unique_entities = {}

    for entity in entities:

        label = entity.get(
            "label",
            ""
        )

        text = entity.get(
            "text",
            ""
        ).strip()

        key = (

            label.lower(),

            text.lower()
        )

        # Keep highest confidence entity
        if key not in unique_entities:

            unique_entities[key] = entity

        else:

            existing_confidence = unique_entities[
                key
            ].get(
                "confidence",
                0
            )

            new_confidence = entity.get(
                "confidence",
                0
            )

            if new_confidence > existing_confidence:

                unique_entities[key] = entity

    return list(
        unique_entities.values()
    )

# =========================================================
# BASIC ENTITY EXTRACTION
# FALLBACK NLP
# =========================================================

def extract_basic_entities(text):

    entities = []

    try:

        lines = text.split("\n")

        # =================================================
        # EMAIL
        # =================================================

        emails = re.finditer(

            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',

            text
        )

        for match in emails:

            entities.append(

                create_entity(

                    label="EMAIL",

                    text=match.group(),

                    confidence=0.99,

                    source="basic",

                    start=match.start(),

                    end=match.end()
                )
            )

        # =================================================
        # PHONE
        # =================================================

        phones = re.finditer(

            r'(?:\+91[-\s]?)?[6-9]\d{9}',

            text
        )

        for match in phones:

            entities.append(

                create_entity(

                    label="PHONE",

                    text=match.group(),

                    confidence=0.95,

                    source="basic",

                    start=match.start(),

                    end=match.end()
                )
            )

        # =================================================
        # DATE
        # =================================================

        dates = re.finditer(

            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',

            text
        )

        for match in dates:

            entities.append(

                create_entity(

                    label="DATE",

                    text=match.group(),

                    confidence=0.90,

                    source="basic",

                    start=match.start(),

                    end=match.end()
                )
            )

        # =================================================
        # PERSON NAME EXTRACTION
        # =================================================

        ignored_words = [

            "government",
            "india",
            "male",
            "female",
            "dob",
            "year",
            "aadhaar",
            "address",
            "unique",
            "identification",
            "authority",
            "invoice",
            "amount",
            "quantity",
            "price",
            "total",
            "date",
            "consulting",
            "descriptions"
        ]

        for line in lines:

            line = line.strip()

            # Skip short/long lines
            if len(line) < 5 or len(line) > 40:

                continue

            # Remove symbols
            cleaned = re.sub(

                r'[^A-Za-z\s]',

                '',

                line
            ).strip()

            if len(cleaned) < 5:

                continue

            words = cleaned.split()

            # Accept only realistic names
            if len(words) < 2 or len(words) > 4:

                continue

            lower_line = cleaned.lower()

            bad = False

            for word in ignored_words:

                if word in lower_line:

                    bad = True
                    break

            if bad:

                continue

            # Strong title-case validation
            valid_words = 0

            for word in words:

                if word[:1].isupper():

                    valid_words += 1

            if valid_words >= 2:

                entities.append(

                    create_entity(

                        label="PERSON",

                        text=cleaned,

                        confidence=0.80,

                        source="basic"
                    )
                )

        return entities

    except Exception as e:

        log_exception(
            f"Basic entity extraction failed: {str(e)}"
        )

        return []

# =========================================================
# SPACY ENTITY EXTRACTION
# =========================================================

def extract_spacy_entities(text):

    entities = []

    try:

        model = load_spacy_model()

        if model is None:

            log_error(
                "spaCy model unavailable"
            )

            return []

        doc = model(text)

        for ent in doc.ents:

            entity_text = clean_entity_text(
                ent.text
            )

            entity_label = normalize_label(
                ent.label_
            )

            if not is_valid_entity(
                entity_text
            ):

                if entity_label == "ACCOUNT_NUMBER":

                    if re.match(
                        r'^[\d,]+\.\d{2}$',
                        entity_text
                    ):

                        continue

                if len(entity_text) > 50:

                    continue

            entities.append(

                create_entity(

                    label=entity_label,

                    text=entity_text,

                    confidence=0.95,

                    source="spacy",

                    start=ent.start_char,

                    end=ent.end_char
                )
            )

        log_info(
            f"spaCy extracted "
            f"{len(entities)} entities"
        )

        return entities

    except Exception as e:

        log_exception(
            f"spaCy extraction failed: {str(e)}"
        )

        return []

# =========================================================
# MAIN ENTITY EXTRACTION PIPELINE
# =========================================================

def extract_entities(text):

    try:

        # =================================================
        # VALIDATION
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

            log_error(
                "Empty text received"
            )

            return []

        # =================================================
        # CLEAN TEXT
        # =================================================

        text = clean_text(text)

        # =================================================
        # LIMIT HUGE TEXT
        # =================================================

        MAX_TEXT_LENGTH = 15000

        if len(text) > MAX_TEXT_LENGTH:

            log_info(
                f"Truncating text from "
                f"{len(text)} to "
                f"{MAX_TEXT_LENGTH}"
            )

            text = text[:MAX_TEXT_LENGTH]

        # =================================================
        # DEBUG LOGS
        # =================================================

        print(
            "\n========== ENTITY EXTRACTION =========="
        )

        print(
            f"TEXT LENGTH: {len(text)}"
        )

        print(
            "\nTEXT SAMPLE:\n"
        )

        print(text[:500])

        # =================================================
        # SPACY EXTRACTION
        # =================================================

        try:

            spacy_entities = extract_spacy_entities(
                text
            )

        except Exception as spacy_error:

            print(
                "\nspaCy extraction failed:"
            )

            print(spacy_error)

            spacy_entities = []

        # =================================================
        # REGEX EXTRACTION
        # =================================================

        try:

            regex_entities = extract_regex_entities(
                text
            )

            # Add source if missing
            for entity in regex_entities:

                entity["source"] = "regex"

                entity["label"] = normalize_label(
                    entity.get(
                        "label",
                        "UNKNOWN"
                    )
                )

        except Exception as regex_error:

            print(
                "\nRegex extraction failed:"
            )

            print(regex_error)

            regex_entities = []

        # =================================================
        # BASIC EXTRACTION
        # =================================================

        try:

            basic_entities = extract_basic_entities(
                text
            )

        except Exception as basic_error:

            print(
                "\nBasic extraction failed:"
            )

            print(basic_error)

            basic_entities = []

        # =================================================
        # MERGE ALL ENTITIES
        # =================================================

        all_entities = (

            spacy_entities
            +
            regex_entities
            +
            basic_entities
        )

        # =================================================
        # REMOVE INVALID ENTITIES
        # =================================================

        filtered_entities = []

        for entity in all_entities:

            if is_valid_entity(

                entity.get(
                    "text",
                    ""
                )
            ):

                filtered_entities.append(
                    entity
                )

        # =================================================
        # DEDUPLICATION
        # =================================================

        all_entities = deduplicate_entities(
            filtered_entities
        )

        # =================================================
        # SORT ENTITIES
        # =================================================

        all_entities = sorted(

            all_entities,

            key=lambda x: (

                x.get("label", ""),

                -x.get(
                    "confidence",
                    0
                )
            )
        )

        # =================================================
        # FINAL LOGS
        # =================================================

        print(
            f"\nFINAL ENTITIES: "
            f"{len(all_entities)}"
        )

        for entity in all_entities[:20]:

            print(entity)

        log_info(
            f"Total entities extracted: "
            f"{len(all_entities)}"
        )

        return all_entities

    except Exception as e:

        print(
            "\n========== ENTITY EXTRACTION FAILED =========="
        )

        traceback.print_exc()

        log_exception(
            f"Entity extraction failed: {str(e)}"
        )

        return [{
            "label": "ERROR",
            "text": str(e),
            "confidence": 0.0,
            "source": "system"
        }]