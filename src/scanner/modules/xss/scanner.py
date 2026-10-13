"""Prueba indicativa de XSS reflejado en parámetros GET existentes."""

from __future__ import annotations

import secrets
from collections.abc import Callable

from scanner.core.findings import HallazgoSeguridad
from scanner.core.http_client import RespuestaHTTP
from scanner.core.targets import parametros_get, sustituir_parametro


def analizar_reflejo(base: str, primera: str, segunda: str, payload1: str, payload2: str) -> bool:
    """Dos reflejos HTML sin codificar y ausentes de la respuesta base."""
    return payload1 not in base and payload2 not in base and payload1 in primera and payload2 in segunda


def escanear(objetivo: str, base: RespuestaHTTP, get: Callable[[str], RespuestaHTTP]) -> list[HallazgoSeguridad]:
    content_type = next((value.lower() for name, value in base.headers.items() if name.lower() == "content-type"), "")
    if not any(mime in content_type for mime in ("text/html", "application/xhtml+xml")):
        return []
    hallazgos = []
    for parametro in parametros_get(objetivo):
        token = secrets.token_hex(4)
        p1 = f'<svg data-scanner="{token}a" onload="void(0)">'
        p2 = f'<svg data-scanner="{token}b" onload="void(0)">'
        url1 = sustituir_parametro(objetivo, parametro, p1)
        url2 = sustituir_parametro(objetivo, parametro, p2)
        r1 = get(url1)
        if p1 not in r1.text:
            continue
        r2 = get(url2)
        if analizar_reflejo(base.text, r1.text, r2.text, p1, p2):
            hallazgos.append(HallazgoSeguridad(
                codigo="XSS-REFLEJO-INDICATIVO", modulo="xss", severidad="media",
                titulo="Posible XSS reflejado en parámetro GET",
                evidencia=f"{parametro}: dos marcadores HTML distintos se reflejaron sin codificar; no se ejecutó JavaScript en un navegador",
                recomendacion="Codificar la salida según su contexto HTML y revisar la política CSP; confirmar manualmente en un navegador controlado.",
                url=objetivo, parametro=parametro,
            ))
    return hallazgos
