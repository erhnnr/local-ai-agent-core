import os
import requests
from src.adapters.base_client import BaseLLMClient

class HuggingFaceClient(BaseLLMClient):
    """
    Hugging Face Serverless Inference API ile haberleşen adaptör.
    Sıfır RAM tüketimi ve bulut tabanlı çalışma sağlar.
    """
    def __init__(self, model_name: str = "Qwen/Qwen2.5-7B-Instruct", api_token: str = None):
        self.model_name = model_name
        # Token'ı parametre olarak alabilir veya sistem ortam değişkeninden (environment variable) okuyabiliriz
        self.api_token = api_token or os.getenv("HF_TOKEN")
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        
        if not self.api_token:
            raise ValueError("Hugging Face API Token bulunamadı! Lütfen token'ınızı tanımlayın.")

    def generate_response(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 250, "return_full_text": False}
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            # Hugging Face API bazen liste döner
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "Yanıt çözümlenemedi.")
            elif isinstance(data, dict):
                return data.get("generated_text", data.get("error", "Yanıt alınamadı."))
                
            return str(data)
        except requests.exceptions.RequestException as e:
            return f"Hugging Face API bağlantı hatası: {e}"