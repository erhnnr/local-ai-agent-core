from src.adapters.base_client import BaseLLMClient

class MockClient(BaseLLMClient):
    """
    İnternet veya harici motor gerektirmeyen, mimari testleri için 
    sahte yanıt üreten adaptör.
    """
    def generate_response(self, prompt: str) -> str:
        return f"[MOCK YANIT]: Mimari başarıyla test edildi! Alınan prompt: '{prompt}'"