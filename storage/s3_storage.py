import os
import boto3

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
# AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
# AWS_REGION = os.getenv("AWS_REGION")
# BUCKET_NAME = os.getenv("AWS_BUCKET")

AWS_ACCESS_KEY = st.secrets.get(
    "AWS_ACCESS_KEY",
    os.getenv("AWS_ACCESS_KEY")
)

AWS_SECRET_KEY = st.secrets.get(
    "AWS_SECRET_KEY",
    os.getenv("AWS_SECRET_KEY")
)

AWS_REGION = st.secrets.get(
    "AWS_REGION",
    os.getenv("AWS_REGION")
)

BUCKET_NAME = st.secrets.get(
    "AWS_BUCKET",
    os.getenv("AWS_BUCKET")
)

if not all([
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_REGION,
    BUCKET_NAME
]):
    raise ValueError(
        "AWS environment variables missing"
    )

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_file_to_s3(
    file_bytes,
    file_name,
    content_type
):

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"uploads/{file_name}",
        Body=file_bytes,
        ContentType=content_type
    )

    return (
        f"https://{BUCKET_NAME}.s3."
        f"{AWS_REGION}.amazonaws.com/"
        f"uploads/{file_name}"
    )