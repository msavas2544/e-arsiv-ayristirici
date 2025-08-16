import pytest
from pathlib import Path
from e_arsiv_ayristirici.parser import parse_invoice


def test_parse_invoice_txt():
    """Test parsing a simple text invoice"""
    # Geçici test dosyası oluştur
    test_content = """Fatura No: TEST-123
Tarih: 01.01.2025
Satıcı: Test Şirket
Alıcı: Test Müşteri
Tutar: 500.00 TL"""
    
    test_file = Path("test_invoice.txt")
    test_file.write_text(test_content, encoding='utf-8')
    
    try:
        result = parse_invoice(test_file)
        
        assert result.invoice_number == "TEST-123"
        assert result.issue_date == "01.01.2025"
        assert result.seller == "Test Şirket"
        assert result.buyer == "Test Müşteri" 
        assert result.total_amount == "500.00"
        assert result.currency == "TL"
        assert result.raw is not None
        
    finally:
        # Test dosyasını temizle
        if test_file.exists():
            test_file.unlink()


def test_parse_invoice_file_not_found():
    """Test handling of non-existent file"""
    with pytest.raises(FileNotFoundError):
        parse_invoice(Path("non_existent_file.txt"))


def test_parse_invoice_empty_content():
    """Test parsing empty file"""
    test_file = Path("empty_test.txt")
    test_file.write_text("", encoding='utf-8')
    
    try:
        result = parse_invoice(test_file)
        
        # Boş dosya için tüm alanlar None olmalı
        assert result.invoice_number is None
        assert result.issue_date is None
        assert result.seller is None
        assert result.buyer is None
        assert result.total_amount is None
        assert result.currency is None
        assert result.raw is not None  # Raw data her zaman olmalı
        
    finally:
        if test_file.exists():
            test_file.unlink()
