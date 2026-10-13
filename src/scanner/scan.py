"""Orquestación secuencial de un escaneo GET no destructivo."""

from __future__ import annotations

import time

from scanner.core.findings import ResultadoEscaneo
from scanner.core.http_client import DEFAULT_TIMEOUT, RespuestaHTTP, get_session, obtener
from scanner.core.metrics import pico_memoria_bytes
from scanner.core.targets import validar_objetivo
from scanner.modules.cms.profiler import perfilar
from scanner.modules.headers.scanner import analizar as analizar_headers
from scanner.modules.recon.scanner import analizar_respuesta
from scanner.modules.sqli.scanner import escanear as escanear_sqli
from scanner.modules.xss.scanner import escanear as escanear_xss

MODULOS = ("recon", "cms", "xss", "sqli", "headers")


def ejecutar(objetivo: str, modulos: list[str] | None = None, timeout: int = DEFAULT_TIMEOUT) -> ResultadoEscaneo:
    validar_objetivo(objetivo)
    seleccionados = list(dict.fromkeys(modulos or MODULOS))
    if any(m not in MODULOS for m in seleccionados):
        raise ValueError("Módulo desconocido")
    inicio = time.perf_counter()
    peticiones = 0
    with get_session() as session:
        def get(url: str) -> RespuestaHTTP:
            nonlocal peticiones
            peticiones += 1
            return obtener(session, url, timeout=timeout)

        base = get(objetivo)
        if 300 <= base.status_code < 400:
            raise ValueError("El objetivo redirige; indique explícitamente la URL final autorizada")
        recon = None
        if "recon" in seleccionados or "cms" in seleccionados:
            recon = analizar_respuesta(base.headers, base.cookies, base.text)
            if recon is not None and "cms" in seleccionados:
                recon = perfilar(recon, base.text)
        hallazgos = []
        if "headers" in seleccionados:
            hallazgos.extend(analizar_headers(objetivo, base))
        if "xss" in seleccionados:
            hallazgos.extend(escanear_xss(objetivo, base, get))
        if "sqli" in seleccionados:
            hallazgos.extend(escanear_sqli(objetivo, base, get))
    return ResultadoEscaneo(
        objetivo=objetivo, codigo_http=base.status_code,
        reconocimiento=recon, hallazgos=hallazgos,
        duracion_segundos=time.perf_counter() - inicio,
        peticiones=peticiones, modulos=seleccionados,
        pico_memoria_bytes=pico_memoria_bytes(),
    )
