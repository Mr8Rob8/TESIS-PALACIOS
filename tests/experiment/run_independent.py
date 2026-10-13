"""Banco local adicional con mecanismos separados y negativos difíciles.

La verdad de referencia es el código de este servidor, no una alerta del escáner.
Solo escucha en 127.0.0.1 y ejecuta SELECT sobre SQLite en memoria.
"""

from __future__ import annotations

import hashlib
import html
import importlib.metadata
import json
import os
import platform
import sqlite3
import statistics
import subprocess
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]
CODES = ("XSS-REFLEJO-INDICATIVO", "SQLI-ERROR-INDICATIVO")
CASES = (
    {"id": "xss-html", "path": "/xss-html", "truth": [CODES[0]], "rationale": "parámetro en cuerpo HTML sin codificar"},
    {"id": "xss-escaped", "path": "/xss-escaped", "truth": [], "rationale": "salida HTML codificada"},
    {"id": "xss-inert-text", "path": "/xss-inert-text", "truth": [], "rationale": "marcador literal en respuesta text/plain, sin análisis como HTML"},
    {"id": "sqli-visible", "path": "/sqli-visible", "truth": [CODES[1]], "rationale": "consulta SELECT concatenada; error SQLite expuesto"},
    {"id": "sqli-fake-error", "path": "/sqli-fake-error", "truth": [], "rationale": "respuesta simula nombre de excepción SQL ante comillas sin llamar a SQLite"},
    {"id": "sqli-prepared", "path": "/sqli-prepared", "truth": [], "rationale": "SELECT con parámetro enlazado"},
    {"id": "sqli-hidden", "path": "/sqli-hidden", "truth": [CODES[1]], "rationale": "consulta SELECT concatenada; excepción capturada y respuesta genérica"},
)


class LocalCases(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        url = urlsplit(self.path)
        value = parse_qs(url.query, keep_blank_values=True).get("q", [""])[0]
        path = url.path
        if path == "/xss-html":
            body = f"<html><body>{value}</body></html>"
        elif path == "/xss-escaped":
            body = f"<html><body>{html.escape(value, quote=True)}</body></html>"
        elif path == "/xss-inert-text":
            body = value
        elif path == "/sqli-fake-error":
            body = "sqlite3.OperationalError: example diagnostic" if "'" in value else "<html><body>ok</body></html>"
        elif path in ("/sqli-visible", "/sqli-hidden", "/sqli-prepared"):
            db = sqlite3.connect(":memory:")
            try:
                if path == "/sqli-prepared":
                    db.execute("SELECT 1 WHERE ? = 'hola'", (value,)).fetchall()
                else:
                    db.execute("SELECT 1 WHERE 'hola' = '" + value + "'").fetchall()
                body = "<html><body>ok</body></html>"
            except sqlite3.Error as exc:
                body = "<html><body>error</body></html>" if path == "/sqli-hidden" else "sqlite3.OperationalError: " + str(exc)
            finally:
                db.close()
        else:
            self.send_error(404)
            return
        encoded = body.encode("utf-8")
        self.send_response(200)
        mime = "text/plain" if path == "/xss-inert-text" else "text/html"
        self.send_header("Content-Type", mime + "; charset=utf-8")
        if path != "/xss-html":
            self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    dest = ROOT / "tests" / "results" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-independent")
    server = ThreadingHTTPServer(("127.0.0.1", 0), LocalCases)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        # El manifiesto se escribe antes de ejecutar el primer caso.
        dest.mkdir(parents=True, exist_ok=False)
        manifest = {
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "scope": "servidor efímero local; dos códigos de indicio comparados con verdad de vulnerabilidad del código",
            "unit": "caso por código; cinco repeticiones para estabilidad, mayoría estricta",
            "repetitions": 5,
            "cases": list(CASES),
            "python": sys.version,
            "platform": platform.platform(),
            "scanner_version": importlib.metadata.version("scanner"),
            "requests_version": importlib.metadata.version("requests"),
            "sha256_fixture": digest(Path(__file__)),
            "sha256_scanner": {str(p.relative_to(ROOT)): digest(p) for p in sorted((ROOT / "src/scanner").rglob("*.py"))},
            "measurement": "CLI wall time by parent perf_counter; scanner internal time and PeakWorkingSetSize from JSON; same machine, local loopback",
        }
        (dest / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        records = []
        with (dest / "runs.jsonl").open("w", encoding="utf-8") as raw:
            for case in CASES:
                for repetition in range(1, 6):
                    url = f"http://127.0.0.1:{server.server_port}{case['path']}?q=hola"
                    command = [sys.executable, "-m", "scanner", url, "--modules", "xss", "sqli", "--format", "json"]
                    started = datetime.now(timezone.utc).isoformat()
                    t0 = time.perf_counter()
                    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=90,
                                             env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
                    wall = time.perf_counter() - t0
                    record = {"case": case["id"], "repetition": repetition, "start_utc": started,
                              "command": command, "exit_code": process.returncode, "stdout": process.stdout,
                              "stderr": process.stderr, "wall_seconds": wall,
                              "result": json.loads(process.stdout) if process.returncode == 0 else None}
                    raw.write(json.dumps(record, ensure_ascii=False) + "\n")
                    raw.flush()
                    records.append(record)
                    if process.returncode:
                        raise RuntimeError(f"{case['id']} repetition {repetition}: {process.stderr}")
                    print(f"{case['id']} {repetition}/5")
        counts = {key: 0 for key in ("TP", "FP", "TN", "FN")}
        detail = []
        by_case = defaultdict(list)
        for record in records:
            by_case[record["case"]].append(set(item["codigo"] for item in record["result"]["hallazgos"]))
        for case in CASES:
            observed = {code for code in CODES if sum(code in row for row in by_case[case["id"]]) >= 3}
            for code in CODES:
                truth, prediction = code in case["truth"], code in observed
                key = "TP" if truth and prediction else "FN" if truth else "FP" if prediction else "TN"
                counts[key] += 1
                detail.append({"case": case["id"], "code": code, "truth": truth, "predicted": prediction, "decision": key})
        summary = {"counts": counts, "precision": counts["TP"] / (counts["TP"] + counts["FP"]),
                   "recall": counts["TP"] / (counts["TP"] + counts["FN"]),
                   "wall_median_seconds": statistics.median(r["wall_seconds"] for r in records),
                   "internal_median_seconds": statistics.median(r["result"]["duracion_segundos"] for r in records),
                   "peak_median_mib": statistics.median(r["result"]["pico_memoria_bytes"] for r in records) / 1048576,
                   "cases": detail,
                   "qualification": "Verdad de vulnerabilidad definida por código local. Una alerta indicativa de reflejo/error no equivale a explotación."}
        (dest / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(dest)
        print(json.dumps({k: summary[k] for k in ("counts", "precision", "recall", "wall_median_seconds", "internal_median_seconds", "peak_median_mib")}, indent=2))
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


if __name__ == "__main__":
    main()
