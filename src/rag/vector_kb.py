import glob
import os

import chromadb
from sentence_transformers import SentenceTransformer


class VectorKnowledgeBase:
    """
    ChromaDB ve SentenceTransformers kullanarak dokümanları vektör uzayında 
    indeksleyen ve semantik (anlamsal) arama yapan sınıf.
    """
    def __init__(self, docs_dir: str = "docs", collection_name: str = "project_docs"):
        self.docs_dir = docs_dir
        # Hafif ve hızlı bir embedding modeli
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # ChromaDB yerel istemcisi
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        
        # Başlangıçta dokümanları indekse yükle
        self._index_documents()

    def _index_documents(self):
        """Docs dizinindeki dokümanları okur, parçalara ayırır ve vektör veritabanına kaydeder."""
        if not os.path.exists(self.docs_dir):
            return

        documents = []
        metadatas = []
        ids = []
        
        doc_id_counter = 0
        for filepath in glob.glob(os.path.join(self.docs_dir, "**/*.*"), recursive=True):
            if filepath.endswith((".md", ".txt")):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Paragraf bazlı basit bölme (chunking)
                        chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 20]
                        for i, chunk in enumerate(chunks):
                            documents.append(chunk)
                            metadatas.append({"source": filepath})
                            ids.append(f"doc_{doc_id_counter}")
                            doc_id_counter += 1
                except Exception:
                    continue

        if documents:
            # Vektörleri hesapla
            embeddings = self.encoder.encode(documents).tolist()
            # Mevcut kayıtları ezmeden ekleme (veya sıfırdan yükleme)
            try:
                self.collection.add(
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    ids=ids
                )
            except Exception:
                pass # Zaten eklenmiş id çakışmalarını yut

    def search(self, query: str, n_results: int = 3) -> str:
        """Kullanıcı sorgusuna en yakın doküman parçalarını semantik olarak arar."""
        if self.collection.count() == 0:
            return "Bilgi tabanında indekslenmiş doküman bulunamadı."

        query_embedding = self.encoder.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(n_results, self.collection.count())
        )

        formatted_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            for doc, meta in zip(docs, metas):
                formatted_results.append(f"--- Kaynak: {meta.get('source')} ---\n{doc}\n")

        return "\n".join(formatted_results) if formatted_results else "Anlamsal eşleşme bulunamadı."