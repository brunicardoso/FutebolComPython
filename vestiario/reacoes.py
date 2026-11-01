"""Reações (GIFs e emojis) para cada momento.

Cada reação de midia/reacoes.json pode ter um "arquivo" (GIF escolhido pelos
pais, em midia/gifs/) ou um "url" (link do GIPHY/Tenor). Se não tiver nenhum,
ou se a imagem não abrir, aparece o texto reserva (fallback) com emojis.
"""

from __future__ import annotations

import base64
import json
import random
from functools import lru_cache

from . import config, som
from .tela import escapar, exibir

LARGURA_MAXIMA = 300  # pixels


@lru_cache(maxsize=1)
def carregar() -> dict[str, list[dict]]:
    with open(config.ARQUIVO_REACOES, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return {k: v for k, v in dados.items() if not k.startswith("_")}


def escolher(categoria: str, sorteio: random.Random | None = None) -> dict:
    """Sorteia uma reação da categoria (sortear deixa a recompensa mais divertida).

    Se a categoria tem GIF (arquivo ou link), sorteia só entre os GIFs, e cada GIF
    fica com a própria legenda. Sem GIF, sorteia entre os emojis."""
    sorteio = sorteio or random
    opcoes = carregar().get(categoria) or [{"url": None, "fallback": "⚽", "texto": ""}]
    com_imagem = [o for o in opcoes if o.get("arquivo") or o.get("url")]
    return sorteio.choice(com_imagem or opcoes)


@lru_cache(maxsize=32)
def _dados_do_arquivo(caminho: str) -> str | None:
    """Lê um GIF de midia/ e devolve como data URI (o Colab não mostra arquivos
    locais num <img>). Se o arquivo não existir, devolve None."""
    arquivo = (config.PASTA_MIDIA / caminho).resolve()
    if config.PASTA_MIDIA.resolve() not in arquivo.parents or not arquivo.is_file():
        return None
    tipo = "image/webp" if arquivo.suffix.lower() == ".webp" else "image/gif"
    return f"data:{tipo};base64,{base64.b64encode(arquivo.read_bytes()).decode('ascii')}"


def html_reacao(entrada: dict, extra: str = "") -> str:
    """Monta o HTML de uma reação. Sem imagem, usa só o texto reserva."""
    texto = f'<div style="font-size:1.3em;font-weight:700">{escapar(entrada.get("texto", ""))}</div>'
    reserva = escapar(entrada.get("fallback", "⚽"))
    url = _dados_do_arquivo(entrada["arquivo"]) if entrada.get("arquivo") else None
    url = url or entrada.get("url")
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
    exibir(html_reacao(entrada, extra + som.html_som(categoria)))
    return entrada
