from storage.s3_storage import upload_file_to_s3

from storage.s3_storage import *


with open(
    "requirements.txt",
    "rb"
) as f:

    file_data = f.read()

url = upload_file_to_s3(
    file_data,
    "requirements.txt",
    "text/plain"
)

print(url)