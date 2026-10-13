from scanner.core.findings import Confianza
from scanner.modules.recon.scanner import analizar_respuesta
from tests.fixtures.html_samples import (
    JOOMLA_COOKIES,
    JOOMLA_HEADERS,
    JOOMLA_HTML,
    LARAVEL_COOKIES,
    LARAVEL_HEADERS,
    LARAVEL_HTML,
    UNKNOWN_COOKIES,
    UNKNOWN_HEADERS,
    UNKNOWN_HTML,
    WORDPRESS_COOKIES,
    WORDPRESS_HEADERS,
    WORDPRESS_HTML,
)


def test_detecta_wordpress_por_meta_generator():
    hallazgo = analizar_respuesta(WORDPRESS_HEADERS, WORDPRESS_COOKIES, WORDPRESS_HTML)
    assert hallazgo is not None
    assert hallazgo.tecnologia == "WordPress"
    assert hallazgo.version == "6.4"
    assert hallazgo.confianza == Confianza.CONFIRMADO


def test_detecta_joomla_por_meta_generator():
    hallazgo = analizar_respuesta(JOOMLA_HEADERS, JOOMLA_COOKIES, JOOMLA_HTML)
    assert hallazgo is not None
    assert hallazgo.tecnologia == "Joomla"
    assert hallazgo.version == "4.4"


def test_detecta_laravel_por_cookie_de_sesion():
    hallazgo = analizar_respuesta(LARAVEL_HEADERS, LARAVEL_COOKIES, LARAVEL_HTML)
    assert hallazgo is not None
    assert hallazgo.tecnologia == "Laravel"


def test_sitio_generico_no_produce_falso_positivo():
    hallazgo = analizar_respuesta(UNKNOWN_HEADERS, UNKNOWN_COOKIES, UNKNOWN_HTML)
    assert hallazgo is None
