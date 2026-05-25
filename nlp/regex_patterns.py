import re

 
# EMAIL
 

EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+\.\w+'

 
# PHONE
 

PHONE_PATTERN = r'(?:\+91[-\s]?)?[6-9]\d{9}'

 
# PAN
 

PAN_PATTERN = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'

 
# AADHAAR
 

AADHAAR_PATTERN = r'\b\d{4}\s\d{4}\s\d{4}\b'

 
# GST
 

GST_PATTERN = (
    r'\d{2}[A-Z]{5}'
    r'\d{4}[A-Z]{1}'
    r'[1-9A-Z]{1}'
    r'Z'
    r'[0-9A-Z]{1}'
)

 
# DATE
 

DATE_PATTERN = (
    r'\b\d{2}[/-]\d{2}[/-]\d{4}\b'
)

 
# AMOUNT
 

AMOUNT_PATTERN = (
    r'(?:₹|\$)?\s?'
    r'\d+(?:,\d{3})*(?:\.\d{2})?'
)

 
# INVOICE NUMBER
 

INVOICE_PATTERN = (
    r'(?:INV|Invoice|Bill)[-:\s]*'
    r'[A-Z0-9\-]+'
)

 
# PINCODE
 

PINCODE_PATTERN = r'\b[1-9][0-9]{5}\b'

 
# PASSPORT
 

PASSPORT_PATTERN = r'\b[A-Z][0-9]{7}\b'

 
# EXTRACT REGEX ENTITIES
 

def extract_regex_entities(text):

    extracted_entities = []

    patterns = {

        "EMAIL": EMAIL_PATTERN,
        "PHONE": PHONE_PATTERN,
        "PAN": PAN_PATTERN,
        "AADHAAR": AADHAAR_PATTERN,
        "GST": GST_PATTERN,
        "DATE": DATE_PATTERN,
        "AMOUNT": AMOUNT_PATTERN,
        "INVOICE_NUMBER": INVOICE_PATTERN,
        "PINCODE": PINCODE_PATTERN,
        "PASSPORT": PASSPORT_PATTERN
    }

    for label, pattern in patterns.items():

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:

            extracted_entities.append({

                "label": label,

                "text": str(match),

                "confidence": 0.99
            })

    return extracted_entities