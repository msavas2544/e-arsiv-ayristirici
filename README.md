# e-arsiv-ayristirici

Basit bir Python kütüphanesi ve CLI aracı. Amaç: e-Arşiv benzeri dosyalardan (ilk aşamada düz metin/HTML/XML) temel bilgileri ayrıştırmak için bir iskelet sunmak.

Durum: Bu, başlangıç iskeletidir. PDF ayrıştırma henüz eklenmedi.

## Kurulum
- Python 3.10+
- (İsteğe bağlı) Sanal ortam kullanın

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Kullanım
```bash
# JSON çıktı ile
python -m e_arsiv_ayristirici.cli parse ./ornek.txt --format json

# Düz metin çıktısı ile
python -m e_arsiv_ayristirici.cli parse ./ornek.html --format text
```

## Geliştirme
- PDF desteği eklemek için `parser.py` içindeki `parse_invoice` fonksiyonunu genişletin.
- İhtiyaç halinde `requirements.txt` içine bağımlılıkları ekleyin (ör. pdfminer.six, PyMuPDF, beautifulsoup4, lxml).

---
Lisans: MIT (bkz. LICENSE)