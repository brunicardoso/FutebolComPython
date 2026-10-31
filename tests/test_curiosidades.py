import importlib

import pandas as pd

curiosidades = importlib.import_module("vestiario.curiosidades")


def test_busca_por_id_no_maximo_n():
    tabela = pd.DataFrame({"player_id": [937958, 1168219, 845654, 971570], "club_id": [131, 3, 506, 1041]})
    achadas = curiosidades.buscar(tabela, n=3)
    assert len(achadas) == 3
    assert achadas[0]["nome"] == "Lamine Yamal"
    assert achadas[0]["link"][0] == "https://pt.wikipedia.org/wiki/Lamine_Yamal"


def test_id_desconhecido_nao_mostra_nada():
    assert curiosidades.buscar(pd.DataFrame({"player_id": [1]})) == []


def test_toda_curiosidade_tem_fonte_e_data():
    base = curiosidades.carregar()
    for grupo in ("jogadores", "clubes"):
        for entrada in base[grupo].values():
            assert entrada.get("wikipedia_pt") or entrada.get("wikipedia_en")
            for fato in entrada["curiosidades"]:
                assert fato["fonte"].startswith("https://") and fato["verificado_em"]
