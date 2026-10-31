from vestiario import reacoes

CATEGORIAS = ["boas_vindas", "sigma", "aura", "yamal_danca", "seis_sete", "beta", "quase", "sequencia"]


def test_todas_as_categorias_tem_reserva():
    dados = reacoes.carregar()
    for categoria in CATEGORIAS:
        assert dados[categoria], categoria
        for entrada in dados[categoria]:
            assert entrada["fallback"] and entrada["texto"]
            assert entrada["url"] is None or entrada["url"].startswith("https://")


def test_url_nula_usa_reserva():
    html = reacoes.html_reacao({"url": None, "fallback": "🗿", "texto": "Sigma"})
    assert "🗿" in html and "<img" not in html


def test_url_quebrada_tem_plano_b():
    html = reacoes.html_reacao({"url": "https://exemplo.invalido/x.gif", "fallback": "🗿", "texto": "Sigma"})
    assert "onerror" in html and "🗿" in html and "max-width:300px" in html


def test_beta_nunca_xinga():
    for entrada in reacoes.carregar()["beta"]:
        assert entrada["texto"].startswith("Modo beta")
