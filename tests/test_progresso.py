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
