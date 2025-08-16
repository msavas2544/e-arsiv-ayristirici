import re
from pathlib import Path
from .types import InvoiceData

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


def parse_invoice(file_path: Path) -> InvoiceData:
    """
    Dosyadan fatura bilgilerini ayrıştırır.
    HTML, XML ve metin dosyalarını destekler.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
    
    # Dosya içeriğini oku
    content = file_path.read_text(encoding='utf-8')
    
    # HTML/XML dosyaları için BeautifulSoup kullan
    if file_path.suffix.lower() in ['.html', '.htm', '.xml'] and HAS_BS4:
        return _parse_html_content(content, file_path)
    else:
        return _parse_text_content(content, file_path)


def _parse_html_content(content: str, file_path: Path) -> InvoiceData:
    """HTML/XML içeriğini BeautifulSoup ile ayrıştır"""
    from bs4 import BeautifulSoup
    
    # XML dosyaları için XML parser kullan
    if file_path.suffix.lower() == '.xml':
        soup = BeautifulSoup(content, 'xml')
    else:
        soup = BeautifulSoup(content, 'html.parser')
    
    text_content = soup.get_text()
    
    # HTML/XML'den metin çıkarıp regex ile ara
    return _parse_text_content(text_content, file_path)


def _parse_text_content(content: str, file_path: Path) -> InvoiceData:
    """
    Metin içeriğini regex ile ayrıştırır.
    """
    # Temel regex desenlerle bilgileri çıkar
    invoice_data = InvoiceData()
    
    # Fatura numarası
    invoice_number_patterns = [
        r'Fatura\s+No[:\s]+([A-Z0-9\-]+)',
        r'Invoice\s+Number[:\s]+([A-Z0-9\-]+)',
        r'Belge\s+No[:\s]+([A-Z0-9\-]+)',
        r'([A-Z]+-\d{4}-\d+)',  # XML-2025-789 formatını yakala
    ]
    
    for pattern in invoice_number_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            invoice_data.invoice_number = match.group(1).strip()
            break
    
    # Tarih
    date_patterns = [
        r'Tarih[:\s]+(\d{2}[./-]\d{2}[./-]\d{4})',
        r'Date[:\s]+(\d{2}[./-]\d{2}[./-]\d{4})',
        r'(\d{4}-\d{2}-\d{2})',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            invoice_data.issue_date = match.group(1).strip()
            break
    
    # Toplam tutar - birden fazla basamak ve ondalık destekli
    amount_patterns = [
        r'Toplam[:\s]+([0-9.,]+)\s*(TL|₺|TRY|USD|EUR)',
        r'Total[:\s]+([0-9.,]+)\s*(TL|₺|TRY|USD|EUR)',
        r'Tutar[:\s]+([0-9.,]+)\s*(TL|₺|TRY|USD|EUR)',
        r'([0-9.,]+)\s+(TRY|TL|USD|EUR)(?!\w)',  # Sadece rakam ve para birimi
        r'([0-9]{1,3}(?:[,.][0-9]{3})*(?:[,.][0-9]{2})?)(?=\s*$)',  # 3,999.99 formatı satır sonunda
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            invoice_data.total_amount = match.group(1).strip()
            if len(match.groups()) > 1 and match.group(2):
                invoice_data.currency = match.group(2).strip()
            else:
                # Para birimini ayrı ara - ham XML içeriğinden
                original_content = file_path.read_text(encoding='utf-8')
                currency_match = re.search(r'currency="(\w+)"', original_content, re.IGNORECASE)
                if currency_match:
                    invoice_data.currency = currency_match.group(1).strip()
            break
    
    # Satıcı
    seller_patterns = [
        r'Satıcı[:\s]+(.+?)(?:\n|$)',
        r'Seller[:\s]+(.+?)(?:\n|$)', 
        r'Şirket[:\s]+(.+?)(?:\n|$)',
        r'([A-ZÇĞıİÖŞÜ][a-zçğıişöü\s]+A\.Ş\.)',  # "... A.Ş." formatını yakala
        r'([A-ZÇĞıİÖŞÜ][a-zçğıişöü\s]+Ltd\.)',  # "... Ltd." formatını yakala
    ]
    
    for pattern in seller_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            invoice_data.seller = match.group(1).strip()
            break
    
    # Alıcı
    buyer_patterns = [
        r'Alıcı[:\s]+(.+?)(?:\n|$)',
        r'Buyer[:\s]+(.+?)(?:\n|$)',
        r'Müşteri[:\s]+(.+?)(?:\n|$)',
        r'([A-ZÇĞıİÖŞÜ][a-zçğıişöü\s]+Ltd\.)',  # "... Ltd." formatını yakala
        r'([A-ZÇĞıİÖŞÜ][a-zçğıişöü\s]+A\.Ş\.)',  # "... A.Ş." formatını yakala
    ]
    
    for pattern in buyer_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            invoice_data.buyer = match.group(1).strip()
            break
    
    # Ham veriyi de sakla
    invoice_data.raw = {"content": content, "file_path": str(file_path)}
    
    return invoice_data
