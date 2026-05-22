# Enterprise Document Intelligence Platform

Live App: https://enterprise-document-intelligence-platform-ujsr9obkeqkfj23jhvjb.streamlit.app/

An AI-powered document intelligence system for analyzing business documents, extracting important information, classifying clauses, reviewing risk indicators, and answering document-specific questions using retrieval-based AI.

This project is built using Python, Streamlit, NLP, semantic search, LLM integration, entity extraction, clause analysis, risk scoring, and voice-enabled interaction.

---

## Business Problem

Business teams often need to review long documents such as contracts, agreements, policies, reports, and business PDFs. Manual document review can be slow, repetitive, and difficult when users need to quickly find clauses, risks, entities, and important information.

This project solves that problem by allowing users to upload PDF documents and perform:

- Document Q&A
- Entity extraction
- Clause analysis
- Risk review
- Executive summary generation
- Retrieval-based document search
- Voice-enabled AI interaction

The system is designed as a document intelligence assistant for business and enterprise use cases.

---

## Live Demo

Streamlit Application:

https://enterprise-document-intelligence-platform-ujsr9obkeqkfj23jhvjb.streamlit.app/

---

## Key Features

- Upload multiple PDF documents
- Extract text from uploaded PDFs
- Split long documents into searchable chunks
- Ask questions about uploaded documents
- Retrieve relevant document evidence
- Generate business-friendly executive summaries
- Extract entities such as dates, money values, emails, percentages, and business terms
- Classify document sections into business clause categories
- Review document risk using transparent keyword-based scoring
- Use semantic search with `all-MiniLM-L6-v2`
- Use fast keyword search with TF-IDF
- Voice input and voice output support
- Download entity and clause reports
- Streamlit Cloud deployment

---

## Tech Stack

| Category | Tools / Libraries |
|---|---|
| Programming Language | Python |
| Web Framework | Streamlit |
| PDF Processing | PyMuPDF |
| NLP | Text cleaning, chunking, entity extraction |
| Retrieval | TF-IDF, Sentence Transformers |
| Semantic Search Model | all-MiniLM-L6-v2 |
| Machine Learning Utility | scikit-learn |
| LLM Integration | Groq API |
| Voice Features | Speech input and text-to-speech |
| Data Handling | Pandas |
| Deployment | Streamlit Cloud |

---

## Project Workflow

```text
PDF Upload
↓
PDF Text Extraction
↓
Text Cleaning
↓
Document Chunking
↓
Entity Extraction
↓
Clause Classification
↓
Risk Scoring
↓
Retrieval Index Creation
↓
Document Q&A
↓
Executive Summary / Reports / Voice Output
```

---

## Project Structure

```text
enterprise-document-intelligence-platform/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── document_loader.py
│   ├── text_processing.py
│   ├── entity_extraction.py
│   ├── retrieval_engine.py
│   ├── clause_classifier.py
│   ├── risk_engine.py
│   ├── llm_service.py
│   └── reporting.py
│
├── data/
├── outputs/
├── screenshots/
└── sample_documents/
```

---

## Application Pages

### 1. Document Q&A

Users can ask questions about the uploaded documents.  
The system retrieves the most relevant document sections and generates an answer using the retrieved context.

Outputs include:

- User question
- AI-generated answer
- Retrieved document evidence
- Relevance score
- Voice output support

---

### 2. Executive Summary

Generates a business-friendly summary of the uploaded documents.

The summary includes:

- Document overview
- Important business terms
- Key clauses or topics
- Risk observations
- Recommended next actions

---

### 3. Entity Intelligence

Extracts important document entities such as:

- Dates
- Email addresses
- Monetary values
- Percentages
- Business terms

The extracted results are displayed in a table and can be downloaded as a CSV report.

---

### 4. Clause Analysis

Classifies document chunks into common business clause categories such as:

- Payment
- Termination
- Confidentiality
- Liability
- Warranty
- Renewal
- Governing Law
- General Business Clause

This helps users quickly understand the structure and major topics inside the document.

---

### 5. Risk Review

Performs keyword-based risk scoring on the uploaded document.

The risk engine checks for high-risk and medium-risk business/legal terms and calculates a risk score.

The output includes:

- Risk level
- Risk score
- High-risk term count
- Medium-risk term count
- Risk explanation

