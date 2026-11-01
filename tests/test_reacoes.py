import importlib

from vestiario import config, reacoes

# A função som() esconde o módulo de mesmo nome no pacote.
som = importlib.import_module("vestiario.som")

CATEGORIAS = ["boas_vindas", "sigma", "aura", "yamal_danca", "seis_sete", "beta", "quase", "sequencia", "fim_notebook"]


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


def test_arquivos_de_gif_existem_e_sao_pequenos():
    for categoria, entradas in reacoes.carregar().items():
        for entrada in entradas:
            if entrada.get("arquivo"):
                caminho = config.PASTA_MIDIA / entrada["arquivo"]
                assert caminho.is_file(), entrada["arquivo"]
                assert caminho.stat().st_size < 1_300_000, entrada["arquivo"]


def test_gif_local_vira_data_uri():
    html = reacoes.html_reacao({"arquivo": "gifs/aura.gif", "url": None, "fallback": "🗿", "texto": "Sigma"})
    assert 'src="data:image/gif;base64,' in html and "onerror" in html


def test_gif_que_sumiu_usa_reserva():
    html = reacoes.html_reacao({"arquivo": "gifs/nao_existe.gif", "url": None, "fallback": "🗿", "texto": "Sigma"})
    assert "<img" not in html and "🗿" in html


def test_arquivo_fora_de_midia_nao_abre():
    html = reacoes.html_reacao({"arquivo": "../dados/clubes.csv", "url": None, "fallback": "🗿", "texto": "x"})
    assert "<img" not in html


def test_som_comeca_ligado_e_o_icone_desliga():
    assert som.ligado()
    html = som.html_som("sigma")
    assert 'Som.tocar("gol")' in html and "🔊" in html and "invokeFunction" in html
    som.ligar(False)
    try:
        html = som.html_som("sigma")
        assert "🔇" in html and 'Som.tocar("gol")' not in html
    finally:
        som.ligar(True)


def test_categoria_com_gif_sempre_mostra_o_gif_com_a_propria_legenda():
    import random
    sorteio = random.Random(1)
    for categoria, entradas in reacoes.carregar().items():
        tem_gif = any(e.get("arquivo") or e.get("url") for e in entradas)
        for _ in range(20):
            escolhida = reacoes.escolher(categoria, sorteio)
            assert bool(escolhida.get("arquivo") or escolhida.get("url")) == tem_gif, categoria
            assert escolhida in entradas  # a legenda é a do próprio GIF
