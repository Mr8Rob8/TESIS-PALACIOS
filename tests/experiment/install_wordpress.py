"""Instala la instancia WordPress del laboratorio, si aún no está configurada."""

from __future__ import annotations

import requests

BASE = "http://127.0.0.1:8081"


def main() -> None:
    session = requests.Session()
    home = session.get(BASE + "/", timeout=15, allow_redirects=False)
    if home.status_code == 200:
        print("WordPress ya responde en la página principal; no se modifica")
        return
    if home.status_code != 302 or "/wp-admin/install.php" not in home.headers.get("Location", ""):
        raise RuntimeError(f"Estado inicial inesperado: HTTP {home.status_code}")
    page = session.get(BASE + "/wp-admin/install.php?step=1", timeout=15)
    page.raise_for_status()
    data = {
        "weblog_title": "Scanner Lab WordPress",
        "user_name": "labadmin",
        "admin_password": "local-test-only-pass-2026",
        "admin_password2": "local-test-only-pass-2026",
        "admin_email": "labadmin@example.invalid",
        "blog_public": "0",
        "Submit": "Install WordPress",
        "language": "",
    }
    result = session.post(BASE + "/wp-admin/install.php?step=2", data=data, timeout=30)
    result.raise_for_status()
    final = session.get(BASE + "/", timeout=15, allow_redirects=False)
    if final.status_code != 200:
        raise RuntimeError(f"WordPress no quedó instalado: HTTP {final.status_code}")
    print("WordPress instalado en 127.0.0.1:8081 para pruebas locales")


if __name__ == "__main__":
    main()
