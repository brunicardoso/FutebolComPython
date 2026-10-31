from vestiario.aura import EstadoAura, nivel


def test_pontos_e_bonus():
    e = EstadoAura()
    r = e.acertou("a")
    assert r.pontos == 150 and r.primeira
    e.errou("b")
    assert e.acertou("b").pontos == 100
    assert e.acertou("c", dificil=True).pontos == 550


def test_aura_nunca_diminui():
    e = EstadoAura(total=500)
    e.errou("x")
    e.ganhar(-300)
    assert e.total == 500


def test_sequencia():
    e = EstadoAura()
    marcos = [e.acertou(f"m{i}").marco_sequencia for i in range(5)]
    assert marcos == [None, None, 3, None, 5]
    e.errou("z")
    assert e.sequencia == 0


def test_niveis():
    assert nivel(0)[0] == "Reserva"
    assert nivel(1000)[0] == "Titular"
    assert nivel(10_000) == ("Sigma Supremo", None, 1.0)
    nome, proximo, fracao = nivel(2000)
    assert (nome, proximo) == ("Titular", "Craque") and fracao == 0.5


def test_subir_de_nivel():
    e = EstadoAura(total=950)
    assert e.acertou("a").subiu_para == "Titular"


def test_jogo_paga_no_maximo_50_e_poucas_vezes():
    e = EstadoAura()
    assert e.premiar_jogo("penalti", 999) == 50
    assert e.premiar_jogo("penalti", 10) == 10
    assert e.premiar_jogo("penalti", 10) == 10
    assert e.premiar_jogo("penalti", 10) == 0
