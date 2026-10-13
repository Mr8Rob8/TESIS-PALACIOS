"""Firmas pasivas de reconocimiento por CMS (headers, cookies, meta generator,
rutas conocidas). Ver tesis.md 3.1 (fingerprinting de tecnologias).

Estas firmas son deliberadamente conservadoras: solo se usan para identificar
la tecnologia base, no para explotar nada (escaneo no destructivo, 1.9).
"""

from __future__ import annotations

import re

WORDPRESS_COOKIE_RE = re.compile(r"wordpress_logged_in|wp-settings", re.IGNORECASE)
WORDPRESS_META_RE = re.compile(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']WordPress\s*([\d.]*)', re.IGNORECASE)
WORDPRESS_PATH_MARKERS = ("/wp-login.php", "/wp-content/", "/wp-includes/", "/wp-json/")

JOOMLA_COOKIE_RE = re.compile(r"joomla_user_state", re.IGNORECASE)
JOOMLA_META_RE = re.compile(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']Joomla!\s*-\s*Open Source Content Management(?:\s*-\s*Version\s*([\d.]+))?', re.IGNORECASE)
JOOMLA_PATH_MARKERS = ("/administrator/", "/components/", "/media/jui/")

LARAVEL_COOKIE_RE = re.compile(r"laravel_session|XSRF-TOKEN", re.IGNORECASE)
LARAVEL_MARKER_RE = re.compile(r"laravel", re.IGNORECASE)
LARAVEL_PATH_MARKERS = ("/up",)


def detect_wordpress(headers: dict, cookies: dict, html: str) -> tuple[bool, str | None, str]:
    # El meta generator va primero: es la unica fuente que trae version, asi
    # que se prioriza sobre las senales que solo confirman "es WordPress".
    match = WORDPRESS_META_RE.search(html or "")
    if match:
        version = match.group(1) or None
        return True, version, "meta generator"
    if any(WORDPRESS_COOKIE_RE.search(str(nombre_cookie)) for nombre_cookie in cookies.keys()):
        return True, None, "cookie wp-*"
    if any(marker in (html or "") for marker in WORDPRESS_PATH_MARKERS):
        return True, None, "marcador de ruta en HTML"
    return False, None, ""


def detect_joomla(headers: dict, cookies: dict, html: str) -> tuple[bool, str | None, str]:
    match = JOOMLA_META_RE.search(html or "")
    if match:
        version = match.group(1) or None
        return True, version, "meta generator"
    if any(JOOMLA_COOKIE_RE.search(str(nombre_cookie)) for nombre_cookie in cookies.keys()):
        return True, None, "cookie joomla_user_state"
    if any(marker in (html or "") for marker in JOOMLA_PATH_MARKERS):
        return True, None, "marcador de ruta en HTML"
    return False, None, ""


def detect_laravel(headers: dict, cookies: dict, html: str) -> tuple[bool, str | None, str]:
    if any(LARAVEL_COOKIE_RE.search(str(k)) for k in cookies.keys()):
        return True, None, "cookie laravel_session/XSRF-TOKEN"
    if LARAVEL_MARKER_RE.search(html or ""):
        return True, None, "texto/estructura de la pagina de bienvenida"
    return False, None, ""
