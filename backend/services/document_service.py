# =========================================================
# backend/services/document_service.py
# STREAMLIT CLOUD DEPLOYMENT READY VERSION
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import numpy as np
from PIL import Image

# =========================================================
# PREPROCESSING
# =========================================================

from preprocessing.image_processing import (
    preprocess_image
)

# =========================================================
# SERVICES
# =========================================================

from backend.services.ocr_service import (
    process_ocr
)

from backend.services.nlp_service import (
    process_entities
)

from backend.services.classification_service import (
    classify_document
)

# =========================================================
# STRUCTURED OUTPUT
# =========================================================

from utils.structure_output import (
    structure_entities
)

# =========================================================
# RESPONSE BUILDER
# =========================================================

from utils.response_builder import (
    build_response
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
# CONVERT STREAMLIT FILE TO IMAGE
# =========================================================

def convert_uploaded_file_to_image(uploaded_file):

    """
    Converts Streamlit UploadedFile
    into OpenCV/Numpy compatible image.
    """

    try:

        uploaded_file.seek(0)

        pil_image = Image.open(
            uploaded_file
        ).convert("RGB")

        image = np.array(
            pil_image
        )

        return image

    except Exception as e:

        log_exception(
            f"Image Conversion Error: {str(e)}"
        )

        return None

# =========================================================
# PROCESS DOCUMENT
# =========================================================

def process_document(uploaded_file):

    """
    Complete Intelligent Document
    Processing Pipeline.

    Steps:
    1. File Conversion
    2. Image Preprocessing
    3. OCR Extraction
    4. Document Classification
    5. NLP Entity Extraction
    6. Structured Output Generation
    7. Final Response Construction
    """

    try:

        log_info(
            "Starting document processing pipeline"
        )

        # =================================================
        # FILE CONVERSION
        # =================================================

        try:

            document_image = (
                convert_uploaded_file_to_image(
                    uploaded_file
                )
            )

            if document_image is None:

                raise ValueError(
                    "Failed to load image"
                )

            log_info(
                "File conversion completed"
            )

        except Exception as conversion_error:

            log_exception(
                f"File Conversion Error: "
                f"{str(conversion_error)}"
            )

            return {

                "success": False,

                "message": (
                    "Document conversion failed"
                ),

                "error": str(
                    conversion_error
                )
            }

        # =================================================
        # IMAGE PREPROCESSING
        # =================================================

        try:

            processed_image = preprocess_image(
                document_image
            )

            if processed_image is None:

                raise ValueError(
                    "Preprocessed image is None"
                )

            log_info(
                "Image preprocessing completed"
            )

        except Exception as preprocessing_error:

            log_exception(
                f"Preprocessing Error: "
                f"{str(preprocessing_error)}"
            )

            return {

                "success": False,

                "message": (
                    "Image preprocessing failed"
                ),

                "error": str(
                    preprocessing_error
                )
            }

        # =================================================
        # OCR EXTRACTION
        # =================================================

        try:

            ocr_results = process_ocr(
                processed_image
            )

            if not ocr_results.get(
                "success",
                False
            ):

                return {

                    "success": False,

                    "message": (
                        "OCR extraction failed"
                    ),

                    "error": ocr_results.get(
                        "message",
                        "Unknown OCR error"
                    )
                }

            extracted_text = ocr_results.get(
                "ocr_text",
                ""
            )

            boxes = ocr_results.get(
                "boxes",
                []
            )

            ocr_confidence = ocr_results.get(
                "ocr_confidence",
                0.0
            )

            log_info(
                "OCR extraction completed"
            )

        except Exception as ocr_error:

            log_exception(
                f"OCR Error: {str(ocr_error)}"
            )

            return {

                "success": False,

                "message": (
                    "OCR processing crashed"
                ),

                "error": str(ocr_error)
            }

        # =================================================
        # EMPTY OCR CHECK
        # =================================================

        if not extracted_text.strip():

            return {

                "success": False,

                "message": (
                    "No text extracted from document"
                )
            }

        # =================================================
        # DOCUMENT CLASSIFICATION
        # =================================================

        try:

            document_type = classify_document(
                extracted_text
            )

            if not document_type:

                document_type = "Document"

            log_info(
                f"Document classified as: "
                f"{document_type}"
            )

        except Exception as classification_error:

            log_error(
                f"Classification Error: "
                f"{str(classification_error)}"
            )

            document_type = "Document"

        # =================================================
        # NLP ENTITY EXTRACTION
        # =================================================

        try:

            nlp_results = process_entities(
                extracted_text
            )

            if not nlp_results.get(
                "success",
                False
            ):

                return {

                    "success": False,

                    "message": (
                        "Entity extraction failed"
                    ),

                    "error": nlp_results.get(
                        "message",
                        "Unknown NLP error"
                    )
                }

            entities = nlp_results.get(
                "entities",
                []
            )

            log_info(
                f"Extracted "
                f"{len(entities)} entities"
            )

        except Exception as nlp_error:

            log_exception(
                f"NLP Error: {str(nlp_error)}"
            )

            return {

                "success": False,

                "message": (
                    "NLP processing crashed"
                ),

                "error": str(nlp_error)
            }

        # =================================================
        # TABLE EXTRACTION
        # =================================================

        table_data = []

        # =================================================
        # STRUCTURED OUTPUT
        # =================================================

        try:

            structured_output = structure_entities(

                document_type,

                entities
            )

            log_info(
                "Structured output generated"
            )

        except Exception as structure_error:

            log_error(
                f"Structure Output Error: "
                f"{str(structure_error)}"
            )

            structured_output = {

                "document_type": document_type,

                "raw_entities": entities
            }

        # =================================================
        # FINAL RESPONSE
        # =================================================

        try:

            final_response = build_response(

                document_type=document_type,

                ocr_text=extracted_text,

                boxes=boxes,

                entities=entities,

                ocr_confidence=ocr_confidence,

                table_data=table_data
            )

        except Exception as response_error:

            log_exception(
                f"Response Builder Error: "
                f"{str(response_error)}"
            )

            return {

                "success": False,

                "message": (
                    "Response building failed"
                ),

                "error": str(response_error)
            }

        # =================================================
        # ADD STRUCTURED OUTPUT
        # =================================================

        final_response[
            "structured_output"
        ] = structured_output

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        final_response[
            "success"
        ] = True

        log_info(
            "Document processing pipeline completed"
        )

        return final_response

    except Exception as e:

        log_exception(
            f"Document Service Error: {str(e)}"
        )

        return {

            "success": False,

            "message": (
                "Document processing failed"
            ),

            "error": str(e)
        }