import pytest
from e_arsiv_ayristirici.types import InvoiceData


def test_invoice_data_to_dict():
    data = InvoiceData(
        invoice_number="123",
        issue_date="2025-08-16",
        total_amount="1000",
        currency="TRY",
        seller="Satıcı",
        buyer="Alıcı",
        raw={"extra": "info"}
    )
    result = data.to_dict()
    assert result["invoice_number"] == "123"
    assert result["issue_date"] == "2025-08-16"
    assert result["total_amount"] == "1000"
    assert result["currency"] == "TRY"
    assert result["seller"] == "Satıcı"
    assert result["buyer"] == "Alıcı"
    assert result["raw"] == {"extra": "info"}
