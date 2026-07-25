
import streamlit as st

from src.adapters.huggingface_client import HuggingFaceClient
from src.adapters.mock_client import MockClient
from src.agents.agent_core import DecisionAgent
from src.database.db_manager import DatabaseManager

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Evrensel Karar Motoru - Akıllı Ajan",
    page_icon="🧠",
    layout="wide"
)

# Veritabanı Başlatma
db = DatabaseManager()

# Arayüz Yan Menü - Model ve Mod Seçimi
st.sidebar.header("⚙️ Sistem ve Model Ayarları")
selected_model_type = st.sidebar.selectbox(
    "LLM Motoru Seçin",
    ["Mock Model (Hızlı Test)", "Hugging Face (Qwen/Qwen2.5-7B-Instruct)"]
)

# Seçilen modele göre istemciyi belirle
if "Mock" in selected_model_type:
    client = MockClient()
else:
    # Gerçek model istemcisi
    client = HuggingFaceClient(model_name="Qwen/Qwen2.5-7B-Instruct")

# Ajanı güncel istemci ile başlat
agent = DecisionAgent(llm_client=client)

mode = st.sidebar.radio("Çalışma Modu", ["Otonom Sohbet (Hafızalı)", "Geçmiş Kararlar (Veritabanı)"])

# Arayüz Başlığı
st.title("🧠 Evrensel Karar Motoru (Çoklu Model Desteği)")
st.markdown(f"Aktif Model: **{selected_model_type}** | Otonom Araçlar ve Kalıcı Hafıza Aktif.")

if mode == "Otonom Sohbet (Hafızalı)":
    st.subheader("🤖 Ajan ile Sohbet Oturumu")
    
    # Sohbet geçmişini veritabanından yükle
    if "messages" not in st.session_state:
        db_history = db.get_chat_history(limit=50)
        st.session_state.messages = []
        if db_history:
            for role, content in db_history:
                st.session_state.messages.append({"role": role, "content": content})
        else:
            welcome_msg = "Merhaba! Ben Evrensel Karar Motoru ajanıyım. Hangi modelle çalışmamı istersiniz?"
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
            db.save_chat_message("assistant", welcome_msg)

    # Sohbet geçmişini ekranda göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcıdan yeni girdi al
    if user_prompt := st.chat_input("Bir şeyler sorun (örn: 'Şu an saat kaç?')..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        db.save_chat_message("user", user_prompt)
        
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Ajan yanıtını üret (Seçilen model ve araçlar üzerinden)
        with st.chat_message("assistant"):
            with st.spinner(f"{selected_model_type} yanıt üretiyor..."):
                response = agent.run(user_prompt)
                
            st.markdown(response)
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        db.save_chat_message("assistant", response)
        db.save_decision(user_prompt, response)

elif mode == "Geçmiş Kararlar (Veritabanı)":
    st.subheader("📚 Kayıtlı Karar Geçmişi ve Loglar")
    
    limit = st.sidebar.slider("Gösterilecek Kayıt Sayısı", 1, 20, 5)
    recent_records = db.get_recent_decisions(limit=limit)
    
    if recent_records:
        for idx, (prompt, response, timestamp) in enumerate(recent_records, 1):
            with st.expander(f"Kayıt #{idx} — {timestamp}"):
                st.markdown(f"**Gönderilen Prompt:** `{prompt}`")
                st.markdown("**Üretilen Yanıt:**")
                st.text(response)
    else:
        st.info("Henüz veritabanında kayıtlı bir karar bulunmuyor.")