---

## Retrieval Methods

### TF-IDF Search

TF-IDF is used for fast keyword-based retrieval.  
It works well when the user’s question contains similar words to the document.

### Semantic Search

Semantic search uses the `all-MiniLM-L6-v2` Sentence Transformer model.  
It helps retrieve relevant document sections based on meaning, not only exact keyword matches.

This improves document Q&A when users ask questions in different wording from the original document.

---

## Risk Scoring Method

The risk review is based on transparent keyword scoring.

The system checks the uploaded document for risk-related terms such as:

- termination
- penalty
- liability
- indemnity
- breach
- exclusivity
- non-compliance
- damages
- dispute
- legal obligation

The score is calculated based on the number and severity of matched risk indicators.

Risk levels are displayed as:

```text
Low Risk
Medium Risk
High Risk
```

This is intended for business triage and should be validated by a human reviewer for final decisions.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/praveenraj9623-sketch/enterprise-document-intelligence-platform.git
cd enterprise-document-intelligence-platform
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

### Mac / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file in the project root.

Add your Groq API key:

```text
GROQ_API_KEY=your_api_key_here
```

For Streamlit Cloud deployment, add the same key inside Streamlit Secrets.

---

## Run Locally

Start the Streamlit app:

```bash
python -m streamlit run app.py
```

Then open the local URL shown in the terminal.

Usually:

```text
http://localhost:8501
```

---

## How to Use

1. Open the Streamlit app
2. Upload one or more PDF documents
3. Select the search engine:
   - Fast Keyword Search
   - Semantic AI Search
4. Adjust chunk size, overlap, and retrieved sections if needed
5. Click **Analyze Documents**
6. Use the tabs:
   - Document Q&A
   - Executive Summary
   - Entity Intelligence
   - Clause Analysis
   - Risk Review
7. Ask questions and review retrieved evidence
8. Download reports if required

---

## Screenshots

Add screenshots inside the `screenshots/` folder.

Recommended screenshot names:

```text
document_qa.png
executive_summary.png
entity_intelligence.png
risk_review.png
```

### Document Q&A

![Document Q&A](screenshots/document_qa.png)

### Executive Summary

![Executive Summary](screenshots/executive_summary.png)

### Entity Intelligence

![Entity Intelligence](screenshots/entity_intelligence.png)

### Risk Review

![Risk Review](screenshots/risk_review.png)

---

## Deployment

This project is deployed using Streamlit Cloud.

Live App:

https://enterprise-document-intelligence-platform-ujsr9obkeqkfj23jhvjb.streamlit.app/

Deployment requirements:

```text
streamlit
pandas
numpy
scikit-learn
sentence-transformers
pymupdf
python-dotenv
groq
```

---

## Skills Demonstrated

- Python
- Streamlit app development
- NLP pipeline development
- PDF text extraction
- Text cleaning
- Document chunking
- Entity extraction
- Information retrieval
- Semantic search
- TF-IDF retrieval
- Sentence Transformers
- Retrieval-Augmented Generation workflow
- LLM integration
- Executive summary generation
- Clause classification
- Risk scoring
- Voice-enabled AI interaction
- Streamlit Cloud deployment

---

## Limitations

- The system works best with text-based PDFs.
- Scanned/image-based PDFs require OCR support.
- The risk score is keyword-based and should be used as a business review indicator, not as final legal advice.
- LLM-generated responses should be reviewed before making business or legal decisions.

---

## Future Improvements

- OCR support for scanned PDFs
- Multi-language document support
- Advanced legal clause classification
- Role-based authentication
- Document comparison
- Batch document processing
- Cloud vector database integration
- User-level document history
- Advanced analytics dashboard

---

## Resume Description

Built an Enterprise Document Intelligence Platform using Python, Streamlit, NLP, semantic search, and LLM integration. Implemented PDF text extraction, document chunking, entity extraction, clause classification, keyword-based risk scoring, retrieval-based document Q&A, executive summary generation, semantic search using all-MiniLM-L6-v2, and voice-enabled interaction. Deployed the application on Streamlit Cloud for live document analysis.

---

## Author

**Praveen Raj A**

LinkedIn:  
https://www.linkedin.com/in/praveen-raj-a-b05abb2a3/

GitHub:  
https://github.com/praveenraj9623-sketch
