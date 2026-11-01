import re

import pytest

from vestiario import erros


def _erro(codigo: str, espaco: dict | None = None) -> BaseException:
    try:
        exec(compile(codigo, "<celula>", "exec"), dict(espaco or {}))
    except Exception as e:  # noqa: BLE001
        return e
    raise AssertionError("o código deveria dar erro")


@pytest.mark.parametrize("codigo, pedaco", [
    ("gols = ___", "___"),
    ("print(1 + 2", "parêntese"),
    ('print("oi)', "aspas"),
    ("x = 1\n  y = 2", "começo de uma linha"),
    ("1 / 0", "dividir por zero"),
    ("[1, 2][5]", "posição"),
    ('{"gols": 1}["gol"]', "coluna"),
    ('"a" + 1', "não combinam"),
    ("int('dez')", "número"),
    ("(1).sort_valores()", ".sort_valores"),
])
def test_dica_para_cada_erro(codigo, pedaco):
    dica = erros.explicar(_erro(codigo))
    assert pedaco in dica


def test_nome_criado_em_outra_celula():
    dica = erros.explicar(_erro("jogadores.head()"), celulas=["jogadores = carregar_jogadores()"])
    assert "mais para cima" in dica


def test_nome_parecido():
    dica = erros.explicar(_erro("chcar(1)"), espaco={"checar": print})
    assert "<code>checar</code>" in dica


CELULAS = ("jogadores = carregar_jogadores()\nprint(\"Jogadores na tabela:\", jogadores.shape[0])",
           "jogadores.head()",
           'checar("___", "m2")')


def test_acha_o_original_quando_apagam_um_pedaco():
    assert erros.codigo_original('print("Jogadores na tabela:", jogadores.shape[0]', CELULAS) == CELULAS[0]
    assert erros.codigo_original("jogadores.hea", CELULAS) == "jogadores.head()"


def test_nao_mostra_original_igual_ou_sem_parecido():
    assert erros.codigo_original("jogadores.head()", CELULAS) is None
    assert erros.codigo_original("import antigravity", CELULAS) is None
    assert erros.codigo_original("algo", ()) is None


def test_notebook_que_nao_existe():
    assert erros.celulas_originais("99_nao_existe") == ()


def test_celulas_originais_pulam_as_escondidas():
    celulas = erros.celulas_originais("02_olheiro")
    assert celulas and not any("Preparar o vestiário" in c for c in celulas)


def test_caixa_em_portugues_sem_vermelho():
    html = erros.html_erro("dica", "x = 1", "Traceback\x1b[31m (most recent call last)")
    assert "Ops!" in html and "ver erro técnico" in html and "Copie e cole" in html
    assert "\x1b" not in html and "red" not in html
    assert re.search(r"<pre[^>]*>x = 1</pre>", html)
