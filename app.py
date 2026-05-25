
# =========================================================
# IMPORTS
# =========================================================

import json
import time
from io import BytesIO

import cv2
import numpy as np
import pandas as pd
import requests
import streamlit as st
from PIL import Image

# =========================================================
# DATABASE
# =========================================================

from database.postgresql import (
    fetch_documents,
    save_document,
    update_document_title
)

# =========================================================
# PDF HANDLER
# =========================================================

from utils.pdf_handler import (
    pdf_to_images
)

# =========================================================
# LOGGER
# =========================================================

from utils.logger import (
    log_exception
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Intelligent Document AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CONSTANTS
# =========================================================

API_URL = "http://127.0.0.1:8000/process-document"

ALLOWED_TYPES = [
    "image/png",
    "image/jpeg",
    "application/pdf"
]

CLASSIFICATION_COLOR = {
    "Invoice": "#10b981",
    "Resume": "#3b82f6",
    "ID Card": "#8b5cf6",
    "Report": "#f59e0b"
}

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.15), transparent 25%),
        radial-gradient(circle at top right, rgba(168,85,247,0.15), transparent 25%),
        linear-gradient(135deg, #020617, #0f172a, #111827);
    color: white;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617,
        #0f172a,
        #111827
    );
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.hero-card {
    position: relative;
    overflow: hidden;
    padding: 3rem;
    border-radius: 30px;
    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.18),
            rgba(124,58,237,0.18)
        );
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    margin-bottom: 2rem;
    box-shadow: 0 0 40px rgba(59,130,246,0.15);
}

.hero-title {
    font-size: 50px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 18px;
    color: #cbd5e1;
}

.hero-badge {
    display: inline-block;
    padding: 8px 18px;
    margin-right: 10px;
    margin-top: 10px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    color: white;
    font-size: 14px;
}

[data-testid="metric-container"] {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.25);
}

.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color: white;
    font-weight: 700;
}

.stDownloadButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(
        90deg,
        #059669,
        #16a34a
    );
    color: white;
    font-weight: 700;
}

[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.65);
    border: 2px dashed rgba(255,255,255,0.15);
    border-radius: 24px;
    padding: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    color: white;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    ) !important;
}

