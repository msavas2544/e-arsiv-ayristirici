# E‑Arşiv / E‑Fatura Ayrıştırıcı (MVP)

Türk e‑Arşiv/e‑Fatura PDF ve HTML dosyalarından temel alanları ayrıştırıp SQLite veritabanına kaydeden basit bir FastAPI servisi.

## Özellikler (MVP)
- PDF ve HTML içe aktarma (tek dosya)
- Alanlar: Fatura No, Tarih, Satıcı, Para Birimi (TRY), Genel Toplam
- SQLite kalıcılık, listeleme endpoint'i
- CI: pytest çalıştırma

> Not: Ayrıştırıcı basit regex kurallarıyla çalışır; sağlayıcıya göre şablonlar farklı olabilir. Zamanla sağlayıcı‑özel kural setleri ve tablo satırları (kalemler) eklenecek.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Arayüz: http://127.0.0.1:8000/docs

## API

- GET `/health` — sağlık kontrolü
- POST `/import/file` — tek PDF/HTML yükle
- GET `/invoices` — kayıtlı faturaları listele

## Docker

```bash
docker build -t e-arsiv-ayristirici .
docker run -p 8000:8000 -v $(pwd)/data.db:/app/data.db e-arsiv-ayristirici
```

## Yol Haritası
- [ ] Sağlayıcı‑özel şablonlar (GİB, özel entegratörler)
- [ ] Kalem (items) çıkarımı ve KDV hesabı
- [ ] Toplu içe aktarma ve IMAP okuma
- [ ] CSV/Excel dışa aktarma
- [ ] Basit web UI (Svelte/React)
- [ ] Test kapsamı ve örnek veri seti

## Lisans
MIT