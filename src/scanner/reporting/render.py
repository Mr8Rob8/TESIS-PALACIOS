"""Salidas legibles y JSON para conservar resultados."""

from __future__ import annotations

import json
from dataclasses import asdict

from scanner.core.findings import ResultadoEscaneo


def como_json(resultado: ResultadoEscaneo) -> str:
    return json.dumps(asdict(resultado), ensure_ascii=False, indent=2)


def como_texto(resultado: ResultadoEscaneo) -> str:
    lines = [
        f"Objetivo: {resultado.objetivo}",
        f"HTTP: {resultado.codigo_http} | Duración: {resultado.duracion_segundos:.3f} s | Peticiones: {resultado.peticiones}",
        f"Módulos: {', '.join(resultado.modulos)}",
    ]
    if resultado.pico_memoria_bytes is not None:
        lines.append(f"Pico de memoria del proceso: {resultado.pico_memoria_bytes / (1024 * 1024):.2f} MiB")
    cms = resultado.reconocimiento
    if cms is not None:
        lines.append(f"Tecnología observada: {cms.tecnologia}" + (f" {cms.version}" if cms.version else " (versión no expuesta)"))
        if cms.detalles:
            lines.append(f"Detalles visibles: {cms.detalles}")
    else:
        lines.append("Tecnología: no identificada con las firmas disponibles")
    if not resultado.hallazgos:
        lines.append("Sin señales reportadas en las pruebas seleccionadas; esto no garantiza ausencia de vulnerabilidades.")
    for i, finding in enumerate(resultado.hallazgos, 1):
        lines.extend([
            f"{i}. [{finding.severidad}] {finding.titulo} ({finding.codigo})",
            f"   Evidencia: {finding.evidencia}",
            f"   Recomendación: {finding.recomendacion}",
        ])
    lines.append("Alcance: solo URL inicial y parámetros GET existentes; señales indicativas, sin ejecución de JavaScript ni extracción de datos.")
    return "\n".join(lines)
