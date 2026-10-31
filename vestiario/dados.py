"""Carrega o retrato (snapshot) da temporada 2025–26 que vem junto com o repositório."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from . import config


@lru_cache(maxsize=1)
def _tabela() -> pd.DataFrame:
    return pd.read_csv(config.ARQUIVO_JOGADORES)


def carregar_jogadores() -> pd.DataFrame:
    """Devolve a tabela de jogadores das 5 grandes ligas (uma cópia nova a cada vez)."""
    return _tabela().copy()
