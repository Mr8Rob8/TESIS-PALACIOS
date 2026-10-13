# Sprints de desarrollo — Escáner ligero OWASP para PYMEs peruanas

**Alcance de este plan:** los cinco sprints originales cubren el desarrollo inicial. Los sprints 6–8 añaden el cierre de resultados, conclusiones, anexos y Word. Los estados y criterios actualizados están en `docs/matriz-brechas.md`; el texto redactado en los sprints previos no se considera cerrado sin evidencia.

La validación con PYMEs depende de participantes, consentimiento y un protocolo que aún no constan en el repositorio. No condiciona el trabajo independiente con entornos locales controlados.

Estructura de capítulos de referencia (según `Estructura de TESIS (1).docx`, plantilla FISI-UNMSM):

| Capítulo | Estado antes de este plan | Sprint que lo trabaja |
|---|---|---|
| 1. Planteamiento del problema | Redactado; fuentes y objetivos requieren auditoría | Auditoría inicial y sprint 6 |
| 2. Marco teórico | Redactado; citas de contenido y cifras requieren auditoría | Auditoría inicial y sprint 6 |
| 3. Estado del arte | Redactado; benchmarking no verificado | Auditoría inicial y sprint 6 |
| 4. Aporte teórico | Diseño redactado; trazabilidad con código pendiente | Sprints 1–4 y auditoría |
| 5. Aporte práctico | Implementación parcial | Sprints 2–4 y 6 |
| 6. Análisis de resultados | Sin datos crudos ni capítulo | Sprints 5–6 |
| Conclusiones / Recomendaciones / Trabajos futuros / Anexos | No iniciados | Sprints 7–8 |

Cada sprint sigue el ciclo **DSR** (identificación del problema → objetivos → diseño/desarrollo → demostración → evaluación → comunicación) definido en la sección 3.5 de la tesis, aplicado a un módulo concreto del escáner.

---

## Reglas fijas para todos los sprints (van también en CLAUDE.md)

1. **Nunca inventar citas, DOIs, estadísticas o resultados.** Toda afirmación académica nueva se agrega primero a `docs/notas-verificacion.md` con su fuente y estado de verificación (verificada / pendiente ⚠️).
2. **Las métricas del prototipo (precisión, recall, RAM, tiempo) se reportan solo cuando salen de pruebas reales** contra entornos locales con verdad de referencia. La Tabla 3.1 actual es un protocolo pendiente, no resultados de otras herramientas.
3. **Yo (el tesista) reviso y verifico toda la redacción académica.** Claude Code puede proponer estructura, resumir hallazgos técnicos del propio desarrollo y redactar un primer borrador, pero cualquier cita o dato externo debe quedar marcado con ⚠️ hasta que yo confirme la fuente primaria.
4. **El código de escaneo es no destructivo** (solo lectura/reflejo, sin payloads que modifiquen datos), consistente con la sección 1.6.
5. Cada unidad termina con cambio verificable, prueba pertinente, sección de tesis afectada y actualización de `notas-verificacion.md`. No hacer commit ni push sin petición expresa del tesista.

---

## Sprint 1 — Cimentación del proyecto y Capítulo 4 (Aporte teórico)

**Duración:** semanas 1-2
**Ciclo DSR:** identificación del problema → definición de objetivos (para todo el proyecto de desarrollo)

### Objetivo
Dejar el repositorio listo para trabajar con Claude Code de forma sostenida, resolver las 5 inconsistencias señaladas en el TODO de `tesis.md`, y producir el diseño de arquitectura que sustenta el Capítulo 4 completo.

