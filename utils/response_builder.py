# =========================================================
# utils/response_builder.py
# =========================================================


def build_response(
    document_type,
    ocr_text,
    boxes,
    entities,
    ocr_confidence,
    table_data
):

    """
    Build standardized API response.
    """

    structured_output = {}

    for entity in entities:

        label = entity["label"]
        text = entity["text"]

        structured_output[label] = text

    response = {

        "success": True,

        "document_type": document_type,

        "ocr_text": ocr_text,

        "boxes": boxes,

        "entities": entities,

        "ocr_confidence": ocr_confidence,

        "structured_output": structured_output,

        "table_data": table_data
    }

    return response