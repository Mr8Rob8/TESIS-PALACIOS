# Escáner ligero de seguridad web orientado a PYMEs peruanas

Prototipo de tesis FISI-UNMSM: escáner modular en Python con CLI, reconocimiento de WordPress/Joomla/Laravel, comprobaciones GET indicativas de XSS reflejado y SQLi basada en errores, observación de cabeceras y reportes de texto o JSON. Su evaluación documentada se realizó **en entornos locales controlados**. No se ha comparado con otra herramienta ni validado con PYMEs; costo total, facilidad de uso y funcionamiento en hosting compartido siguen sin evaluar.

## Inicio rápido en Windows PowerShell

Usa Python 3.12 para el escáner; Docker Compose se necesita solo para el laboratorio. La [guía de despliegue](docs/guia-despliegue.md) detalla requisitos, instalación, arranque de los tres CMS, verificación, pruebas, reproducción de resultados y solución de fallos. Desde la raíz:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m scanner --help
```

La guía explica cómo levantar WordPress (`127.0.0.1:8081`), Joomla (`127.0.0.1:8082`) y Laravel (`127.0.0.1:8083`) antes de escanearlos. Los endpoints de seguridad se montan desde un mismo archivo PHP de prueba; no son fallas nativas de esos CMS. Ejecuta el escáner solo contra objetivos propios o expresamente autorizados.

## Archivos principales

| Ruta | Contenido |
|---|---|
| `src/scanner/` | CLI y módulos del escáner |
| `docker/` | Tres entornos locales y endpoint PHP controlado |
| `tests/` | Suite automatizada, instrumentos y datos crudos |
| `docs/tesis.md` | Manuscrito fuente con metodología, resultados y límites |
| `docs/tesis-para-tutor.docx` y `.pdf` | Versión académica para revisión del tutor |
| `docs/informe-revision-tutor.md` | Decisiones metodológicas y estado de la evidencia |

## Alcance comprobado

El CLI recibe una URL HTTP(S), no sigue redirecciones y solo prueba hasta diez parámetros GET existentes; cada respuesta se limita a 1 MB. No recorre un sitio completo ni prueba formularios POST, sesiones autenticadas, XSS almacenado o SQLi ciega. Las alertas son indicios para confirmación humana; la ausencia de alertas no certifica seguridad.

El capítulo 6 conserva por separado el banco Docker revisado (`tests/results/20261013T203602Z/`) y el banco de mecanismos independientes (`tests/results/20261013T203541Z-independent/`). En el entorno documentado, la suite pasó **20 pruebas**, sin omisiones y con **92 % de cobertura de líneas**. Las cifras de detección y recursos corresponden solo a esos casos locales.