### Tareas
**Proyecto / infraestructura**
- Crear `CLAUDE.md` en la raíz (contexto fijo: objetivo, alcance OWASP seleccionado, stack, convenciones de commits, qué SÍ/NO debe inventar Claude).
- Crear `docs/notas-verificacion.md` con tabla: Afirmación → Fuente citada → Verificada (sí/no) → Enlace/DOI directo. Precargarla con las 5 inconsistencias del TODO actual.
- Crear `docs/referencias.bib` en formato BibTeX a partir de la sección 3 de `tesis.md`, dejando comentado (`% ⚠️ pendiente`) cualquier entrada no verificada.
- Crear `README.md` (propósito del repo, cómo correr el escáner, estructura de carpetas).
- Inicializar repositorio Git si aún no existe (`git init`, `.gitignore` para Python/Docker).
- Andamiaje `src/scanner/`: `__init__.py`, `cli.py` (esqueleto con `argparse`), `core/` (config, http client con `requests`/`aiohttp`), `modules/` (carpetas vacías `recon/`, `xss/`, `sqli/`, `headers/`, `cms/`), `reporting/`.
- `pyproject.toml` con Poetry, dependencias base (`requests`, `aiohttp`, `beautifulsoup4`, `lxml`, `colorama`, `pytest`).

**Verificación (Cap. 1-3)**
- Resolver el DOI contradictorio de Abraham et al. (2020) contra Crossref/doi.org — determinar si son dos papers distintos o un error de transcripción, y corregir `tesis.md`.
- Confirmar contra el documento oficial OWASP Top 10 2021 si Injection es A03 y corregir la entrada de SQLi en el glosario (2.3).
- Mantener retirada la cita textual atribuida a Jain y Gupta (2020, p. 45): la auditoría de `notas-verificacion.md` no encontró respaldo. No reutilizarla.
- Marcar en `notas-verificacion.md` el estado real de las estadísticas de Fortinet, Movistar Empresas, OSIPTEL, INEI y CERT-Perú (verificada / no encontrada / requiere acceso de pago).
- Confirmar que todos los DOIs de la sección 3 resuelven correctamente en doi.org.

**Capítulo 4: Aporte teórico**
- 4.1 Definición de la solución, arquitectura y metodología: formalizar la arquitectura modular (recon → fingerprinting → módulos DAST selectivos → validación en dos fases → motor de reportes) ya esbozada en 2.2.3 y 3.1.
- 4.2 Fundamentación de la solución, arquitectura y metodología: separar decisiones propias del prototipo de afirmaciones tomadas de fuentes. Los metadatos de Aljebry et al. (2022), Prabakar et al. (2013) y Amankwah et al. (2020) constan en `notas-verificacion.md`, pero sus aportes específicos requieren lectura del texto completo antes de atribuirlos. No reutilizar Jain y Gupta, Anupama y Venkataramani, Egele ni Kumar como sustento.
- 4.3 Definición de la arquitectura de datos, sistemas y tecnológica: diagrama de componentes (CLI → core → módulos → reporting), formato de datos internos (estructura de "hallazgo": módulo, severidad, evidencia, confianza, recomendación), stack tecnológico (ya listado en 3.6, formalizarlo como arquitectura).
- 4.4 Ampliar fundamentación con el mapeo explícito objetivo específico → componente de arquitectura → capítulo de tesis que lo sustenta.
- Adelantar 5.1.1 (diagramas de casos de uso: "administrador PYME ejecuta escaneo", "administrador revisa reporte") y 5.1.4 (requerimientos funcionales/no funcionales, estos últimos ya casi definidos por 3.6: <500MB RAM, <30min/500 páginas, <5h de aprendizaje).

### Entregables
- `CLAUDE.md`, `README.md`, `docs/notas-verificacion.md`, `docs/referencias.bib`.
- Esqueleto ejecutable de `src/scanner` (`python -m scanner --help` funciona).
- `tesis.md` con Cap. 1-3 corregidos (sin ⚠️ de inconsistencia interna; las que dependan de fuentes externas de pago quedan honestamente marcadas como pendientes, no resueltas a ciegas).
- Borrador Capítulo 4 completo (4.1-4.4) + adelanto de 5.1.1 y 5.1.4.

### Criterios de aceptación
- Cero inconsistencias internas sin resolver o sin justificar en el documento.
- El esqueleto corre sin errores y tiene al menos un test de humo (`pytest` verde).
- Cada afirmación nueva del Capítulo 4 traza a una referencia ya presente en 2.6/3.4, o está marcada ⚠️.

---

## Sprint 2 — Módulo de Reconocimiento/Fingerprinting + entornos Docker

