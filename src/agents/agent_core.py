from src.agents.tools import ToolRegistry

class DecisionAgent:
    """
    Gelen istekleri analiz eden ve gerekirse araçları (tools) 
    devreye sokarak karar üreten akıllı ajan sınıfı.
    """
    def __init__(self, llm_client):
        self.client = llm_client

    def run(self, user_prompt: str) -> str:
        """
        Basit bir ajan mantığı: Prompt içinde matematiksel bir işlem veya 
        zaman sorgusu varsa ilgili aracı tetikler, yoksa doğrudan LLM kullanır.
        """
        prompt_lower = user_prompt.lower()
        
        # Basit bir niyet tespiti (Intent Recognition) ve Tool Routing
        if "saat kaç" in prompt_lower or "tarih nedir" in prompt_lower:
            tool_result = ToolRegistry.execute_tool("get_current_time", "")
            return f"[Tool: get_current_time] Sonuç: {tool_result}"
            
        elif "hesapla" in prompt_lower or "kaç eder" in prompt_lower:
            # Örnek basit ayıklama
            # Gerçek senaryoda bu kısmı LLM parse eder
            return "[Tool Kullanımı]: Lütfen hesaplanacak matematiksel ifadeyi belirtin (örn: calculate_expression)."
            
        # Eğer araç gerektirmeyen genel bir sorgu ise doğrudan LLM istemcisine gönder
        return self.client.generate_response(user_prompt)