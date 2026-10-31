from vestiario.aura import EstadoAura, eh_67


def test_detecta_67():
    for valor in (67, 670, 6700, "67", 67.0, "6700"):
        assert eh_67(valor)
    for valor in (66, 68, 6.7, True, "sessenta", None):
        assert not eh_67(valor)


def test_67_uma_vez_por_missao():
    e = EstadoAura()
    assert e.avisar_67(67, "m1")
    assert not e.avisar_67(67, "m1")
    assert e.avisar_67(670, "m2")


def test_67_aparece_no_checar(sessao, tela):
    sessao.chute(67, 70)
    assert any("SIX SEVEN" in h for h in tela)
