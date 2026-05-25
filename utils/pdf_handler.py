# =========================================================
# utils/pdf_handler.py
# STREAMLIT CLOUD READY VERSION
# =========================================================

import io
import fitz

from PIL import Image

# =========================================================
# PDF TO IMAGES
# =========================================================

def pdf_to_images(pdf_file):

    """
    Convert PDF pages into PIL images
    using PyMuPDF.

    Streamlit Cloud compatible.
    """

    try:

        images = []

        pdf_file.seek(0)

        pdf_bytes = pdf_file.read()

        pdf_document = fitz.open(

            stream=pdf_bytes,

            filetype="pdf"
        )

        for page_number in range(

            len(pdf_document)
        ):

            page = pdf_document.load_page(

                page_number
            )

            pix = page.get_pixmap(

                dpi=300
            )

            image_bytes = pix.tobytes(

                "png"
            )

            pil_image = Image.open(

                io.BytesIO(image_bytes)
            ).convert("RGB")

            images.append(

                pil_image
            )

        return images

    except Exception as e:

        raise Exception(

            f"PDF Processing Error: {str(e)}"
        )