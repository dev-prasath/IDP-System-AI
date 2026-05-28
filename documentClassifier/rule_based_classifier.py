import re


def classify_document(text):

    text = text.lower()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    scores = {
        "Invoice": 0,
        "Resume": 0,
        "ID Card": 0,
        "Healthcare Document": 0,
        "Insurance Document": 0,
        "Logistics Document": 0,
        "Government Document": 0
    }

    # Invoice Keywords
    invoice_keywords = [
        "invoice",
        "gst",
        "tax invoice",
        "invoice number",
        "bill to",
        "total amount",
        "amount"
    ]

    # Resume Keywords
    resume_keywords = [
        "education",
        "skills",
        "experience",
        "projects",
        "internship",
        "linkedin",
        "github"
    ]

    # ID Card Keywords
    id_keywords = [
        "government of india",
        "aadhaar",
        "date of birth",
        "dob",
        "pan",
        "uid"
    ]

    # Healthcare Keywords
    healthcare_keywords = [
        "hospital",
        "patient",
        "diagnosis",
        "prescription",
        "doctor"
    ]

    # Insurance Keywords
    insurance_keywords = [
        "policy",
        "claim",
        "insured",
        "premium"
    ]

    # Logistics Keywords
    logistics_keywords = [
        "shipment",
        "consignee",
        "tracking",
        "delivery"
    ]

    # Government Keywords
    government_keywords = [
        "application form",
        "department",
        "citizen",
        "registration"
    ]

    # Scoring Function
    def calculate_score(keywords, category):

        for keyword in keywords:

            if keyword in text:
                scores[category] += 1

    calculate_score(invoice_keywords, "Invoice")
    calculate_score(resume_keywords, "Resume")
    calculate_score(id_keywords, "ID Card")
    calculate_score(healthcare_keywords, "Healthcare Document")
    calculate_score(insurance_keywords, "Insurance Document")
    calculate_score(logistics_keywords, "Logistics Document")
    calculate_score(government_keywords, "Government Document")

    predicted_class = max(scores, key=scores.get)

    if scores[predicted_class] == 0:
        return "Unknown Document"

    return predicted_class