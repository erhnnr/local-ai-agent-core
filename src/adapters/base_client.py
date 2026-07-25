from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """
    Tüm LLM adaptörlerinin uyması gereken soyut arayüz (Interface).
    Model-Agnostic felsefenin temel taşıdır.
    """
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Verilen prompt için modelden yanıt üretir.
        
        Args:
            prompt (str): Modele gönderilecek girdi metni.
            
        Returns:
            str: Modelin ürettiği yanıt.
        """
