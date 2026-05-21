# Enterprise RAG Document Intelligence Platform

Enterprise Document Intelligence Platform is a voice-enabled AI application that helps users analyze PDF documents using NLP, retrieval-based search, LLM-powered question answering, executive summaries, entity extraction, clause analysis, and rule-based risk review. The system is built with Python, Streamlit, PyMuPDF, scikit-learn, Groq LLM, and voice AI libraries.
---
## Live Demo

🔗 Streamlit Application:  
https://enterprise-document-intelligence-platform-ujsr9obkeqkfj23jhvjb.streamlit.app/

---

## Deployment Notes

The deployed Streamlit Cloud version currently uses lightweight retrieval for stable cloud execution.

### Semantic Search Support

This project supports two retrieval modes:

- Fast Keyword Search (TF-IDF based)
- Semantic AI Search (Sentence Transformers + Vector Embeddings)

### Important Note About Streamlit Cloud Deployment

The complete semantic vector search pipeline works correctly in the local development environment. However, Streamlit Community Cloud has memory and dependency limitations for heavy AI libraries such as:

```txt
sentence-transformers
torch
```

Because of these cloud limitations, the deployed public version may automatically fall back to lightweight TF-IDF retrieval for stability and faster deployment.

### Full Semantic Search (Local Machine)

To run full semantic embedding-based retrieval locally, add the following packages to `requirements.txt`:

```txt
sentence-transformers
torch
faiss-cpu
```

Then run locally using:

```bash
streamlit run app.py
```


# Features

## Intelligent PDF Processing
- Upload multiple business PDF documents
- Automatic text extraction
- Smart document chunking
- Semantic indexing

## Conversational AI Document Q&A
- Ask questions about uploaded documents
- Context-aware retrieval using vector search
- LLM-powered intelligent answers
- Evidence-grounded responses

## Executive Summary Generation
- AI-generated executive summaries
- Business-focused document insights
- Risk observations and recommendations

## Entity Intelligence
Automatically extracts:
- Emails
- Dates
- Percentages
- Monetary values
- Business entities

## Clause Analysis
Classifies:
- Payment clauses
- Termination clauses
- Confidentiality clauses
- Liability clauses
- Legal/business sections

## Risk Review Engine
- Automated business risk scoring
- High-risk keyword detection
- Medium-risk indicator analysis

## Voice AI Support
- Voice-based document questioning
- Text-to-speech AI answers
- Conversational AI interaction

---

# Tech Stack

## Frontend
- Streamlit

## NLP & AI
- Groq LLM
- Sentence Transformers
- Semantic Search
- Vector Retrieval
- NLP Pipelines

## Machine Learning
- scikit-learn
- TF-IDF Retrieval
- Embedding Similarity

## Voice AI
- streamlit-mic-recorder
- gTTS

## Data Processing
- pandas
- NumPy

## PDF Processing
- PyMuPDF

---

# Project Architecture

```text
enterprise_doc_ai_production/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── clause_classifier.py
│   ├── document_loader.py
│   ├── entity_extraction.py
│   ├── llm_service.py
│   ├── reporting.py
│   ├── retrieval_engine.py
│   ├── risk_engine.py
│   └── text_processing.py
│
├── data/
├── outputs/
└── screenshots/
```

---

## Deployment

This application can be deployed for free using:

- Streamlit Community Cloud

---

# Use Cases

- Enterprise document intelligence
- Legal contract analysis
- Conversational AI document assistant
- Risk review automation
- Business clause analysis
- Semantic document search
- Voice-enabled AI assistant

---

# Skills Demonstrated

- Natural Language Processing (NLP)
- Conversational AI
- Semantic Search
- Vector Retrieval
- Retrieval-Augmented Generation (RAG)
- Large Language Model (LLM) Integration
- Voice AI
- Information Extraction
- Streamlit Deployment
- Enterprise AI Workflow Design

---

# Future Improvements

- OCR support for scanned PDFs
- Multi-language document support
- Fine-tuned transformer models
- Cloud vector database integration
- Role-based authentication
- Real-time collaboration support
- Advanced legal AI pipelines

---

# Author

## Praveen Raj

- LinkedIn:  
  https://www.linkedin.com/in/praveen-raj-a-b05abb2a3/

- GitHub:  
  https://github.com/praveenraj9623-sketch
