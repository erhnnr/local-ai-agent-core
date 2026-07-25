from src.agents.tools import ToolRegistry
from src.logger import setup_logger
from src.rag.vector_kb import VectorKnowledgeBase

logger = setup_logger("DecisionAgent")

class DecisionAgent:
    """
    Geçmiş sohbetleri tutan, hata korumalı ve esnek niyet yönetimine sahip akıllı ajan sınıfı.
    """
    def __init__(self, llm_client):
        self.client = llm_client
        self.kb = VectorKnowledgeBase()
        self.chat_history = []
        logger.info("DecisionAgent başlatıldı ve Gelişmiş Niyet Yönetimi aktifleşti.")

    def _detect_intent(self, prompt: str) -> str:
        """Kullanıcı girdisini analiz ederek en uygun niyet kategorisini belirler."""
        p = prompt.lower()
        
        # Zaman niyetleri
        if any(k in p for k in ["saat kaç", "tarih nedir", "bugün günlerden", "saat kaçta"]):
            return "time"
            
        # Sistem durumu niyetleri
        if any(k in p for k in ["sistem bilgisi", "bilgisayar durumu", "ram", "işletim sistemi", "bellek durumu", "cpu"]):
            return "system_info"
            
        # Dosya okuma niyetleri
        if any(k in p for k in ["dosyayı oku", "oku:", "dosya içeriği", "kodunu göster"]):
            return "read_file"
            
        # Bilgi tabanı / RAG niyetleri
        if any(k in p for k in ["adr", "doküman", "bilgi tabanı", "araştır", "nasıl", "mimari", "strateji"]):
            return "knowledge_base"
            
        return "general_llm"

    def run(self, user_prompt: str) -> str:
        logger.info(f"Kullanıcı girdisi alındı: '{user_prompt}'")
        self.chat_history.append({"role": "user", "content": user_prompt})
        
        try:
            intent = self._detect_intent(user_prompt)
            response_text = ""
            
            if intent == "time":
                logger.info("Niyet tespiti [Gelişmiş Router]: Zaman sorgusu çalıştırılıyor.")
                tool_result = ToolRegistry.execute_tool("get_current_time", "")
                response_text = f"[Tool: get_current_time] Sonuç:\n{tool_result}"
                
            elif intent == "system_info":
                logger.info("Niyet tespiti [Gelişmiş Router]: Sistem bilgisi sorgusu çalıştırılıyor.")
                tool_result = ToolRegistry.execute_tool("get_system_info", "")
                response_text = f"[Tool: get_system_info] Sonuç:\n{tool_result}"

            elif intent == "read_file":
                words = user_prompt.split()
                target_file = "app.py"
                for word in words:
                    if "." in word:
                        target_file = word.strip(".,'\"")
                        break
                logger.info(f"Niyet tespiti [Gelişmiş Router]: Dosya okuma ({target_file}).")
                tool_result = ToolRegistry.execute_tool("read_local_file", target_file)
                response_text = f"[Tool: read_local_file ({target_file})] Sonuç:\n```python\n{tool_result}\n```"

            elif intent == "knowledge_base":
                logger.info("Niyet tespiti [Gelişmiş Router]: Semantik RAG araması tetikleniyor.")
                response_text = f"[Semantic RAG Sonucu]:\n{self.kb.search(user_prompt)}"

            else:
                logger.info("Niyet tespiti [Gelişmiş Router]: Genel LLM yanıt üretiliyor.")
                response_text = self.client.generate_response(user_prompt)

        except Exception as e:
            error_msg = f"Üzgünüm, isteğinizi işlerken beklenmeyen bir hata oluştu: {e!s}"
            logger.error(error_msg)
            response_text = f"[Hata Koruması]: {error_msg}"

        self.chat_history.append({"role": "assistant", "content": response_text})
        return response_text