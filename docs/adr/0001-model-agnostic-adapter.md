# 1. Model-Agnostic Mimari ve Adapter Pattern Kullanımı

* Durum: Kabul Edildi (Accepted)
* Tarih: 2026-07-22

## Bağlam (Context)
Yapay zeka modelleri ve yerel/bulut servis sağlayıcıları çok hızlı değişmektedir. Doğrudan belirli bir model API'sine veya kütüphanesine bağımlı kalmak, gelecekte model değiştiğinde kod tabanının baştan yazılmasına yol açacaktır.

## Karar
Sistemin çekirdek iş mantığının (Core) herhangi bir LLM sağlayıcısına bağımlı olmamasını sağlamak için **Adapter Pattern (Adaptör Deseni)** ve soyut bir arayüz (`BaseLLMClient`) kullanılacaktır. Dış dünya ile tüm iletişim somut adaptörler (örn: OllamaClient) üzerinden yürütülecektir.

## Sonuç
- Model değişiklikleri sadece `src/adapters/` altında yeni bir adaptör yazarak çözülecektir.
- Çekirdek (Core) kodlar ve iş mantığı bu değişimden etkilenmeyecektir.