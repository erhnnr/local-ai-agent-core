import sys
import os

# Proje kök dizinini Python yoluna ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import streamlit as st
import psutil
import platform
from datetime import datetime
from src.agents.agent_core import DecisionAgent
from src.llm.local_client import LocalLLMClient
import streamlit as st
import psutil
import platform
from datetime import datetime
from src.agents.agent_core import DecisionAgent
from src.llm.local_client import LocalLLMClient

# --- 1. SAYFA YAPILANDIRMASI VE ÖZEL CSS ---
st.set_page_config(
    page_title="Local AI Agent Core - Control Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern ve koyu ağırlıklı kurumsal tema için özel CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. BAŞLANGIÇ VE STATE YÖNETİMİ ---
@st.cache_resource
def init_agent():
    llm_client = LocalLLMClient()
    return DecisionAgent(llm_client)

agent = init_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL (SIDEBAR) - KONTROL MERKEZİ ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=70)
    st.title("AI Command Center")
    st.caption("v2.0-core | Yerel Otonom Ekosistem")
    
    st.divider()
    
    # Ajan Modu / Rol Seçimi
    st.subheader("🎯 Ajan Yapılandırması")
    selected_mode = st.selectbox(
        "Çalışma Modu (Router)",
        ["Auto-Router (Akıllı Niyet)", "CoderAgent (Yazılım Uzmanı)", "ArchitectAgent (Sistem Mimarı)"]
    )
    
    st.divider()
    
    # Canlı Sistem Kaynak Monitörü
    st.subheader("💻 Donanım Monitörü")
    mem = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=None)
    
    st.markdown(f"""
        <div class="metric-card">
            <b>CPU Kullanımı:</b> %{cpu_percent}<br>
            <b>RAM Kullanımı:</b> %{mem.percent} ({round(mem.used / (1024**3), 1)} GB / {round(mem.total / (1024**3), 1)} GB)
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Sohbeti Temizle Butonu
    if st.button("🗑️ Sohbet Geçmişini Temizle", use_container_width=True):
        st.session_state.messages = []
        agent.chat_history = []
        st.rerun()

# --- 4. ANA EKRAN - SOHBET ARAYÜZÜ ---
st.title("💬 Local AI Agent Ekosistemi")
st.markdown("Bilgisayarınızda tamamen yerel ve güvenli çalışan otonom yapay zeka asistanı.")

# Geçmiş mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi alma
if prompt := st.chat_input("Komutunuzu veya sorunuzu yazın (Örn: 'app.py dosyasını oku' veya 'Antalya hava durumu')..."):
    # Kullanıcı mesajını ekle ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ajan yanıtı
    with st.chat_message("assistant"):
        with st.spinner("Ajan düşünüyor ve araçları çalıştırıyor..."):
            # Eğer sidebar'dan manuel mod seçildiyse ona göre yönlendirilebilir, 
            # şu an ana DecisionAgent (Master Router) tam otonom devrede.
            response = agent.run(prompt)
            st.markdown(response)
            
    # Asistan yanıtını geçmişe kaydet
    st.session_state.messages.append({"role": "assistant", "content": response})