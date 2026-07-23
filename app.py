import streamlit as st
import os
from src.adapters.mock_client import MockClient
from src.adapters.huggingface_client import HuggingFaceClient
from src.database.db_manager import DatabaseManager
from src.agents.agent_core import DecisionAgent

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Evrensel Karar Motoru - Akıllı Ajan",
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

# Arayüz Başlığı
st.title("🧠 Evrensel Karar Motoru (Hafızalı Ajan Modu)")
st.markdown("Model-Agnostic mimari, otonom araçlar ve kalıcı SQLite hafıza desteğiyle güçlendirilmiş karar destek paneli.")

# Yan Menü (Sidebar)
st.sidebar.header("⚙️ Kontrol Paneli")
mode = st.sidebar.radio("Çalışma Modu", ["Otonom Sohbet (Hafızalı)", "Geçmiş Kararlar (Veritabanı)"])

if mode == "Otonom Sohbet (Hafızalı)":
    st.subheader("🤖 Ajan ile Sohbet Oturumu")
    
    # Veritabanından geçmiş sohbetleri yükle ve Streamlit session_state içine aktar
    if "messages" not in st.session_state:
        db_history = db.get_chat_history(limit=50)
        st.session_state.messages = []
        if db_history:
            for role, content in db_history:
                st.session_state.messages.append({"role": role, "content": content})
        else:
            # Varsayılan Karşılama
            welcome_msg = "Merhaba! Ben Evrensel Karar Motoru ajanıyım. Size nasıl yardımcı olabilirim?"
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
            db.save_chat_message("assistant", welcome_msg)

    # Sohbet geçmişini ekranda göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcıdan yeni girdi al
    if user_prompt := st.chat_input("Bir şeyler sorun veya komut verin (örn: 'Şu an saat kaç?')..."):
        # Kullanıcı mesajını ekrana ekle ve kaydet
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        db.save_chat_message("user", user_prompt)
        
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Ajan yanıtını üret
        with st.chat_message("assistant"):
            with st.spinner("Ajan düşünüyor ve karar üretiyor..."):
                response = agent.run(user_prompt)
                
            st.markdown(response)
            
        # Asistan yanıtını kaydet
        st.session_state.messages.append({"role": "assistant", "content": response})
        db.save_chat_message("assistant", response)
        
        # Kararı ayrıca karar günlüklerine de işleyelim
        db.save_decision(user_prompt, response)

elif mode == "Geçmiş Kararlar (Veritabanı)":
    st.subheader("📚 Kayıtlı Karar Geçmişi ve Loglar")
    
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