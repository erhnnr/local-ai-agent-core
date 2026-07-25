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

    def generate_response(self, user_prompt: str) -> str:
        url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
            
        payload = {"inputs": user_prompt}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json() # Veriyi burada 'data' değişkenine atıyoruz
            
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "Yanıt çözümlenemedi.")
            elif isinstance(data, dict):
                return data.get("generated_text", data.get("error", "Yanıt alınamadı."))
                
            return str(data)
        except requests.exceptions.RequestException as e:
            return f"Hugging Face API bağlantı hatası: {e}"