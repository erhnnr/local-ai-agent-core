import os

from src.adapters.huggingface_client import HuggingFaceClient
from src.adapters.mock_client import MockClient
from src.agents.agent_core import DecisionAgent
from src.database.db_manager import DatabaseManager


def get_llm_client():
    use_mock = os.getenv("USE_MOCK", "true").lower() == "true"
    if use_mock:
        return MockClient()
    else:
        return HuggingFaceClient(model_name="Qwen/Qwen2.5-7B-Instruct")

def main():
    print("Evrensel Karar Motoru (Ajan Modu) başlatılıyor...")
    
    db = DatabaseManager()
    client = get_llm_client()
    
    # Ajanı başlatıyoruz
    agent = DecisionAgent(llm_client=client)
    
    prompt = "Merhaba, şu an saat kaç?"
    print(f"Gönderilen Prompt: {prompt}\n")
    
    # Ajan üzerinden yanıtı alıyoruz (Gerekirse araç çalıştıracak)
    response = agent.run(prompt)
    
    print("--- Ajanın Yanıtı ---")
    print(response)
    
    # Veritabanına kaydet
    db.save_decision(prompt, response)
    print("\n[Bilgi]: Ajan kararı veritabanına başarıyla kaydedildi.")

if __name__ == "__main__":
    main()