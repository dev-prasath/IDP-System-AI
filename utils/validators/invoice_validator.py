import re


def validate_invoice(invoice_data):

    validation = {

        "missing_fields": [],

        "validation_errors": [],

        "confidence_score": 100
    }

    required_fields = [

        "vendor_name",

        "invoice_number",

        "invoice_date",

        "total_amount"
    ]

    # ====================================
    # REQUIRED FIELD CHECK
    # ====================================

    for field in required_fields:

        if not invoice_data.get(field):

            validation[
                "missing_fields"
            ].append(field)

            validation[
                "confidence_score"
            ] -= 15

    # ====================================
    # GST VALIDATION
    # ====================================

    gst = invoice_data.get(
        "gst_number"
    )

    if gst:

        gst_pattern = (
            r'^\d{2}[A-Z]{5}\d{4}'
            r'[A-Z][A-Z0-9]Z[A-Z0-9]$'
        )

        if not re.match(
            gst_pattern,
            gst
        ):

            validation[
                "validation_errors"
            ].append(
                "Invalid GST Number"
            )

            validation[
                "confidence_score"
            ] -= 10

    # ====================================
    # AMOUNT VALIDATION
    # ====================================

    amount = invoice_data.get(
        "total_amount"
    )

    if amount:

        try:

            float(

                str(amount)

                .replace(",", "")

                .replace("₹", "")

            )

        except Exception:

            validation[
                "validation_errors"
            ].append(
                "Invalid Amount"
            )

            validation[
                "confidence_score"
            ] -= 10

    validation[
        "confidence_score"
    ] = max(
        validation[
            "confidence_score"
        ],
        0
    )

    return validation