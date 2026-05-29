# =========================================================
# database/postgresql.py
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import psycopg2
import json

from datetime import datetime

# =========================================================
# DATABASE CONFIG
# =========================================================

DB_CONFIG = {

    "host": "localhost",

    "database": "idp_system",

    "user": "postgres",

    "password": "280402",

    "port": "5432"
}

# =========================================================
# GET CONNECTION
# =========================================================

def get_connection():

    connection = psycopg2.connect(
        **DB_CONFIG
    )

    return connection

# =========================================================
# CREATE TABLE
# =========================================================

def create_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS documents (

        id SERIAL PRIMARY KEY,

        document_title TEXT,

        document_type TEXT,

        ocr_text TEXT,

        entities JSONB,

        structured_output JSONB,

        created_at TIMESTAMP
    )

    """)

    connection.commit()

    cursor.close()

    connection.close()

# =========================================================
# INITIALIZE DATABASE
# =========================================================

create_table()

# =========================================================
# NUMPY TYPE CONVERSION
# =========================================================

def convert_numpy_types(obj):

    if isinstance(obj, dict):

        return {

            key: convert_numpy_types(value)

            for key, value in obj.items()
        }

    elif isinstance(obj, list):

        return [

            convert_numpy_types(item)

            for item in obj
        ]

    elif hasattr(obj, "item"):

        return obj.item()

    else:

        return obj

# =========================================================
# SAVE DOCUMENT
# =========================================================

def save_document(
    document_title,
    document_type,
    ocr_text,
    entities,
    structured_output,
    s3_url
):

    connection = None

    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """
            INSERT INTO documents (

                document_title,
                document_type,
                ocr_text,
                entities,
                structured_output,
                s3_url,
                created_at

            )

            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,

            (
                document_title,
                document_type,
                ocr_text,

                json.dumps(
                    convert_numpy_types(
                        entities
                    )
                ),

                json.dumps(
                    convert_numpy_types(
                        structured_output
                    )
                ),

                s3_url,

                datetime.now()
            )
        )

        connection.commit()

        return True

    except Exception as e:

        if connection:

            connection.rollback()

        print(
            f"Database Insert Error: {e}"
        )

        return False

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

# =========================================================
# FETCH ALL DOCUMENTS
# =========================================================

def fetch_documents():

    connection = None

    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

    SELECT

        id,

        COALESCE(
            document_title,
            ''
        ),

        document_type,

        created_at,

        structured_output,

        s3_url

    FROM documents

    ORDER BY created_at DESC

""")

        documents = cursor.fetchall()

        return documents

    except Exception as e:

        print(f"Fetch Error: {e}")

        return []

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

# =========================================================
# FETCH DOCUMENT BY ID
# =========================================================

def fetch_document_by_id(

    doc_id
):

    connection = None

    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """

            SELECT *

            FROM documents

            WHERE id = %s

            """,

            (doc_id,)
        )

        document = cursor.fetchone()

        return document

    except Exception as e:

        print(
            f"Fetch By ID Error: {e}"
        )

        return None

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

# =========================================================
# UPDATE DOCUMENT TITLE
# =========================================================

def update_document_title(

    doc_id,

    new_title
):

    connection = None

    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """

            UPDATE documents

            SET document_title = %s

            WHERE id = %s

            """,

            (

                new_title,

                doc_id
            )
        )

        connection.commit()

        return True

    except Exception as e:

        if connection:

            connection.rollback()

        print(
            f"Update Error: {e}"
        )

        return False

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

# =========================================================
# DELETE DOCUMENT
# =========================================================

def delete_document_by_id(

    doc_id
):

    connection = None

    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """

            DELETE FROM documents

            WHERE id = %s

            """,

            (doc_id,)
        )

        connection.commit()

        return True

    except Exception as e:

        if connection:

            connection.rollback()

        print(
            f"Delete Error: {e}"
        )

        return False

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

# =========================================================
# CLOSE DATABASE CONNECTION
# =========================================================

def close_connection(

    connection,

    cursor
):

    if cursor:

        cursor.close()

    if connection:

        connection.close()