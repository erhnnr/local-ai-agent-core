ADR 0003: Otonom Ajan Çekirdeği, Araç Entegrasyonu ve Bellek Yönetimi
Durum (Status)
Kabul Edildi (Accepted)

Bağlam (Context)
Model-agnostik adaptör altyapısı kurulduktan sonra, projenin sadece metin üreten statik bir model olmaktan çıkarılıp; dış dünya ile etkileşime girebilen, dokümanlar üzerinde anlamsal arama yapabilen, kendi donanım durumunu okuyabilen ve sohbet bağlamını koruyabilen akıllı bir Otonom Ajan (Autonomous Agent) seviyesine taşınması gerekiyordu.

Karar (Decision)
Sistemin yetenek setini genişletmek ve kararlılığını artırmak amacıyla aşağıdaki mimari kararlar alınmıştır:

Semantik RAG Entegrasyonu: Proje dokümanlarında kelime bazlı arama yerine anlam bütünlüğünü yakalayan vektör tabanlı bilgi tabanı (VectorKnowledgeBase) devreye sokuldu.

Merkezi Araç Kayıt Defteri (Tool Registry): Ajanın sistem donanımını (RAM, CPU, İşletim Sistemi), anlık zaman bilgisini ve yerel dosyaları güvenli bir şekilde okuyabilmesi için modüler bir araç mimarisi (ToolRegistry) kuruldu.

Esnek Niyet Yönetimi (Intent Router): Kullanıcı girdilerini analiz ederek doğru aracı, bilgi tabanını veya genel LLM akışını dinamik olarak tetikleyen kural tabanlı bir yönlendirici eklendi.

Kalıcı Sohbet Hafızası (Memory): Oturum boyunca kullanıcı bağlamının kaybolmaması adına chat_history mekanizması entegre edildi.

Merkezi Hata Koruması (Robustness): Beklenmeyen dosya okuma veya sistem sorgusu hatalarında uygulamanın çökmesini önlemek için try-except güvenli yanıt sarmalayıcısı uygulandı.

Sonuçlar (Consequences)
Olumlu: Ajan, harici verilere ve yerel donanıma bağımsız olarak erişebilen, bağlamı unutmayan ve hatalar karşısında çökmeden güvenli çalışan kararlı bir yapıya kavuştu.

Olumsuz: Bileşen sayısı arttıkça (RAG, araçlar, niyet yönlendiricisi) kod tabanındaki modüler bağımlılıkların yönetimi ve hata ayıklama (debugging) süreci dikkatli bir loglama altyapısını zorunlu kıldı (bu durum logger modülü ile çözüldü).