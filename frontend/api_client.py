import requests
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str = None):
        # 1. Check if 'BACKEND_URL' is set in the cloud environment
        # 2. If not (like on your local PC), default to localhost
        if base_url is None:
            base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
            
        self.base_url = base_url.rstrip('/')  # Clean any trailing slashes
        self.session = requests.Session()
    
    def summarize(self, document_text: str, max_length: int = 500) -> str:
        response = self.session.post(f"{self.base_url}/api/summarize", json={"document_text": document_text, "max_length": max_length})
        response.raise_for_status()
        return response.json().get("summary", "")
    
    def ask_question(self, document_text: str, question: str) -> str:
        response = self.session.post(f"{self.base_url}/api/ask", json={"document_text": document_text, "question": question})
        response.raise_for_status()
        return response.json().get("answer", "")

    def get_history(self):
        try:
            response = self.session.get(f"{self.base_url}/api/history")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            return []

    def clear_all(self):
        try:
            response = self.session.delete(f"{self.base_url}/api/clear-all")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
            raise