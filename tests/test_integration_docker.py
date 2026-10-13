"""Pruebas de integracion contra los 3 entornos Docker definidos en docker/.

Requieren tener los contenedores levantados de antemano:
    cd docker/wordpress && docker compose up -d
    cd docker/joomla    && docker compose up -d
    cd docker/laravel   && docker compose up -d --build

Se saltan automaticamente (skip) si el sitio no responde en el puerto
esperado, para no romper la suite en maquinas sin Docker corriendo.
"""

import time

import pytest
import requests

from scanner.modules.cms.profiler import run as run_cms
from scanner.modules.recon.scanner import run as run_recon

OBJETIVOS = {
    "WordPress": "http://localhost:8081",
    "Joomla": "http://localhost:8082",
    "Laravel": "http://localhost:8083",
}


def _sitio_disponible(url: str) -> bool:
    try:
        requests.get(url, timeout=3)
        return True
    except requests.exceptions.RequestException:
        return False


@pytest.mark.parametrize("tecnologia_esperada,url", OBJETIVOS.items())
def test_recon_identifica_cms_correcto_en_entorno_real(tecnologia_esperada, url):
    if not _sitio_disponible(url):
        pytest.skip(f"{url} no responde — levanta el entorno Docker correspondiente primero")

    inicio = time.perf_counter()
    hallazgo = run_recon(url)
    duracion = time.perf_counter() - inicio

    assert hallazgo is not None, f"recon no detecto ninguna tecnologia en {url}"
    assert hallazgo.tecnologia == tecnologia_esperada

    print(f"[perf] fingerprinting de {tecnologia_esperada}: {duracion:.3f}s")


def test_cms_perfila_wordpress_en_entorno_real():
    url = OBJETIVOS["WordPress"]
    if not _sitio_disponible(url):
        pytest.skip(f"{url} no responde — levanta el entorno Docker de WordPress primero")

    hallazgo_recon = run_recon(url)
    assert hallazgo_recon is not None

    hallazgo_perfilado = run_cms(url, hallazgo_recon)
    assert "plugins_visibles" in hallazgo_perfilado.detalles
