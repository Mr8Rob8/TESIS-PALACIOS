from __future__ import annotations

import re

from scanner.core.findings import Confianza, HallazgoRecon
from scanner.core.http_client import get_session, obtener

# Rutas de plugins/temas de WordPress se ven en el HTML como
# /wp-content/plugins/<slug>/ o /wp-content/themes/<slug>/ — deteccion pasiva,
# no se intenta acceder a rutas administrativas (escaneo no destructivo, 1.6).
WP_PLUGIN_RE = re.compile(r"/wp-content/plugins/([a-zA-Z0-9_-]+)/")
WP_THEME_RE = re.compile(r"/wp-content/themes/([a-zA-Z0-9_-]+)/")
JOOMLA_COMPONENT_RE = re.compile(r"/components/(com_[a-zA-Z0-9_-]+)/")
JOOMLA_TEMPLATE_RE = re.compile(r"/templates/([a-zA-Z0-9_-]+)/")


def perfilar_wordpress(html: str) -> dict:
    return {
        "plugins_visibles": sorted(set(WP_PLUGIN_RE.findall(html or ""))),
        "tema_visible": next(iter(sorted(set(WP_THEME_RE.findall(html or "")))), None),
    }


def perfilar_joomla(html: str) -> dict:
    return {
        "componentes_visibles": sorted(set(JOOMLA_COMPONENT_RE.findall(html or ""))),
        "plantillas_visibles": sorted(set(JOOMLA_TEMPLATE_RE.findall(html or ""))),
    }


def perfilar(hallazgo_recon: HallazgoRecon, html: str) -> HallazgoRecon:
    """Enriquece el hallazgo de recon con detalles especificos del CMS
    detectado (version mas precisa, plugins/temas visibles). No vuelve a
    tocar la red: opera sobre el HTML ya obtenido por el modulo recon."""
    detalles = dict(hallazgo_recon.detalles)

    if hallazgo_recon.tecnologia == "WordPress":
        detalles.update(perfilar_wordpress(html))
    elif hallazgo_recon.tecnologia == "Joomla":
        detalles.update(perfilar_joomla(html))
    elif hallazgo_recon.tecnologia == "Laravel":
        # Laravel no publica necesariamente versión ni paquetes en HTML.
        detalles["version_no_expuesta"] = hallazgo_recon.version is None

    return HallazgoRecon(
        tecnologia=hallazgo_recon.tecnologia,
        version=hallazgo_recon.version,
        confianza=hallazgo_recon.confianza,
        evidencia=hallazgo_recon.evidencia,
        metodo_deteccion=hallazgo_recon.metodo_deteccion,
        detalles=detalles,
    )


def run(target: str, hallazgo_recon: HallazgoRecon, timeout: int = 10) -> HallazgoRecon:
    """Vuelve a pedir la pagina objetivo para perfilar en detalle. Se separa
    del modulo recon para poder activarse/desactivarse independientemente
    (arquitectura de plugins, tesis.md 4.1)."""
    with get_session() as session:
        response = obtener(session, target, timeout=timeout)
    return perfilar(hallazgo_recon, response.text)
