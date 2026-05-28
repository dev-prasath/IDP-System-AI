# =========================================================
# app.py
# NEXT-GEN ENTERPRISE IDP UI
# CLEAN + PREMIUM UI
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import json
import time
from io import BytesIO

import cv2
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import requests

from PIL import Image

# =========================================================
# DATABASE
# =========================================================

from database.postgresql import (
    fetch_documents,
    save_document
)

# =========================================================
# UTILITIES
# =========================================================

from utils.pdf_handler import pdf_to_images

from utils.logger import log_exception

from utils.highlight_entities import highlight_entities

from utils.export_utils import (
    export_entities_csv,
    export_entities_excel
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Document AI Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CONSTANTS
# =========================================================

ALLOWED_TYPES = [
    "image/png",
    "image/jpeg",
    "application/pdf"
]

DOC_COLORS = {
    "Invoice": "#22c55e",
    "Resume": "#3b82f6",
    "ID Card": "#a855f7",
    "Report": "#f59e0b",
    "Medical Document": "#ef4444",
    "Unknown": "#94a3b8"
}

# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* =========================================================
BACKGROUND
========================================================= */

.stApp {

    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.10), transparent 22%),
        radial-gradient(circle at top right, rgba(168,85,247,0.08), transparent 22%),
        linear-gradient(180deg, #020617 0%, #0f172a 100%);

    color: white;
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #020617,
            #0f172a,
            #111827
        );

    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* =========================================================
SCROLLBAR
========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

/* =========================================================
HERO
========================================================= */

.hero-container {

    padding: 1.5rem 2.2rem;

    border-radius: 24px;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.14),
            rgba(168,85,247,0.10)
        );

    border: 1px solid rgba(255,255,255,0.06);

    backdrop-filter: blur(18px);

    box-shadow:
        0 0 40px rgba(59,130,246,0.08);

    margin-bottom: 1.2rem;
}

.hero-title {

    font-size: 40px;

    font-weight: 800;

    margin-bottom: 6px;

    color: white;
}

.hero-subtitle {

    color: #cbd5e1;

    font-size: 14px;

    line-height: 1.5;

    margin-bottom: 14px;

    max-width: 900px;
}

.badge-row {

    display: flex;

    flex-wrap: nowrap;

    gap: 10
/* =========================================================
CARDS
========================================================= */

.glass-card {

    background:
        rgba(15,23,42,0.72);

    border: 1px solid rgba(255,255,255,0.06);

    border-radius: 24px;

    padding: 1.4rem;

    backdrop-filter: blur(18px);

    margin-bottom: 1.2rem;
}

.metric-card {

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.92),
            rgba(15,23,42,0.92)
        );

    border: 1px solid rgba(255,255,255,0.05);

    border-radius: 20px;

    padding: 18px;

    text-align: center;
}

.metric-title {

    color: #94a3b8;

    font-size: 13px;

    font-weight: 600;
}

.metric-value {

    font-size: 28px;

    font-weight: 800;

    margin-top: 8px;

    color: white;
}

/* =========================================================
DOC HEADER
========================================================= */

.doc-header {

    background:
        rgba(15,23,42,0.75);

    border: 1px solid rgba(255,255,255,0.06);

    border-radius: 24px;

    padding: 1.6rem;

    margin-bottom: 1.5rem;
}

.doc-title {

    font-size: 28px;

    font-weight: 800;

    margin-bottom: 18px;
}

.doc-type {

    display: inline-flex;

    align-items: center;

    gap: 10px;

    padding: 10px 18px;

    border-radius: 999px;

    font-size: 14px;

    font-weight: 700;

    color: white;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {

    width: 100%;

    height: 52px;

    border: none;

    border-radius: 16px;

    font-weight: 700;

    color: white;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        );

    transition: 0.3s;
}

.stButton > button:hover {

    transform: translateY(-1px);
}

.stDownloadButton > button {

    width: 100%;

    height: 50px;

    border-radius: 14px;

    border: none;

    font-weight: 700;

    color: white;

    margin-bottom: 12px;

    background:
        linear-gradient(
            90deg,
            #059669,
            #16a34a
        );
}

