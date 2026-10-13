"""Recalcula el banco independiente solo desde manifiesto y corridas crudas."""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

CODES = ("XSS-REFLEJO-INDICATIVO", "SQLI-ERROR-INDICATIVO")


def analyze(directory: Path) -> dict:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    records = [json.loads(line) for line in (directory / "runs.jsonl").read_text(encoding="utf-8").splitlines()]
    by_case = defaultdict(list)
    for record in records:
        if record["exit_code"] != 0 or record["result"] is None:
            raise ValueError(f"corrida fallida: {record['case']} {record['repetition']}")
        by_case[record["case"]].append(record)
    counts = {key: 0 for key in ("TP", "FP", "TN", "FN")}
    detail = []
    for case in manifest["cases"]:
        runs = by_case[case["id"]]
        if len(runs) != manifest["repetitions"] or sorted(r["repetition"] for r in runs) != list(range(1, manifest["repetitions"] + 1)):
            raise ValueError(f"corridas incompletas: {case['id']}")
        observed = [{finding["codigo"] for finding in record["result"]["hallazgos"]} for record in runs]
        for code in CODES:
            truth = code in case["truth"]
            prediction = sum(code in row for row in observed) > len(observed) // 2
            key = "TP" if truth and prediction else "FN" if truth else "FP" if prediction else "TN"
            counts[key] += 1
            detail.append({"case": case["id"], "code": code, "truth": truth, "predicted": prediction, "decision": key})
    return {
        "counts": counts,
        "precision": counts["TP"] / (counts["TP"] + counts["FP"]),
        "recall": counts["TP"] / (counts["TP"] + counts["FN"]),
        "wall_median_seconds": statistics.median(r["wall_seconds"] for r in records),
        "internal_median_seconds": statistics.median(r["result"]["duracion_segundos"] for r in records),
        "peak_median_mib": statistics.median(r["result"]["pico_memoria_bytes"] for r in records) / 1048576,
        "cases": detail,
        "qualification": "Verdad de vulnerabilidad definida por código local. Una alerta indicativa de reflejo/error no equivale a explotación.",
    }


if __name__ == "__main__":
    result = analyze(Path(sys.argv[1]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