**Duración:** semanas 3-4
**Ciclo DSR:** diseño y desarrollo (primer módulo) → demostración temprana

### Objetivo
Implementar el módulo de reconocimiento pasivo (fingerprinting de WordPress/Joomla/Laravel, detección de endpoints) y levantar los entornos Docker Compose que servirán de banco de pruebas para todos los módulos siguientes.

### Tareas
**Código**
- `docker/wordpress/`, `docker/joomla/`, `docker/laravel/`: `docker-compose.yml` por CMS, versiones mínimas de 3.6 (WordPress 6.0+, Joomla 4.0+, Laravel 9.0+), sin datos sensibles reales.
- `src/scanner/modules/recon/`: detección de tecnología por señales pasivas observables en headers, cookies y HTML. Las rutas visibles son pistas, no evidencia de que el escáner solicite rutas administrativas. Esta es una decisión de diseño propia; no atribuirla a Kumar (2019).
- `src/scanner/modules/cms/`: perfilado más fino por CMS (versión, plugins/temas visibles si aplica).
- Cliente HTTP compartido en `core/http_client.py` (pool de conexiones reutilizables, sección 2.2.4).
- Estructura de datos "hallazgo de reconocimiento" (tecnología, versión, confianza) que alimenta 4.3.
- Tests unitarios de fingerprinting contra fixtures HTML/headers.
- Test de integración contra los 3 contenedores Docker levantados.

### Tesis
- 5.1.2 Definición de la arquitectura de la solución, datos y tecnológica: concretar con el diagrama real de cómo `recon` alimenta a los módulos DAST (fingerprinting condiciona qué pruebas se ejecutan, sección 2.2.4 "ejecución selectiva").
- 5.1.3 Modelamiento de datos: documentar el esquema interno de "hallazgo" definido en el código.
- 5.2.3 Lista de módulos principales: primera entrada completa (módulo `recon`), con su contrato de entrada/salida.

### Entregables
- 3 entornos Docker levantables con `docker compose up`.
- Módulo `recon` con cobertura de tests ≥80% (meta de 3.6).
- Sección 5.1.2/5.1.3 en borrador, 5.2.3 con la primera entrada.

### Criterios de aceptación
- El módulo identifica correctamente el CMS y versión en los 3 entornos Docker de prueba.
- Tiempo de fingerprinting por sitio documentado (primer dato real de rendimiento, sin extrapolar aún precisión/recall globales).

---

## Sprint 3 — Módulos DAST: XSS reflejado y SQL Injection

**Duración:** semanas 5-6
**Ciclo DSR:** diseño y desarrollo (núcleo de detección) → demostración

### Objetivo
Implementar XSS reflejado y SQLi no destructiva, seleccionados por el alcance de la tesis y su pertenencia a A03:2021 Injection. La validación en dos fases es una hipótesis de diseño propia cuya contribución a los falsos positivos debe medirse; no atribuirla a Egele et al. (2019).

### Tareas
**Código**
- `src/scanner/modules/sqli/`: comparación de respuestas y patrones de errores SQL con entradas no destructivas. Especificar y medir el algoritmo realmente implementado; no atribuir complejidad O(n) sin análisis, ni citar a Anupama y Venkataramani (2018).
- `src/scanner/modules/xss/`: análisis sintáctico de respuestas HTTP para XSS reflejado, heurística de coincidencia contextual entrada→salida (2.2.3).
- `core/validation.py`: pipeline de validación en dos fases reutilizable por ambos módulos (detección inicial → confirmación secundaria antes de reportar).
- Payloads de prueba documentados y justificados (por qué cada payload, qué variante de la vulnerabilidad cubre).
- Tests unitarios por payload/heurística + tests de integración contra los entornos Docker (con endpoints deliberadamente vulnerables agregados de forma controlada, sin exponer datos reales).

