# src/data_processing/data_cleaner.py
import pandas as pd
import os
from datetime import datetime

def clean_data():
    os.makedirs("C:/Users/Dheeraj/Desktop/Projects/LLM-Powered Booking Analytics & QA System/data/processed", exist_ok=True)
    df = pd.read_csv("C:/Users/Dheeraj/Desktop/Projects/LLM-Powered Booking Analytics & QA System/data/raw/hotel_bookings.csv")
    
    # Data cleaning
    df['children'] = df['children'].fillna(0).astype(int)
    df['country'] = df['country'].fillna('Unknown')
    df['agent'] = df['agent'].fillna(0).astype(int)
    df = df.dropna(subset=['adr'])
    
    # Create datetime column
    df['arrival_date'] = pd.to_datetime(
        df['arrival_date_year'].astype(str) + '-' +
        df['arrival_date_month'].str.strip().str.title() + '-' +
        df['arrival_date_day_of_month'].astype(str),
        errors='coerce'
    )
    
    df.to_csv("C:/Users/Dheeraj/Desktop/Projects/LLM-Powered Booking Analytics & QA System/data/processed/clean_bookings.csv", index=False)
    return df

if __name__ == "__main__":
    clean_data()