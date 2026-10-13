# Prompt de revisión integral para presentar la tesis al tutor

Copia el texto comprendido entre las líneas horizontales en una sesión del agente con acceso a este repositorio.

---

Continúa el trabajo en `C:\Users\Administrador\Downloads\TESIS`. Necesito una **versión académica sólida para revisión de mi tutor de tesis**, no un informe de avance ni una declaración de que el borrador ya está terminado. Mi tesis original, visible en `docs/tesis-palacios Calle-MT (2).docx` y `(3).docx`, plantea un escáner ligero OWASP dirigido a PYMEs peruanas, modular en Python, con una **evaluación comparativa**. El texto actual de `docs/tesis.md` y `docs/tesis-borrador-2026-10-13.docx` cambió el énfasis hacia un laboratorio local. Necesito recuperar la pregunta, el aporte y la motivación de la tesis original **sin recuperar datos falsos ni afirmar que se validó en PYMEs**.

## Resultado que debes producir

Entrega `docs/tesis-para-tutor.docx` y su PDF de revisión, ambos derivados de un `docs/tesis.md` corregido. Entrega además `docs/informe-revision-tutor.md`, breve y verificable, con cambios sustantivos, matriz de afirmaciones y fuentes, estado de experimentos, decisiones metodológicas y **solo los asuntos que realmente requieren mi decisión o la del tutor**. Conserva los archivos anteriores como versiones históricas. No hagas commit ni push.

## Bucle de trabajo obligatorio

Trabaja en ciclos: **localiza una deficiencia → determina la evidencia necesaria → busca o ejecuta la comprobación → corrige código, datos y texto afectados → verifica la corrección → actualiza la matriz → continúa**. No termines después de hacer una auditoría o una lista de pendientes. Resuelve cada pendiente abordable mediante fuente primaria, prueba reproducible, reformulación sustentada o eliminación justificada. Si algo depende exclusivamente de una decisión mía, márcalo en el informe para el tutor y avanza con todas las demás tareas. No conviertas la falta de una fuente en una frase de relleno dentro de la tesis.

### Ciclo 1: recuperar la identidad de la investigación

Lee íntegramente el proyecto original en Word, la plantilla FISI, `docs/tesis.md`, `docs/matriz-brechas.md`, `docs/notas-verificacion.md`, `docs/referencias.bib`, el código y los resultados. Compara **título, problema, población objetivo, justificación, objetivos, aporte, metodología y promesa de evaluación** entre el proyecto original y el manuscrito actual. Registra cada cambio, su motivo y si cuenta con evidencia. No trates el proyecto original como fuente de cifras: sus afirmaciones externas deben auditarse.

Reescribe título/subtítulo propuestos, resumen, abstract, introducción del problema, justificación, objetivos y conclusiones como un mismo argumento: necesidad concreta que motiva el trabajo; brecha técnica demostrable; artefacto propuesto y aporte propio; método; resultados que sí se obtuvieron; límites; utilidad potencial para PYMEs peruanas pendiente de evaluación directa. El resumen debe ser una síntesis académica con **problema, objetivo, método, resultado y aporte**, no una lista de módulos y cifras. El abstract debe corresponder fielmente al resumen final. Explica con precisión qué significa «ligero», «bajo costo» y «orientado a PYMEs»; mide lo que sea medible y evita dar por demostrada la utilidad para esa población sin participantes.

La frase «evaluación comparativa» aparece en el título original. Comprueba si el trabajo actual tiene una comparación válida con herramientas de referencia ejecutadas bajo el **mismo protocolo y entorno**. Si es viable con recursos locales, diseña y ejecuta una comparación justa, registra versiones, configuración, datos crudos y límites. Si no es viable, no finjas una comparación: presenta al tutor dos opciones concretas de título/objetivos, una que exige la comparación pendiente y otra ajustada a la validación realmente realizada; recomienda una con argumentos y deja la elección explícita para mi revisión. No cambies silenciosamente la promesa central de la tesis.

### Ciclo 2: verificar de extremo a extremo el manuscrito

Audita **cada afirmación factual externa, cita, porcentaje, definición técnica, atribución de método y dato bibliográfico** de capítulos 1–6, tablas, figuras, resumen y conclusiones. Crea una matriz con ubicación exacta, afirmación, fuente primaria, página/sección o dato crudo, alcance de la fuente, veredicto y corrección aplicada. Verifica los DOI contra metadatos editoriales o Crossref y verifica el contenido de la afirmación contra el texto disponible; un DOI correcto por sí solo no prueba una interpretación. Prioriza fuentes oficiales y artículos completos. Distingue artículo completo, resumen editorial, metadatos y fuente secundaria.

