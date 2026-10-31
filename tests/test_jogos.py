import re

import pytest

from vestiario import config, jogos

ARQUIVOS = sorted(config.PASTA_JOGOS.glob("*.html"))


def test_todos_os_jogos_do_catalogo_existem():
    assert {a.stem for a in ARQUIVOS} >= set(jogos.CATALOGO)


@pytest.mark.parametrize("arquivo", ARQUIVOS, ids=lambda a: a.name)
def test_jogo_autocontido(arquivo):
    texto = arquivo.read_text(encoding="utf-8")
    assert arquivo.stat().st_size < 200_000
    assert "http" not in texto, "jogos não podem fazer chamadas de rede"
    assert re.search(r"<(script|link)[^>]+(src|href)=", texto) is None
    for obrigatorio in ('lang="pt-BR"', "viewport", "</head>", "Fim de jogo!", "postMessage"):
        assert obrigatorio in texto


def test_html_jogo_injeta_configuracao():
    html = jogos.html_jogo("treino_rapido", modo="treino", dica="Use o sinal +")
    assert "<iframe" in html and "window.CONFIG" in html and "Use o sinal +" in html
