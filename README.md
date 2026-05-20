# Enterprise Document Intelligence Platform

A production-style Streamlit application for AI-powered business document review.

## Overview

This project analyzes long business documents such as contracts, policies, agreements, and reports. It extracts text, identifies key entities, classifies clauses, retrieves relevant sections for user questions, and creates risk-aware summaries.

## Core Capabilities

- PDF document ingestion
- Text extraction and preprocessing
- Document chunking
- Entity extraction
- Clause classification
- Retrieval-based question answering
- Executive summary generation
- Risk review dashboard
- Streamlit user interface

## Tech Stack

- Python
- Streamlit
- pandas
- pypdf
- scikit-learn
- TF-IDF retrieval
- HuggingFace SentenceTransformers
- Gemini API with graceful fallback
- Logistic Regression clause classifier

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables

Create a `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
```

The app works without the API key using retrieval-based fallback answers.

## Recommended Dataset

CUAD - Contract Understanding Atticus Dataset.

Use 3 to 5 PDF contracts first for testing.

## Resume Description

Built a production-style enterprise document intelligence platform for business contract analysis using NLP, information extraction, retrieval-based question answering, clause classification, and risk summarization. Developed a Streamlit interface for PDF upload, entity intelligence, clause review, document Q&A, and executive summary generation.
