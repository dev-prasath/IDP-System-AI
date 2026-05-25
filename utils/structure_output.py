def structure_entities(
    document_type,
    entities
):

    document_type = str(
        document_type
    ).lower()

    # =====================================================
    # BASE OUTPUT
    # =====================================================

    structured_data = {

        "document_type": document_type,

        "persons": [],

        "organizations": [],

        "dates": [],

        "locations": [],

        "emails": [],

        "phones": [],

        "amounts": [],

        "invoice_numbers": [],

        "aadhaar_numbers": [],

        "pan_numbers": [],

        "gst_numbers": [],

        "passport_numbers": [],

        "miscellaneous": []
    }

    # =====================================================
    # ENTITY MAPPING
    # =====================================================

    for entity in entities:

        label = entity["label"]

        text = entity["text"]

        # =================================================
        # PERSON
        # =================================================

        if label == "PERSON":

            if text not in structured_data[
                "persons"
            ]:

                structured_data[
                    "persons"
                ].append(text)

        # =================================================
        # ORGANIZATION
        # =================================================

        elif label == "ORGANIZATION":

            if text not in structured_data[
                "organizations"
            ]:

                structured_data[
                    "organizations"
                ].append(text)

        # =================================================
        # DATE
        # =================================================

        elif label == "DATE":

            if text not in structured_data[
                "dates"
            ]:

                structured_data[
                    "dates"
                ].append(text)

        # =================================================
        # LOCATION
        # =================================================

        elif label == "LOCATION":

            if text not in structured_data[
                "locations"
            ]:

                structured_data[
                    "locations"
                ].append(text)

        # =================================================
        # EMAIL
        # =================================================

        elif label == "EMAIL":

            if text not in structured_data[
                "emails"
            ]:

                structured_data[
                    "emails"
                ].append(text)

        # =================================================
        # PHONE
        # =================================================

        elif label == "PHONE":

            if text not in structured_data[
                "phones"
            ]:

                structured_data[
                    "phones"
                ].append(text)

        # =================================================
        # AMOUNT
        # =================================================

        elif label == "AMOUNT":

            if text not in structured_data[
                "amounts"
            ]:

                structured_data[
                    "amounts"
                ].append(text)

        # =================================================
        # INVOICE NUMBER
        # =================================================

        elif label == "INVOICE_NUMBER":

            if text not in structured_data[
                "invoice_numbers"
            ]:

                structured_data[
                    "invoice_numbers"
                ].append(text)

        # =================================================
        # AADHAAR
        # =================================================

        elif label == "AADHAAR":

            if text not in structured_data[
                "aadhaar_numbers"
            ]:

                structured_data[
                    "aadhaar_numbers"
                ].append(text)

        # =================================================
        # PAN
        # =================================================

        elif label == "PAN":

            if text not in structured_data[
                "pan_numbers"
            ]:

                structured_data[
                    "pan_numbers"
                ].append(text)

        # =================================================
        # GST
        # =================================================

        elif label == "GST":

            if text not in structured_data[
                "gst_numbers"
            ]:

                structured_data[
                    "gst_numbers"
                ].append(text)

        # =================================================
        # PASSPORT
        # =================================================

        elif label == "PASSPORT":

            if text not in structured_data[
                "passport_numbers"
            ]:

                structured_data[
                    "passport_numbers"
                ].append(text)

        # =================================================
        # MISC
        # =================================================

        else:

            if text not in structured_data[
                "miscellaneous"
            ]:

                structured_data[
                    "miscellaneous"
                ].append(text)

    # =====================================================
    # DOCUMENT-SPECIFIC OUTPUT
    # =====================================================

    if "invoice" in document_type:

        structured_data["primary_amount"] = (
            structured_data["amounts"][0]
            if structured_data["amounts"]
            else None
        )

        structured_data["primary_invoice_number"] = (
            structured_data["invoice_numbers"][0]
            if structured_data["invoice_numbers"]
            else None
        )

    elif "resume" in document_type:

        structured_data["candidate_name"] = (
            structured_data["persons"][0]
            if structured_data["persons"]
            else None
        )

        structured_data["candidate_email"] = (
            structured_data["emails"][0]
            if structured_data["emails"]
            else None
        )

    elif "id" in document_type:

        structured_data["primary_person"] = (
            structured_data["persons"][0]
            if structured_data["persons"]
            else None
        )

        structured_data["primary_id"] = (

            structured_data["aadhaar_numbers"][0]

            if structured_data["aadhaar_numbers"]

            else (

                structured_data["pan_numbers"][0]

                if structured_data["pan_numbers"]

                else None
            )
        )

    return structured_data