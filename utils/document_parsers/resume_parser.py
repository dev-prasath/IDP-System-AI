# utils/document_parsers/resume_parser.py

import re


def parse_resume(
    ocr_text,
    entities
):

    resume = {

        "candidate_name": None,
        "email": None,
        "phone": None,
        "skills": [],
        "education": [],
        "experience": []
    }

    # --------------------
    # PERSON
    # --------------------

    for entity in entities:

        if entity["label"] == "PERSON":

            resume["candidate_name"] = entity["text"]

        elif entity["label"] == "EMAIL":

            resume["email"] = entity["text"]

        elif entity["label"] == "PHONE":

            resume["phone"] = entity["text"]

    # --------------------
    # SKILLS SECTION
    # --------------------

    skill_match = re.search(

        r"SKILLS(.*?)EXPERIENCE",

        ocr_text,

        re.DOTALL | re.IGNORECASE
    )

    if skill_match:

        skills_text = skill_match.group(1)

        resume["skills"] = [

            line.strip()

            for line in skills_text.split("\n")

            if line.strip()
        ]

    return resume