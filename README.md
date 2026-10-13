# Escáner ligero OWASP para PYMEs peruanas

Tesis de pregrado (FISI-UNMSM) + prototipo: un escáner de vulnerabilidades web en Python, orientado a PYMEs peruanas que usan WordPress, Joomla o Laravel en hosting compartido, priorizando ligereza (<500MB RAM), un subconjunto seleccionado del OWASP Top 10, y reportes comprensibles para administradores sin perfil técnico especializado.

## Estructura del repositorio

```
docs/
  tesis.md               documento de tesis (Markdown)
  sprints.md             plan ampliado hasta el Word final
  notas-verificacion.md  seguimiento de fuentes verificadas vs. pendientes
  matriz-brechas.md       estado real y criterios de cierre por apartado
  referencias.bib        bibliografía en BibTeX (solo entradas verificadas)
  tesis-borrador-2026-10-13.docx  borrador Word revisado visualmente
src/scanner/             código del prototipo (CLI)
docker/                  entornos WordPress/Joomla/Laravel para pruebas
tests/                   pruebas unitarias e integración (pytest)
```

## Requisitos

- Python 3.9+
- [Poetry](https://python-poetry.org/) para dependencias
- Docker y Docker Compose para los entornos de prueba

## Instalación

```bash
poetry install
```

## Uso

```bash
poetry run python -m scanner --help
poetry run python -m scanner 'http://127.0.0.1:8081/?q=prueba' --format json --output reporte.json
poetry run python -m scanner 'http://127.0.0.1:8081/' --modules recon cms headers
```

El CLI ejecuta reconocimiento de WordPress, Joomla o Laravel, perfilado de señales públicas, comprobación de cabeceras y pruebas indicativas de XSS reflejado y SQLi basada en errores. Solo envía GET a la URL indicada y a variantes de hasta diez parámetros GET ya presentes; no sigue redirecciones ni rastrea otras páginas. Cada respuesta se limita a 1 MB. El reporte distingue señales indicativas de vulnerabilidades confirmadas. Ejecútalo únicamente contra objetivos propios o expresamente autorizados.

`--format text` es la salida predeterminada; `--format json` conserva el resultado estructurado. `--output` guarda el reporte. `--timeout` fija los segundos máximos por petición. La ausencia de hallazgos no demuestra que el sitio sea seguro: no se prueban formularios POST, XSS almacenado, SQLi ciega ni sesiones autenticadas.

## Entornos de prueba

Cada CMS tiene su propio `docker-compose.yml` en `docker/<cms>/`. El arranque requiere un motor Docker disponible:

```bash
cd docker/wordpress && docker compose up -d
```

## Pruebas

```bash
poetry run pytest
```

## Estado del proyecto

El pipeline y los reportes se validaron en un servidor local y en WordPress, Joomla y Laravel bajo Docker en `127.0.0.1`. La corrida final está en `tests/results/20261013T191303Z/`: 45 procesos del CLI, manifiesto, salidas crudas, identificadores de imagen y resumen recalculable. La suite final pasó 19 pruebas con 92% de cobertura. El capítulo 6 reporta resultados **solo del laboratorio construido**; no estima desempeño, prevalencia de fallas ni usabilidad en PYMEs peruanas.

El manuscrito está en `docs/tesis.md` y el borrador Word de 35 páginas en `docs/tesis-borrador-2026-10-13.docx`; sus páginas renderizadas para revisión se conservan en `docs/qa/render10/`. La matriz de pendientes y los límites de las fuentes figuran en `docs/matriz-brechas.md` y `docs/notas-verificacion.md`. La dedicatoria, los agradecimientos, la norma institucional vigente y la aprobación académica requieren intervención del tesista y la asesoría.
