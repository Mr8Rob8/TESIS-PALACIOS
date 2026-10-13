"""Prueba de extremo a extremo sobre servidor efímero exclusivamente local."""

from __future__ import annotations

import html
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

import pytest

from scanner.scan import ejecutar
from scanner.cli import main
import json


class SitioControlado(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        parsed = urlsplit(self.path)
        value = parse_qs(parsed.query, keep_blank_values=True).get("q", [""])[0]
        vulnerable = parsed.path == "/vulnerable"
        is_plain = parsed.path == "/plain"
        if is_plain:
            body = value
        elif vulnerable and "'" in value:
            body = "You have an error in your SQL syntax"
        else:
            displayed = value if vulnerable else html.escape(value, quote=True)
            body = f'<html><head><meta name="generator" content="WordPress 6.4"></head><body>{displayed}</body></html>'
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ("text/plain" if is_plain else "text/html") + "; charset=utf-8")
        if not vulnerable:
            self.send_header("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'")
            self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


@pytest.fixture
def sitio_local():
    server = ThreadingHTTPServer(("127.0.0.1", 0), SitioControlado)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_escaneo_completo_detecta_casos_positivos_conocidos(sitio_local):
    resultado = ejecutar(sitio_local + "/vulnerable?q=hola")
    assert resultado.reconocimiento is not None
    assert resultado.reconocimiento.tecnologia == "WordPress"
    assert {h.modulo for h in resultado.hallazgos} >= {"xss", "sqli", "headers"}
    assert resultado.peticiones >= 5


def test_escaneo_completo_no_alerta_sobre_casos_negativos_conocidos(sitio_local):
    resultado = ejecutar(sitio_local + "/seguro?q=hola")
    assert resultado.reconocimiento is not None
    assert resultado.hallazgos == []


def test_modulos_seleccionables_y_sin_parametros_no_hacen_sondeo(sitio_local):
    resultado = ejecutar(sitio_local + "/seguro", ["recon", "xss", "sqli"])
    assert resultado.peticiones == 1
    assert resultado.hallazgos == []


def test_cli_generar_reporte_json_local(sitio_local, tmp_path):
    reporte = tmp_path / "reporte.json"
    code = main([sitio_local + "/vulnerable?q=hola", "--format", "json", "--output", str(reporte)])
    assert code == 0
    data = json.loads(reporte.read_text(encoding="utf-8"))
    assert data["reconocimiento"]["tecnologia"] == "WordPress"
    assert {h["modulo"] for h in data["hallazgos"]} >= {"xss", "sqli", "headers"}


def test_no_clasifica_reflejo_texto_plano_como_xss_html(sitio_local):
    resultado = ejecutar(sitio_local + "/plain?q=hola", ["xss"])
    assert all(h.codigo != "XSS-REFLEJO-INDICATIVO" for h in resultado.hallazgos)
    assert resultado.peticiones == 1
