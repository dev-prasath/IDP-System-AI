from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFPageCountError,
    PDFSyntaxError
)

POPPLER_PATH = r"E:\Poppler\poppler-26.02.0\Library\bin"


def pdf_to_images(pdf_file):

    try:

        images = convert_from_bytes(
            pdf_file.read(),
            dpi=300,
            poppler_path=POPPLER_PATH,
            thread_count=1
        )

        return images

    except PDFPageCountError:

        raise Exception(
            "Invalid or corrupted PDF file."
        )

    except PDFSyntaxError:

        raise Exception(
            "PDF syntax error."
        )

    except Exception as e:

        raise Exception(
            f"PDF Processing Error: {str(e)}"
        )