"""Recalcula las métricas de caso desde manifest.json y runs.jsonl."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path

SECURITY_CODES = ["XSS-REFLEJO-INDICATIVO", "SQLI-ERROR-INDICATIVO", "HEADER-CSP", "HEADER-FRAME", "HEADER-NOSNIFF"]


def analizar(directory: Path) -> dict:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    records = [json.loads(line) for line in (directory / "runs.jsonl").read_text(encoding="utf-8").splitlines()]
    by_case = defaultdict(list)
    for record in records:
        if record["codigo_salida"] != 0 or record["resultado"] is None:
            raise ValueError(f"Corrida fallida: {record['caso']} {record['repeticion']}")
        by_case[record["caso"]].append(record["resultado"])
    confusion = {code: {"VP": 0, "FP": 0, "VN": 0, "FN": 0} for code in SECURITY_CODES}
    details = []
    cms_correct = 0
    cms_total = 0
    resources = {"seguridad": {"tiempos": [], "memorias": []}, "cms": {"tiempos": [], "memorias": []}}
    unstable = []
    for case in manifest["casos"]:
        runs = by_case[case["id"]]
        if len(runs) != manifest["repeticiones_por_caso"]:
            raise ValueError(f"Número de corridas incompleto: {case['id']}")
        resources[case["tipo"]]["tiempos"].extend(r["duracion_segundos"] for r in runs)
        resources[case["tipo"]]["memorias"].extend(r["pico_memoria_bytes"] for r in runs)
        if case["tipo"] == "cms":
            observed = [r["reconocimiento"]["tecnologia"] if r["reconocimiento"] else None for r in runs]
            votes = sum(name == case["cms_esperado"] for name in observed)
            cms_correct += votes > len(runs) // 2
            cms_total += 1
            if len(set(observed)) > 1:
                unstable.append(case["id"])
            details.append({"caso": case["id"], "esperado": case["cms_esperado"], "observado_por_corrida": observed})
            continue
        observed = [set(h["codigo"] for h in r["hallazgos"]) for r in runs]
        majority = {code for code in SECURITY_CODES if sum(code in row for row in observed) > len(runs) // 2}
        if len({tuple(sorted(row)) for row in observed}) > 1:
            unstable.append(case["id"])
        expected = set(case["esperados"])
        for code in SECURITY_CODES:
            truth = code in expected
            predicted = code in majority
            key = "VP" if truth and predicted else "FN" if truth else "FP" if predicted else "VN"
            confusion[code][key] += 1
        details.append({"caso": case["id"], "esperados": sorted(expected), "observados_mayoria": sorted(majority), "observados_por_corrida": [sorted(row) for row in observed]})
    total = {name: sum(row[name] for row in confusion.values()) for name in ("VP", "FP", "VN", "FN")}
    precision = total["VP"] / (total["VP"] + total["FP"]) if total["VP"] + total["FP"] else None
    recall = total["VP"] / (total["VP"] + total["FN"]) if total["VP"] + total["FN"] else None
    accuracy = (total["VP"] + total["VN"]) / sum(total.values()) if sum(total.values()) else None
    resource_summary = {}
    for kind, values in resources.items():
        resource_summary[kind] = {
            "duracion_segundos": {"mediana": statistics.median(values["tiempos"]), "minimo": min(values["tiempos"]), "maximo": max(values["tiempos"])},
            "pico_memoria_bytes": {"mediana": statistics.median(values["memorias"]), "minimo": min(values["memorias"]), "maximo": max(values["memorias"])},
        }
    return {
        "casos": details, "inestables": unstable, "confusion_por_codigo": confusion,
        "confusion_total": total, "precision": precision, "recall": recall, "exactitud": accuracy,
        "cms_correctos": cms_correct, "cms_total": cms_total,
        "recursos_por_tipo": resource_summary,
        "nota": "Resultados exclusivos de endpoints PHP de laboratorio y páginas base de contenedores; repeticiones no se tratan como casos independientes.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directorio", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(analizar(args.directorio), ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(result + "\n", encoding="utf-8")
    else:
        print(result)
