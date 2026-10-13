"""Genera la tabla de las 35 corridas independientes desde JSONL crudo."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "tests/results/20261013T203541Z-independent/runs.jsonl"
THESIS = ROOT / "docs/tesis.md"
START = "<!-- INICIO_TABLA_INDEPENDIENTE -->"
END = "<!-- FIN_TABLA_INDEPENDIENTE -->"


def main() -> None:
    records = [json.loads(line) for line in RUNS.read_text(encoding="utf-8").splitlines()]
    if len(records) != 35 or any(record["exit_code"] != 0 for record in records):
        raise ValueError("Se esperaban 35 procesos completos")
    lines = ["| Ruta | Rep. | Indicios | Pared (s) | Interno (s) | Pico (MiB) |",
             "|---|---:|---|---:|---:|---:|"]
    for row in records:
        result = row["result"]
        codes = ", ".join("XSS" if item["codigo"].startswith("XSS") else "SQLI" for item in result["hallazgos"])
        lines.append(
            f'| {row["case"]} | {row["repetition"]} | {codes or "ninguno"} '
            f'| {row["wall_seconds"]:.4f} | {result["duracion_segundos"]:.4f} '
            f'| {result["pico_memoria_bytes"] / 1048576:.2f} |'
        )
    source = THESIS.read_text(encoding="utf-8")
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError("Marcadores de tabla independiente no únicos")
    first = source.index(START)
    last = source.index(END) + len(END)
    table = START + "\n" + "\n".join(lines) + "\n" + END
    THESIS.write_text(source[:first] + table + source[last:], encoding="utf-8")


if __name__ == "__main__":
    main()
