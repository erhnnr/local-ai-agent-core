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
        Niyet tespiti yaparak zaman, hesaplama veya dosya okuma araçlarını tetikler,
        aksi halde doğrudan LLM yanıtı üretir.
        """
        prompt_lower = user_prompt.lower()
        
        # 1. Zaman Sorgusu
        if "saat kaç" in prompt_lower or "tarih nedir" in prompt_lower:
            tool_result = ToolRegistry.execute_tool("get_current_time", "")
            return f"[Tool: get_current_time] Sonuç:\n{tool_result}"
            
        # 2. Dosya Okuma Sorgusu (Örn: "app.py dosyasını oku")
        elif "dosyayı oku" in prompt_lower or "oku:" in prompt_lower or "dosya içeriği" in prompt_lower:
            # Basit bir kelime ayıklama (örneğin dosya adını bulma)
            words = user_prompt.split()
            target_file = "app.py" # Varsayılan
            for word in words:
                if "." in word: # Uzantısı olan bir dosya adı yakala
                    target_file = word.strip(".,'\"")
                    break
            
            tool_result = ToolRegistry.execute_tool("read_local_file", target_file)
            return f"[Tool: read_local_file ({target_file})] Sonuç:\n```python\n{tool_result}\n```"

        # 3. Genel LLM Yanıtı
        return self.client.generate_response(user_prompt)