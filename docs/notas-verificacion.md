# Notas de verificación

Registro de toda afirmación académica (cita, DOI, estadística) que entra a `tesis.md`, con su estado de verificación. Regla: nada entra al cuerpo de la tesis como definitivo sin pasar primero por esta tabla.

**Método de verificación de DOIs:** resolución directa contra la API de Crossref (`api.crossref.org/works/<doi>`) y, para libros/arXiv, búsqueda directa en el sitio de la editorial o en arxiv.org. No se acepta un DOI como válido solo porque "suena" a la revista correcta — se compara título/autor/año reales devueltos por Crossref contra lo citado.

**Última auditoría completa:** 2026-07-14 (Sprint 1).

---

## 1. Auditoría de citas de Capítulo 2-3 (hallazgo principal del Sprint 1)

Al verificar los 8 DOIs presentes en `tesis.md` (5 en "Artículos científicos relevantes" + 3 adicionales en "Referencias bibliográficas" con DOI distinto para el mismo autor/año), **ninguno de los 8 apuntaba al paper que el documento decía citar.** Detalle:

| # | DOI | Atribución original en tesis.md | Lo que Crossref devuelve realmente | Estado |
|---|---|---|---|---|
| 1 | `10.26634/jse.17.4.19813` | Abraham et al., 2020 | Abualese, H. & Al-Rousan, T. (2023) — mismo título | ⚠️ Autor/año equivocado, título correcto |
| 2 | `10.1109/ICACCI.2018.8554823` | Anupama & Venkataramani, 2018 (SQLi pattern matching) | Tomar, N. & Matam, R. (2018) — "Optimal Query-Processing-Node Discovery in IoT-Fog Computing" — sin relación | ❌ Cita sin paper real detrás |
| 3 | `10.59934/jaiea.v4i3.1029` | Prasad et al., 2021 | Syarifudin, M., Widyawati, L., Asroni, O. (2025) — mismo título | ⚠️ Autor/año equivocado, título correcto |
| 4 | `10.1002/spe.2870` | Egele et al., 2019 | Amankwah, R., Chen, J., Kudjo, P.K., Towey, D. (2020) — mismo título | ⚠️ Autor/año equivocado, título correcto |
| 5 | `10.1007/978-981-16-2594-7_34` | Jain & Gupta, 2020 ("Analyzing Security Testing Tools...") | Aljebry, A.F., Alqahtani, Y.M., Sulaiman, N. (2022) — mismo título | ⚠️ Autor/año equivocado, título correcto |
| 6 | `10.1109/ACCESS.2020.2970910` | Abraham, S., & Cheng, Y. (2020), IEEE Access | **No existe** — doi.org devuelve 404 | ❌ DOI inexistente |
| 7 | `10.1109/ICACCS51430.2021.9441920` | Prasad, Verma, Sinha (2021) | Magadum et al. — "Optimal Placement of Multiple STATCOM..." — sin relación | ❌ Cita sin paper real detrás |
| 8 | `10.1109/ICCMC48092.2020.ICCMC-00045` | Jain, A., & Gupta, R. (2020), "Modular Architecture..." | Subbulakshmi et al. — "Methodologies for selection of Quality Web Services..." — sin relación | ❌ Cita sin paper real detrás |

Búsquedas adicionales por autor+tema (no solo por DOI) confirmaron que no existe ningún paper real de "Anupama & Venkataramani" sobre SQLi, ni de "Jain & Gupta" sobre arquitectura modular, bajo esos nombres exactos.

