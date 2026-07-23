import os
from src.adapters.mock_client import MockClient
from src.adapters.huggingface_client import HuggingFaceClient
from src.database.db_manager import DatabaseManager

def get_llm_client():
    use_mock = os.getenv("USE_MOCK", "true").lower() == "true"
    if use_mock:
        return MockClient()
    else:
        return HuggingFaceClient(model_name="Qwen/Qwen2.5-7B-Instruct")

def main():
    print("Evrensel Karar Motoru başlatılıyor...")
    
    # Veritabanı yöneticisini ve LLM istemcisini hazırlıyoruz
    db = DatabaseManager()
    client = get_llm_client()
    
    prompt = "Merhaba! Sen kimsin ve hangi mimariyle çalışıyorsun?"
    print(f"Gönderilen Prompt: {prompt}\n")
    
    # Yanıtı al
    response = client.generate_response(prompt)
    print("--- Modelin Yanıtı ---")
    print(response)
    
    # Veritabanına kaydet
    db.save_decision(prompt, response)
    print("\n[Bilgi]: Karar veritabanına başarıyla kaydedildi.")

if __name__ == "__main__":
    main()