import argparse
import json
from pathlib import Path

from .parser import parse_invoice

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="e-arsiv-ayristirici",
        description="e-Arşiv benzeri dosyalardan temel bilgileri ayrıştırır.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_parse = sub.add_parser("parse", help="Bir dosyayı ayrıştır")
    p_parse.add_argument("path", type=str, help="Girdi dosyası yolu (txt/html/xml)")
    p_parse.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Çıktı formatı",
    )

    args = parser.parse_args()

    if args.command == "parse":
        data = parse_invoice(Path(args.path))
        if args.format == "json":
            print(json.dumps(data.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(
                "\n".join(
                    [
                        f"Fatura No: {data.invoice_number or ''}",
                        f"Tarih: {data.issue_date or ''}",
                        f"Tutar: {data.total_amount or ''} {data.currency or ''}",
                        f"Satıcı: {data.seller or ''}",
                        f"Alıcı: {data.buyer or ''}",
                    ]
                )
            )


if __name__ == "__main__":
    main()