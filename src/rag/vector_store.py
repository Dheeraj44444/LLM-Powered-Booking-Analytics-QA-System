# src/rag/vector_store.py
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store():
    df = pd.read_csv("C:/Users/Dheeraj/Desktop/Projects/LLM-Powered Booking Analytics & QA System/data/processed/clean_bookings.csv")
    
    # Convert string dates to datetime
    df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')
    
    # Handle missing/invalid dates
    df['arrival_date'] = df['arrival_date'].fillna(pd.Timestamp('2023-01-01'))
    
    # Create page content with safe date formatting
    df["page_content"] = df.apply(
        lambda row: (
            f"Country: {row['country']} | "
            f"Status: {'Canceled' if row['is_canceled'] else 'Kept'} | "
            f"Price: €{row['adr']} | "
            f"Arrival: {row['arrival_date'].strftime('%b %Y') if pd.notnull(row['arrival_date']) else 'Unknown'} | "  # Safe formatting
            f"Nights: {row['stays_in_week_nights'] + row['stays_in_weekend_nights']}"
        ), axis=1
    )
    
    loader = DataFrameLoader(df, page_content_column="page_content")
    docs = loader.load()
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store