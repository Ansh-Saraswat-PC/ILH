import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
# Swap with Google/OpenAI embeddings as needed
from langchain_openai import OpenAIEmbeddings 

class EnterpriseRAG:
    def __init__(self, embedding_model=None):
        self.embeddings = embedding_model or OpenAIEmbeddings()
        self.vector_store = None

    def ingest_data(self, file_path: str):
        """Dynamically load based on file extension."""
        print(f"Ingesting {file_path}...")
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.csv'):
            loader = CSVLoader(file_path)
        else:
            raise ValueError("Unsupported file type. Add loader logic here.")
            
        docs = loader.load()
        
        # Chunking strategy: Crucial for enterprise accuracy
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=150
        )
        splits = text_splitter.split_documents(docs)
        
        # Build Vector Store
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        print(f"Successfully vectorized {len(splits)} chunks.")

    def get_retriever(self):
        if not self.vector_store:
            raise Exception("No data ingested yet!")
        return self.vector_store.as_retriever(search_kwargs={"k": 4})