# import requests
# import logging

# logger = logging.getLogger(__name__)

# class APIClient:
#     def __init__(self, base_url: str = None):
#         # 1. Check if 'BACKEND_URL' is set in the cloud environment
#         # 2. If not (like on your local PC), default to localhost
#         if base_url is None:
#             base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
            
#         self.base_url = base_url.rstrip('/')  # Clean any trailing slashes
#         self.session = requests.Session()
    
#     def summarize(self, document_text: str, max_length: int = 500) -> str:
#         response = self.session.post(f"{self.base_url}/api/summarize", json={"document_text": document_text, "max_length": max_length})
#         response.raise_for_status()
#         return response.json().get("summary", "")
    
#     def ask_question(self, document_text: str, question: str) -> str:
#         response = self.session.post(f"{self.base_url}/api/ask", json={"document_text": document_text, "question": question})
#         response.raise_for_status()
#         return response.json().get("answer", "")

#     def get_history(self):
#         try:
#             response = self.session.get(f"{self.base_url}/api/history")
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             logger.error(f"Error fetching history: {e}")
#             return []

#     def clear_all(self):
#         try:
#             response = self.session.delete(f"{self.base_url}/api/clear-all")
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             logger.error(f"Error clearing memory: {e}")
#             raise


import os
import requests
import logging

# Configure logging to see errors in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str = None):
        # 1. Prioritize environment variable for production (Render)
        # 2. Default to localhost for your local development
        if base_url is None:
            base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
            
        self.base_url = base_url.rstrip('/')  # Ensure no trailing slash
        self.session = requests.Session()
        
        logger.info(f"APIClient initialized with BASE_URL: {self.base_url}")

    def summarize(self, document_text: str, max_length: int = 500) -> str:
        try:
            payload = {"document_text": document_text, "max_length": max_length}
            response = self.session.post(
                f"{self.base_url}/api/summarize", 
                json=payload,
                timeout=60  # Increased timeout for LLM processing
            )
            response.raise_for_status()
            return response.json().get("summary", "No summary returned from server.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Summarization request failed: {e}")
            raise Exception("Backend is starting up or unreachable. Please try again in a moment.")

    def ask_question(self, document_text: str, question: str) -> str:
        try:
            payload = {"document_text": document_text, "question": question}
            response = self.session.post(
                f"{self.base_url}/api/ask", 
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json().get("answer", "I couldn't generate an answer.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Q&A request failed: {e}")
            raise Exception("Failed to connect to the AI engine. Check if the backend is running.")

    def get_history(self):
        try:
            # Short timeout here as history should be fast
            response = self.session.get(f"{self.base_url}/api/history", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Could not fetch history: {e}")
            return []

    def clear_all(self):
        try:
            response = self.session.delete(f"{self.base_url}/api/clear-all", timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
            raise Exception("Could not clear system memory.")