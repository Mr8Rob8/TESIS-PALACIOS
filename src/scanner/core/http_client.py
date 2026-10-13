from __future__ import annotations

from dataclasses import dataclass

import requests

DEFAULT_TIMEOUT = 10
DEFAULT_HEADERS = {
    "User-Agent": "scanner-owasp-pyme/0.1 (no destructivo; ver docs/tesis.md 1.9)",
}
MAX_BODY_BYTES = 1_000_000


@dataclass(frozen=True)
class RespuestaHTTP:
    url: str
    status_code: int
    headers: dict[str, str]
    cookies: dict[str, str]
    text: str


def obtener(session: requests.Session, url: str, timeout: int = DEFAULT_TIMEOUT) -> RespuestaHTTP:
    """GET acotada; no sigue redirecciones ni retiene cuerpos mayores de 1 MB."""
    with session.get(url, timeout=timeout, allow_redirects=False, stream=True) as response:
        chunks = []
        total = 0
        for chunk in response.iter_content(chunk_size=16384):
            remaining = MAX_BODY_BYTES - total
            if remaining <= 0:
                break
            chunks.append(chunk[:remaining])
            total += min(len(chunk), remaining)
            if total >= MAX_BODY_BYTES:
                break
        raw = b"".join(chunks)
        encoding = response.encoding or "utf-8"
        text = raw.decode(encoding, errors="replace")
        return RespuestaHTTP(
            url=url,
            status_code=response.status_code,
            headers=dict(response.headers),
            cookies={c.name: c.value for c in response.cookies},
            text=text,
        )


def get_session() -> requests.Session:
    """Sesion HTTP con pool de conexiones reutilizable (ver tesis.md 2.2.4)."""
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    return session