**Interpretación:** los 5 títulos del listado "Artículos científicos relevantes" sí corresponden a papers reales y verificables — el error fue de autor/año, no de tema. Las 3 entradas adicionales de "Referencias bibliográficas" (#6, #7, #8) son duplicados fallidos sin correspondencia real y se recomienda eliminarlas en vez de reemplazarlas.

**Resolución aplicada en tesis.md (Sprint 1):**

| Cita final usada en tesis.md | Verificada |
|---|---|
| Abualese, H., & Al-Rousan, T. (2023). *A comparative study of web application security scanners for vulnerability detection.* i-manager's J. on Software Engineering, 17(4). DOI: 10.26634/jse.17.4.19813 | ✅ Sí — Crossref |
| Prabakar, M.A., Karthikeyan, M., & Marimuthu, K. (2013). *An efficient technique for preventing SQL injection attack using pattern matching algorithm.* IEEE ICECCN. DOI: 10.1109/ICE-CCN.2013.6528551 | ✅ Sí — Crossref |
| Syarifudin, M., Widyawati, L., & Asroni, O. (2025). *Web Security Vulnerability Analysis and Mitigation Based on OWASP TOP 10.* JAIEA, 4(3). DOI: 10.59934/jaiea.v4i3.1029 | ✅ Sí — Crossref |
| Amankwah, R., Chen, J., Kudjo, P.K., & Towey, D. (2020). *An empirical comparison of commercial and open-source web vulnerability scanners.* Software: Practice and Experience. DOI: 10.1002/spe.2870 | ✅ Sí — Crossref |
| Aljebry, A.F., Alqahtani, Y.M., & Sulaiman, N. (2022). *Analyzing Security Testing Tools for Web Applications.* Advances in Intelligent Systems and Computing. DOI: 10.1007/978-981-16-2594-7_34 | ✅ Sí — Crossref |
| OWASP Foundation (2021). *OWASP Top 10.* | ✅ Sí — fuente oficial |
| Grimes, R. A. (2017). *Hacking the Hacker.* Wiley. ISBN 9781119396215 | ✅ Sí — confirmado en Wiley/Amazon/Goodreads |

**Eliminado del documento (sin sustituto encontrado):**
- Kumar, M. (2019). *Web Application Security: Exploitation and Countermeasures for Cross-Site Scripting.* Packt Publishing — no se encontró rastro de este libro en Packt, Google Books ni librerías. Se usaba en 2.2.2, 2.6, 3.1 y 3.4 para sustentar la técnica de fingerprinting pasivo; esas menciones se reescribieron para apoyarse en Aljebry et al. (2022) o quedaron marcadas ⚠️ como afirmación propia del tesista (no atribuida a una fuente externa) hasta encontrar un sustituto real.
- Egele, Scholte, Kirda, Kruegel (2019), "An Empirical Analysis of False Positives...", ACM TWEB (sin DOI) — no se encontró este paper; el argumento de falsos positivos ahora se apoya en Amankwah et al. (2020).
- Las 3 entradas duplicadas de "Referencias bibliográficas" (DOIs #6, #7, #8 de la tabla de arriba).

---

## 2. Estadísticas y datos de contexto (Capítulo 1-2)

| Afirmación | Fuente citada | Verificada | Enlace / nota |
|---|---|---|---|
| Perú registró +45,500 millones de intentos de ciberataque en 2024 | Fortinet / Franz Erni (country manager Fortinet Perú) | ⚠️ Solo fuente secundaria | [Diario Ahora](https://ahora.com.pe/economia/ciberataques-en-peru-mas-de-45-mil-millones-de-intentos-en-2024-segun-fortinet), [Gestión](https://gestion.pe/economia/empresas/ciberseguridad-intentos-de-ciberataques-en-peru-se-multiplicaron-por-9-que-empresas-estan-en-la-mira-noticia/); no prueba incidentes en PYMEs ni vulnerabilidades web. Retirado del argumento principal. |
| 88% de PYMEs peruanas reconoce necesidad urgente de reforzar protección | Movistar Empresas, Sondeo de Adopción Digital 2023 | ⚠️ Solo fuente secundaria | Cobertura de prensa; falta informe e instrumento original. Retirado como evidencia del problema. |
| 36% de PYMEs ya fue víctima de ciberataques en el año previo | Movistar Empresas 2023 | ⚠️ No confirmado en esta pasada | Pendiente: rastrear el sondeo original completo (no solo notas de prensa) |
| Crecimiento 300% en sitios WordPress/Joomla/Laravel 2020-2024 | "OSIPTEL, 2024" | ❌ Muy probablemente incorrecto | OSIPTEL es el regulador de telecomunicaciones del Perú; no publica estadísticas de adopción de CMS. No se encontró ningún reporte de OSIPTEL con este dato. **Recomendado: eliminar o buscar fuente real (p. ej. W3Techs, BuiltWith) antes de la versión final.** |
| 89% de PYMEs opera sin análisis periódico de vulnerabilidades / 67% desconoce OWASP Top 10 | "INEI, 2023" | ⚠️ No verificado | INEI es el instituto de estadística; no se confirmó que publique esta cifra específica sobre OWASP. Pendiente de rastreo directo en inei.gob.pe. |
| 45% de incidentes reportados a CERT-Perú son SQLi/XSS | "CERT-Perú, 2023" | ❌ No encontrado | La búsqueda solo devolvió resultados de CERT-Paraguay y CERT-Brasil, nada de CERT-PE. Pendiente de verificación directa en gob.pe/cert-pe o descartar la cifra. |
| SQLi con prevalencia 23% en aplicaciones web | OWASP, 2021 | ⚠️ Pendiente | El Top 10 2021 oficial reporta datos de prevalencia agregados para A03 (94% de apps testeadas, incidencia máxima 19%, promedio 3.37%), no un "23%" aislado para SQLi. Revisar contra el documento oficial antes de citar el número exacto. |
| 34% de sitios WordPress con fallas de autenticación / 41% de instalaciones Joomla con misconfiguration | (sin fuente explícita en el documento) | ❌ Sin fuente | No hay cita asociada a estos dos números en el texto actual. Pendiente: encontrar fuente real o quitar la cifra y dejar la afirmación cualitativa. |

---

## 3. Clasificación OWASP (Capítulo 2, glosario)

| Afirmación | Verificada | Corrección aplicada |
|---|---|---|
| SQL Injection clasificada como "A01" en OWASP Top 10 2021 (glosario 2.3) | ❌ Incorrecto | Confirmado en [owasp.org/Top10/2021/A03_2021-Injection](https://owasp.org/Top10/2021/A03_2021-Injection/): **A03:2021 – Injection** incluye SQLi (CWE-89), XSS (CWE-79/80) y otras inyecciones. Corregido en el glosario y en el cuerpo del texto. |

---

## 4. Pendientes abiertos para sprints posteriores

- [ ] Confirmar cifra real del 36% de víctimas de ciberataque (Movistar 2023) contra el informe completo, no solo prensa.
- [ ] Encontrar fuente real para el crecimiento de CMS en Perú, o retirar la cifra de OSIPTEL.
- [ ] Verificar directamente en inei.gob.pe si existe la estadística atribuida al INEI 2023.
- [ ] Verificar directamente en el sitio de CERT-Perú si existe un reporte 2023 con desagregado SQLi/XSS.
- [ ] Buscar sustituto real para la técnica de fingerprinting pasivo antes atribuida a Kumar (2019).
- [x] Se retiraron del manuscrito las cifras no verificadas de la antigua Tabla 2.1/3.1. Una comparación futura requerirá versiones, configuración y datos crudos propios o fuentes primarias que permitan comparar condiciones.

---

## 5. Auditoría iterativa del 2026-10-13

| Fuente primaria o dato | Enlace / archivo | Afirmación que sí respalda | Estado y límite |
|---|---|---|---|
| OWASP Top 10:2021, A03 Injection | https://top10.owasp.org/2021/A03_2021-Injection/ | A03 incluye CWE-79 (XSS) y CWE-89 (SQLi); la tabla oficial consigna 19,09% de incidencia máxima, 3,37% promedio y 94,04% de cobertura máxima para el conjunto de inyecciones | ✅ Página primaria consultada. No son prevalencias específicas de SQLi, XSS, WordPress ni PYMEs peruanas. |
| OWASP WSTG v4.2 | https://wstg.owasp.org/v4.2/ y https://wstg.owasp.org/downloads/ | Existe una versión 4.2 publicada el 3 de diciembre de 2020 que puede usarse como marco para diseñar pruebas web | ✅ Sitio oficial consultado. Corrige la atribución imprecisa «Testing Guide v4 (OWASP, 2021)». No verifica que los algoritmos particulares del prototipo sigan cada caso WSTG. |
| Peffers et al. (2007), *A Design Science Research Methodology for Information Systems Research* | https://zhang.ist.psu.edu/teaching/504/readings/Peffers.pdf ; DOI 10.2753/MIS0742-1222240302 | El artículo original presenta seis actividades nominales: problema, objetivos, diseño y desarrollo, demostración, evaluación y comunicación (pp. 52–56) | ✅ Texto primario consultado; respalda el marco metodológico de 3.5. No demuestra por sí mismo relevancia empírica para PYMEs ni valida el prototipo. |
| Fortinet y Movistar, cifras del contexto peruano | Enlaces secundarios de la sección 2 | La prensa atribuye cifras a esas organizaciones | ⚠️ Falta publicación primaria e instrumento; las cifras no se usan para inferir situación de PYMEs ni justificar el diseño. |
| Metadatos de cinco artículos con DOI | Sección 1 y `docs/referencias.bib` | Identidad bibliográfica de los trabajos | ⚠️ En el corte inicial no demostraban aportes concretos, Aho-Corasick, arquitectura de plugins ni validación en dos fases. La lectura posterior se detalla más abajo. |
| Línea base antes de la unidad técnica 2 | `src/scanner/`, `tests/`; `.venv/Scripts/python.exe -m pytest -q` | En ese corte solo había reconocimiento y perfilado parcial; 9 tests pasaron y 4 se omitieron | ✅ Verificación histórica del 2026-10-13. El estado actualizado está en el párrafo siguiente. |

**Unidad técnica 2 (2026-10-13):** el CLI ya ejecuta una GET inicial y módulos seleccionables de reconocimiento, perfilado, XSS reflejado indicativo, SQLi por errores indicativa y cabeceras. Produce texto o JSON; limita cada respuesta a 1 MB, no sigue redirecciones y solo prueba hasta diez parámetros GET existentes. `tests/test_scan_local.py` usa un servidor efímero en `127.0.0.1` con casos positivos y negativos conocidos. Comando `.venv/Scripts/python.exe -m pytest --cov=scanner --cov-report=term-missing -q`: **15 passed, 4 skipped, cobertura total 90%**, Python 3.12.0. Esta evidencia valida integración local, no sensibilidad, precisión o usabilidad en WordPress, Joomla, Laravel desplegados o PYMEs reales. Las cuatro omisiones se deben a servicios Docker no activos.

**Unidad editorial 1:** se creó `docs/matriz-brechas.md`, se corrigió el plan para no citar obras descartadas, se normalizó el índice FISI y se retiraron del argumento principal números sin fuente primaria y tablas comparativas sin protocolo. La bibliografía añade WSTG v4.2. La afirmación de que el capítulo 6 estaba pendiente corresponde al corte anterior al experimento Docker.

**Unidad experimental 3 (2026-10-13):** se levantaron WordPress 6.4, Joomla 4 y Laravel 12 en Docker Compose, con MariaDB 10.11 y puertos vinculados a `127.0.0.1`. Cada contenedor sirvió un mismo endpoint PHP positivo y uno negativo; por ello, las tres instalaciones no son tres vulnerabilidades independientes. El PHP positivo refleja `q` sin escape y concatena `q` en una consulta `SELECT 1` real; el negativo escapa HTML, parametriza la consulta y envía tres protecciones de cabecera. Los archivos `docker/lab/scanner_case.php`, `docker/*/docker-compose.yml`, `tests/experiment/README.md` y `tests/results/20261013T191303Z/manifest.json` documentan implementación, versiones, parámetros, etiquetas y regla de mayoría. Los identificadores de imagen están en `docker-images.txt`.

Las **45 corridas crudas** (9 casos × 5 repeticiones) están en `tests/results/20261013T191303Z/runs.jsonl`; `summary.json` se recalcula con `.venv/Scripts/python.exe tests/experiment/analyze_docker.py tests/results/20261013T191303Z --output resumen-recalculado.json`. El análisis por caso y código dio **15 VP, 0 FP, 15 VN, 0 FN**; precisión, recall y exactitud de **1,00 solo para ese banco construido**. Los tres CMS se reconocieron en sus páginas principales. En 30 procesos de seguridad, la duración interna mediana fue 0,0309 s y el pico de memoria mediano 30,26 MiB; los máximos fueron 0,0952 s y 30,43 MiB. En 15 procesos de reconocimiento, mediana 0,0558 s y 30,46 MiB, máximos 0,1541 s y 30,70 MiB. Los tiempos internos excluyen arranque de Python. El anexo D de `docs/tesis.md` enumera las 45 corridas; `tests/experiment/export_annex.py` regenera esa tabla a partir del JSONL. La suite final en `pruebas.txt` fue **19 passed, 92% de cobertura, sin omisiones**, Python 3.12.0. Estas mediciones no prueban eficacia en aplicaciones de PYMEs, usabilidad, costo de hosting ni cobertura de fallas fuera del mecanismo diseñado.

`tests/results/20261013T191200Z` registra un intento abortado antes de recolectar datos por una codificación de consola y `20261013T191209Z` una corrida piloto anterior a la ejecución completa de módulos. Ambas carpetas se conservaron con `incidencia.md` y se excluyeron del capítulo 6. La versión inicial de Laravel 9 no se construyó porque Composer rechazó dependencias bajo sus avisos de seguridad; se usó Laravel 12 con PHP 8.2, según las [notas oficiales de Laravel 12](https://laravel.com/framework/docs/12.x/releases). La nueva elección no altera el alcance de reconocimiento de Laravel, pero debe quedar explícita al comparar con el plan antiguo.

**Unidad bibliográfica 4 (2026-10-13):** se volvió a las fuentes primarias disponibles, separando artículo completo de resumen editorial:

| Trabajo | Fuente y afirmación comprobada | Límite |
|---|---|---|
| Amankwah et al. (2020) | [Manuscrito completo difundido por un coautor](https://www.researchgate.net/profile/Dave-Towey/publication/342683707_An_empirical_comparison_of_commercial_and_open-source_web_vulnerability_scanners/links/5f1c3f9392851cd5fa4551dc/An-empirical-comparison-of-commercial-and-open-source-web-vulnerability-scanners.pdf), resumen y secciones de método/discusión: compara ocho escáneres en WebGoat y DVWA con precisión, recall, índice de Youden y otros criterios. | El PDF es versión de autor; no se transcriben cifras de terceros al capítulo 6 ni se extrapola a PYMEs. |
| Abualese y Al-Rousan (2023) | [Resumen de la editorial](https://www.imanagerpublications.com/article/19813/): seis escáneres, dos aplicaciones vulnerables, dimensiones de exactitud, precisión, recall y tipos detectados. | Texto completo restringido; no se atribuyen resultados específicos. |
| Syarifudin et al. (2025) | [Resumen de la revista](https://www.ioinformatic.org/index.php/JAIEA/article/view/1029): caso de institución XYZ y hallazgos de configuración, componentes y autenticación. | No es estudio de PYMEs peruanas; el enlace de PDF de la revista no abrió en esta revisión, por lo que solo se usa el resumen. |
| Aljebry et al. (2022) | [Resumen de Springer](https://link.springer.com/chapter/10.1007/978-981-16-2594-7_34): compara ZAP y Acunetix en un sitio de prueba. | Texto completo sujeto a suscripción. No respalda arquitectura de plugins, fingerprinting de CMS ni reducción del 60% de falsos positivos. |
| Prabakar et al. (2013) | DOI 10.1109/ICE-CCN.2013.6528551 y título comprobados en el registro bibliográfico previo. | No se obtuvo el texto de IEEE; no se atribuye Aho-Corasick, método ni resultados concretos. |

La subsección 3.4 de `docs/tesis.md` se reescribió según estas lecturas. Las citas antiguas descartadas en la sección 1 permanecen descartadas.

**Unidad editorial 5: Word y revisión visual (2026-10-13).** `docs/build_word.py` generó `docs/tesis-borrador-2026-10-13.docx` a partir de una copia de la plantilla `docs/Estructura de TESIS (1).docx`, cuyo SHA-256 sigue siendo `A2156A3612050420FB260EBB3F2EA66D592DE353607C16E0F37924EB8D04BE00`. Se exportó el Word con LibreOffice a `docs/qa/render10/tesis-borrador-2026-10-13.pdf` y se renderizaron las **35 páginas** en `docs/qa/render10/pages/`. Se inspeccionaron las 35 miniaturas, además de las páginas 4, 28, 33, 34 y 35 a mayor tamaño. El índice general y los índices de tablas y figuras coinciden con esa paginación. La tabla de 45 corridas ocupa las páginas 34–35, con encabezado repetido y filas sin división; no se observaron cortes de texto ni páginas vacías. La compresión de 6.2–6.4 cambió solo la redacción, sin alterar cifras ni límites. Los índices de esta versión son texto estático y deberán actualizarse si cambia la paginación. El documento permanece como **borrador para revisión**, no como versión institucional aprobada: faltan dedicatoria, agradecimientos, confirmación de portada/norma vigente y revisión del tesista y la asesoría. Las mediciones de campo o con usuarios siguen sin realizarse.

**Unidad bibliográfica 6: contexto peruano primario (2026-10-13).** Se consultó el [informe original del INEI publicado en julio de 2022](https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1906/libro.pdf), *Perú: Tecnologías de Información y Comunicación en las Empresas, 2019*. La presentación (p. 3) indica que usa el módulo TIC de la Encuesta Económica Anual 2020, ejercicio 2019, para empresas privadas con ventas superiores a 150 UIT. En la sección 2.1.4.2 (p. 42), el gráfico 2.19 consigna sitio web o presencia en uno para 24,3% de pequeñas empresas y 43,4% de medianas. Se añadió la referencia al capítulo 1 y al contexto de 2.2.1, con año de datos y población explícitos. **No** mide seguridad, vulnerabilidades, CMS ni la situación actual de todas las PYMEs; no sustituye la validación de campo. El informe 2023 publicado por INEI en 2026 se localizó, pero no se extrajeron cifras de él; no se lo cita como sustento numérico.

## Revisión integral para tutor (2026-10-13)

1. Se compararon las versiones originales `(2).docx` y `(3).docx` con `docs/tesis.md`. Ambas conservan título con «evaluación comparativa», promesa de facilidad de uso, operación en hosting compartido y posible validación con PYMEs. Ninguna contiene corridas comparables ni entrevistas documentadas. Sus cifras de ciberataques, precios, adopción de CMS y desempeño de terceros se mantuvieron descartadas según la auditoría anterior; la historia queda aquí y en `docs/informe-revision-tutor.md`, no en el argumento principal.
2. Fuentes primarias revisadas para la versión del tutor: [OWASP WSTG-INPV-01](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting/), [WSTG-INPV-05](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection/) y [A03:2021](https://top10.owasp.org/2021/A03_2021-Injection/) respaldan la clasificación y la necesidad de examinar el contexto. [Abualese y Al-Rousan](https://www.imanagerpublications.com/article/19813) verifica título, autores, año, pp. 1–8 y contenido del resumen; [Syarifudin et al.](https://www.ioinformatic.org/index.php/JAIEA/article/view/1029) verifica pp. 1829–1834 y resumen; [Aljebry et al.](https://link.springer.com/chapter/10.1007/978-981-16-2594-7_34) verifica pp. 411–419, volumen 1387, año de cita 2022 y resumen; [Wiley](https://onlinelibrary.wiley.com/doi/10.1002/spe.2870) verifica pp. 1842–1857 y síntesis de ocho escáneres, contrastada con el manuscrito completo difundido por coautor. Los DOI identifican obras; solo se atribuye contenido disponible. Prabakar (solo metadatos) y Grimes (no citado) se eliminaron de la bibliografía activa.
3. `tests/results/20261013T191303Z/summary.json` coincidió exactamente con un recálculo desde `runs.jsonl` (`docs/qa/tutor-recalculo-original.json`). La nueva corrida Docker `20261013T203602Z` usa el escáner tras restringir XSS a HTML: 45 procesos, 15 VP, 15 VN, 0 FP y 0 FN en señales diseñadas; los tres CMS comparten el mismo PHP. Sus métricas de recursos y hashes están en el manifiesto y resumen nuevos. No se equiparan despliegues con mecanismos independientes.
4. El banco adicional `20261013T203541Z-independent` contiene siete rutas × cinco repeticiones, con verdad de referencia derivada de `run_independent.py`. `analyze_independent.py` reprodujo exactamente `summary.json`: 2 VP, 1 FP, 10 VN y 1 FN frente a vulnerabilidad de código; precisión y recall 2/3. El falso positivo SQL proviene de un texto que imita una excepción sin ejecutar SQLite; el falso negativo, de SQL concatenado cuyo error se oculta. Las medianas fueron 0,4307 s de pared, 0,0269 s internos y 30,21 MiB de pico. Los pilotos `203317Z`, `203358Z` y `203505Z` conservan `incidencia.md` y no se usan en la tesis. La suite final aprobó 20 pruebas con 92 % de cobertura.
5. No existe ejecutable local ni imagen Docker local de OWASP ZAP o Nikto. No se ejecutó escaneo de referencia. El protocolo de la tabla 3.1 y del anexo E fija los datos necesarios si el tutor conserva el título comparativo. El título recomendado para la evidencia presente omite esa promesa sin borrar su origen. La pertinencia para PYMEs y el costo total siguen sin datos de participantes.
6. Se localizó una [directiva general UNMSM de 2020](https://viceacademico.unmsm.edu.pe/wp-content/uploads/2020/09/Directiva-General-para-trabajo-de-investigaci%C3%B3n-para-Bachiller-tesis-o-trabajo-de-suficiencia-para-t%C3%ADtulo-profesional.-RR-N%C2%BA-00744-R-20-del-18-de-febrero-del-2020..pdf) y la [guía de pregrado 2025](https://viceacademico.unmsm.edu.pe/wp-content/uploads/2025/04/Gu%C3%ADa-del-estudiante-de-pregrado-2025_Digital.pdf), que la enumera. No se obtuvo de una página oficial una pauta FISI vigente de maquetación que permita sustituir la plantilla local `Estructura de TESIS (1).docx`; se pide al tutor confirmar solo ese punto para la etapa institucional.
7. La suite final se repitió con `.venv/Scripts/python.exe -m pytest --cov=scanner --cov-report=term-missing -q` y se guardó en `tests/results/20261013T203602Z/pruebas.txt`: **20 passed, 92 %**, ninguna omisión. `docs/tesis-para-tutor.docx` se reconstruyó desde `docs/tesis.md` con `docs/build_word.py --output docs/tesis-para-tutor.docx --toc-pages docs/qa/toc-pages-tutor.json`; LibreOffice exportó `docs/tesis-para-tutor.pdf`. El PDF final tiene 35 páginas. Se renderizaron y examinaron **las 35 páginas completas** a 144 ppp; `docs/qa/tutor-final/revision-visual.md` registra intervalos, índice y continuaciones de tablas. No se observaron páginas vacías, texto fuera de margen ni filas cortadas. La portada y la pauta FISI específica requieren confirmación institucional para una entrega distinta de la lectura del tutor.
