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
            
        # Hava durumu niyetleri
        if any(k in p for k in ["hava durumu", "hava nasıl", "sıcaklık"]):
            return "weather"
            
        # Dosya okuma niyetleri
        if any(k in p for k in ["dosyayı oku", "oku:", "dosya içeriği", "kodunu göster"]):
            return "read_file"
            
        # Bilgi tabanı / RAG niyetleri
        if any(k in p for k in ["adr", "doküman", "bilgi tabanı", "araştır", "nasıl", "mimari", "strateji"]):
            return "knowledge_base"
            
        return "general_llm"

    def run(self, user_prompt: str) -> str:
        logger.info(f"Kullanıcı girdisi alındı [Otonom Döngü Aktif]: '{user_prompt}'")
        self.chat_history.append({"role": "user", "content": user_prompt})
        
        try:
            # Otonom zincir / planlama aşaması
            prompt_lower = user_prompt.lower()
            response_parts = []
            
            # Çoklu niyet analizi (Otonom döngü bileşenleri)
            if "sistem" in prompt_lower or "ram" in prompt_lower:
                logger.info("[Otonom Adım] Sistem bilgisi toplanıyor.")
                sys_res = ToolRegistry.execute_tool("get_system_info", "")
                response_parts.append(f"**[Sistem Durumu]**\n{sys_res}")
                
            if "saat" in prompt_lower or "tarih" in prompt_lower:
                logger.info("[Otonom Adım] Zaman bilgisi alınıyor.")
                time_res = ToolRegistry.execute_tool("get_current_time", "")
                response_parts.append(f"**[Zaman Bilgisi]**\n{time_res}")

            if any(k in prompt_lower for k in ["hava durumu", "hava nasıl", "sıcaklık"]):
                logger.info("[Otonom Adım] Canlı hava durumu alınıyor.")
                city = "Antalya"
                for word in user_prompt.split():
                    if word.istitle() or word.lower() in ["antalya", "istanbul", "ankara", "izmir", "bursa"]:
                        city = word.capitalize()
                        break
                weather_res = ToolRegistry.execute_tool("get_weather", city)
                response_parts.append(f"**[Hava Durumu Bilgisi]**\n{weather_res}")
                
            if any(k in prompt_lower for k in ["oku", "kod", "dosya"]):
                logger.info("[Otonom Adım] Dosya okuma adımı tetikleniyor.")
                target_file = "app.py"
                for word in user_prompt.split():
                    if "." in word:
                        target_file = word.strip(".,'\"")
                        break
                file_res = ToolRegistry.execute_tool("read_local_file", target_file)
                response_parts.append(f"**[Dosya İçeriği ({target_file})]**\n```python\n{file_res}\n```")

            # Eğer özel bir otonom araç tetiklenmediyse standart LLM / RAG akışına dön
            if not response_parts:
                intent = self._detect_intent(user_prompt)
                if intent == "knowledge_base":
                    logger.info("[Otonom Döngü] Bilgi tabanı (RAG) tarandı.")
                    response_parts.append(f"[Semantic RAG Sonucu]:\n{self.kb.search(user_prompt)}")
                else:
                    logger.info("[Otonom Döngü] Doğrudan LLM yanıtı üretiliyor.")
                    response_parts.append(self.client.generate_response(user_prompt))

            response_text = "\n\n".join(response_parts)

        except Exception as e:
            error_msg = f"Otonom yürütme sırasında hata oluştu: {e!s}"
            logger.error(error_msg)
            response_text = f"[Hata Koruması]: {error_msg}"

        self.chat_history.append({"role": "assistant", "content": response_text})
        return response_text