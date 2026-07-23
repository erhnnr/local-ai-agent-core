import streamlit as st
import os
from src.adapters.mock_client import MockClient
from src.adapters.huggingface_client import HuggingFaceClient
from src.database.db_manager import DatabaseManager
from src.agents.agent_core import DecisionAgent

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Evrensel Karar Motoru",
    page_icon="🧠",
    layout="wide"
)

# Veritabanı ve Ajan Başlatma
db = DatabaseManager()

def get_llm_client():
    use_mock = os.getenv("USE_MOCK", "true").lower() == "true"
    if use_mock:
        return MockClient()
    else:
        return HuggingFaceClient(model_name="Qwen/Qwen2.5-7B-Instruct")

client = get_llm_client()
agent = DecisionAgent(llm_client=client)

# Arayüz Tasarımı
st.title("🧠 Evrensel Karar Motoru (Universal Decision Engine)")
st.markdown("Model-Agnostic mimariyle güçlendirilmiş otonom ajan ve karar destek paneli.")

# Yan Menü (Sidebar) - Geçmiş Kararlar ve Ayarlar
st.sidebar.header("⚙️ Kontrol Paneli")
mode = st.sidebar.radio("Çalışma Modu", ["Ajan Sohbeti", "Geçmiş Kararlar (Veritabanı)"])

if mode == "Ajan Sohbeti":
    st.subheader("Otonom Ajan ile İletişim")
    
    user_prompt = st.text_input("Ajana iletmek istediğiniz prompt veya soru:", "Merhaba, şu an saat kaç?")
    
    if st.button("Karar Üret / Çalıştır"):
        if user_prompt.strip():
            with st.spinner("Ajan çalışıyor ve karar üretiyor..."):
                # Ajanı çalıştır
                response = agent.run(user_prompt)
                
                # Veritabanına kaydet
                db.save_decision(user_prompt, response)
            
            st.success("İşlem tamamlandı ve veritabanına kaydedildi!")
            
            # Sonucu Göster
            st.markdown("### 🤖 Ajanın Yanıtı:")
            st.info(response)
        else:
            st.warning("Lütfen geçerli bir prompt girin.")

elif mode == "Geçmiş Kararlar (Veritabanı)":
    st.subheader("📚 Kayıtlı Karar Geçmişi")
    
    limit = st.sidebar.slider("Gösterilecek Kayıt Sayısı", 1, 20, 5)
    recent_records = db.get_recent_decisions(limit=limit)
    
    if recent_records:
        for idx, (prompt, response, timestamp) in enumerate(recent_records, 1):
            with st.expander(f"Kayıt #{idx} — {timestamp}"):
                st.markdown(f"**Gönderilen Prompt:** `{prompt}`")
                st.markdown(f"**Üretilen Yanıt:**")
                st.text(response)
    else:
        st.info("Henüz veritabanında kayıtlı bir karar bulunmuyor.")