import os
from src.adapters.mock_client import MockClient
from src.adapters.huggingface_client import HuggingFaceClient

def get_llm_client():
    """
    Ortam değişkenine veya duruma göre kullanılacak istemciyi seçer.
    İnternet/Model varsa gerçek istemci, yoksa Mock istemci döner.
    """
    use_mock = os.getenv("USE_MOCK", "true").lower() == "true"
    
    if use_mock:
        return MockClient()
    else:
        return HuggingFaceClient(model_name="Qwen/Qwen2.5-7B-Instruct")

def main():
    print("Yapay zeka motoruna bağlanılıyor...")
    
    # Mimari üzerinden istemciyi alıyoruz
    client = get_llm_client()
    
    prompt = "Merhaba! Sen kimsin ve hangi mimariyle çalışıyorsun? Türkçe olarak tek cümleyle özetle."
    print(f"Gönderilen Prompt: {prompt}\n")
    
    response = client.generate_response(prompt)
    
    print("--- Modelin Yanıtı ---")
    print(response)

if __name__ == "__main__":
    main()