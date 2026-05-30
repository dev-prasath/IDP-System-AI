# =========================================================
# backend/services/document_service.py
# ENTERPRISE IDP PIPELINE
# OCR + LAYOUT AI + NLP + HYBRID FUSION
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from email.mime import image
import traceback

from PIL import Image
import numpy as np

# =========================================================
# OCR SERVICE
# =========================================================

from backend.services.ocr_service import (
    process_ocr
)

# =========================================================
# NLP SERVICE
# =========================================================

from backend.services.nlp_service import (
    process_entities
)

# =========================================================
# HYBRID ENTITY ENGINE
# =========================================================

from documentClassifier.rule_based_classifier import classify_document
from nlp.hybrid_entityengine import (
    process_hybrid_entities
)

# =========================================================
# CLASSIFICATION SERVICE
# =========================================================

from backend.services.deep_classification_service import (
    classify_document_image
)

# =========================================================
# STRUCTURED OUTPUT
# =========================================================

from utils.structure_output import (
    structure_entities
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
# PDF HANDLER
# =========================================================

from utils.pdf_handler import (
    pdf_to_images
)

# =========================================================
# IMAGE PROCESSING
# =========================================================

from preprocessing.image_processing import (
    preprocess_image
)

# =========================================================
# LAYOUT INTELLIGENCE ENGINE
# =========================================================

from layout_extraction.layout_parser import (
    parse_document_layout
)

from PIL import Image
import numpy as np

from utils.document_parsers.invoice_parser import (
    parse_invoice
)

from utils.validators.invoice_validator import (
    validate_invoice
)
from utils.document_parsers.resume_parser import (
    parse_resume
)
from utils.document_parsers.id_card_parser import (
    parse_id_card
)
# =========================================================
# PROCESS DOCUMENT
# =========================================================

def process_document(uploaded_file):

    # =============================================
    # HANDLE INPUT TYPES
    # =============================================

    is_pil_image = isinstance(
        uploaded_file,
        Image.Image
    )

    is_numpy_image = isinstance(
        uploaded_file,
        np.ndarray
    )
    """
    Main intelligent document processing pipeline.

    Pipeline:
        OCR
        ↓
        Spatial Layout Analysis
        ↓
        Table Extraction
        ↓
        Key-Value Extraction
        ↓
        NLP Extraction
        ↓
        Hybrid Entity Fusion
        ↓
        Structured JSON Output
    """

    try:

        # =================================================
        # START LOG
        # =================================================

        log_info(
            "Starting document processing"
        )

        # =================================================
        # VALIDATION
        # =================================================

        if uploaded_file is None:

            raise ValueError(
                "Uploaded file is None"
            )

        # =================================================
        # FILE TYPE
        # =================================================

        if is_pil_image or is_numpy_image:

            file_type = "image/jpeg"

        else:

            file_type = getattr(
                uploaded_file,
                "type",
                "image/jpeg"
            )

        # =================================================
        # STORAGE VARIABLES
        # =================================================

        all_text = []
        all_boxes = []
        all_entities = []

        layout_fields = {}
        table_data = []

        pages = 1

        ocr_confidences = []

        classification_confidence = 95.0

        # =================================================
        # HANDLE PDF
        # =================================================

        if file_type == "application/pdf":

            log_info(
                "Processing PDF document"
            )

            uploaded_file.seek(0)

            pdf_images = pdf_to_images(
                uploaded_file
            )

            if not pdf_images:

                raise ValueError(
                    "Failed to convert PDF pages"
                )

            pages = len(pdf_images)

            document_images = pdf_images

        # =================================================
        # HANDLE IMAGE
        # =================================================

        else:

            log_info(
                "Processing image document"
            )

            # =============================================
            # PIL IMAGE INPUT
            # =============================================

            if is_pil_image:

                pil_image = uploaded_file.convert(
                    "RGB"
                )

            # =============================================
            # NUMPY IMAGE INPUT
            # =============================================

            elif is_numpy_image:

                pil_image = Image.fromarray(
                    uploaded_file
                ).convert("RGB")

            # =============================================
            # FILE OBJECT INPUT
            # =============================================

            else:

                uploaded_file.seek(0)

                pil_image = Image.open(
                    uploaded_file
                ).convert("RGB")

            document_images = [
                pil_image
            ]

        # =================================================
        # PROCESS EACH PAGE
        # =================================================

        for page_index, image in enumerate(
            document_images
        ):

            try:

                print(
                    f"\n========== PAGE {page_index + 1} ==========\n"
                )

                # =============================================
                # CONVERT TO NUMPY
                # =============================================

                image_np = np.array(
                    image
                )

                # =============================================
                # PREPROCESS IMAGE
                # =============================================

                processed_image = preprocess_image(
                    image_np
                )

                # =============================================
                # OCR
                # =============================================

                ocr_result = process_ocr(
                    processed_image
                )

                if not ocr_result.get(
                    "success",
                    False
                ):

                    continue

                page_text = ocr_result.get(
                    "ocr_text",
                    ""
                )

                page_boxes = ocr_result.get(
                    "boxes",
                    []
                )

                page_confidence = ocr_result.get(
                    "ocr_confidence",
                    0.0
                )

                # =============================================
                # STORE OCR RESULTS
                # =============================================

                all_text.append(
                    page_text
                )

                all_boxes.extend(
                    page_boxes
                )

                ocr_confidences.append(
                    page_confidence
                )

            except Exception as page_error:

                log_exception(
                    f"Page Processing Error: {str(page_error)}"
                )

                continue

        # =================================================
        # FINAL OCR TEXT
        # =================================================

        final_ocr_text = "\n".join(
            all_text
        )        

        # =================================================
        # OCR VALIDATION
        # =================================================

        if len(final_ocr_text.strip()) == 0:

            raise ValueError(
                "No OCR text extracted"
            )

        # =================================================
        # DOCUMENT CLASSIFICATION
        # =================================================

        log_info(
            "Starting document classification"
        )
        print("\n========== CLASSIFICATION START ==========")
        print("Image Type:", type(image))

        classification_results = classify_document_image(
            image
        )
        print("\nCLASSIFICATION_RESULTS")
        print(classification_results)
        mobilenet_result = classification_results.get(
            "mobilenet",
            {}
        )

        efficientnet_result = classification_results.get(
            "efficientnet",
            {}
        )

        best_prediction = (
            efficientnet_result
            if efficientnet_result["confidence"]
            >= mobilenet_result["confidence"]
            else mobilenet_result
        )

        document_type = best_prediction["label"]

        classification_confidence = (
            best_prediction["confidence"]
        )

        # ==========================================
        # FALLBACK OCR CLASSIFICATION
        # ==========================================

        if classification_confidence < 70:

            fallback_type = classify_document(
                final_ocr_text
            )

            log_info(
                f"CNN Confidence Low: {classification_confidence}"
            )

            log_info(
                f"Fallback Result: {fallback_type}"
            )

            if fallback_type != "Unknown":

                document_type = fallback_type

                log_info(
                    f"Using OCR Classification: {document_type}"
                )

        log_info(
            f"Detected document type: {document_type}"
        )

        # =================================================
        # SPATIAL LAYOUT ANALYSIS
        # =================================================

        log_info(
            "Starting layout intelligence engine"
        )

        layout_result = parse_document_layout(

            all_boxes,

            document_type
        )

        table_data = layout_result.get(
            "table_data",
            []
        )
        from layout_extraction.invoice_table_parser import (
            parse_invoice_table
        )

        try:

            rows = layout_result.get(
                "rows",
                []
            )
            parsed_invoice_table = parse_invoice_table(
                rows
            )

        except Exception as invoice_error:

            log_exception(
                f"Invoice Parser Error: "
                f"{str(invoice_error)}"
            )

            parsed_invoice_table = []

        layout_fields = layout_result.get(
            "key_value_data",
            {}
        )

        layout_type = layout_result.get(
            "layout_type",
            "unknown"
        )

        summary_data = layout_result.get(
            "summary_data",
            {}
        )

        invoice_details = layout_result.get(
            "invoice_details",
            {}
        )

        # rows = layout_result.get(
        #     "rows",
        #     []
        # )

        # =================================================
        # DEBUG OUTPUT
        # =================================================

        print(
            "\n========== LAYOUT TYPE ==========\n"
        )

        print(layout_type)

        print(
            "\n========== LAYOUT FIELDS ==========\n"
        )

        print(layout_fields)

        print(
            "\n========== TABLE DATA ==========\n"
        )

        print(table_data)

        # =================================================
        # NLP PIPELINE
        # =================================================

        log_info(
            "Starting NLP pipeline"
        )

        nlp_result = process_entities(
            final_ocr_text
        )

        if not nlp_result.get(
            "success",
            False
        ):

            nlp_entities = []

        else:

            nlp_entities = nlp_result.get(
                "entities",
                []
            )

        # =================================================
        # HYBRID ENTITY FUSION
        # =================================================

        log_info(
            "Starting hybrid entity fusion"
        )

        hybrid_result = process_hybrid_entities(

            nlp_entities=nlp_entities,

            layout_fields=layout_fields,

            table_data=table_data,

            document_type=document_type
        )

        if not hybrid_result.get(
            "success",
            False
        ):

            all_entities = nlp_entities

        else:

            all_entities = hybrid_result.get(
                "entities",
                []
            )

        log_info(
            f"Final hybrid entities: {len(all_entities)}"
        )

        structured_output = structure_entities(

            document_type,

            all_entities
        )

        # ==========================================
        # INVOICE PARSER
        # ==========================================

        if "invoice" in str(document_type).lower():

            parsed_invoice = parse_invoice(

                final_ocr_text,

                all_entities,

                table_data,

                layout_fields
            )

            structured_output[
                "parsed_invoice"
            ] = parsed_invoice

        if "resume" in document_type.lower():

                parsed_resume = parse_resume(

                    final_ocr_text,

                    all_entities
                )

                structured_output[
                    "parsed_resume"
                ] = parsed_resume


        if "id" in str(document_type).lower():

            parsed_id_card = parse_id_card(

                final_ocr_text,

                all_entities
            )

            structured_output[
                "parsed_id_card"
            ] = parsed_id_card
        # =================================================
        # MERGE LAYOUT OUTPUT
        # =================================================

        structured_output[
            "layout_type"
        ] = layout_type

        structured_output[
            "layout_fields"
        ] = layout_fields

        structured_output[
            "table_data"
        ] = table_data

        structured_output[
            "invoice_details_layout"
        ] = invoice_details

        structured_output[
            "invoice_summary"
        ] = summary_data

        # parsed_invoice = parse_invoice(
        #     final_ocr_text,
        #     all_entities,
        #     table_data,
        #     layout_fields,
        #     structured_output.get(
        #         "invoice_summary",
        #         {}
        #     )
        # )

        structured_output[
            "layout_summary"
        ] = {

            "total_rows": len(rows),

            "total_tables": len(table_data),

            "layout_engine": "Spatial AI"
        }

        structured_output[
            "parsed_invoice_table"
        ] = parsed_invoice_table

        # =================================================
        # OCR CONFIDENCE
        # =================================================

        if ocr_confidences:

            average_ocr_confidence = round(

                sum(ocr_confidences)

                / len(ocr_confidences),

                2
            )

        else:

            average_ocr_confidence = 0.0

        # =================================================
        # FINAL RESPONSE
        # =================================================

        response = {

            "success": True,

            "document_type": document_type,

            "mobilenet_prediction": mobilenet_result,
            "efficientnet_prediction": efficientnet_result, 

            "classification_confidence":
                classification_confidence,

            "ocr_text": final_ocr_text,

            "entities": all_entities,

            "structured_output":
                structured_output,

            "table_data": table_data,

            "layout_fields": layout_fields,

            "layout_type": layout_type,

            "boxes": all_boxes,

            "rows": rows,

            "pages": pages,

            "ocr_confidence":
                average_ocr_confidence
        }

        log_info(
            "Document processing completed"
        )

        return response

    except Exception as e:

        # =================================================
        # ERROR HANDLING
        # =================================================

        print(
            "\n========== DOCUMENT PROCESSING FAILED ==========\n"
        )

        traceback.print_exc()

        log_exception(
            f"Document Service Error: {str(e)}"
        )

        print("\n========== DOCUMENT SERVICE RETURN ==========")

        print("\n========== DOCUMENT SERVICE RETURN ==========")
        print("mobilenet_result =", mobilenet_result)
        print("efficientnet_result =", efficientnet_result)
    print(response)
    return {
            "success": True,

            "document_type": document_type,

            "mobilenet_prediction": mobilenet_result,

            "efficientnet_prediction": efficientnet_result,

            "ocr_text": all_text,

            "entities": all_entities,

            "structured_output": structured_output,

            "boxes": all_boxes,

            "table_data": all_tables
        }
    