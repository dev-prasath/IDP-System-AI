# 📄 Intelligent Document Processing System

AI-powered Intelligent Document Processing (IDP) system built using OCR, NLP, Computer Vision, FastAPI, Streamlit, and PostgreSQL.

The system automatically extracts structured information from unstructured documents such as:

- Invoices
- Resumes
- ID Cards
- Reports
- Forms
- Healthcare Documents

using Deep Learning, OCR, and Named Entity Recognition (NER).

---

# 🚀 Features

## ✅ OCR Text Extraction

- Multi-format document support
- PDF, PNG, JPG, JPEG support
- Multi-page PDF processing
- OCR visualization with bounding boxes
- OCR confidence scoring

### OCR Engines

- EasyOCR
- Tesseract OCR
- TrOCR (Optional)

---

## ✅ NLP Entity Extraction

Automatically extracts:

- Names
- Dates
- Addresses
- Phone Numbers
- Emails
- Invoice Numbers
- Amounts
- Skills
- Education
- Experience

using:

- HuggingFace Transformers
- SpaCy
- Regex Validation

---

## ✅ Intelligent Document Classification

Automatically detects:

- Invoice
- Resume
- ID Card
- Report
- Medical Document

---

## ✅ AI-Powered Table Extraction

Extracts:

- Invoice tables
- Structured rows and columns
- Line items
- Financial tables

---

## ✅ Streamlit Dashboard

Modern responsive dashboard with:

- Multi-file upload
- OCR visualization
- Entity highlighting
- Structured JSON output
- Export functionality
- Document history
- Search functionality

---

## ✅ FastAPI Backend

REST APIs for:

- Document upload
- OCR processing
- NLP extraction
- Structured response generation
- Database integration

---

## ✅ PostgreSQL Integration

Stores:

- Uploaded documents
- OCR text
- Extracted entities
- Structured outputs
- Processing timestamps

---

# 🏗️ System Architecture

```plaintext
User Upload
     ↓
Streamlit Frontend
     ↓
FastAPI Backend
     ↓
Image Preprocessing
     ↓
OCR Extraction
     ↓
NLP + Entity Extraction
     ↓
Validation + Postprocessing
     ↓
Structured JSON Output
     ↓
PostgreSQL Database
```

---

# 📂 Project Structure

```plaintext
Intelligent_Document_Processing_System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── schemas/
│
├── preprocessing/
│   ├── image_processing.py
│   ├── image_enhancement.py
│   └── pdf_processing.py
│
├── ocr/
│   ├── easyocr_engine.py
│   ├── tesseract_engine.py
│   └── trocr_engine.py
│
├── nlp/
│   ├── entity_extractor.py
│   ├── regex_patterns.py
│   ├── validators.py
│   └── postprocessing.py
│
├── database/
│   ├── postgresql.py
│   └── db_manager.py
│
├── utils/
│   ├── logger.py
│   ├── entity_highlighter.py
│   ├── table_extractor.py
│   ├── response_builder.py
│   └── validators.py
│
├── uploads/
├── exports/
├── logs/
├── tests/
├── assets/
├── docs/
└── notebooks/
```

---

# 🧠 Technologies Used

## Frontend

- Streamlit

## Backend

- FastAPI
- Uvicorn

## OCR

- EasyOCR
- Tesseract OCR
- TrOCR

## NLP

- HuggingFace Transformers
- SpaCy
- Regex

## Computer Vision

- OpenCV
- Pillow

## Database

- PostgreSQL

## Machine Learning / Deep Learning

- PyTorch
- Transformers

## Deployment

- Docker
- Streamlit Cloud
- HuggingFace Spaces

---

# 📊 Supported Document Types

| Document Type | Supported |
|---|---|
| Invoice | ✅ |
| Resume | ✅ |
| ID Card | ✅ |
| Medical Record | ✅ |
| Report | ✅ |
| Forms | ✅ |

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/intelligent-document-processing-system.git
```

```bash
cd intelligent-document-processing-system
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Setup

## Create Database

```sql
CREATE DATABASE intelligent_document_ai;
```

---

## Update Database Credentials

Inside `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=intelligent_document_ai
DB_USER=postgres
DB_PASSWORD=your_password
```

---

# ▶️ Running the Application

## Step 1 — Start FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs on:

```plaintext
http://127.0.0.1:8000
```

---

## Step 2 — Start Streamlit Frontend

```bash
streamlit run app.py
```

Frontend runs on:

```plaintext
http://localhost:8501
```

---

# 📌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/process-document` | Process uploaded document |
| GET | `/documents` | Fetch processed documents |
| GET | `/health` | Health check |

---

# 📄 Sample Workflow

## Step 1

Upload document

## Step 2

Image preprocessing

## Step 3

OCR extraction

## Step 4

Entity extraction using NLP

## Step 5

Validation and postprocessing

## Step 6

Structured JSON generation

## Step 7

Save results to PostgreSQL

## Step 8

Display results in Streamlit dashboard

---

# 📊 Sample Structured Output

```json
{
    "document_type": "Invoice",
    "invoice_number": "INV-1024",
    "vendor_name": "ABC Technologies",
    "invoice_date": "2026-05-23",
    "total_amount": "$2500"
}
```

---

# 🎯 OCR Visualization

The system provides:

- OCR bounding box visualization
- Text region detection
- Entity highlighting
- Confidence scoring

---

# 📈 Validation Features

The system validates:

- Email formats
- Phone numbers
- Dates
- Invoice numbers
- Amount fields

using:

- Regex patterns
- Rule-based validation
- NLP confidence filtering

---

# 🔐 Error Handling

The application gracefully handles:

- Invalid file uploads
- OCR failures
- API failures
- Empty documents
- Corrupted PDFs
- Unsupported formats

---

# 🧪 Testing

Run tests using:

```bash
pytest tests/
```
---

# 📚 Future Enhancements

- LayoutLM integration
- Multilingual OCR
- Human-in-the-loop correction
- Async batch processing
- Cloud-native scaling
- Vector database integration
- LLM-based document understanding

---

# 👨‍💻 Author

Dev Prasath RP

---

# 🌐 Deployment

Deployment instructions will be added in the final stage of the project.

Possible deployment platforms:

- Streamlit Cloud
- HuggingFace Spaces
- Render
- Railway
- AWS EC2
- Docker Deployment