/* =========================================================
UPLOAD BOX
========================================================= */

[data-testid="stFileUploader"] {

    background:
        rgba(15,23,42,0.72);

    border: 2px dashed rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 1.6rem;
}

/* =========================================================
TABS
========================================================= */

.stTabs [data-baseweb="tab"] {

    background:
        rgba(255,255,255,0.04);

    border-radius: 12px;

    padding: 10px 18px;

    color: white;

    margin-right: 8px;

    font-weight: 600;
}

.stTabs [aria-selected="true"] {

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        ) !important;
}

/* =========================================================
JSON + TABLE
========================================================= */

.stJson {

    background:
        rgba(15,23,42,0.82) !important;

    border-radius: 18px;

    padding: 12px;
}

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.05);
}

/* =========================================================
TEXT AREA
========================================================= */

textarea {

    background:
        rgba(15,23,42,0.90) !important;

    color: white !important;

    border-radius: 18px !important;
}

/* =========================================================
IMAGE
========================================================= */

img {
    border-radius: 20px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🧠 Document AI")

    menu = st.radio(
        "Navigation",
        [
            "📤 Upload Documents",
            "📚 Document History",
            "ℹ️ About Project"
        ]
    )

    st.divider()

    st.markdown("## 📂 Supported Files")

    st.success("""
✔ PDF
✔ PNG
✔ JPG
✔ JPEG
""")

    st.markdown("## 🤖 AI Pipeline")

    st.info("""
✔ OCR Extraction
✔ NLP Processing
✔ Layout Analysis
✔ Table Detection
✔ Structured Parsing
✔ PostgreSQL Storage
""")

# =========================================================
# HERO ONLY FOR UPLOAD PAGE
# =========================================================

if menu == "📤 Upload Documents":

    st.markdown("""
    <div class="hero-container">

    <div class="hero-title">
    🧠 Document AI Studio
    </div>

    <div class="hero-subtitle">

    Intelligent Document Processing platform powered by OCR,
    NLP, Layout Intelligence, Table Extraction, and Structured Parsing.

    </div>

    <div>

    <span class="badge">⚡ OCR AI</span>

    <span class="badge">🧠 NLP</span>

    <span class="badge">📊 Tables</span>

    <span class="badge">📄 Layout AI</span>

    <span class="badge">☁ FastAPI</span>

    </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# UPLOAD PAGE
# =========================================================

if menu == "📤 Upload Documents":

    st.markdown("## 📤 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF or Image Files",
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=True
    )

    if not uploaded_files:

        st.info("Upload documents to begin processing.")

    else:

        progress_bar = st.progress(0)

        for file_index, uploaded_file in enumerate(uploaded_files):

            st.markdown("---")

            try:

                start_time = time.time()

                # =====================================================
                # VALIDATION
                # =====================================================

                if uploaded_file.type not in ALLOWED_TYPES:

                    st.error("❌ Unsupported file type.")
                    continue

                if uploaded_file.size > 10 * 1024 * 1024:

                    st.error("❌ File size exceeds 10MB.")
                    continue

                # =====================================================
                # PREVIEW
                # =====================================================

                preview_image = None

                try:

                    uploaded_file.seek(0)

                    if uploaded_file.type != "application/pdf":

                        image_bytes = uploaded_file.read()

                        pil_image = Image.open(
                            BytesIO(image_bytes)
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

                except Exception as preview_error:

                    log_exception(preview_error)

                # =====================================================
                # PROCESS
                # =====================================================

                uploaded_file.seek(0)

                with st.spinner("🧠 Processing document..."):

                    files = {

                        "file": (

                            uploaded_file.name,

                            uploaded_file,

                            uploaded_file.type
                        )
                    }

                    response = requests.post(
                        "http://127.0.0.1:8000/process-document",
                        files=files
                    )

                    if response.status_code != 200:

                        st.error(f"API Error: {response.text}")

                        continue

                    result = response.json()

                if not result.get("success", False):

                    st.error("❌ Processing failed.")
                    continue

                # =====================================================
                # RESULTS
                # =====================================================

                document_type = result.get(
                    "document_type",
                    "Unknown"
                )

                ocr_text = result.get("ocr_text", "")

                entities = result.get("entities", [])

                structured_output = result.get(
                    "structured_output",
                    {}
                )

                table_data = result.get(
                    "table_data",
                    []
                )

                layout_fields = result.get(
                    "layout_fields",
                    {}
                )

                boxes = result.get("boxes", [])

                total_pages = result.get(
                    "pages",
                    1
                )

                ocr_confidence = round(
                    result.get(
                        "ocr_confidence",
                        0
                    ),
                    2
                )

                processing_time = round(
                    time.time() - start_time,
                    2
                )

                # =====================================================
                # DOCUMENT HEADER
                # =====================================================

                st.markdown(f"""
                <div class="doc-header">

                <div class="doc-title">
                📄 {uploaded_file.name}
                </div>

                <div class="doc-type"
                style="background:{DOC_COLORS.get(document_type, "#64748b")};">

                {document_type}

                </div>

                </div>
                """, unsafe_allow_html=True)

                # =====================================================
                # METRICS
                # =====================================================

                cols = st.columns(5)

                metrics = [

                    ("📄 Pages", total_pages),
                    ("📊 OCR", f"{ocr_confidence}%"),
                    ("🎯 Entities", len(entities)),
                    ("📦 Tables", len(table_data)),
                    ("⚡ Time", f"{processing_time}s")
                ]

                for col, metric in zip(cols, metrics):

                    with col:

                        st.markdown(f"""
                        <div class="metric-card">

                        <div class="metric-title">
                        {metric[0]}
                        </div>

                        <div class="metric-value">
                        {metric[1]}
                        </div>

                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # =====================================================
                # DOCUMENT IMAGE
                # =====================================================

                if preview_image is not None:

                    st.markdown("## 🖼 Document Preview")

                    visual = preview_image.copy()

                    for item in boxes:

                        try:

                            polygon = item.get("box", [])

                            if polygon:

                                points = np.array(
                                    polygon,
                                    dtype=np.int32
                                )

                                cv2.polylines(
                                    visual,
                                    [points],
                                    True,
                                    (0, 255, 0),
                                    2
                                )

                        except Exception:
                            continue

                    visual = cv2.cvtColor(
                        visual,
                        cv2.COLOR_BGR2RGB
                    )

                    st.image(
                        Image.fromarray(visual),
                        width='stretch'
                    )

                # =====================================================
                # JSON
                # =====================================================

                st.markdown("## 📋 Structured Output")

                st.json(
                    structured_output,
                    expanded=True
                )

                # =====================================================
                # TABS
                # =====================================================

                tabs = st.tabs([
                    "📄 OCR Text",
                    "🎯 Entities",
                    "📊 Tables",
                    "🧠 Layout Fields",
                    "✨ Highlighted",
                    "⬇ Export"
                ])

                # OCR TAB

                with tabs[0]:

                    st.text_area(
                        "OCR Result",
                        ocr_text,
                        height=400,
                        key=f"ocr_{file_index}"
                    )

                # ENTITY TAB

                with tabs[1]:

                    if entities:

                        entity_df = pd.DataFrame(
                            entities
                        )

                        st.dataframe(
                            entity_df,
                            width='stretch'
                        )

                    else:

                        st.warning(
                            "No entities detected."
                        )

                # TABLE TAB

                with tabs[2]:

                    if table_data:

                        try:

                            table_df = pd.DataFrame(
                                table_data
                            )

                            st.dataframe(
                                table_df,
                                width='stretch'
                            )

                        except Exception:

                            st.json(table_data)

                    else:

                        st.warning(
                            "No tables detected."
                        )

                # LAYOUT TAB

                with tabs[3]:

                    if layout_fields:

                        st.json(layout_fields)

                    else:

                        st.info(
                            "No layout fields detected."
                        )

                # HIGHLIGHT TAB

                with tabs[4]:

                    try:

                        highlighted = highlight_entities(
                            ocr_text,
                            entities
                        )

                        st.markdown(
                            highlighted,
                            unsafe_allow_html=True
                        )

                    except Exception:

                        st.warning(
                            "Highlighting unavailable."
                        )

                # EXPORT TAB

                with tabs[5]:

                    col1, col2 = st.columns(2)

                    json_data = json.dumps(
                        structured_output,
                        indent=4
                    )

                    with col1:

                        st.download_button(
                            "⬇ Download JSON",
                            json_data,
                            file_name=f"{uploaded_file.name}.json",
                            mime="application/json"
                        )

                        st.download_button(
                            "⬇ Download CSV",
                            export_entities_csv(entities),
                            file_name=f"{uploaded_file.name}_entities.csv",
                            mime="text/csv"
                        )

                    with col2:

                        st.download_button(
                            "⬇ Download OCR Text",
                            ocr_text,
                            file_name=f"{uploaded_file.name}.txt",
                            mime="text/plain"
                        )

                        st.download_button(
                            "⬇ Download Excel",
                            export_entities_excel(entities),
                            file_name=f"{uploaded_file.name}_entities.xlsx",
                            mime=(
                                "application/vnd.openxmlformats-"
                                "officedocument.spreadsheetml.sheet"
                            )
                        )

                # =====================================================
                # SAVE DATABASE
                # =====================================================

                try:

                    save_document(
                        uploaded_file.name,
                        document_type,
                        ocr_text,
                        entities,
                        structured_output
                    )

                except Exception as db_error:

                    log_exception(db_error)

            except Exception as e:

                log_exception(e)

                st.error(
                    f"Error processing {uploaded_file.name}"
                )

                st.exception(e)

            progress_bar.progress(
                (file_index + 1) / len(uploaded_files)
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

        st.warning(
            "No processed documents found."
        )

    else:

        history_df = pd.DataFrame(

            documents,

            columns=[
                "id",
                "document_title",
                "document_type",
                "created_at",
                "structured_output"
            ]
        )

        # =====================================================
        # METRICS
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "📄 Total Documents",
                len(history_df)
            )

        with c2:

            st.metric(
                "🧾 Invoices",
                len(
                    history_df[
                        history_df["document_type"] == "Invoice"
                    ]
                )
            )

        with c3:

            st.metric(
                "📑 Resumes",
                len(
                    history_df[
                        history_df["document_type"] == "Resume"
                    ]
                )
            )

        with c4:

            st.metric(
                "🪪 ID Cards",
                len(
                    history_df[
                        history_df["document_type"] == "ID Card"
                    ]
                )
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================================
        # CHART
        # =====================================================

        pie_chart = px.pie(
            history_df,
            names="document_type",
            hole=0.55
        )

        pie_chart.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=420
        )

        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )

        # =====================================================
        # SEARCH
        # =====================================================

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

        # =====================================================
        # DOCUMENTS
        # =====================================================

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
                <div class="glass-card">

                <h3>📋 Document Information</h3>

                <ul style="line-height:2;">

                <li><b>Document Type:</b> {document_type}</li>

                <li><b>Document ID:</b> {doc_id}</li>

                <li><b>Processed At:</b> {created_at}</li>

                </ul>

                </div>
                """, unsafe_allow_html=True)

                st.json(structured_output)

# =========================================================
# ABOUT PROJECT
# =========================================================

if menu == "ℹ️ About Project":

    st.markdown("""
    <div class="hero-container">

    <div class="hero-title">
    ℹ️ About Intelligent Document AI
    </div>

    <div class="hero-subtitle">

    AI-powered Intelligent Document Processing System capable of extracting,
    analyzing, classifying, and structuring information from invoices,
    resumes, ID cards, reports, and enterprise documents.

    </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # MAIN LAYOUT
    # =====================================================

    left_col, right_col = st.columns([2.3, 1])

    # =====================================================
    # LEFT SIDE CONTENT
    # =====================================================

    with left_col:

        # =================================================
        # OVERVIEW
        # =================================================

        st.markdown("## 🚀 Project Overview")

        st.markdown("""
        <div class="glass-card">

        <p style="
        line-height:1.9;
        font-size:15px;
        color:#cbd5e1;
        ">

        This project is a modern Intelligent Document Processing (IDP)
        platform developed using OCR, NLP, Computer Vision,
        and Layout Intelligence.

        The system automatically extracts structured information
        from invoices, resumes, ID cards, reports,
        and other enterprise documents.

        The platform combines OCR extraction,
        table detection, entity recognition,
        layout analysis, and structured JSON generation
        into a complete AI-powered automation pipeline.

        </p>

        </div>
        """, unsafe_allow_html=True)

        # =================================================
        # TECHNOLOGIES
        # =================================================

        st.markdown("## 🛠 Technologies Used")

        tech1, tech2 = st.columns(2)

        with tech1:

            st.markdown("""
            <div class="glass-card">

            <h3>🧠 AI & NLP</h3>

            <ul style="line-height:2;">

            <li>spaCy NLP</li>
            <li>Regex Extraction</li>
            <li>NER Processing</li>
            <li>Document Classification</li>

            </ul>

            </div>
            """, unsafe_allow_html=True)

        with tech2:

            st.markdown("""
            <div class="glass-card">

            <h3>📄 OCR & Backend</h3>

            <ul style="line-height:2;">

            <li>PaddleOCR</li>
            <li>EasyOCR</li>
            <li>FastAPI</li>
            <li>PostgreSQL</li>

            </ul>

            </div>
            """, unsafe_allow_html=True)

        # =================================================
        # FEATURES
        # =================================================

        st.markdown("## ✨ Key Features")

        st.markdown("""
        <div class="glass-card">

        <ul style="
        line-height:2.2;
        font-size:15px;
        color:#cbd5e1;
        ">

        <li>📄 Multi-format document upload support</li>

        <li>🧠 AI-powered OCR text extraction</li>

        <li>📊 Intelligent table extraction and parsing</li>

        <li>🎯 Named Entity Recognition using NLP</li>

        <li>📋 Structured JSON output generation</li>

        <li>📚 Document history and analytics dashboard</li>

        <li>⬇ Export support for JSON, CSV, and Excel</li>

        <li>☁ Modular FastAPI backend architecture</li>

        <li>🗄 PostgreSQL database integration</li>

        <li>🎨 Modern enterprise-grade user interface</li>

        </ul>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # RIGHT SIDE WORKFLOW
    # =====================================================

    with right_col:

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">

        <h3 style="
        text-align:center;
        margin-bottom:28px;
        ">
        ⚙️ System Workflow
        </h3>

        <div style="
        display:flex;
        flex-direction:column;
        align-items:center;
        gap:10px;
        ">

        <div class="badge" style="
        width:100%;
        text-align:center;
        justify-content:center;
        ">
        📤 Upload
        </div>

        ⬇

        <div class="badge" style="
        width:100%;
        text-align:center;
        ">
        🖼 Preprocessing
        </div>

        ⬇

        <div class="badge" style="
        width:100%;
        text-align:center;
        ">
        📄 OCR
        </div>

        ⬇

        <div class="badge" style="
        width:100%;
        text-align:center;
        ">
        📊 Layout AI
        </div>

        ⬇

        <div class="badge" style="
        width:100%;
        text-align:center;
        ">
        🧠 NLP
        </div>

        ⬇

        <div class="badge" style="
        width:100%;
        text-align:center;
        ">
        📋 JSON
        </div>

        ⬇

        <div class="badge" style="
        width:100%;
        text-align:center;
        ">
        🗄 Storage
        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
    text-align:center;
    color:#94a3b8;
    padding:18px;
    font-size:14px;
    ">

    Built with ❤️ using OCR, NLP, FastAPI, Streamlit, and PostgreSQL

    </div>
    """, unsafe_allow_html=True)