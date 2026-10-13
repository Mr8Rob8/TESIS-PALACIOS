"""Regenera la tabla compacta del Anexo D desde las corridas crudas."""

from __future__ import annotations

import json
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUNS = ROOT / "tests/results/20261013T203602Z/runs.jsonl"
THESIS = ROOT / "docs/tesis.md"
MARKER_START = "<!-- INICIO_TABLA_CORRIDAS -->"
MARKER_END = "<!-- FIN_TABLA_CORRIDAS -->"
SHORT = {
    "HEADER-CSP": "CSP",
    "HEADER-FRAME": "FRAME",
    "HEADER-NOSNIFF": "NOSNIFF",
    "SQLI-ERROR-INDICATIVO": "SQLI",
    "XSS-REFLEJO-INDICATIVO": "XSS",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=DEFAULT_RUNS)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.runs.read_text(encoding="utf-8").splitlines()]
    if len(rows) != 45 or any(row["codigo_salida"] != 0 for row in rows):
        raise ValueError("Se esperaban 45 corridas completas con salida 0")
    lines = [
        "| Caso | Rep. | HTTP | Señales / CMS | Tiempo (s) | Pico (MiB) |",
        "|---|---:|---:|---|---:|---:|",
    ]
    for row in rows:
        result = row["resultado"]
        codes = ", ".join(SHORT[finding["codigo"]] for finding in result["hallazgos"])
        recognition = result.get("reconocimiento")
        observed = codes or (recognition or {}).get("tecnologia") or "ninguno"
        lines.append(
            f'| {row["caso"]} | {row["repeticion"]} | {result["codigo_http"]} '
            f'| {observed} | {result["duracion_segundos"]:.4f} '
            f'| {result["pico_memoria_bytes"] / 1048576:.2f} |'
        )
    thesis = THESIS.read_text(encoding="utf-8")
    table = MARKER_START + "\n" + "\n".join(lines) + "\n" + MARKER_END
    if thesis.count(MARKER_START) != 1 or thesis.count(MARKER_END) != 1:
        raise ValueError("No se encontraron los límites de la tabla del Anexo D")
    start = thesis.index(MARKER_START)
    end = thesis.index(MARKER_END) + len(MARKER_END)
    thesis = thesis[:start] + table + thesis[end:]
    THESIS.write_text(thesis, encoding="utf-8")


if __name__ == "__main__":
    main()
