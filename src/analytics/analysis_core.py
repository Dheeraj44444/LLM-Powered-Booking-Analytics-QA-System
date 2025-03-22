# src/analytics/analysis_core.py
import pandas as pd
import calendar

class BookingAnalytics:
    def __init__(self):
        self.df = pd.read_csv("C:/Users/Dheeraj/Desktop/Projects/LLM-Powered Booking Analytics & QA System/data/processed/clean_bookings.csv")
        self.df['arrival_date'] = pd.to_datetime(self.df['arrival_date'])
    
    def revenue_trend(self):
        monthly_rev = self.df.resample('ME', on='arrival_date')['adr'].sum()
        return {
            "dates": monthly_rev.index.strftime('%Y-%m-%d').tolist(),
            "values": monthly_rev.values.tolist()
        }
    
    def cancellation_rate(self):
        return float((self.df['is_canceled'].mean() * 100).round(2))
    
    def geographical_distribution(self):
        country_counts = self.df['country'].value_counts().head(10)
        return {
            "countries": country_counts.index.tolist(),
            "counts": country_counts.values.tolist()
        }
    
    def monthly_revenue(self, month: int, year: int):
        filtered = self.df[
            (self.df['arrival_date'].dt.month == month) &
            (self.df['arrival_date'].dt.year == year)
        ]
        return filtered['adr'].sum()
    
    def cancellation_by_location(self):
        cancelled = self.df[self.df['is_canceled'] == 1]
        return cancelled['country'].value_counts().head(5).to_dict()
    
    def average_price(self):
        return float(self.df['adr'].mean().round(2))