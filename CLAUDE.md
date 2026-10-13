# CLAUDE.md

Contexto fijo para trabajar en este repositorio con Claude Code. Léelo completo antes de tocar código o texto de tesis.

## Qué es este proyecto

Tesis de pregrado (FISI-UNMSM, Ingeniería de Sistemas): **"Desarrollo de un escáner ligero OWASP para aplicaciones web de bajo costo en PYMEs peruanas"**. Combina dos entregables:

1. **`docs/tesis.md`** — borrador de tesis en Markdown. El estado real por apartado y los criterios de cierre están en `docs/matriz-brechas.md`.
2. **`src/scanner/`** — un prototipo CLI en Python que escanea WordPress, Joomla y Laravel contra un subconjunto priorizado del OWASP Top 10 (reconocimiento/fingerprinting, XSS reflejado, SQLi, headers de seguridad), pensado para correr con <500MB RAM en hosting compartido.

El plan de trabajo ampliado está en `docs/sprints.md`. El tesista pidió cubrir también capítulos finales, anexos y Word; `docs/matriz-brechas.md` registra la prioridad y evidencia real de cada sección.

## Reglas que no se negocian

1. **Nunca inventes citas, DOIs, estadísticas ni resultados académicos.** Toda afirmación nueva se agrega primero a `docs/notas-verificacion.md` con su fuente y estado (✅ verificada / ⚠️ pendiente). Si no puedes verificar algo con búsqueda web activa o resolviendo el DOI contra Crossref, márcalo con ⚠️ en el texto — no lo completes "a ojo".
2. **Verifica DOIs contra la API de Crossref** (`https://api.crossref.org/works/<doi>`), no solo por búsqueda web ni porque "el prefijo parece correcto". En el Sprint 1 se descubrió que los 8 DOIs del borrador original apuntaban a papers equivocados o inexistentes — ver `docs/notas-verificacion.md` sección 1 para el caso de estudio completo.
3. **Las métricas del prototipo (precisión, recall, RAM, tiempo) se reportan solo cuando salen de pruebas reales** contra los entornos Docker de este repo. Nunca reutilices cifras de otras herramientas (ZAP, Burp, Nikto, WPScan) como si fueran resultados del prototipo propio.
4. **El tesista revisa y da el visto bueno final a toda redacción académica y a toda cita externa.** Esa revisión final no impide avanzar en la implementación, experimentación y redacción independiente; mantener los textos como borrador hasta entonces.
5. **El escáner es no destructivo.** Nada de payloads que modifiquen, borren o corrompan datos — solo detección (lectura/reflejo).

## Stack técnico (prototipo)

- Python 3.9+, gestionado con Poetry (`pyproject.toml`).
- `requests` / `aiohttp` para HTTP, `beautifulsoup4` + `lxml` para parseo HTML, `argparse` para el CLI, `colorama` para salida coloreada.
- `pytest` para pruebas, cobertura objetivo >80%.
- Entornos de prueba en `docker/` (WordPress 6.0+, Joomla 4.0+, Laravel 9.0+), sin datos sensibles reales.
- Documentación técnica en español (Sphinx/MkDocs, cuando se llegue a esa parte del plan).

## Estructura de carpetas

```
docs/            tesis.md, sprints.md, notas-verificacion.md, referencias.bib
src/scanner/      cli.py, core/ (http_client, config, validation), modules/ (recon, cms, xss, sqli, headers), reporting/
docker/          docker-compose por CMS (wordpress/, joomla/, laravel/)
tests/           pytest — unitarios + integración contra los entornos Docker
```

## Comandos habituales

```bash
poetry install                              # instalar dependencias
poetry run python -m scanner --help         # ejecutar el CLI
poetry run pytest                           # toda la suite
poetry run pytest tests/test_recon_module.py -k nombre_test  # un solo test
poetry run pytest --cov=scanner --cov-report=term-missing    # con cobertura

cd docker/wordpress && docker compose up -d           # WordPress -> http://localhost:8081
cd docker/joomla    && docker compose up -d           # Joomla    -> http://localhost:8082
cd docker/laravel   && docker compose up -d --build   # Laravel   -> http://localhost:8083
```

