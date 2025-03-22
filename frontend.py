# frontend.py
import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Configuration
BACKEND_URL = "http://localhost:8000"
st.set_page_config(page_title="Booking Analytics", layout="wide")

def get_analytics_data():
    """Fetch analytics data from backend"""
    try:
        response = requests.post(f"{BACKEND_URL}/analytics")
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.ConnectionError:
        return None

def ask_question(question: str):
    """Send question to Q&A endpoint"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"text": question}
        )
        return response.json()["answer"] if response.status_code == 200 else "Error fetching response"
    except requests.exceptions.ConnectionError:
        return "Backend service unavailable"

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Analytics Dashboard", "Ask Questions"])

    if page == "Analytics Dashboard":
        st.title("📊 Booking Analytics Dashboard")
        
        data = get_analytics_data()
        if not data:
            st.error("Could not connect to analytics service")
            return

        # Revenue Trend
        st.subheader("Monthly Revenue Trend")
        df_revenue = pd.DataFrame({
            "Date": data["revenue_trend"]["dates"],
            "Revenue": data["revenue_trend"]["values"]
        })
        st.line_chart(df_revenue.set_index("Date"))

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cancellation Rate", f"{data['cancellation_rate']}%")
        with col2:
            st.metric("Average Price", f"€{data['average_price']:.2f}")
        
        # Country Distribution
        st.subheader("Top Booking Countries")
        df_countries = pd.DataFrame({
            "Country": data["country_distribution"]["countries"],
            "Bookings": data["country_distribution"]["counts"]
        })
        st.bar_chart(df_countries.set_index("Country"))

    elif page == "Ask Questions":
        st.title("❓ Booking Data Q&A")
        
        question = st.text_input("Ask a question about booking data:", 
                               placeholder="e.g. What's the average price in Portugal?")
        
        if question:
            answer = ask_question(question)
            st.info(f"**Question:** {question}")
            st.success(f"**Answer:** {answer}")

        st.subheader("Example Questions")
        examples = [
            "Show me total revenue for July 2017",
            "Which locations had the highest booking cancellations?",
            "What is the average price of a hotel booking?",
            "Compare cancellations between Portugal and Spain"
        ]
        
        for example in examples:
            if st.button(example):
                answer = ask_question(example)
                st.info(f"**Question:** {example}")
                st.success(f"**Answer:** {answer}")

if __name__ == "__main__":
    main()