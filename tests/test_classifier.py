from PIL import Image

from backend.services.deep_classification_service import (
    classify_document_image
)

from backend.services.deep_classification_service import (
    INDEX_TO_LABEL
)


image = Image.open(
    r"Test_images\id_card\Screenshot (399).png"
)

result = classify_document_image(
    image
)
print(INDEX_TO_LABEL)

print(result)