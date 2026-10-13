# Guía de instalación del escáner y despliegue del laboratorio local

Esta guía usa **Windows PowerShell** desde la raíz del repositorio. El escáner es una aplicación de línea de comandos que corre en el equipo del operador; no tiene servidor web propio ni necesita instalarse dentro de WordPress, Joomla o Laravel. Los tres sitios Docker son **objetivos de prueba locales**, con endpoints deliberadamente inseguros. Sus credenciales son de laboratorio y sus puertos se publican solo en `127.0.0.1`; no expongas este laboratorio a Internet.

## 1. Preparar el equipo

Necesitas Python **3.12** (versión usada en la evaluación), `pip`, Docker Engine/Desktop en ejecución y Docker Compose. El primer `pip install`, la descarga de imágenes y la construcción de Laravel requieren acceso a Internet. Comprueba las herramientas:

```powershell
py -3.12 --version
docker info
docker compose version
```

Los puertos locales **8081**, **8082** y **8083** deben estar libres. Si ya tienes este repositorio, abre PowerShell en su carpeta raíz. En una copia nueva:

```powershell
git clone https://github.com/Mr8Rob8/TESIS-PALACIOS.git
Set-Location .\TESIS-PALACIOS
```

## 2. Instalar y comprobar el escáner

Desde la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m scanner --version
.\.venv\Scripts\python.exe -m scanner --help
```

`pip install -e .` instala el paquete y sus dependencias desde `pyproject.toml`; los cambios posteriores en `src/scanner/` se reflejan sin reinstalar. Para ejecutar las pruebas automatizadas instala además sus dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install "pytest>=8,<10" "pytest-cov>=4,<8"
```

Si ya existe `.venv`, usa el entorno actual y omite la creación. Si `py -3.12` no existe, instala Python 3.12 o usa el ejecutable de Python 3.12 disponible; la compatibilidad con otras versiones no forma parte de la evaluación publicada.

## 3. Levantar WordPress, Joomla y Laravel de prueba

Estos comandos pueden ejecutarse desde la raíz, sin cambiar de carpeta. El tercer comando construye la imagen Laravel y puede tardar varios minutos la primera vez:

```powershell
docker compose -f .\docker\wordpress\docker-compose.yml up -d
docker compose -f .\docker\joomla\docker-compose.yml up -d
docker compose -f .\docker\laravel\docker-compose.yml up -d --build
```

Las bases MariaDB y los sitios se levantan en proyectos Compose separados. **No uses `down -v`** si deseas conservar la instalación y los datos de laboratorio. Espera a que los sitios respondan y completa WordPress con el instalador reproducible del repositorio; el script no modifica una instalación que ya responde:

```powershell
.\.venv\Scripts\python.exe tests\experiment\install_wordpress.py
```

Joomla se configura mediante las variables del `docker-compose.yml`; Laravel se construye desde `docker/laravel/Dockerfile` y ejecuta su inicialización al arrancar. Comprueba los contenedores y las páginas principales:

```powershell
docker compose -f .\docker\wordpress\docker-compose.yml ps
docker compose -f .\docker\joomla\docker-compose.yml ps
docker compose -f .\docker\laravel\docker-compose.yml ps

(Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8081/' -TimeoutSec 10).StatusCode
(Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8082/' -TimeoutSec 10).StatusCode
(Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8083/' -TimeoutSec 10).StatusCode
```

Después de instalar WordPress, las tres páginas principales deben responder **HTTP 200**. Cada sitio expone dos casos locales en el mismo puerto:

| Sitio | Puerto | Caso con señales | Caso de control |
|---|---:|---|---|
| WordPress | 8081 | `/scanner-vulnerable.php?q=hola` | `/scanner-safe.php?q=hola` |
| Joomla | 8082 | `/scanner-vulnerable.php?q=hola` | `/scanner-safe.php?q=hola` |
| Laravel | 8083 | `/scanner-vulnerable.php?q=hola` | `/scanner-safe.php?q=hola` |

Ambas rutas se montan desde **el mismo** `docker/lab/scanner_case.php` en los tres sitios. Son instrumentación para el experimento, no vulnerabilidades propias de los CMS. En cada caso positivo el código refleja `q` sin escape, concatena `q` en una consulta SQL de solo lectura y omite CSP, protección de embebido y `nosniff`. El caso de control codifica HTML, parametriza la consulta y envía esas cabeceras.

## 4. Ejecutar un escaneo de comprobación

La URL debe incluir un parámetro GET existente (`q` en el ejemplo) para que XSS y SQLi puedan sondearlo. Ejecuta el caso positivo y el caso de control:

```powershell
.\.venv\Scripts\python.exe -m scanner 'http://127.0.0.1:8081/scanner-vulnerable.php?q=hola' --format json
.\.venv\Scripts\python.exe -m scanner 'http://127.0.0.1:8081/scanner-safe.php?q=hola' --format json
```

En el laboratorio revisado, la primera salida contiene cinco códigos: `HEADER-CSP`, `HEADER-FRAME`, `HEADER-NOSNIFF`, `XSS-REFLEJO-INDICATIVO` y `SQLI-ERROR-INDICATIVO`. La segunda tiene `"hallazgos": []`. Las alertas XSS/SQLi son **indicios**; el escáner no demuestra explotación en navegador ni extracción de datos. El reconocimiento CMS se comprueba en la página principal, por ejemplo:

