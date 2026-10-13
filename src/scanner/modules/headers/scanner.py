"""Comprobaciones de presencia de cabeceras, no pruebas de explotación."""

from __future__ import annotations

from scanner.core.findings import HallazgoSeguridad
from scanner.core.http_client import RespuestaHTTP


def analizar(objetivo: str, respuesta: RespuestaHTTP) -> list[HallazgoSeguridad]:
    headers = {k.lower(): v for k, v in respuesta.headers.items()}
    content_type = headers.get("content-type", "").lower()
    hallazgos = []

    def falta(codigo: str, titulo: str, recomendacion: str) -> None:
        hallazgos.append(HallazgoSeguridad(
            codigo=codigo, modulo="headers", severidad="baja", titulo=titulo,
            evidencia=f"Cabecera ausente en respuesta HTTP {respuesta.status_code} de {objetivo}",
            recomendacion=recomendacion, url=objetivo, confianza="observada",
        ))

    if "text/html" in content_type:
        if "content-security-policy" not in headers:
            falta("HEADER-CSP", "No se observó Content-Security-Policy", "Definir una CSP compatible con los recursos del sitio y probarla antes de aplicarla.")
        csp = headers.get("content-security-policy", "").lower()
        if "x-frame-options" not in headers and "frame-ancestors" not in csp:
            falta("HEADER-FRAME", "No se observó protección contra embebido", "Definir frame-ancestors en CSP o X-Frame-Options según compatibilidad requerida.")
    if headers.get("x-content-type-options", "").lower() != "nosniff":
        falta("HEADER-NOSNIFF", "No se observó X-Content-Type-Options: nosniff", "Enviar X-Content-Type-Options: nosniff.")
    if objetivo.lower().startswith("https://") and "strict-transport-security" not in headers:
        falta("HEADER-HSTS", "No se observó Strict-Transport-Security", "Evaluar HSTS solo cuando todo el sitio y sus subdominios sean compatibles con HTTPS.")
    return hallazgos
