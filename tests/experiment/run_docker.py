"""Corridas de laboratorio sobre los tres contenedores del repositorio.

No escanea direcciones distintas de 127.0.0.1:8081-8083. Cada ejecución del
CLI usa un proceso fresco. El directorio de salida tiene marca UTC y no se
sobrescribe, para conservar datos crudos y el plan previo a las corridas.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
PORTS = {"wordpress": 8081, "joomla": 8082, "laravel": 8083}
CMS = {"wordpress": "WordPress", "joomla": "Joomla", "laravel": "Laravel"}
SECURITY_CODES = ["XSS-REFLEJO-INDICATIVO", "SQLI-ERROR-INDICATIVO", "HEADER-CSP", "HEADER-FRAME", "HEADER-NOSNIFF"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def casos() -> list[dict]:
    result = []
    for name, port in PORTS.items():
        host = f"http://127.0.0.1:{port}"
        result.extend([
            {"id": f"{name}-vulnerable", "tipo": "seguridad", "url": host + "/scanner-vulnerable.php?q=hola", "esperados": SECURITY_CODES},
            {"id": f"{name}-seguro", "tipo": "seguridad", "url": host + "/scanner-safe.php?q=hola", "esperados": []},
            {"id": f"{name}-cms", "tipo": "cms", "url": host + "/", "cms_esperado": CMS[name]},
        ])
    return result


def run(repeticiones: int, destino: Path) -> None:
    if repeticiones < 1 or repeticiones % 2 != 1:
        raise ValueError("Use un número impar positivo de repeticiones")
    plan = casos()
    for case in plan:
        try:
            response = requests.get(case["url"], timeout=10, allow_redirects=False)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Caso {case['id']} no disponible: {exc}") from exc
    destino.mkdir(parents=True, exist_ok=False)
    source_paths = sorted((ROOT / "src" / "scanner").rglob("*.py"))
    manifest = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "repeticiones_por_caso": repeticiones,
        "unidad": "caso por código de señal; repeticiones para estabilidad y distribución de recursos",
        "voto": "mayoría estricta de las repeticiones por caso y código, predefinido",
        "python": sys.version,
        "plataforma": platform.platform(),
        "paquetes": {name: importlib.metadata.version(name) for name in ("requests", "scanner")},
        "medida_memoria": "PeakWorkingSetSize del proceso en Windows; ru_maxrss en POSIX, convertida a bytes",
        "medida_tiempo": "perf_counter desde antes de GET inicial hasta fin de módulos; no incluye arranque de Python ni serialización",
        "casos": plan,
        "sha256_fuentes": {str(path.relative_to(ROOT)): sha256(path) for path in source_paths},
        "sha256_laboratorio": sha256(ROOT / "docker" / "lab" / "scanner_case.php"),
        "sha256_compose": {name: sha256(ROOT / "docker" / name / "docker-compose.yml") for name in PORTS},
        "sha256_experimento": {name: sha256(ROOT / "tests" / "experiment" / name) for name in ("run_docker.py", "analyze_docker.py")},
    }
    (destino / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    with (destino / "runs.jsonl").open("w", encoding="utf-8") as raw:
        for case in plan:
            modules = ["recon", "cms"] if case["tipo"] == "cms" else ["recon", "cms", "xss", "sqli", "headers"]
            for repetition in range(1, repeticiones + 1):
                command = [sys.executable, "-m", "scanner", case["url"], "--modules", *modules, "--format", "json"]
                started = datetime.now(timezone.utc).isoformat()
                completed = subprocess.run(
                    command, cwd=ROOT, text=True, capture_output=True, timeout=90,
                    encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
                )
                payload = json.loads(completed.stdout) if completed.returncode == 0 else None
                record = {
                    "caso": case["id"], "repeticion": repetition, "inicio_utc": started,
                    "comando": command, "codigo_salida": completed.returncode,
                    "stdout": completed.stdout, "stderr": completed.stderr, "resultado": payload,
                }
                raw.write(json.dumps(record, ensure_ascii=False) + "\n")
                raw.flush()
                if completed.returncode != 0:
                    raise RuntimeError(f"Escaneo falló en {case['id']} repetición {repetition}; datos parciales conservados en {destino}")
                print(f"{case['id']} {repetition}/{repeticiones} OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeticiones", type=int, default=5)
    parser.add_argument("--destino", type=Path, default=ROOT / "tests" / "results" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    args = parser.parse_args()
    run(args.repeticiones, args.destino)
