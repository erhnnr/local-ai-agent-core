import requests

from src.adapters.base_client import BaseLLMClient


class OllamaClient(BaseLLMClient):
    """
    Ollama veya LM Studio gibi yerel sunucularla haberleşen somut adaptör.
    BaseLLMClient arayüzünü uygular.
    """
    def __init__(self, model_name: str = "qwen2.5:7b", base_url: str = "http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.base_url = base_url

    def generate_response(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "Yanıt alınamadı.")
        except requests.exceptions.RequestException as e:
            return f"Yerel motora bağlanırken hata oluştu: {e}"