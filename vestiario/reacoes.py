"""Reações (GIFs e emojis) para cada momento.

Os links ficam em midia/reacoes.json. Se o link for null ou não abrir,
aparece o texto reserva (fallback) com emojis.
"""

from __future__ import annotations

import json
import random
from functools import lru_cache

from . import config
from .tela import escapar, exibir

LARGURA_MAXIMA = 300  # pixels


@lru_cache(maxsize=1)
def carregar() -> dict[str, list[dict]]:
    with open(config.ARQUIVO_REACOES, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return {k: v for k, v in dados.items() if not k.startswith("_")}


def escolher(categoria: str, sorteio: random.Random | None = None) -> dict:
    """Sorteia uma reação da categoria (sortear deixa a recompensa mais divertida)."""
    opcoes = carregar().get(categoria) or [{"url": None, "fallback": "⚽", "texto": ""}]
    return (sorteio or random).choice(opcoes)


def html_reacao(entrada: dict, extra: str = "") -> str:
    """Monta o HTML de uma reação. Sem link, usa só o texto reserva."""
    texto = f'<div style="font-size:1.3em;font-weight:700">{escapar(entrada.get("texto", ""))}</div>'
    reserva = escapar(entrada.get("fallback", "⚽"))
    url = entrada.get("url")
    if url:
        # Se a imagem falhar (sem internet, link quebrado), troca pelo texto reserva.
        figura = (f'<img src="{escapar(url)}" alt="" style="max-width:{LARGURA_MAXIMA}px;'
                  f'width:100%;border-radius:10px" '
                  f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'block\'">'
                  f'<div style="display:none;font-size:3em">{reserva}</div>')
    else:
        figura = f'<div style="font-size:3em">{reserva}</div>'
    return (f'<div style="text-align:center;padding:8px;font-family:system-ui,sans-serif">'
            f'{figura}{texto}{extra}</div>')


def mostrar(categoria: str, extra: str = "") -> dict:
    entrada = escolher(categoria)
    exibir(html_reacao(entrada, extra))
    return entrada
