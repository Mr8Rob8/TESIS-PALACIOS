from scanner.core.findings import Confianza, HallazgoRecon
from scanner.modules.cms.profiler import perfilar
from tests.fixtures.html_samples import WORDPRESS_HTML


def test_perfilar_wordpress_detecta_plugin_y_tema_visibles():
    hallazgo_recon = HallazgoRecon(
        tecnologia="WordPress",
        version="6.4",
        confianza=Confianza.CONFIRMADO,
        evidencia="meta generator",
        metodo_deteccion="meta generator",
    )

    hallazgo = perfilar(hallazgo_recon, WORDPRESS_HTML)

    assert hallazgo.detalles["plugins_visibles"] == ["akismet"]
    assert hallazgo.detalles["tema_visible"] == "twentytwentyfour"
    # perfilar() no debe alterar los campos ya establecidos por recon
    assert hallazgo.tecnologia == "WordPress"
    assert hallazgo.version == "6.4"


def test_perfilar_no_wordpress_no_agrega_detalles_de_wordpress():
    hallazgo_recon = HallazgoRecon(
        tecnologia="Joomla",
        version="4.4",
        confianza=Confianza.CONFIRMADO,
        evidencia="meta generator",
        metodo_deteccion="meta generator",
    )

    hallazgo = perfilar(hallazgo_recon, "<html></html>")

    assert "plugins_visibles" not in hallazgo.detalles
    assert hallazgo.detalles["componentes_visibles"] == []


def test_perfilar_joomla_extrae_componentes_visibles():
    hallazgo = HallazgoRecon("Joomla", "4.4", Confianza.CONFIRMADO, "meta generator", "meta generator")
    perfil = perfilar(hallazgo, '<link href="/components/com_content/site.css"><link href="/templates/cassiopeia/css/site.css">')
    assert perfil.detalles["componentes_visibles"] == ["com_content"]
    assert perfil.detalles["plantillas_visibles"] == ["cassiopeia"]


def test_perfilar_laravel_no_inventa_version():
    hallazgo = HallazgoRecon("Laravel", None, Confianza.CONFIRMADO, "cookie", "cookie")
    perfil = perfilar(hallazgo, "<html>Laravel</html>")
    assert perfil.version is None
    assert perfil.detalles["version_no_expuesta"] is True
