"""Fixtures de HTML/headers/cookies simulados por CMS, usados para probar el
modulo recon/cms sin depender de contenedores Docker reales. Estructura
inspirada en instalaciones limpias reales de cada CMS (meta generator, rutas
tipicas de assets, cookies de sesion)."""

WORDPRESS_HTML = """
<!DOCTYPE html>
<html lang="es-PE">
<head>
<meta name="generator" content="WordPress 6.4" />
<link rel="stylesheet" href="/wp-content/themes/twentytwentyfour/style.css" />
<script src="/wp-content/plugins/akismet/akismet.js"></script>
<script src="/wp-includes/js/jquery/jquery.min.js"></script>
</head>
<body>
<h1>Bienvenido a WordPress</h1>
</body>
</html>
"""
WORDPRESS_HEADERS = {"Server": "Apache/2.4.58", "Link": '<http://localhost:8081/wp-json/>; rel="https://api.w.org/"'}
WORDPRESS_COOKIES = {"wordpress_test_cookie": "WP+Cookie+check"}

JOOMLA_HTML = """
<!DOCTYPE html>
<html lang="es-pe">
<head>
<meta name="generator" content="Joomla! - Open Source Content Management - Version 4.4" />
<link rel="stylesheet" href="/media/jui/css/bootstrap.min.css" />
</head>
<body>
<h1>Bienvenido a Joomla</h1>
<a href="/administrator/">Admin</a>
</body>
</html>
"""
JOOMLA_HEADERS = {"Server": "Apache/2.4.58"}
JOOMLA_COOKIES = {"joomla_user_state": "logged_out"}

LARAVEL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head><title>Laravel</title></head>
<body class="antialiased">
<div class="min-h-screen bg-white">Laravel</div>
</body>
</html>
"""
LARAVEL_HEADERS = {"Server": "Apache/2.4.58", "X-Powered-By": "PHP/8.2.0"}
LARAVEL_COOKIES = {"laravel_session": "eyJpdiI6IIn0%3D", "XSRF-TOKEN": "eyJpdiI6IIn0%3D"}

UNKNOWN_HTML = "<html><head><title>Sitio generico</title></head><body>Hola</body></html>"
UNKNOWN_HEADERS = {"Server": "nginx"}
UNKNOWN_COOKIES = {}
