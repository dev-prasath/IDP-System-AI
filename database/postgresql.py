import psycopg2
import json
from datetime import datetime

# =========================================================
# DATABASE CONNECTION
# =========================================================

conn = psycopg2.connect(
    host="localhost",
    database="idp_system",
    user="postgres",
    password="280402",
    port="5432"
)

cursor = conn.cursor()

# =========================================================
# CREATE TABLE
# =========================================================

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

conn.commit()

# =========================================================
# ADD COLUMN SAFETY CHECK
# =========================================================

try:

    cursor.execute("""

    ALTER TABLE documents
    ADD COLUMN document_title TEXT

    """)

    conn.commit()

except Exception:

    conn.rollback()

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
    structured_output
):

    try:

        cursor.execute(

            """
            INSERT INTO documents (

                document_title,
                document_type,
                ocr_text,
                entities,
                structured_output,
                created_at

            )

            VALUES (%s, %s, %s, %s, %s, %s)
            """,

            (
                document_title,
                document_type,
                ocr_text,

                json.dumps(
                    convert_numpy_types(entities)
                ),

                json.dumps(
                    convert_numpy_types(structured_output)
                ),

                datetime.now()
            )
        )

        conn.commit()

    except Exception as e:

        conn.rollback()

        print(f"Database Insert Error: {e}")

# =========================================================
# FETCH DOCUMENTS
# =========================================================

def fetch_documents():

    try:

        cursor.execute("""

            SELECT

                id,
                COALESCE(document_title, ''),
                document_type,
                created_at,
                structured_output

            FROM documents

            ORDER BY created_at DESC

        """)

        documents = cursor.fetchall()

        return documents

    except Exception as e:

        conn.rollback()

        print(f"Fetch Error: {e}")

        return []

# =========================================================
# UPDATE DOCUMENT TITLE
# =========================================================

def update_document_title(
    doc_id,
    new_title
):

    try:

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

        conn.commit()

    except Exception as e:

        conn.rollback()

        print(f"Update Error: {e}")

# =========================================================
# CLOSE CONNECTION
# =========================================================

def close_connection():

    cursor.close()

    conn.close()