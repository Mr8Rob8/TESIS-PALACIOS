from __future__ import annotations

from scanner.core.findings import Confianza, HallazgoRecon
from scanner.core.http_client import get_session
from scanner.modules.recon.signatures import detect_joomla, detect_laravel, detect_wordpress

_DETECTORS = (
    ("WordPress", detect_wordpress),
    ("Joomla", detect_joomla),
    ("Laravel", detect_laravel),
)


def analizar_respuesta(headers: dict, cookies: dict, html: str) -> HallazgoRecon | None:
    """Aplica los detectores pasivos de tecnologia sobre una respuesta HTTP ya
    obtenida. Separado de run() para poder testear con fixtures sin red real.
    """
    for tecnologia, detector in _DETECTORS:
        detectado, version, metodo = detector(headers, cookies, html)
        if detectado:
            return HallazgoRecon(
                tecnologia=tecnologia,
                version=version,
                confianza=Confianza.CONFIRMADO,
                evidencia=metodo,
                metodo_deteccion=metodo,
            )
    return None


def run(target: str, timeout: int = 10) -> HallazgoRecon | None:
    """Ejecuta el modulo de reconocimiento contra una URL real (escaneo no
    destructivo: una unica peticion GET, sin payloads)."""
    session = get_session()
    response = session.get(target, timeout=timeout)
    cookies = {c.name: c.value for c in response.cookies}
    return analizar_respuesta(dict(response.headers), cookies, response.text)
