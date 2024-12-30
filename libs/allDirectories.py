import os
allDirectories = {
    "UPLOAD_DIR" : os.getenv("UPLOAD_DIR","uploads"),
    "VECTORSTORE_DIR" : os.getenv("VECTORSTORE_DIR","vectorstores/chromaDB")
}