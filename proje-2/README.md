# 🍳 Proje 2: AI Destekli Yemek Tarifi & Akıllı Alışveriş Listesi Asistanı

Bu proje; kullanıcının evdeki mevcut malzemelerini, diyet kısıtlamalarını ve zaman tercihlerini analiz ederek **kişiselleştirilmiş yemek tarifleri**, **besin değeri tahminleri** ve **otomatik alışveriş listesi** üreten FastAPI tabanlı bir yapay zekâ servisidir.

## 🚀 Özellikler
- **Pantry-to-Plate:** Eldeki malzemeler önceliklendirilerek tarif üretilir.
- **Strict JSON Şema:** Pydantic v2 ve Gemini Structured Output ile tip güvenli çıktı.
- **Akıllı Alışveriş Listesi:** Tarif için evde eksik olan malzemeler otomatik tespit edilir ve kategorize edilir.
- **Kiler Eşleşme Oranı (%):** Eldeki malzemelerin tarifi karşılama yüzdesi hesaplanır.
- **Docker Desteği:** Tek komutla ayağa kalkar.

## 🛠️ Kurulum & Çalıştırma (Docker ile)

1. Klasöre girin:
```bash
cd proje-2