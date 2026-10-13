# Prompt de trabajo iterativo para culminar la tesis FISI

Copia el texto siguiente en una sesión de un agente con acceso a este repositorio:

---

Actúa como asistente de investigación, editor académico e ingeniero de software para culminar mi tesis de pregrado FISI-UNMSM, titulada provisionalmente **«Desarrollo de un escáner ligero OWASP para aplicaciones web de bajo costo en PYMEs peruanas»**. Trabaja en `C:\Users\Administrador\Downloads\TESIS`. El resultado abarca **el prototipo funcional, la evaluación reproducible y el documento completo**, no solo el código.

## 1. Lee, compara y establece el estado real

Antes de editar, lee `CLAUDE.md`, `README.md`, `docs/tesis.md`, `docs/sprints.md`, `docs/notas-verificacion.md`, `docs/referencias.bib`, `docs/Estructura de TESIS (1).docx`, `docs/tesis-palacios Calle-MT (3).docx`, el código de `src/scanner/` y las pruebas. Revisa también la copia anidada `TESIS/` y comprueba si diverge; no borres ni sobrescribas versiones sin justificación. Considera `docs/tesis.md` como borrador de trabajo y la plantilla FISI como referencia de estructura, sujeto a cualquier norma institucional más reciente que yo proporcione.

Construye una matriz de brechas por apartado con: estado actual, evidencia disponible, trabajo pendiente, archivo de destino y criterio de cierre. Distingue entre texto redactado, texto sustentado, función implementada y función validada. Detecta contradicciones entre el plan, el manuscrito, el código y las notas de verificación. En particular, revisa las citas antiguas que `docs/notas-verificacion.md` descartó y que todavía aparecen en `docs/sprints.md`; no las reutilices como sustento.

Normaliza el índice con la estructura FISI: preliminares; capítulos 1 a 6; conclusiones; recomendaciones; trabajos futuros; referencias; anexos. Corrige la numeración errónea del capítulo 2 (`3.x` en la lista proporcionada debe ser `2.x`), resuelve el apartado 4.4 duplicado y corrige «Defunción de Algoritmos» por «Definición de algoritmos». No inventes una base de datos para cumplir 5.1.3: si el escáner solo usa estructuras o archivos, describe y justifica ese modelo de datos.

## 2. Trabaja en un bucle verificable

Repite este ciclo hasta cumplir los criterios finales:

1. **Diagnostica** la brecha de mayor prioridad que desbloquea otras secciones o pruebas.
2. **Planifica** una unidad pequeña con archivos, evidencia necesaria y criterio de aceptación.
3. **Ejecuta** tanto el cambio técnico como la sección del documento que lo explica. Si el trabajo es solo bibliográfico o editorial, registra igualmente la evidencia y las secciones afectadas.
4. **Verifica** con pruebas pertinentes, lectura crítica y trazabilidad. Para tablas o resultados, conserva los datos crudos, comandos, versiones, configuración y método de cálculo.
5. **Corrige** lo que falle y vuelve a verificar. Actualiza la matriz de brechas y `docs/notas-verificacion.md`.
6. **Informa** brevemente qué quedó hecho, qué evidencia lo respalda y qué sigue. Continúa con la siguiente unidad sin esperar una nueva orden, salvo que falte una decisión o dato que solo yo pueda aportar.

No declares terminado un capítulo porque tenga texto: ciérralo cuando sea coherente con objetivos, método, implementación, resultados y fuentes. No te detengas al terminar los cinco sprints actuales: amplía el plan hasta cubrir conclusiones, recomendaciones, trabajos futuros, anexos y versión final en Word.

## 3. Reglas de rigor académico y técnico

- No inventes citas, DOI, autores, estadísticas, páginas, resultados, entrevistas, pruebas ni aprobación institucional. Una coincidencia de DOI en Crossref confirma metadatos; para apoyar una afirmación concreta, consulta también el contenido de la fuente cuando sea posible. Registra fuente primaria, enlace, afirmación respaldada y estado de verificación. Si no hay evidencia, retira la cifra, reformula como hipótesis explícita o marca `[PENDIENTE DE VERIFICACIÓN]`.
- Separa siempre **metas de diseño**, **resultados medidos** y **resultados de terceros**. La precisión, el recall, los falsos positivos, el consumo de RAM y el tiempo del prototipo solo se calculan a partir de ejecuciones reales reproducibles. No presentes pruebas unitarias con HTML simulado como validación de campo.
- Implementa únicamente el alcance aprobado: reconocimiento y perfilado de WordPress, Joomla y Laravel; XSS reflejado; SQLi no destructiva; cabeceras de seguridad; CLI y reportes. Usa entornos locales controlados para pruebas. No escanees sitios de terceros sin autorización explícita. Registra limitaciones y falsos negativos esperables.
- Mantén correspondencia trazable entre problema, objetivos, requisitos, arquitectura, módulos, experimentos, resultados y conclusiones. Si un objetivo no puede evaluarse, señálalo y propón la prueba faltante.
- Respeta el historial y los archivos del usuario. No hagas commit ni push salvo instrucción expresa. Todo texto académico queda como borrador para mi revisión final; esa revisión no debe impedir que avances en el resto del trabajo.

## 4. Secuencia de cierre

Primero audita y corrige capítulos 1 a 4 y la bibliografía. Después termina e integra el prototipo conforme a los requisitos verificables; documenta arquitectura, casos de uso, modelo de datos, algoritmos, módulos y pruebas en el capítulo 5. Diseña el experimento con casos positivos y negativos conocidos, ejecuta corridas suficientes y conserva resultados crudos; redacta el capítulo 6 exclusivamente con esos datos. Luego redacta conclusiones vinculadas a cada objetivo, recomendaciones derivadas de resultados y limitaciones, trabajos futuros concretos y anexos con instrucciones, instrumentos, configuración, tablas completas y evidencias. Prepara resumen, índices, figuras, tablas, referencias cruzadas y bibliografía final. Exporta a Word siguiendo la plantilla FISI y revisa visualmente todas las páginas para detectar numeración, cortes, tablas o figuras defectuosas.

## 5. Criterios para decir «tesis lista para revisión final»

Todos los apartados exigidos están presentes y numerados; cada afirmación externa importante tiene fuente verificable o está señalada como pendiente; el código ejecuta un escaneo completo local y sus pruebas pertinentes pasan; las métricas del capítulo 6 se pueden recalcular desde datos crudos; las conclusiones responden a los objetivos sin exceder los resultados; bibliografía, citas, figuras y tablas coinciden; el Word final está revisado página por página. Entrega una lista corta y precisa de cualquier dato, firma, validación con PYMEs o decisión institucional que requiera mi intervención. Si alguno falta, informa el estado real y continúa con todo el trabajo independiente posible.

Empieza ahora con el inventario y la matriz de brechas, y realiza la primera unidad de trabajo verificable en esta misma sesión.
