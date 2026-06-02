import os
import boto3
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# AWS CONFIG
# =========================================================

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


# =========================================================
# CREATE S3 CLIENT ONLY WHEN NEEDED
# =========================================================

def get_s3_client():

    if not all([
        AWS_ACCESS_KEY,
        AWS_SECRET_KEY,
        AWS_REGION,
        BUCKET_NAME
    ]):
        raise ValueError(
            "AWS environment variables missing. "
            "Check Streamlit Secrets."
        )

    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )


# =========================================================
# UPLOAD FILE
# =========================================================

def upload_file_to_s3(
    file_bytes,
    file_name,
    content_type
):

    s3 = get_s3_client()

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