"""Parámetros GET existentes: superficie deliberadamente acotada del prototipo."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def validar_objetivo(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Se requiere una URL HTTP(S) con host y sin credenciales")
    return url


def parametros_get(url: str, limite: int = 10) -> list[str]:
    pairs = parse_qsl(urlsplit(url).query, keep_blank_values=True)
    return list(dict.fromkeys(name for name, _ in pairs))[:limite]


def sustituir_parametro(url: str, nombre: str, valor: str) -> str:
    parsed = urlsplit(url)
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    changed = False
    result = []
    for key, old in pairs:
        if key == nombre and not changed:
            result.append((key, valor))
            changed = True
        else:
            result.append((key, old))
    if not changed:
        raise ValueError(f"El parámetro {nombre!r} no existe en el objetivo")
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(result), ""))
