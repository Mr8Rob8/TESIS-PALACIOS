import argparse
import sys
from pathlib import Path

import requests

from scanner import __version__
from scanner.reporting.render import como_json, como_texto
from scanner.scan import ejecutar


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scanner",
        description="Escaner ligero OWASP para PYMEs peruanas (WordPress, Joomla, Laravel).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("target", nargs="?", help="URL objetivo a escanear")
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=["recon", "cms", "xss", "sqli", "headers"],
        default=["recon", "cms", "xss", "sqli", "headers"],
        help="Modulos a ejecutar (por defecto: todos)",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Formato del reporte")
    parser.add_argument("--output", type=Path, help="Guardar reporte en un archivo")
    parser.add_argument("--timeout", type=int, default=10, help="Tiempo máximo por petición en segundos")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.target:
        parser.print_help()
        return 1

    if args.timeout <= 0:
        parser.error("--timeout debe ser positivo")
    try:
        resultado = ejecutar(args.target, args.modules, args.timeout)
    except (ValueError, requests.RequestException) as exc:
        print(f"Error de escaneo: {exc}", file=sys.stderr)
        return 2
    reporte = como_json(resultado) if args.format == "json" else como_texto(resultado)
    if args.output:
        args.output.write_text(reporte + "\n", encoding="utf-8")
    else:
        print(reporte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
