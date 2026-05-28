# 🧠 Intelligent Document AI Studio

Enterprise-grade Intelligent Document Processing (IDP) System built using OCR, NLP, Computer Vision, Layout Intelligence, and FastAPI.

The system automatically extracts structured information from unstructured documents such as invoices, resumes, ID cards, reports, and medical documents.

---

# 🚀 Features

## 📄 OCR Extraction

* PaddleOCR Integration
* EasyOCR Support
* Multi-format document processing
* PDF/Image support

## 🧠 NLP & Entity Extraction

* spaCy Named Entity Recognition (NER)
* Regex-based extraction
* Hybrid entity pipeline
* Structured field extraction

## 📊 Table Extraction

* Intelligent table parsing
* Invoice item extraction
* Row/column detection
* Structured table outputs

## 📋 Structured Output

* JSON generation
* Key-value extraction
* Document-specific parsing
* Layout-aware extraction

## 📚 Analytics Dashboard

* Document analytics
* Classification statistics
* Processing history
* Interactive charts

## ⬇ Export System

* JSON Export
* CSV Export
* Excel Export
* OCR text download

## ☁ Enterprise Architecture

* FastAPI backend
* Streamlit frontend
* PostgreSQL database
* Modular code structure

---

# 🏗 System Architecture

```text
User Upload
     ↓
Image Preprocessing
     ↓
OCR Extraction
     ↓
Layout Analysis
     ↓
Table Detection
     ↓
NLP + Entity Extraction
     ↓
Structured Parsing
     ↓
JSON Generation
     ↓
Database Storage
     ↓
Analytics + Export
```

---

# 🛠 Technologies Used

## AI / NLP

* spaCy
* Regex Extraction
* NLP Entity Recognition

## OCR / Computer Vision

* PaddleOCR
* EasyOCR
* OpenCV
* PDF Processing

## Backend

* FastAPI
* REST APIs
* Python

## Frontend

* Streamlit
* Plotly
* Modern Enterprise UI

## Database

* PostgreSQL

---

# 📂 Project Structure

```text
Intelligent_Document_Processing_System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── backend/
│   ├── api/
│   └── services/
│
├── database/
│
├── ocr/
│
├── nlp/
│
├── preprocessing/
│
├── layout_extraction/
│
├── utils/
│
├── exports/
│
├── models/
│
└── test_documents/
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/intelligent-document-ai.git
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄 PostgreSQL Setup

Create a PostgreSQL database.

Update database configuration inside:

```text
database/postgresql.py
```

Example:

```python
DB_NAME = "document_ai"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

---

# ▶️ Run FastAPI Backend

```bash
uvicorn backend.api.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# ▶️ Run Streamlit Frontend

```bash
streamlit run app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# 📄 Supported Document Types

* Invoices
* Resumes
* ID Cards
* Reports
* Medical Documents

---

# 📂 Supported File Formats

* PDF
* PNG
* JPG
* JPEG

---

# 🎯 Key Capabilities

✅ OCR Text Extraction
✅ Named Entity Recognition
✅ Table Detection
✅ Structured JSON Output
✅ Layout Intelligence
✅ Export Functionality
✅ Analytics Dashboard
✅ PostgreSQL Storage
✅ Multi-document Processing
✅ Enterprise UI

---

# 📊 Outputs Generated

The system generates:

* Structured JSON
* Extracted OCR text
* CSV files
* Excel reports
* Entity tables
* Layout fields

---

# 📸 Application Modules

## 📤 Upload Documents

Upload and process multiple documents using the AI pipeline.

## 📚 Document History

View processed documents, analytics, and extraction history.

## ℹ️ About Project

Detailed overview of architecture, workflow, and technologies.

---

# 🚀 Future Improvements

* Advanced table extraction
* Custom trained NER model
* Cloud deployment
* Multi-language OCR
* Real-time document processing
* AI validation engine

---

# 🧪 Evaluation Metrics

* OCR Accuracy
* Entity Extraction Accuracy
* Table Parsing Quality
* Processing Speed
* UI/UX Quality
* Modular Architecture
* API Performance

---

# 👨‍💻 Developed Using

* Python
* FastAPI
* Streamlit
* PostgreSQL
* spaCy
* PaddleOCR
* OpenCV
* Plotly

---

# 📌 Project Status

```text
Project Completion: ~90%
```

---

# ❤️ Acknowledgement

This project was developed as an AI-powered Intelligent Document Processing System using OCR, NLP, Computer Vision, and FastAPI-based enterprise architecture.

---
