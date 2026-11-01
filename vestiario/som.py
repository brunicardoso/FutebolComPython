"""Sons das reações. Os sons são sintetizados no navegador (midia/som.js):
nenhum arquivo de áudio, nenhuma rede. Começa mudo; o aluno liga com som()."""

from __future__ import annotations

from functools import lru_cache

from . import config

# Qual som toca em cada tipo de reação.
SOM_DA_REACAO = {
    "boas_vindas": "apito",
    "sigma": "gol",
    "aura": "gol",
    "sequencia": "torcida",
    "yamal_danca": "torcida",
    "fim_notebook": "torcida",
    "seis_sete": "gol",
    "quase": "defesa",
    "beta": "erro",
}

_estado = {"ligado": False}


def ligado() -> bool:
    return _estado["ligado"]


def ligar(sim: bool) -> None:
    _estado["ligado"] = bool(sim)


@lru_cache(maxsize=1)
def biblioteca_js() -> str:
    return (config.PASTA_MIDIA / "som.js").read_text(encoding="utf-8")


def html_som(categoria: str) -> str:
    """Tenta tocar o som da reação. Se o navegador bloquear, fica um botão 🔊 para tocar."""
    nome = SOM_DA_REACAO.get(categoria)
    if not ligado() or not nome:
        return ""
    return (f'<button onclick="Som.ligar(true);Som.tocar(\'{nome}\')" aria-label="Ouvir de novo" '
            f'style="min-width:48px;min-height:48px;border:0;border-radius:12px;'
            f'background:#eceff1;font-size:22px;cursor:pointer;margin-top:6px">🔊</button>'
            f'<script>{biblioteca_js()}\nSom.ligar(true);Som.tocar("{nome}");</script>')
