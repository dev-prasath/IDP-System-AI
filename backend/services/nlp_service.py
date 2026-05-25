# =========================================================
# backend/services/nlp_service.py
# FULL UPDATED VERSION
# =========================================================


from nlp.entity_extractor import (
    extract_entities
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
# PROCESS ENTITIES
# =========================================================

def process_entities(text):

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

            return {

                "success": True,

                "entities": []
            }

        log_info(
            "Starting entity extraction"
        )

        print("\n========== NLP INPUT ==========")

        print("TEXT LENGTH:", len(text))

        print("\nTEXT SAMPLE:\n")

        print(text[:500])

        # =================================================
        # ENTITY EXTRACTION
        # =================================================

        entities = extract_entities(
            text
        )

        # =================================================
        # HANDLE NONE
        # =================================================

        if entities is None:

            entities = []

        log_info(
            f"Extracted "
            f"{len(entities)} entities"
        )

        print("\n========== NLP OUTPUT ==========")

        print(entities)

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        return {

            "success": True,

            "entities": entities
        }

    except Exception as e:

        log_exception(
            f"NLP Service Error: {str(e)}"
        )

        print("\n========== NLP SERVICE FAILED ==========")

        import traceback

        traceback.print_exc()

        return {

            "success": False,

            "entities": [],

            "message": str(e)
        }