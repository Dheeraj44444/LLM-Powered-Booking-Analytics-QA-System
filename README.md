# LLM-Powered Booking Analytics & QA System

A comprehensive solution for processing hotel booking data, extracting actionable insights, and enabling retrieval-augmented question answering (RAG) using an open-source LLM. This system provides both analytical reports (e.g., revenue trends, cancellation rates, geographical distributions) and an interactive Q&A interface for booking-related queries.

## Project Overview

The **LLM-Powered Booking Analytics & QA System** is designed to:

- **Clean & Preprocess Data:**  
  - Handle missing values, drop invalid rows, and consolidate date fields into a single `arrival_date`.  
  - Save the processed data for reproducible analysis.
  
- **Generate Analytics:**  
  - **Revenue Trends:** Analyze monthly revenue through time-series resampling.  
  - **Cancellation Rate:** Compute the percentage of canceled bookings.  
  - **Geographical Distribution:** Break down bookings by country.  
  - **Lead Time Analysis:** Categorize booking lead times into bins.

- **Integrate RAG for Q&A:**  
  - Store booking records as vectors in FAISS.  
  - Use an open-source LLM (e.g., Mistral-7B) with custom prompt engineering to answer user queries.  
  - Retrieve top relevant booking records before generating answers.

- **Expose Functionality via REST API & Dashboard:**  
  - **`POST /analytics`:** Returns aggregated metrics.  
  - **`POST /ask`:** Accepts natural language questions and returns context-based answers.  
  - **Streamlit Dashboard:** Visualizes analytics and performance metrics.

## Key Features

- **Data Preprocessing:**  
  - Cleans raw data by filling missing values (e.g., `children`, `country`), dropping invalid entries (e.g., negative ADR values), and merging date columns into a unified field.
  
- **Analytics & Reporting:**  
  - **Revenue Trends:** Monthly revenue analysis using time-series resampling.  
  - **Cancellation Rate:** Calculation based on canceled bookings over total bookings.  
  - **Geographical Distribution:** Aggregation of booking counts by country.  
  - **Lead Time Analysis:** Binning of booking lead times for insight on booking behavior.

- **Retrieval-Augmented Q&A:**  
  - Uses FAISS for efficient vector similarity search.  
  - Leverages an LLM for generating answers based on retrieved context.
  
- **REST API & Dashboard:**  
  - Provides API endpoints for analytics and Q&A.  
  - Includes a Streamlit dashboard for monitoring system performance and visualizing results.


## Dataset

This project uses the [Hotel Booking Demand dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) from Kaggle. The dataset includes a variety of attributes related to hotel bookings, which are utilized for:

- Cleaning and preprocessing the data.
- Extracting analytical insights such as revenue trends, cancellation rates, and geographical distribution.
- Building the vector store for the RAG system.

## Installation & Usage

### Clone the Repository

```bash
git clone https://github.com/Dheeraj44444/LLM-Powered-Booking-Analytics-QA-System.git
cd LLM-Powered-Booking-Analytics-QA-System
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment

Create a `.env` file in the project root with your HuggingFace API key:

```env
HF_API_KEY="your_huggingface_token"
```

### Data Preparation

1. **Clean the Data:**

   Run the data cleaning script to process the raw hotel booking data:

   ```bash
   python src/data_processing/data_cleaner.py
   ```

2. **Build the Vector Store:**

   Generate vector embeddings for the booking records:

   ```bash
   python -c "from src.rag.vector_store import create_vector_store; create_vector_store()"
   ```

### Run the API Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn src.api.main:app --reload
```

### Launch the Frontend Dashboard

Open the Streamlit dashboard to monitor analytics and performance metrics:

```bash
streamlit run frontend.py
```
Below is the README file with the sections in the same order as provided, including a dedicated Dataset section:

---

## Screenshots & API Endpoints

### Booking Analytics Dashboard

![analytics dashboard](https://github.com/user-attachments/assets/8109f225-0e15-4606-9845-089200b1b9df)

- **Visualization:**  
  - Monthly revenue trend visualization, cancellation rate, average booking price, and top booking countries are displayed on the dashboard.

### Booking Data Q&A

![1](https://github.com/user-attachments/assets/50a6404c-c50f-415e-a588-001501ccbb54)
![2](https://github.com/user-attachments/assets/2f73992d-63f0-49d2-ad2b-84fdddd78464)
![3](https://github.com/user-attachments/assets/2ecfd6fe-481a-4cd5-a863-75a0c04e791a)
![4](https://github.com/user-attachments/assets/9866221e-fdf3-45e7-bbdc-e2669974ac82)

- **Interactive Interface:**  
  - Ask questions in natural language and receive context-driven answers using the RAG system.

### API Endpoints

#### POST `/analytics`

- **Purpose:**  
  Returns key analytics including revenue trends, cancellation rate, and geographical distribution.

- **Example Response:**

  ```json
  {
    "revenue_trend": {"dates": ["2021-01", "2021-02"], "values": [15000, 16000]},
    "cancellation_rate": 37.04,
    "country_distribution": {"countries": ["PRT", "GBR"], "counts": [200, 150]}
  }
  ```

#### POST `/ask`

- **Purpose:**  
  Accepts natural language questions about booking data and returns an answer using the RAG approach.

- **Example Request:**

  ```json
  {"text": "What is the cancellation rate?"}
  ```

- **Example Response:**

  ```json
  {"answer": "37.04%"}
  ```