textarea {
    background: rgba(15,23,42,0.85) !important;
    color: white !important;
    border-radius: 18px !important;
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

.custom-card {
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}

img {
    border-radius: 18px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero-card">

<div class="hero-title">
📄 Intelligent Document Processing AI
</div>

<div class="hero-subtitle">
Advanced OCR • NLP • Computer Vision • FastAPI • PostgreSQL
</div>

<div style="margin-top:20px;">
<span class="hero-badge">⚡ AI Powered</span>
<span class="hero-badge">🧠 NLP Extraction</span>
<span class="hero-badge">📊 Structured Data</span>
<span class="hero-badge">☁ Cloud Ready</span>
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🚀 Navigation")

    menu = st.radio(
        "Select Page",
        [
            "📤 Upload Documents",
            "📚 Document History"
        ]
    )

    st.divider()

    st.markdown("## 📂 Supported Formats")

    st.success("""
✔ PDF
✔ PNG
✔ JPG
✔ JPEG
""")

    st.markdown("## 🤖 AI Features")

    st.info("""
✔ OCR Detection
✔ Text Detection
✔ Entity Extraction
✔ Document Classification
✔ Table Extraction
✔ JSON Export
✔ PostgreSQL Storage
""")

# =========================================================
# UPLOAD PAGE
# =========================================================

if menu == "📤 Upload Documents":

    st.markdown("## 📤 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF or Images",
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=True
    )

    if not uploaded_files:

        st.info(
            "Upload one or more documents to begin AI processing."
        )

    else:

        total_files = len(uploaded_files)

        st.success(
            f"✅ {total_files} document(s) uploaded successfully."
        )

        progress_bar = st.progress(0)

        for file_index, uploaded_file in enumerate(uploaded_files):

            st.markdown("---")

            try:

                start_time = time.time()

                if uploaded_file.type not in ALLOWED_TYPES:

                    st.error("❌ Unsupported file type.")
                    continue

                if uploaded_file.size > 10 * 1024 * 1024:

                    st.error("❌ File size exceeds 10MB.")
                    continue

                preview_image = None
                pdf_preview_images = []

                try:

                    uploaded_file.seek(0)

                    if uploaded_file.type != "application/pdf":

                        file_bytes = uploaded_file.read()

                        pil_image = Image.open(
                            BytesIO(file_bytes)
                        ).convert("RGB")

                        preview_image = np.array(
                            pil_image,
                            dtype=np.uint8
                        )

                    else:

                        uploaded_file.seek(0)

                        pdf_images = pdf_to_images(
                            uploaded_file
                        )

                        if pdf_images:

                            preview_image = np.array(
                                pdf_images[0].convert("RGB"),
                                dtype=np.uint8
                            )

                            pdf_preview_images = [
                                np.array(
                                    img.convert("RGB"),
                                    dtype=np.uint8
                                )
                                for img in pdf_images[:6]
                            ]

                except Exception as e:

                    log_exception(e)
                    st.error(f"Preview Error: {str(e)}")

                uploaded_file.seek(0)

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=300
                )

                result = response.json()

                if not result.get("success", False):

                    st.error("Processing failed.")
                    continue

                document_type = result.get(
                    "document_type",
                    "Document"
                )

                all_text = result.get(
                    "ocr_text",
                    ""
                )

                entities = result.get(
                    "entities",
                    []
                )

                structured_output = result.get(
                    "structured_output",
                    {}
                )

                boxes = result.get(
                    "boxes",
                    []
                )

                table_data = result.get(
                    "table_data",
                    []
                )

                total_pages = result.get(
                    "pages",
                    1
                )

                confidence = round(
                    result.get("ocr_confidence", 0),
                    2
                )

                processing_time = round(
                    time.time() - start_time,
                    2
                )

                # =================================================
                # FIXED OCR VISUALIZATION
                # =================================================

                ocr_visualization = None
                text_detection_visualization = None

                if preview_image is not None and boxes:

                    try:

                        ocr_visualization = (
                            preview_image.copy()
                        )

                        text_detection_visualization = (
                            preview_image.copy()
                        )

                        image_height, image_width = (
                            preview_image.shape[:2]
                        )

                        for item in boxes:

                            try:

                                raw_points = item.get(
                                    "box",
                                    []
                                )

                                text = item.get(
                                    "text",
                                    ""
                                )

                                if len(raw_points) < 4:
                                    continue

                                points = np.array(
                                    raw_points,
                                    dtype=np.float32
                                )

                                points[:, 0] = np.clip(
                                    points[:, 0],
                                    0,
                                    image_width - 1
                                )

                                points[:, 1] = np.clip(
                                    points[:, 1],
                                    0,
                                    image_height - 1
                                )

                                points = points.astype(int)

                                x_min = np.min(points[:, 0])
                                y_min = np.min(points[:, 1])

                                x_max = np.max(points[:, 0])
                                y_max = np.max(points[:, 1])

                                # OCR BOX

                                cv2.rectangle(
                                    ocr_visualization,
                                    (x_min, y_min),
                                    (x_max, y_max),
                                    (0, 255, 0),
                                    2
                                )

                                label_y = max(
                                    y_min - 10,
                                    15
                                )

                                cv2.putText(
                                    ocr_visualization,
                                    text[:25],
                                    (x_min, label_y),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.55,
                                    (255, 255, 255),
                                    2,
                                    cv2.LINE_AA
                                )

                                # TEXT DETECTION

                                overlay = (
                                    text_detection_visualization.copy()
                                )

                                cv2.rectangle(
                                    overlay,
                                    (x_min, y_min),
                                    (x_max, y_max),
                                    (0, 255, 0),
                                    -1
                                )

                                cv2.addWeighted(
                                    overlay,
                                    0.22,
                                    text_detection_visualization,
                                    0.78,
                                    0,
                                    text_detection_visualization
                                )

                                cv2.rectangle(
                                    text_detection_visualization,
                                    (x_min, y_min),
                                    (x_max, y_max),
                                    (0, 255, 0),
                                    2
                                )

                            except Exception:
                                continue

                    except Exception as e:

                        log_exception(e)

                # =================================================
                # DOCUMENT HEADER
                # =================================================

                st.markdown(f"""
<div class="custom-card">

<h2 style="margin-bottom:0;">
📄 {uploaded_file.name}
</h2>

<p style="
font-size:18px;
color:{CLASSIFICATION_COLOR.get(document_type, '#fff')};
font-weight:700;
margin-top:5px;
">
Detected Type: {document_type}
</p>

</div>
""", unsafe_allow_html=True)

                m1, m2, m3, m4, m5, m6 = st.columns(6)

                m1.metric("📄 Pages", total_pages)
                m2.metric("🎯 Entities", len(entities))
                m3.metric("📊 Confidence", f"{confidence}%")
                m4.metric("⚡ Time", f"{processing_time}s")
                m5.metric("📂 Format", uploaded_file.type.split("/")[-1])
                m6.metric("📦 Tables", len(table_data))

                # =================================================
                # VISUALIZATION SECTION
                # =================================================

                if preview_image is not None:

                    st.markdown("## 🖼 Document Visualizations")

                    # ORIGINAL

                    st.markdown("### 📄 Original Document")

                    c1, c2, c3 = st.columns([0.08, 1, 0.08])

                    with c2:

                        st.image(
                            Image.fromarray(preview_image),
                            width=850
                        )

                    # OCR DETECTION

                    if ocr_visualization is not None:

                        st.markdown("### 🎯 OCR Detection")

                        c1, c2, c3 = st.columns([0.08, 1, 0.08])

                        with c2:

                            st.image(
                                Image.fromarray(
                                    ocr_visualization
                                ),
                                width=850
                            )

                    # TEXT DETECTION

                    if text_detection_visualization is not None:

                        st.markdown("### 📝 Text Detection")

                        c1, c2, c3 = st.columns([0.08, 1, 0.08])

                        with c2:

                            st.image(
                                Image.fromarray(
                                    text_detection_visualization
                                ),
                                width=850
                            )

                # =================================================
                # STRUCTURED OUTPUT
                # =================================================

                st.markdown("## 📋 Structured Output")

                st.json(
                    structured_output,
                    expanded=True
                )

                # =================================================
                # TABS
                # =================================================

                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📄 OCR Text",
                    "🎯 Entities",
                    "📊 Tables",
                    "🧪 Test Status",
                    "⬇ Export"
                ])

                with tab1:

                    st.text_area(
                        "OCR Result",
                        all_text,
                        height=320,
                        key=f"text_{file_index}"
                    )

                with tab2:

                    if entities:

                        entity_df = pd.DataFrame(entities)

                        st.dataframe(
                            entity_df,
                            use_container_width=True
                        )

                    else:

                        st.warning(
                            "No entities detected."
                        )

                with tab3:

                    if table_data:

                        try:

                            table_df = pd.DataFrame(
                                table_data
                            )

                            st.dataframe(
                                table_df,
                                use_container_width=True
                            )

                        except Exception:

                            st.json(table_data)

                    else:

                        st.warning(
                            "No tables detected."
                        )

                with tab4:

                    test_results = {
                        "Upload": True,
                        "OCR": bool(all_text),
                        "OCR Visualization":
                            ocr_visualization is not None,
                        "Text Detection":
                            text_detection_visualization
                            is not None,
                        "NER":
                            len(entities) > 0,
                        "Structured Output":
                            bool(structured_output),
                        "Export":
                            True
                    }

                    test_df = pd.DataFrame([
                        {
                            "Feature": key,
                            "Status":
                            "✅ Passed"
                            if value
                            else "❌ Failed"
                        }
                        for key, value
                        in test_results.items()
                    ])

                    st.dataframe(
                        test_df,
                        use_container_width=True
                    )

                with tab5:

                    json_data = json.dumps(
                        structured_output,
                        indent=4
                    )

                    d1, d2 = st.columns(2)

                    with d1:

                        st.download_button(
                            "⬇ Download JSON",
                            json_data,
                            file_name=(
                                f"{uploaded_file.name}_output.json"
                            ),
                            mime="application/json"
                        )

                    with d2:

                        st.download_button(
                            "⬇ Download OCR Text",
                            all_text,
                            file_name=(
                                f"{uploaded_file.name}_ocr.txt"
                            ),
                            mime="text/plain"
                        )

                try:

                    save_document(
                        uploaded_file.name,
                        document_type,
                        all_text,
                        entities,
                        structured_output
                    )

                except Exception as e:

                    log_exception(e)

                    st.error(
                        "Failed to save document."
                    )

            except Exception as e:

                log_exception(e)

                st.error(
                    f"Error processing {uploaded_file.name}"
                )

                st.exception(e)

            progress_bar.progress(
                (file_index + 1) / total_files
            )

        st.success(
            "🎉 All documents processed successfully."
        )

# =========================================================
# DOCUMENT HISTORY
# =========================================================

if menu == "📚 Document History":

    st.markdown("## 📚 Processed Documents")

    documents = fetch_documents()

    if not documents:

        st.warning("No documents found.")

    else:

        search = st.text_input(
            "🔍 Search Documents"
        )

        filtered_docs = []

        for doc in documents:

            title = str(doc[1])

            if search.lower() in title.lower():

                filtered_docs.append(doc)

        if search == "":

            filtered_docs = documents

        for doc in filtered_docs:

            doc_id = doc[0]
            document_title = doc[1]
            document_type = doc[2]
            created_at = doc[3]
            structured_output = doc[4]

            with st.expander(
                f"📄 {document_title}"
            ):

                st.markdown(f"""
### 📋 Document Information

- **Document Type:** {document_type}
- **Document ID:** {doc_id}
- **Processed At:** {created_at}
                """)

                st.json(structured_output)