```powershell
.\.venv\Scripts\python.exe -m scanner 'http://127.0.0.1:8081/' --modules recon cms --format text
```

Opciones útiles: `--modules recon cms xss sqli headers` selecciona módulos; `--format text` es el valor predeterminado; `--format json` da una salida estructurada; `--timeout 10` fija segundos por petición; `--output RUTA` guarda el reporte. Para no mezclar reportes de prueba con archivos del repositorio:

```powershell
.\.venv\Scripts\python.exe -m scanner 'http://127.0.0.1:8081/scanner-safe.php?q=hola' --format json --output "$env:TEMP\tesis-reporte-local.json"
```

Para analizar un sitio propio o expresamente autorizado, sustituye la URL local por su URL HTTP(S). El escáner solo hace GET sobre la URL indicada y variantes de hasta diez parámetros GET **ya presentes**. No rastrea enlaces, no envía formularios POST, no sigue redirecciones y limita cada respuesta a 1 MB. Una salida sin hallazgos no certifica seguridad. El laboratorio Docker permanece en el equipo local aunque el objetivo del escáner sea otro.

## 5. Ejecutar las pruebas y reproducir las corridas

Con los tres sitios activos, ejecuta la suite:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=scanner --cov-report=term-missing -q
```

En la versión documentada del 13 de octubre de 2026 hubo **20 pruebas aprobadas y 92 % de cobertura**. Si Docker no responde, las cuatro pruebas de integración con CMS se omiten; esa ejecución no equivale a verificar el laboratorio completo.

Para generar **una corrida Docker nueva**, usa un directorio UTC nuevo. El analizador crea `summary.json` a partir de `manifest.json` y `runs.jsonl`:

```powershell
$destino = Join-Path 'tests\results' ((Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ'))
.\.venv\Scripts\python.exe tests\experiment\run_docker.py --repeticiones 5 --destino $destino
.\.venv\Scripts\python.exe tests\experiment\analyze_docker.py $destino --output (Join-Path $destino 'summary.json')
```

El instrumento comprueba los nueve casos antes de crear el directorio. Conserva comandos, horas, salida JSON, hashes de código y configuración; cinco repeticiones por caso dan **45 procesos**, pero no 45 vulnerabilidades independientes. El recálculo histórico puede hacerse sin volver a escanear:

```powershell
.\.venv\Scripts\python.exe tests\experiment\analyze_docker.py 'tests\results\20261013T203602Z' --output "$env:TEMP\tesis-resumen-docker.json"
```

El segundo banco, con siete rutas Python/SQLite en un servidor efímero ligado a `127.0.0.1`, no requiere Docker. Crea su propia carpeta UTC y su `summary.json`:

```powershell
.\.venv\Scripts\python.exe tests\experiment\run_independent.py
```

Las corridas publicadas permanecen en `tests/results/20261013T203602Z/` y `tests/results/20261013T203541Z-independent/`. No las edites ni las reutilices como si fueran corridas nuevas. El banco Docker comparte el PHP entre los tres CMS; el banco Python/SQLite incluye negativos difíciles y documenta un falso positivo y un falso negativo. Consulta `tests/experiment/README.md`, `docs/tesis.md` (capítulo 6) y los manifiestos para interpretar etiquetas, métricas y límites.

## 6. Detener el laboratorio y resolver fallos habituales

Para detener los sitios sin borrar sus volúmenes:

```powershell
docker compose -f .\docker\wordpress\docker-compose.yml stop
docker compose -f .\docker\joomla\docker-compose.yml stop
docker compose -f .\docker\laravel\docker-compose.yml stop
```

| Síntoma | Comprobación y acción |
|---|---|
| `docker info` no conecta | Inicia Docker Desktop/Engine y espera a que termine de arrancar. |
| Puerto 8081–8083 ocupado | Comprueba `Get-NetTCPConnection -LocalPort 8081,8082,8083` y libera el puerto o cambia **juntos** Compose, URLs del experimento y documentación. |
| Un sitio no devuelve 200 | Revisa `docker compose -f .\docker\<cms>\docker-compose.yml ps` y `logs --tail=100`; WordPress puede requerir el instalador del paso 3. |
| La construcción Laravel falla | Revisa `docker compose -f .\docker\laravel\docker-compose.yml logs --tail=100` y la salida de `up -d --build`; necesita descargar dependencias Composer. No desactives controles de seguridad de Composer para forzar la construcción. |
| XSS/SQLi no aparecen en la salida | Usa una URL con `?q=hola`, activa los módulos y comprueba que se trata del endpoint positivo. El detector XSS exige respuesta HTML. |
| El escáner informa una redirección | Proporciona explícitamente la URL final autorizada; el CLI no sigue redirecciones. |
| Las medidas difieren de la tesis | Compara versiones, hashes, configuración, host y método en el manifiesto. El tiempo interno excluye arranque de Python y serialización; el pico de memoria depende del sistema operativo. |

Las contraseñas de `docker/*/docker-compose.yml` y `tests/experiment/install_wordpress.py` son **solo de prueba**. No reutilices esas configuraciones para producción ni ejecutes el banco experimental contra sistemas de terceros.