### Tesis
- 5.2.2 Definición de algoritmos principales: documentar en detalle el algoritmo de pattern matching de SQLi y la heurística de XSS, con pseudocódigo o diagrama de flujo.
- 5.2.3 Lista de módulos principales: agregar entradas `sqli` y `xss`.
- 5.2.1 (adelanto): definir formalmente qué se va a medir en Sprint 5 (precisión, recall, tasa de falsos positivos/negativos) y cómo, ya con el pipeline de dos fases implementado como variable de diseño.

### Entregables
- Módulos `sqli` y `xss` funcionando contra los entornos Docker con vulnerabilidades conocidas insertadas.
- Sección 5.2.2 en borrador (algoritmos con pseudocódigo).

### Criterios de aceptación
- Ambos módulos detectan las vulnerabilidades conocidas insertadas deliberadamente en los entornos de prueba, sin ejecutar payloads destructivos.
- El pipeline de dos fases reduce demostrablemente falsos positivos frente a una versión sin segunda fase (comparación interna documentada, no frente a otras herramientas todavía).

---

## Sprint 4 — Headers de seguridad, motor de reportes y suite de pruebas

**Duración:** semanas 7-8
**Ciclo DSR:** diseño y desarrollo (módulos restantes + instrumentación) → preparación de evaluación

### Objetivo
Cerrar el conjunto de módulos previstos en el objetivo específico 3 (headers HTTP) y construir el motor de reportes legible para no especialistas (objetivo específico 5), además de dejar lista la instrumentación de métricas para el Sprint 5.

### Tareas
**Código**
- `src/scanner/modules/headers/`: verificar cabeceras de seguridad aplicables (CSP, X-Frame-Options, HSTS solo en HTTPS, X-Content-Type-Options). Justificar cada comprobación por su efecto de seguridad y contexto; el supuesto 41% de instalaciones Joomla carece de fuente y no se usa para priorizar.
- `src/scanner/reporting/`: motor de reportes con salida coloreada (`colorama`) y plantilla de "respuesta técnica para administradores" (objetivo específico 5), con explicación en lenguaje simple + pasos de mitigación por hallazgo.
- Integración de los 5 módulos (`recon`, `cms`, `sqli`, `xss`, `headers`) en el CLI único (`cli.py`), con banderas para activar/desactivar módulos (arquitectura de plugins, 4.1).
- Instrumentación: medición de tiempo de ejecución y uso de RAM por escaneo (para las métricas del objetivo específico 4).
- Suite de pruebas con Pytest, cobertura >80% (meta de 3.6), incluyendo pruebas de regresión sobre los módulos de sprints anteriores.
- Documentación técnica inicial con Sphinx/MkDocs (en español, según 3.6).

### Tesis
- 5.2.1 Definición de métricas y prueba del sistema: cerrar esta sección con el diseño completo del experimento de medición (qué se mide, con qué entornos, cuántas corridas, qué se considera verdadero positivo/negativo dado que se conocen las vulnerabilidades insertadas).
- 5.2.3 Lista de módulos principales: completar con `headers` y el motor de reportes.
- Actualizar 5.1.4 (requerimientos no funcionales) con los umbrales reales de instrumentación ya integrados en el código (no solo aspiracionales).

### Entregables
- CLI integrado funcionando end-to-end sobre los 3 entornos Docker.
- Reportes de ejemplo generados (uno por CMS).
- Suite de pruebas >80% cobertura corriendo en CI local (o script único `make test` / `poetry run pytest`).
- Sección 5.2.1 completa, 5.2.3 completa.

### Criterios de aceptación
- Un único comando ejecuta un escaneo completo contra un sitio y genera un reporte legible.
- La suite de pruebas pasa de forma reproducible y mide cobertura.

---

## Sprint 5 — Evaluación local reproducible y primer borrador del Capítulo 6

**Duración:** semanas 9-10
**Ciclo DSR:** demostración → evaluación → comunicación

### Objetivo
Ejecutar el escáner completo contra los 3 entornos Docker, medir precisión/recall/RAM/tiempo con datos propios (no de otras herramientas), y redactar el primer borrador del Capítulo 6 con esos resultados reales.

