import glob
import os


class KnowledgeBase:
    """
    Proje içerisindeki markdown, metin ve dokümanları tarayarak 
    RAG (Retrieval-Augmented Generation) tabanlı arama ve bağlam sunan sınıf.
    """
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = docs_dir

    def search_documents(self, query: str) -> str:
        """
        Kullanıcı sorgusuyla eşleşen doküman içeriklerini arar ve bulduğu 
        ilgili metin parçalarını bağlam olarak döndürür.
        """
        if not os.path.exists(self.docs_dir):
            return "Bilgi tabanı dizini (docs/) bulunamadı."

        search_results = []
        # docs altındaki tüm md ve txt dosyalarını tara
        for filepath in glob.glob(os.path.join(self.docs_dir, "**/*.*"), recursive=True):
            if filepath.endswith((".md", ".txt")):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Basit anahtar kelime eşleşmesi (Gelişmiş aşamada vektör veritabanı eklenebilir)
                        if any(keyword.lower() in content.lower() for keyword in query.split()):
                            search_results.append(f"--- Kaynak Doküman: {filepath} ---\n{content[:1500]}\n")
                except Exception:
                    continue

        if search_results:
            return "\n".join(search_results[:3]) # En ilgili 3 sonucu döndür
        else:
            return "Bilgi tabanında bu sorguyla doğrudan eşleşen bir doküman bulunamadı."