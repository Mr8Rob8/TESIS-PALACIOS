"""Prueba indicativa de SQLi por errores diferenciales, solo con GET."""

from __future__ import annotations

import re
from collections.abc import Callable
from urllib.parse import parse_qsl, urlsplit

from scanner.core.findings import HallazgoSeguridad
from scanner.core.http_client import RespuestaHTTP
from scanner.core.targets import parametros_get, sustituir_parametro

_ERRORES = (
    re.compile(r"you have an error in your sql syntax", re.I),
    re.compile(r"SQLSTATE\[(?:42000|HY000|42601)\]", re.I),
    re.compile(r"sqlite3?\.(?:OperationalError|ProgrammingError)", re.I),
    re.compile(r"unclosed quotation mark after the character string", re.I),
    re.compile(r"PG::SyntaxError|ORA-009(?:17|33|36)", re.I),
)


def errores_sql(texto: str) -> set[int]:
    return {i for i, patron in enumerate(_ERRORES) if patron.search(texto)}


def analizar_error(base: str, primera: str, segunda: str) -> bool:
    """La misma familia de error aparece dos veces y estaba ausente en base."""
    inicial = errores_sql(base)
    return bool((errores_sql(primera) & errores_sql(segunda)) - inicial)


def escanear(objetivo: str, base: RespuestaHTTP, get: Callable[[str], RespuestaHTTP]) -> list[HallazgoSeguridad]:
    values = {}
    for name, value in parse_qsl(urlsplit(objetivo).query, keep_blank_values=True):
        values.setdefault(name, value)
    hallazgos = []
    for parametro in parametros_get(objetivo):
        original = values[parametro]
        # Las comillas no contienen sentencias SQL ni modifican datos.
        r1 = get(sustituir_parametro(objetivo, parametro, original + "'"))
        if not (errores_sql(r1.text) - errores_sql(base.text)):
            continue
        r2 = get(sustituir_parametro(objetivo, parametro, original + "'scan"))
        if analizar_error(base.text, r1.text, r2.text):
            hallazgos.append(HallazgoSeguridad(
                codigo="SQLI-ERROR-INDICATIVO", modulo="sqli", severidad="media",
                titulo="Posible inyección SQL basada en errores",
                evidencia=f"{parametro}: dos variantes de comillas generaron la misma familia de error SQL, ausente en la respuesta base",
                recomendacion="Revisar consultas parametrizadas y manejo de errores; confirmar con revisión de código o entorno de prueba controlado.",
                url=objetivo, parametro=parametro,
            ))
    return hallazgos
