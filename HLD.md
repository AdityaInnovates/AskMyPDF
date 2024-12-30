# High-Level Design (HLD) for PDF Q&A Chatbot Backend

## Overview

The PDF Q&A Chatbot Backend is a FastAPI application that allows users to upload PDF documents and ask questions about their content. The application processes the uploaded PDFs, stores them in a database, and utilizes a question-answering model to provide answers based on the document's content.

## Architecture Diagram

```
+-------------------+
|   User Interface  |
|     (Web App)     |
+---------+---------+
          |
          v
+---------+---------+
|   FastAPI Server  |
|   (API Endpoints) |
+---------+---------+
          |
          v
+---------+-----------------+
|   Database (PostgreSQL)   |
|   (Document Metadata &    |
|   Question-Answer Pairs)  |
+---------+-----------------+
          |
          v
+---------+-----------------+
|   Vector Store (Chroma)   |
|   (Document Embeddings)   |
+---------+-----------------+
          |
          v
+---------+--------------+
|     OpenAI API         |
|   (Question Answering) |
+------------------------+
```

## Components

- **Description**: The front-end application web that interacts with the FastAPI backend.

- **Functionality**: Allows users to upload PDF files and ask questions.

### 2. FastAPI Server

- **Description**: The core of the application that handles API requests.

- **Endpoints**:

  - **POST /upload/**: Uploads and processes a PDF file.

  - **POST /question/**: Accepts a document ID and a question, returns the answer.

  - **GET /documents/**: Lists all uploaded documents.

- **Middleware**: CORS middleware to allow cross-origin requests.

### 3. Database (PostgreSQL)

- **Description**: Stores metadata about uploaded documents and question-answer pairs.

- **Tables**:

  - **documents**: Stores information about each uploaded document (ID, filename, upload date, file path, vector store path).

  - **question_answers**: Stores questions and answers related to each document (ID, document ID, question, answer).

### 4. Vector Store (Chroma)

- **Description**: A vector store used for storing and retrieving document embeddings.

- **Functionality**: Processes PDF documents to create embeddings for question answering.

### 5. OpenAI API

- **Description**: Utilizes OpenAI's models for generating answers based on the context provided.
- **Functionality**: Takes the context of previous questions and answers along with the current question to generate a response.

## Data Flow

1. **User uploads a PDF**: The user uploads a PDF file through the front-end interface.
2. **File Processing**: The FastAPI server processes the file, stores it in the database, and creates a vector store for the document.
3. **Question Submission**: The user submits a question related to the uploaded document.
4. **Answer Generation**: The FastAPI server retrieves the document's context and uses the OpenAI API to generate an answer.
5. **Response to User**: The answer is sent back to the user through the front-end interface.

## Environment Variables

- **UPLOAD_DIR**: Directory for storing uploaded PDF files.
- **VECTORSTORE_DIR**: Directory for storing vector embeddings.
- **OPENAI_API_KEY**: API key for accessing OpenAI services.
- **DATABASE_URL**: Connection string for the PostgreSQL database.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: Database for storing document metadata and question-answer pairs.
- **Langchain**: Library for processing documents and generating embeddings.
- **ChromaDB**: Vector store for storing and retrieving document embeddings.
- **CORS Middleware**: To handle cross-origin requests.
