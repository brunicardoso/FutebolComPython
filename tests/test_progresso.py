from vestiario.aura import EstadoAura
from vestiario.progresso import gerar_codigo, ler_codigo


def test_ida_e_volta():
    e = EstadoAura(total=1350, jogos={"embaixadinhas", "penalti"}, notebooks={1, 2, 4})
    codigo = gerar_codigo(e)
    assert codigo.startswith("AURA-1350-J")
    volta = ler_codigo(codigo.lower().replace("-", "- "))
    assert (volta.total, volta.jogos, volta.notebooks) == (1350, e.jogos, e.notebooks)


def test_codigo_errado():
    codigo = gerar_codigo(EstadoAura(total=1350))
    adulterado = codigo.replace("1350", "9350")
    assert ler_codigo(adulterado) is None
    assert ler_codigo("qualquer coisa") is None


def test_carregar_progresso(sessao):
    codigo = gerar_codigo(EstadoAura(total=700, jogos={"penalti"}, notebooks={1}))
    assert sessao.carregar_progresso(codigo)
    assert sessao._estado.total == 700 and "penalti" in sessao._estado.jogos
    assert not sessao.carregar_progresso("AURA-1-J0N0-000")


def _novo(monkeypatch):
    import vestiario
    monkeypatch.setattr(vestiario, "_estado", EstadoAura())
    monkeypatch.setattr(vestiario.progresso, "ler_drive", lambda: None)
    return vestiario


def test_campo_do_codigo_secreto_no_iniciar(tela, monkeypatch):
    vestiario = _novo(monkeypatch)
    antigo = EstadoAura(total=1350)
    antigo.jogos.add("penalti")
    vestiario.iniciar(1, "02_olheiro", codigo=gerar_codigo(antigo))
    assert vestiario._estado.total == 1350 and "penalti" in vestiario._estado.jogos
    assert any("Código secreto aceito" in t for t in tela)


def test_campo_vazio_ou_errado_nao_quebra(tela, monkeypatch):
    vestiario = _novo(monkeypatch)
    vestiario.iniciar(1, "02_olheiro", codigo="")
    assert vestiario._estado.total == 0
    vestiario.iniciar(1, "02_olheiro", codigo="AURA-errado")
    assert vestiario._estado.total == 0
    assert any("não bateu" in t for t in tela)
