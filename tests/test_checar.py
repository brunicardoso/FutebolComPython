from vestiario import missoes
from vestiario.missoes import Missao, Qualquer, comparar, normalizar


def test_normalizar_tira_acentos_maiusculas_e_espacos():
    assert normalizar("  Kylian   MBAPPÉ ") == "kylian mbappe"
    assert normalizar("Kenan Yıldız") == "kenan yildiz"


def test_texto_com_acento_e_sobrenome():
    m = Missao("Carlos Espí", "", "", parcial=True)
    assert comparar("carlos espi", m)
    assert comparar("ESPÍ", m)
    assert not comparar("es", m)
    assert not comparar("Said", m)


def test_numero_com_tolerancia_e_texto_numerico():
    m = Missao(1 / 3, "", "", tolerancia=0.01)
    assert comparar(0.33, m)
    assert comparar("0,333", m)
    assert not comparar(0.3, m)
    assert comparar(2.0, Missao(2, "", ""))
    assert not comparar(True, Missao(1, "", ""))


def test_qualquer_aceita_empates():
    m = Missao(Qualquer(["Endrick", "Rayan"]), "", "", parcial=True)
    assert comparar("rayan", m) and comparar("Endrick", m)


def test_lista():
    assert comparar([4, 3, 3], Missao([4, 3, 3], "", ""))
    assert not comparar([4, 4, 2], Missao([4, 3, 3], "", ""))


def test_respostas_de_dados_vem_do_snapshot():
    m = missoes.buscar("02_olheiro", "aquecimento")
    from vestiario.dados import carregar_jogadores
    assert m.esperado() == carregar_jogadores().iloc[0]["nome"]


def test_checar_acerto_da_aura_e_bonus(sessao, tela):
    assert sessao.checar(4, "m1")
    assert sessao._estado.total == 150
    assert any("+150 de aura" in h for h in tela)


def test_checar_tres_erros_mostra_resposta_sem_aura(sessao, tela):
    for _ in range(2):
        assert not sessao.checar(99, "m1")
    assert any("Modo beta" in h or "Na trave" in h for h in tela)
    assert any("treino_rapido" in h or "Treino" in h for h in tela)
    sessao.checar(99, "m1")
    assert any("Vamos ver juntos?" in h for h in tela)
    assert sessao._estado.total == 0
    sessao.checar(4, "m1")
    assert sessao._estado.total == 0  # a missão já foi mostrada, não dá aura


def test_checar_avisa_espaco_vazio(sessao, tela):
    assert not sessao.checar("___", "m1")
    assert any("___" in h for h in tela)
    assert sessao._estado.erros == {}


def test_chute_na_trave(sessao, tela):
    assert sessao.chute(95, 100) == 5.0
    assert sessao._estado.total == 100
    sessao.chute(95, 100)
    assert sessao._estado.total == 100  # a mesma pergunta só paga uma vez


EMPATES = {"m2": ["Michael Olise", "Bruno Fernandes"],
           "desafio1": ["Erling Haaland", "Lamine Yamal"],
           "desafio2": ["Endrick", "Rayan"]}


def test_empates_dos_dados_aceitam_todos_os_nomes():
    for missao, nomes in EMPATES.items():
        m = missoes.buscar("02_olheiro", missao)
        assert sorted(m.esperado()) == sorted(nomes), missao
        for nome in nomes:
            variantes = [nome, nome.upper(), f"  {nome} ", nome + "\u200b",
                         nome.replace(" ", "\u00a0"), nome.split()[-1]]
            for v in variantes:
                assert comparar(v, m), (missao, v)


def test_erro_de_escrita_nao_vale():
    m = missoes.buscar("02_olheiro", "m2")
    for v in ["Bruno Fernandez", "Olisse", "B. Fernandes", "Fernandes, Bruno", "Bruno Fernandes.",
              '"Bruno Fernandes"', "93 Bruno Fernandes", "Dimarco", "Messi"]:
        assert not comparar(v, m), v
    for v in ["Bruno Fernandez", "Olisse", "B. Fernandes", "Fernandes, Bruno", "Bruno Fernandes."]:
        assert missoes.quase_escrito(v, m), v
    for v in ["Dimarco", "Messi"]:
        assert not missoes.quase_escrito(v, m), v


def test_empate_aparece_e_errinho_ganha_dica_de_escrita(tela, monkeypatch):
    import vestiario
    from vestiario.aura import EstadoAura
    monkeypatch.setattr(vestiario, "_estado", EstadoAura())
    monkeypatch.setattr(vestiario.progresso, "ler_drive", lambda: None)
    vestiario.iniciar(1, "02_olheiro")
    tela.clear()
    assert not vestiario.checar("Bruno Fernandez", "m2")
    assert any("cada letra conta" in t for t in tela) and vestiario._estado.total == 0
    tela.clear()
    assert vestiario.checar("Bruno Fernandes", "m2")
    assert any("Empate!" in t and "Michael Olise" in t for t in tela)
    assert not any("escrito certinho" in t for t in tela)
