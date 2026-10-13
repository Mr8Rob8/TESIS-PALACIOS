# Protocolo del experimento Docker local

La unidad de clasificación es el par **caso–código de señal**. Hay dos endpoints de laboratorio dentro de cada contenedor web: `scanner-vulnerable.php` refleja `q` sin codificación, concatena `q` en una consulta `SELECT 1` y omite CSP, protección de embebido y `nosniff`; `scanner-safe.php` codifica HTML, usa una consulta parametrizada y envía las tres cabeceras. Las bases de datos y credenciales son de prueba. El código fuente que establece esta verdad de referencia es `docker/lab/scanner_case.php` y su hash se guarda en cada `manifest.json`.

La página principal de cada contenedor se usa por separado para evaluar reconocimiento de CMS. Esos resultados no se incluyen en VP/FP/VN/FN de seguridad. Los endpoints PHP de laboratorio **no son aplicaciones reales de PYMEs** ni una muestra representativa de vulnerabilidades de WordPress, Joomla o Laravel; solo comprueban el comportamiento del prototipo ante casos conocidos bajo Apache/PHP y MariaDB.

Antes de ejecutar, levantar los tres Compose del repositorio y confirmar que las URLs locales responden. Ejecutar con el Python del entorno del proyecto:

```powershell
.\.venv\Scripts\python.exe tests\experiment\run_docker.py --repeticiones 5
.\.venv\Scripts\python.exe tests\experiment\analyze_docker.py tests\results\<directorio_utc>
```

El número impar de cinco repeticiones se fijó antes de la primera corrida para comprobar estabilidad y describir la variación de duración y memoria con un costo acotado de peticiones. Una decisión por caso y código se obtiene por mayoría estricta de las cinco corridas; se listan los casos inestables. Las repeticiones no se cuentan como observaciones independientes para inflar precisión o recall. Si se quieren intervalos de confianza poblacionales, este diseño no los permite.

`manifest.json` guarda casos, etiquetas, comandos implícitos, versiones de Python y plataforma, método de medición y hashes de fuentes. `runs.jsonl` conserva cada comando, salida JSON completa, stderr, hora y código de salida. `analyze_docker.py` recalcula VP, FP, VN, FN, precisión, recall, exactitud, aciertos de CMS, medianas y extremos. No borrar ni editar corridas originales. El pico de memoria es el *Peak Working Set* del proceso en Windows; la duración excluye arranque de Python y serialización. Ambos dependen de la máquina y no deben extrapolarse a hosting compartido.
