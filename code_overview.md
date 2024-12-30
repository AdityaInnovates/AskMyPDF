# Code Architecture Overview for AskMyPdf Chatbot Backend

## Overview

The AskMyPdf Chatbot Backend is built using FastAPI and is designed to allow users to upload PDF documents and ask questions about their content. The architecture consists of several key components that work together to provide a seamless experience.

## Key Components

### 1. FastAPI Server

- **Role**: Acts as the core of the application, handling API requests and responses.
- **Endpoints**:
  - **POST /upload/**: Accepts PDF uploads and processes them.
  - **POST /question/**: Handles questions related to uploaded documents and returns answers.
  - **GET /documents/**: Lists all uploaded documents.
- **Middleware**: Implements CORS to allow cross-origin requests.

### 2. Database (PostgreSQL)

- **Role**: Stores metadata about uploaded documents and question-answer pairs.
- **Tables**:
  - **documents**: Contains information about each uploaded document (ID, filename, upload date, file path, vector store path).
  - **question_answers**: Stores questions and answers related to each document (ID, document ID, question, answer).

### 3. Vector Store (Chroma)

- **Role**: Manages document embeddings for efficient retrieval during question answering.
- **Functionality**: Processes PDF documents to create embeddings that are stored and retrieved for generating answers.

### 4. OpenAI API

- **Role**: Utilizes OpenAI's models to generate answers based on the context provided.
- **Functionality**: Takes the context of previous questions and answers along with the current question to generate a response.

### 5. Libraries and Utilities

- **Langchain**: Used for processing documents and generating embeddings.
- **SQLAlchemy**: ORM for database interactions, facilitating easy data manipulation.
- **dotenv**: Manages environment variables for configuration.

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
