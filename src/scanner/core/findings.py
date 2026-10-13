from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Confianza(str, Enum):
    """Resultado de la validacion en dos fases (ver tesis.md 4.1/4.3)."""

    CONFIRMADO = "confirmado"
    NO_CONFIRMADO = "no_confirmado"


@dataclass
class HallazgoRecon:
    """Salida del modulo recon/cms: tecnologia detectada y version, con su
    nivel de confianza. Alimenta el resto del pipeline (ver tesis.md 4.3, 5.1.2).
    """

    tecnologia: str
    version: str | None
    confianza: Confianza
    evidencia: str
    metodo_deteccion: str
    detalles: dict = field(default_factory=dict)


@dataclass(frozen=True)
class HallazgoSeguridad:
    """Observación reproducible; una señal no equivale a explotación probada."""

    codigo: str
    modulo: str
    severidad: str
    titulo: str
    evidencia: str
    recomendacion: str
    url: str
    parametro: str | None = None
    confianza: str = "indicativa"


@dataclass
class ResultadoEscaneo:
    objetivo: str
    codigo_http: int
    reconocimiento: HallazgoRecon | None
    hallazgos: list[HallazgoSeguridad]
    duracion_segundos: float
    peticiones: int
    modulos: list[str]
    pico_memoria_bytes: int | None = None
