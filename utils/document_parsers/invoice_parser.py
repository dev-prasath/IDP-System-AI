import re


def get_entity(entities, label):

    for entity in entities:

        if entity.get("label") == label:
            return entity.get("text")

    return None


def get_all_entities(entities, label):

    return [

        entity.get("text")

        for entity in entities

        if entity.get("label") == label
    ]


def parse_invoice(
    ocr_text,
    entities,
    table_data=None,
    layout_fields=None
):

    total_amount = None

    summary_total = None

    if layout_fields:
        summary_total = layout_fields.get(
            "total"
        )

    if summary_total:
        total_amount = summary_total

    else:

        amounts = get_all_entities(
            entities,
            "AMOUNT"
        )

        if amounts:

            def safe_amount(value):

                cleaned = (
                    str(value)
                    .replace("$", "")
                    .replace("₹", "")
                    .replace("rs", "")
                    .replace(",", "")
                    .replace("[", "")
                    .replace("]", "")
                    .replace("(", "")
                    .replace(")", "")
                    .strip()
                )

                try:
                    return float(cleaned)
                except:
                    return 0.0


            total_amount = max(
                amounts,
                key=safe_amount
            )
            def safe_amount(value):

                cleaned = (
                    str(value)
                    .replace("$", "")
                    .replace("₹", "")
                    .replace(",", "")
                    .replace("[", "")
                    .replace("]", "")
                    .strip()
                )

                try:
                    return float(cleaned)
                except:
                    return 0

    invoice_data = {

        "vendor_name":
            get_entity(
                entities,
                "ORGANIZATION"
            ),

        "invoice_number":
            get_entity(
                entities,
                "INVOICE_NUMBER"
            ),

        "gst_number":
            get_entity(
                entities,
                "GST"
            ),

        "invoice_date":
            get_entity(
                entities,
                "DATE"
            ),

        "total_amount":
            total_amount,

        "tax_amount":
            None,

        "line_items":
            table_data if table_data else []
    }

    tax_match = re.search(

        r"(?:gst|tax)\s*[:\-]?\s*([\d,.]+)",

        ocr_text,

        re.IGNORECASE
    )

    if tax_match:

        invoice_data[
            "tax_amount"
        ] = tax_match.group(1)

    return invoice_data