# PDF Q&A API

## Overview

The PDF Q&A API is a FastAPI application that allows users to upload PDF documents and ask questions about their content. The application processes the uploaded PDFs, stores them in a database, and utilizes a question-answering model to provide answers based on the document's content.

### Architecture

- **FastAPI**: The web framework used to build the API.
- **SQLAlchemy**: The ORM used for database interactions.
- **PostgreSQL**: The database used to store document metadata and question-answer pairs.
- **Langchain**: A library used for processing documents and generating embeddings for question answering.
- **ChromaDB**: A vector store used for storing and retrieving document embeddings.
- **CORS Middleware**: Allows cross-origin requests to the API.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following content:

   ```env
   UPLOAD_DIR=uploads
   VECTORSTORE_DIR=vectorstores/chromaDB
   OPENAI_API_KEY=<your_openai_api_key>
   DATABASE_URL=<your_posgresql_db_full_url>
   ```

5. **Run the database migrations** (if applicable):
   Ensure your database is set up and run any necessary migrations.

6. **Start the application**:
   ```bash
   fastapi run
   ```

## API Documentation

### Endpoints

#### 1. Upload PDF

- **POST** `/upload/`
- **Description**: Upload and process a PDF file.
- **Request**:
  - `file`: The PDF file to upload.
- **Response**:
  - `document_id`: The ID of the uploaded document.
  - `message`: Success message.

#### 2. Ask Question

- **POST** `/question/`
- **Description**: Ask a question about a specific document.
- **Request**:
  - `document_id`: The ID of the document.
  - `question`: The question to ask.
- **Response**:
  - `answer`: The answer to the question.
  - `document_id`: The ID of the document.

#### 3. List Documents

- **GET** `/documents/`
- **Description**: List all uploaded documents.
- **Response**:
  - A list of documents with their IDs, filenames, and upload dates.

### Example Requests

#### Upload PDF

```bash
curl -X POST "http://localhost:8000/upload/" -F "file=@path/to/your/file.pdf"
```

#### Ask Question

```bash
curl -X POST "http://localhost:8000/question/" -H "Content-Type: application/json" -d '{"document_id": 1, "question": "What is the main topic of the document?"}'
```

#### List Documents

```bash
curl -X GET "http://localhost:8000/documents/"
```