Las pruebas en `tests/test_integration_docker.py` requieren esos contenedores corriendo; si un entorno no responde en su puerto, el test correspondiente se salta (`pytest.skip`) en vez de fallar — así la suite queda verde en máquinas sin Docker activo.

## Arquitectura del prototipo

Pipeline lineal, pensado como arquitectura de plugins (cada módulo se puede activar/desactivar por CLI vía `--modules`):

```
cli.py → core/http_client (sesión requests compartida)
        → modules/recon   (fingerprinting pasivo: headers/cookies/HTML → CMS + versión)
        → modules/cms     (perfilado fino por CMS: plugins/temas visibles; reusa el HTML ya obtenido por recon, sin volver a golpear la red salvo que se llame standalone)
        → modules/xss, modules/sqli, modules/headers  (señales indicativas y cabeceras)
        → reporting       (texto/JSON)
```

- **Formato de datos interno**: `core/findings.py` define `HallazgoRecon`, `HallazgoSeguridad` y `ResultadoEscaneo`. El primero une recon→cms; el segundo representa señales DAST y cabeceras; el tercero alimenta reportes.
- **Validación en dos fases**: XSS y SQLi comparan dos respuestas de prueba con una respuesta base dentro de cada módulo. No existe todavía un `core/validation.py` compartido; su extracción requiere justificar una regla común sin confundir los dos detectores.
- **Separación red/lógica**: los módulos separan la función que hace la petición HTTP (`run()`) de la función pura que analiza una respuesta ya obtenida (p. ej. `analizar_respuesta()` en recon, `perfilar()` en cms). Esto es intencional para poder testear con fixtures HTML sin red real (ver `tests/fixtures/html_samples.py`) — sigue este mismo patrón al agregar módulos nuevos.
- **Detección de CMS**: `modules/recon/signatures.py` tiene los detectores por regex/headers para WordPress/Joomla/Laravel; `modules/recon/scanner.py` los orquesta y devuelve el primer match.
- El CLI (`cli.py`) ejecuta los módulos, limita peticiones a GET sobre la URL y parámetros existentes, y genera texto o JSON. `tests/test_scan_local.py` verifica un flujo completo en un servidor efímero local. La suite Docker se ejecutó sin omisiones: 19 pruebas aprobadas y 92% de cobertura; las 45 corridas finales y sus métricas se conservan en `tests/results/20261013T191303Z/`.

Cada decisión de arquitectura de esta sección debe trazar a una sección de `docs/tesis.md` (Cap. 4) o a `docs/sprints.md` — si cambias el pipeline, actualiza ambos.

## Convenciones de commits

Commits semánticos en español, formato `tipo: descripción breve` (`feat: agrega módulo de fingerprinting`, `fix: corrige clasificación OWASP en glosario`, `docs: audita citas de Cap. 2-3`). Un commit por unidad de trabajo coherente (p. ej. un módulo, o la corrección de una sección de tesis), no mezclar código y redacción de tesis en el mismo commit salvo que estén directamente relacionados.

## Qué SÍ puede hacer Claude Code sin preguntar

- Implementar y testear módulos del escáner siguiendo `docs/sprints.md`.
- Buscar (WebSearch) y verificar (Crossref/doi.org) fuentes para reemplazar citas marcadas ⚠️, proponiendo el reemplazo con evidencia antes de aplicarlo.
- Refactorizar/limpiar código propio del prototipo.

## Qué NO debe hacer sin que el tesista lo apruebe explícitamente

- Cerrar una cita o estadística como "verificada" sin mostrar la fuente primaria.
- Reemplazar una cita fabricada por otra sin verificarla igual de rigurosamente.
- Ejecutar payloads destructivos, incluso en los entornos Docker de prueba.
- Hacer commit o push sin que el tesista lo pida explícitamente.
