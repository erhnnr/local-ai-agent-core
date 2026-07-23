# ADR 0002: Model-Agnostic Adaptör ve Esnek İstemci Yönetimi

## Durum (Status)
Kabul Edildi (Accepted)

## Bağlam (Context)
Proje geliştirme sürecinde, harici yapay zeka sağlayıcılarına (Hugging Face API, Google Colab) veya yerel donanıma (Ollama) yönelik ağ bağlantısı kısıtlamaları, DNS çözüpleme hataları ve donanım (GPU) sınırlarıyla karşılaşıldı. Bu durum, projenin test edilebilirliğini ve çevrimdışı geliştirme sürekliliğini olumsuz etkiledi.

## Karar (Decision)
Ağ veya donanım bağımlılıklarından bağımsız olarak sistemin kesintisiz çalışabilmesi ve test edilebilmesi için şu stratejiler benimsenmiştir:
1. Tüm LLM etkileşimleri `BaseLLMClient` soyut sınıfı arkasında soyutlanacaktır.
2. Ağ veya donanım sorunları yaşandığında mimari testlerin yapılabilmesi için bir `MockClient` (Sahte İstemci) geliştirilmiştir.
3. `main.py` ve ana akış, ortam değişkenlerine (`USE_MOCK` vb.) bağlı olarak dinamik istemci seçimi yapabilecek esnekliğe kavuşturulmuştur.

## Sonuçlar (Consequences)
* **Olumlu:** İnternet veya donanım kısıtlamalarından bağımsız olarak kod tabanı her an test edilebilir durumdadır. İleride farklı bir modele veya yerel motora geçiş, ana koda dokunulmadan sadece adaptör seviyesinde gerçekleştirilecektir.
* **Olumsuz:** Gerçek model çıktıları yerine test aşamasında simüle edilmiş yanıtlarla çalışılmaktadır.