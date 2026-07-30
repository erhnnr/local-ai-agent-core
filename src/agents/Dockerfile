# Resmi hafif Python imajını kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini belirle
WORKDIR /app

# Sistem bağımlılıklarını güncelleyip gerekli araçları kuralım
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılık dosyasını kurala uygun kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarının tamamını konteynere aktar
COPY . .

# FastAPI ve Streamlit portlarını dışarıya açıyoruz
EXPOSE 8000
EXPOSE 8501

# Konteyner ayağa kalktığında çalışacak varsayılan komut (Streamlit Arayüzü)
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]