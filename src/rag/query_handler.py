# src/rag/query_handler.py
import re
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import settings

class BookingQA:
    def __init__(self):
        self.llm = HuggingFaceEndpoint(
            endpoint_url="mistralai/Mistral-7B-Instruct-v0.1",
            temperature=0.1,
            max_new_tokens=100,
            huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY
        )
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vector_store = FAISS.load_local(
            "faiss_index",
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        self.prompt_template = """Answer question using only this context:
        {context}
        
        Question: {question}
        Answer:"""
        
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={
                "prompt": PromptTemplate(
                    template=self.prompt_template,
                    input_variables=["context", "question"]
                )
            }
        )

    def ask(self, question: str) -> str:
        try:
            result = self.qa.invoke({"query": question})
            return self._smart_parse(result["result"], question)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _smart_parse(self, text: str, question: str) -> str:
        # Handle currency values
        if any(word in question.lower() for word in ["price", "cost", "adr"]):
            match = re.search(r"€?\d+([.,]\d+)+", text)
            return match.group(0) if match else "Price data unavailable"
        
        # Handle location queries
        if "location" in question.lower() or "country" in question.lower():
            countries = re.findall(r"[A-Z]{3}", text)
            return ", ".join(countries[:3]) if countries else "Location data unavailable"
        
        return text