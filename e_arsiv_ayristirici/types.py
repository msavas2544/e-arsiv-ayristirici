from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class InvoiceData:
    invoice_number: Optional[str] = None
    issue_date: Optional[str] = None
    total_amount: Optional[str] = None
    currency: Optional[str] = None
    seller: Optional[str] = None
    buyer: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)