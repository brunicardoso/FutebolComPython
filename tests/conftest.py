import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def tela(monkeypatch):
    """Guarda tudo o que seria mostrado na tela, em vez de mostrar."""
    import importlib

    import vestiario
    from vestiario import reacoes

    # A função curiosidades() esconde o módulo de mesmo nome no pacote.
    curiosidades = importlib.import_module("vestiario.curiosidades")

    saida: list[str] = []
    for modulo in (vestiario, reacoes, curiosidades):
        monkeypatch.setattr(modulo, "exibir", saida.append)
    return saida


@pytest.fixture
def sessao(tela, monkeypatch):
    """Um vestiário novinho, sem aura, no notebook 01."""
    import vestiario
    from vestiario.aura import EstadoAura

    monkeypatch.setattr(vestiario, "_estado", EstadoAura())
    monkeypatch.setattr(vestiario.progresso, "ler_drive", lambda: None)
    vestiario.iniciar(1, "01_calculadora")
    tela.clear()
    return vestiario
