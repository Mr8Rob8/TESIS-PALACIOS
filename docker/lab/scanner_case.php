<?php
/* Banco de prueba local. Solo ejecuta SELECT 1; sin datos reales ni escrituras. */
declare(strict_types=1);

$unsafe = str_contains((string) ($_SERVER['SCRIPT_NAME'] ?? ''), 'vulnerable');
$value = (string) ($_GET['q'] ?? '');
header('Content-Type: text/html; charset=utf-8');
if (!$unsafe) {
    header("Content-Security-Policy: default-src 'self'; frame-ancestors 'none'");
    header('X-Content-Type-Options: nosniff');
}

$shown = $unsafe ? $value : htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$message = '';
try {
    if (class_exists('mysqli')) {
        $db = new mysqli((string) getenv('LAB_DB_HOST'), (string) getenv('LAB_DB_USER'), (string) getenv('LAB_DB_PASSWORD'), (string) getenv('LAB_DB_NAME'));
        if ($unsafe) {
            // Vulnerabilidad deliberada: concatenación en una consulta SELECT sin efectos de escritura.
            $db->query("SELECT 1 WHERE 'fixed' = '" . $value . "'");
        } else {
            $statement = $db->prepare("SELECT 1 WHERE 'fixed' = ?");
            $statement->bind_param('s', $value);
            $statement->execute();
        }
    } else {
        $dsn = sprintf('mysql:host=%s;dbname=%s;charset=utf8mb4', getenv('LAB_DB_HOST'), getenv('LAB_DB_NAME'));
        $db = new PDO($dsn, (string) getenv('LAB_DB_USER'), (string) getenv('LAB_DB_PASSWORD'), [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        if ($unsafe) {
            $db->query("SELECT 1 WHERE 'fixed' = '" . $value . "'");
        } else {
            $statement = $db->prepare("SELECT 1 WHERE 'fixed' = ?");
            $statement->execute([$value]);
        }
    }
} catch (Throwable $error) {
    // El caso inseguro expone un error para la prueba basada en errores.
    $message = $unsafe ? htmlspecialchars($error->getMessage(), ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') : 'Error interno';
}
echo '<!doctype html><html><head><meta charset="utf-8"><title>Laboratorio local</title></head><body>';
echo $shown;
if ($message !== '') {
    echo '<pre>' . $message . '</pre>';
}
echo '</body></html>';
