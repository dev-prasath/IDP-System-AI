from PIL import Image

from classifier import classify_document

# ==========================================
# TEST IMAGE
# ==========================================

IMAGE_PATH = r"invoice-template-us-classic-white-750px.png"

image = Image.open(IMAGE_PATH).convert("RGB")

result = classify_document(image)

print(result)