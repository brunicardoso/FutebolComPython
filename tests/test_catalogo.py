import json

import nbformat

from vestiario import config, missoes

CATALOGO = json.loads(config.ARQUIVO_CATALOGO.read_text(encoding="utf-8"))
PRONTOS = [n for n in CATALOGO["notebooks"] if n["status"] == "pronto"]


def test_dezesseis_notebooks_em_quatro_niveis():
    assert [n["numero"] for n in CATALOGO["notebooks"]] == list(range(1, 17))
    assert {n["nivel"] for n in CATALOGO["notebooks"]} == {1, 2, 3, 4}


def test_notebooks_prontos_existem_e_seguem_o_modelo():
    for info in PRONTOS:
        nb = nbformat.read(config.RAIZ / info["arquivo"], as_version=4)
        primeira = nb.cells[0]
        assert primeira.metadata.get("cellView") == "form"
        assert f'REPO = "{config.REPO_URL}"' in primeira.source
        assert f'notebook="{info["id"]}"' in primeira.source
        assert "#@markdown" in primeira.source and "Run anyway" in primeira.source  # aviso do Colab
        assert all(not c.get("outputs") for c in nb.cells if c.cell_type == "code")
        textos = "\n".join(c.source for c in nb.cells)
        for parte in ("Para os pais e professores", "Aquecimento", "Desafio do Técnico", "🔑 Respostas", "terminar()"):
            assert parte in textos, (info["id"], parte)
        assert info["id"] in missoes.MISSOES
        assert info["jogo"] in __import__("vestiario").jogos.CATALOGO


def test_link_do_colab():
    import sys
    sys.path.insert(0, str(config.RAIZ / "scripts"))
    from construir_site import link_colab
    assert link_colab("notebooks/nivel1_sub9/01_calculadora.ipynb") == (
        "https://colab.research.google.com/github/brunicardoso/FutebolComPython/blob/main/"
        "notebooks/nivel1_sub9/01_calculadora.ipynb")
