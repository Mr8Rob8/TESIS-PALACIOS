from scanner.cli import build_parser, main
from scanner.core.findings import ResultadoEscaneo


def test_build_parser_requires_no_args():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.target is None


def test_main_without_target_returns_error_and_prints_help(capsys):
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "usage" in captured.out.lower()


def test_main_with_target_runs_ok(capsys, monkeypatch):
    monkeypatch.setattr("scanner.cli.ejecutar", lambda *args: ResultadoEscaneo(
        objetivo="http://127.0.0.1:8080", codigo_http=200, reconocimiento=None,
        hallazgos=[], duracion_segundos=0.0, peticiones=1, modulos=["recon"],
    ))
    exit_code = main(["http://127.0.0.1:8080", "--modules", "recon"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "http://127.0.0.1:8080" in captured.out
