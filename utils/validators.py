import re
from datetime import datetime

# =========================================================
# EMAIL VALIDATION
# =========================================================

def validate_email(email):

    """
    Validate email format
    """

    if not email:

        return False

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return bool(
        re.match(pattern, str(email))
    )

# =========================================================
# PHONE NUMBER VALIDATION
# =========================================================

def validate_phone(phone):

    """
    Validate Indian phone numbers
    """

    if not phone:

        return False

    phone = str(phone).replace(" ", "")

    pattern = r'^[6-9]\d{9}$'

    return bool(
        re.match(pattern, phone)
    )

# =========================================================
# PAN CARD VALIDATION
# =========================================================

def validate_pan(pan):

    """
    Validate Indian PAN number
    Example: ABCDE1234F
    """

    if not pan:

        return False

    pan = str(pan).upper()

    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'

    return bool(
        re.match(pattern, pan)
    )

# =========================================================
# AADHAAR VALIDATION
# =========================================================

def validate_aadhaar(aadhaar):

    """
    Validate Aadhaar number
    """

    if not aadhaar:

        return False

    aadhaar = re.sub(
        r"\s+",
        "",
        str(aadhaar)
    )

    pattern = r'^\d{12}$'

    return bool(
        re.match(pattern, aadhaar)
    )

# =========================================================
# PASSPORT VALIDATION
# =========================================================

def validate_passport(passport):

    """
    Validate Indian passport number
    Example: A1234567
    """

    if not passport:

        return False

    passport = str(passport).upper()

    pattern = r'^[A-Z]{1}[0-9]{7}$'

    return bool(
        re.match(pattern, passport)
    )

# =========================================================
# GST NUMBER VALIDATION
# =========================================================

def validate_gst(gst):

    """
    Validate GSTIN
    """

    if not gst:

        return False

    gst = str(gst).upper()

    pattern = (
        r'^[0-9]{2}'
        r'[A-Z]{5}'
        r'[0-9]{4}'
        r'[A-Z]{1}'
        r'[1-9A-Z]{1}'
        r'Z'
        r'[0-9A-Z]{1}$'
    )

    return bool(
        re.match(pattern, gst)
    )

# =========================================================
# DATE VALIDATION
# =========================================================

def validate_date(date_string):

    """
    Validate date formats
    """

    if not date_string:

        return False

    date_formats = [

        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%d %b %Y",
        "%d %B %Y"

    ]

    for fmt in date_formats:

        try:

            datetime.strptime(
                str(date_string),
                fmt
            )

            return True

        except ValueError:

            continue

    return False

# =========================================================
# INVOICE NUMBER VALIDATION
# =========================================================

def validate_invoice_number(invoice):

    """
    Validate invoice number
    """

    if not invoice:

        return False

    invoice = str(invoice)

    pattern = r'^[A-Za-z0-9\-/]{3,30}$'

    return bool(
        re.match(pattern, invoice)
    )

# =========================================================
# PINCODE VALIDATION
# =========================================================

def validate_pincode(pincode):

    """
    Validate Indian pincode
    """

    if not pincode:

        return False

    pattern = r'^[1-9][0-9]{5}$'

    return bool(
        re.match(pattern, str(pincode))
    )

# =========================================================
# AMOUNT VALIDATION
# =========================================================

def validate_amount(amount):

    """
    Validate monetary amount
    """

    if amount is None:

        return False

    try:

        amount = str(amount)

        amount = amount.replace(",", "")
        amount = amount.replace("₹", "")
        amount = amount.replace("$", "")

        float(amount)

        return True

    except Exception:

        return False

# =========================================================
# NAME VALIDATION
# =========================================================

def validate_name(name):

    """
    Validate person name
    """

    if not name:

        return False

    pattern = r'^[A-Za-z\s\.]{2,100}$'

    return bool(
        re.match(pattern, str(name))
    )

# =========================================================
# GENERIC REQUIRED FIELD CHECK
# =========================================================

def validate_required(value):

    """
    Check if field exists
    """

    if value is None:

        return False

    if str(value).strip() == "":

        return False

    return True

# =========================================================
# DOCUMENT VALIDATION PIPELINE
# =========================================================

def validate_entities(entities):

    """
    Validate extracted entities
    Supports:
    - dictionary entities
    - string entities
    """

    validated_entities = []

    if not entities:

        return validated_entities

    for entity in entities:

        # =====================================================
        # HANDLE DICTIONARY ENTITIES
        # =====================================================

        if isinstance(entity, dict):

            label = str(
                entity.get("label", "UNKNOWN")
            ).upper()

            text = str(
                entity.get("text", "")
            )

        # =====================================================
        # HANDLE STRING ENTITIES
        # =====================================================

        else:

            label = "UNKNOWN"

            text = str(entity)

        # =====================================================
        # DEFAULT VALIDATION STATUS
        # =====================================================

        validation_status = True

        validation_message = "Valid"

        # =====================================================
        # EMAIL VALIDATION
        # =====================================================

        if label == "EMAIL":

            validation_status = validate_email(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid email format"
                )

        # =====================================================
        # PHONE VALIDATION
        # =====================================================

        elif label == "PHONE":

            validation_status = validate_phone(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid phone number"
                )

        # =====================================================
        # PAN VALIDATION
        # =====================================================

        elif label == "PAN":

            validation_status = validate_pan(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid PAN number"
                )

        # =====================================================
        # AADHAAR VALIDATION
        # =====================================================

        elif label == "AADHAAR":

            validation_status = validate_aadhaar(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid Aadhaar number"
                )

        # =====================================================
        # PASSPORT VALIDATION
        # =====================================================

        elif label == "PASSPORT":

            validation_status = validate_passport(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid passport number"
                )

        # =====================================================
        # GST VALIDATION
        # =====================================================

        elif label == "GST":

            validation_status = validate_gst(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid GST number"
                )

        # =====================================================
        # DATE VALIDATION
        # =====================================================

        elif label == "DATE":

            validation_status = validate_date(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid date format"
                )

        # =====================================================
        # AMOUNT VALIDATION
        # =====================================================

        elif label == "AMOUNT":

            validation_status = validate_amount(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid amount"
                )

        # =====================================================
        # PINCODE VALIDATION
        # =====================================================

        elif label == "PINCODE":

            validation_status = validate_pincode(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid pincode"
                )

        # =====================================================
        # NAME VALIDATION
        # =====================================================

        elif label in ["NAME", "PERSON"]:

            validation_status = validate_name(
                text
            )

            if not validation_status:

                validation_message = (
                    "Invalid name"
                )

        # =====================================================
        # UNKNOWN ENTITY TYPE
        # =====================================================

        else:

            validation_status = True

            validation_message = (
                "No validation rule applied"
            )

        # =====================================================
        # FINAL ENTITY OBJECT
        # =====================================================

        validated_entity = {

            "label": label,

            "text": text,

            "is_valid": validation_status,

            "validation_message": validation_message
        }

        # =====================================================
        # PRESERVE EXTRA FIELDS IF PRESENT
        # =====================================================

        if isinstance(entity, dict):

            for key, value in entity.items():

                if key not in validated_entity:

                    validated_entity[key] = value

        # =====================================================
        # APPEND RESULT
        # =====================================================

        validated_entities.append(
            validated_entity
        )

    return validated_entities