### Tareas
**Código / experimentación**
- Diseñar el set de vulnerabilidades "conocidas" en cada entorno Docker (ground truth) para poder calcular VP/VN/FP/FN de forma objetiva.
- Definir antes de la medición el número de corridas por escenario y justificarlo; ejecutar todas las corridas previstas por CMS y registrar resultados crudos (JSON/CSV) en `tests/results/`.
- Calcular precisión, recall, consumo de RAM y tiempo de escaneo reales; comparar contra las metas de 2.2.4 (<500MB, <30min/500 páginas) y el objetivo del Cap. 1 (precisión ≥80%, recall ≥75%, sección 3.7).
- (Opcional) Ejecutar OWASP ZAP y/o Nikto contra los mismos entornos, conservando versiones, configuración y datos crudos para una comparación propia.
- Revisión de todo `notas-verificacion.md`: marcar qué quedó verificado en estos 5 sprints y qué sigue pendiente para los siguientes (feedback de PYMEs reales, fuentes de pago no accesibles, etc.).

### Tesis
- Capítulo 6 (primer borrador):
  - 6.1 Interpretación de los resultados: con las métricas reales obtenidas.
  - 6.2 Sobre el sistema: rendimiento, limitaciones observadas durante las pruebas.
  - 6.3 Sobre la metodología: qué tan bien funcionó el ciclo ágil+DSR en la práctica (retrospectiva honesta de los 5 sprints).
  - 6.4 Sobre el diseño de la arquitectura: qué decisiones de 4.1-4.3 se sostuvieron y cuáles habría que ajustar a la luz de los resultados.
- Mantener la Tabla 3.1 como protocolo hasta disponer de comparaciones de terceros ejecutadas bajo las mismas condiciones; los resultados propios del prototipo pertenecen al capítulo 6.

### Entregables
- `tests/results/` con datos crudos de todas las corridas.
- Tabla de métricas reales del prototipo.
- Capítulo 6 en borrador (6.1-6.4) basado 100% en datos propios.
- `notas-verificacion.md` actualizado con estado final de esta fase.

### Criterios de aceptación
- Ninguna cifra atribuida al prototipo en el capítulo 6 proviene de otra herramienta; todas deben proceder de corridas crudas identificables.
- Las métricas están respaldadas por los archivos crudos en `tests/results/`, trazables.
- Queda explícito qué falta para cerrar la tesis (validación con PYMEs reales, Conclusiones/Recomendaciones/Trabajos futuros/Anexos) como trabajo posterior a estos 5 sprints.

---

## Sprint 6 — Cierre de resultados y trazabilidad

- Auditar que cada cifra del capítulo 6 se pueda recalcular desde `tests/results/`, con configuración, versiones, comandos, verdad de referencia y fórmula. Distinguir casos simulados de validación con aplicaciones reales.
- Relacionar cada resultado y limitación con objetivos 1.4.2, requisitos 5.1.4 y módulos 5.2.3. Corregir las afirmaciones de capítulos 1 a 5 que los resultados contradigan.
- Cierre: ningún resultado sin dato crudo ni ningún objetivo declarado validado sin prueba pertinente.

## Sprint 7 — Conclusiones, recomendaciones y anexos

- Redactar una conclusión por objetivo, limitada a los resultados medidos; recomendaciones vinculadas con limitaciones observadas; trabajos futuros concretos.
- Preparar anexos con instrucciones reproducibles, instrumentos, configuración, tablas completas y evidencias. Si se consigue participación voluntaria de PYMEs, registrar consentimiento, protocolo y datos sin atribuirla retroactivamente a pruebas Docker.
- Cierre: trazabilidad comprobada de objetivos a evidencia y anexos suficientes para repetir el experimento.

## Sprint 8 — Preliminares y Word final

- Completar resumen, índices, figuras, tablas, referencias cruzadas y bibliografía final. Confirmar el formato institucional vigente con el tesista si difiere de la plantilla FISI disponible.
- Exportar a Word siguiendo `docs/Estructura de TESIS (1).docx`, renderizar e inspeccionar todas las páginas; corregir numeración, cortes y tablas.
- Cierre: documento íntegro y revisión visual página por página. El contenido sigue siendo borrador hasta la revisión final del tesista; firmas y validación institucional requieren su intervención.
