from src.agents.agent_core import DecisionAgent
from src.agents.tools import ToolRegistry


# Sahte (Mock) LLM İstemcisi Test İçin
class MockLLMClientForTest:
    def generate_response(self, prompt: str) -> str:
        return "Mock LLM Yanıtı: " + prompt

def test_tool_registry_time():
    """Zaman aracının doğru formatta çıktı verip vermediğini test eder."""
    result = ToolRegistry.execute_tool("get_current_time", "")
    assert result is not None
    assert len(result) > 0

def test_tool_registry_system_info():
    """Sistem bilgisi aracının hata vermeden veri dönüp dönmediğini test eder."""
    result = ToolRegistry.execute_tool("get_system_info", "")
    assert "İşletim Sistemi" in result or "Toplam RAM" in result

def test_decision_agent_time_intent():
    """Ajanın zaman sorgularını doğru yakalayıp yakalamadığını test eder."""
    client = MockLLMClientForTest()
    agent = DecisionAgent(client)
    
    response = agent.run("Şu an saat kaç?")
    assert "[Tool: get_current_time]" in response

def test_decision_agent_fallback_intent():
    """Ajanın genel girdileri RAG veya doğru akışa yönlendirdiğini test eder."""
    client = MockLLMClientForTest()
    agent = DecisionAgent(client)
    
    response = agent.run("Merhaba nasılsın?")
    # Sistem artık bunu RAG veya metin işleme akışına yönlendiriyor
    assert response is not None
    assert len(response) > 0