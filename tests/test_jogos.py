import re

import pytest

from vestiario import config, jogos

SOM = (config.PASTA_MIDIA / "som.js").read_text(encoding="utf-8")

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


@pytest.mark.parametrize("arquivo", ARQUIVOS, ids=lambda a: a.name)
def test_jogo_tem_som_mudo_e_botao(arquivo):
    texto = arquivo.read_text(encoding="utf-8")
    assert SOM in texto, "rode: pixi run sincronizar-som"
    assert 'id="som"' in texto and "Som.botao(" in texto and "Som.ligar(CONFIG.som)" in texto
    assert "var CONFIG = window.CONFIG || {" in texto and "som:" not in texto.split("var CONFIG")[1].split(";")[0]


def test_html_jogo_injeta_configuracao():
    html = jogos.html_jogo("treino_rapido", modo="treino", dica="Use o sinal +")
    assert "<iframe" in html and "window.CONFIG" in html and "Use o sinal +" in html