Revisa expresamente los marcadores `[PENDIENTE DE VERIFICACIÓN]`, notas editoriales visibles y alusiones a «borradores anteriores» en `docs/tesis.md`. Busca la fuente primaria y comprueba la afirmación; si no existe evidencia suficiente, retira el dato o redacta una afirmación más estrecha que sí tenga respaldo. Guarda la discusión de fuentes descartadas en `docs/notas-verificacion.md`, no en la lectura principal del tutor. Asegura que la bibliografía cite solo obras utilizadas y que cada referencia citada aparezca en la lista con datos correctos. No inventes fuentes, citas textuales, páginas ni cifras de PYMEs peruanas.

### Ciclo 3: poner a prueba la fuerza de la evaluación

Recalcula `tests/results/20261013T191303Z/runs.jsonl` y `summary.json` desde los datos crudos; ejecuta las pruebas pertinentes y comprueba que el código, los contenedores, las etiquetas y el capítulo 6 coinciden. Examina críticamente que los tres CMS usan el **mismo archivo PHP** como caso positivo/negativo: tres despliegues no equivalen a tres mecanismos de vulnerabilidad independientes. Revisa si la precisión y recall de 1,00 solo reflejan casos diseñados para el detector, si los encabezados ausentes son una señal bien definida, y si las mediciones de RAM/tiempo incluyen o excluyen costos relevantes. Corrige el protocolo y amplía casos **independientes y negativos difíciles** si es factible y necesario para sostener las conclusiones. Conserva resultados anteriores y nuevos por separado; nunca reetiquetes corridas viejas como nuevas. Si una prueba no puede ejecutarse, informa la razón exacta y no mantengas cifras sin comprobación.

Revisa la correspondencia entre el objetivo general y cada conclusión. Reduce o reformula cualquier afirmación sobre costo, facilidad de uso, hosting compartido, mitigación, prevalencia o valor para PYMEs que el experimento no evaluó. Mantén explícita la diferencia entre **detectar indicios** de XSS/SQLi y demostrar vulnerabilidades explotables. Si decides que hace falta un estudio con usuarios o PYMEs para sostener el título original, diseña un protocolo concreto para aprobación del tutor, sin inventar participantes ni respuestas.

### Ciclo 4: calidad académica y entrega al tutor

Revisa coherencia, profundidad, redacción y repeticiones de todos los capítulos; fortalece la contribución propia frente al estado del arte y explica por qué la arquitectura y los algoritmos seleccionados responden al problema. Cada tabla y figura debe aportar al argumento, tener título, fuente y mención en el texto. Revisa numeración, citas, índice, referencias cruzadas, anexos y consistencia entre Markdown, Word y PDF. Consulta una norma FISI-UNMSM vigente de fuente oficial si está disponible; registra versión/enlace y aplica sus requisitos comprobables. Si no se obtiene, usa la plantilla local y señala únicamente las diferencias cuya confirmación sea imprescindible.

Genera Word y PDF **después** de corregir el contenido. Renderiza y examina visualmente todas las páginas de la versión final, no solo miniaturas; corrige desbordes, tablas cortadas, páginas vacías e índices estáticos desactualizados. Dedicatoria y agradecimientos pueden quedar reservados para mí si la entrega es solo para revisión del tutor; no los conviertas en obstáculo para producir el documento académico revisable. No afirmes «listo para entrega institucional» sin mi revisión y la del tutor.

## Criterio de cierre

Termina cuando el tutor pueda leer un documento coherente que preserve la idea original, entienda exactamente qué se construyó y evaluó, pueda seguir cada cifra y fuente, y vea con claridad las decisiones científicas aún abiertas. En tu respuesta final indica: archivos entregados; correcciones de fondo; fuentes y experimentos verificados; límites que permanecen; **máximo tres decisiones concretas** que deba discutir con mi tutor. No uses «todo verificado» si alguna afirmación depende solo de un resumen, un dato secundario o una evaluación futura.

Empieza con la comparación entre el proyecto original y el manuscrito actual; completa enseguida la primera corrección sustantiva del problema y del resumen, y continúa los ciclos sin esperar otra instrucción.

---
