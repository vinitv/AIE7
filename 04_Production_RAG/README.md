# Production RAG Application

This repository contains a production-ready RAG (Retrieval-Augmented Generation) application built with LangChain, LangGraph, and LangSmith for processing student loan documents.

## Quick Start

### Using UV (Recommended)
```bash
uv sync
python app.py
```

### Using Pip
```bash
pip install -r requirements.txt
python app.py
```

## What's Included

- **app.py**: Complete RAG application with LangSmith integration
- **requirements.txt**: Package dependencies
- **pyproject.toml**: UV package management configuration
- **APP_README.md**: Detailed documentation for the app.py application
- **data/**: Directory containing PDF documents for processing
- **LangSmith_and_Evaluation.ipynb**: Jupyter notebook with tasks and activities

## Features

- Document processing from PDF files
- Intelligent chunking with tiktoken
- Vector storage using Qdrant
- LangGraph pipeline architecture
- Enhanced prompt engineering for context relevance
- LangSmith integration for tracing and monitoring

## API Keys Required

- OpenAI API Key
- LangSmith API Key (free account at https://www.langchain.com/langsmith)

## Documentation

For detailed setup and usage instructions, see [APP_README.md](APP_README.md). 