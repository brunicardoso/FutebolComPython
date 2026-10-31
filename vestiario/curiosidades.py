"""Curiosidades com link para a Wikipédia em português.

Primeiro usamos as curiosidades conferidas de dados/curiosidades.json.
Se um jogador não tem curiosidade conferida, mas tem página da Wikipédia
já mapeada, dá para buscar a primeira frase do resumo (opcional).
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from functools import lru_cache

from . import config
from .tela import escapar, exibir

_cache_resumos: dict[str, str | None] = {}


@lru_cache(maxsize=1)
def carregar() -> dict:
    try:
        with open(config.ARQUIVO_CURIOSIDADES, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"jogadores": {}, "clubes": {}}


def resumo_wikipedia(url_pagina: str) -> str | None:
    """Primeira frase do resumo da Wikipédia (3 s no máximo; se falhar, nada)."""
    if url_pagina in _cache_resumos:
        return _cache_resumos[url_pagina]
    frase = None
    try:
        partes = urllib.parse.urlparse(url_pagina)
        titulo = partes.path.rsplit("/", 1)[-1]
        api = f"{partes.scheme}://{partes.netloc}/api/rest_v1/page/summary/{titulo}"
        pedido = urllib.request.Request(api, headers={"User-Agent": config.USER_AGENT})
        with urllib.request.urlopen(pedido, timeout=3) as resposta:
            extrato = json.load(resposta).get("extract", "")
        frase = extrato.split(". ")[0].strip().rstrip(".") + "." if extrato else None
    except Exception:
        frase = None
    _cache_resumos[url_pagina] = frase
    return frase


def _link(entrada: dict) -> tuple[str, str] | None:
    if entrada.get("wikipedia_pt"):
        return entrada["wikipedia_pt"], "📖 Leia mais na Wikipédia"
    if entrada.get("wikipedia_en"):
        return entrada["wikipedia_en"], "📖 Leia mais na Wikipédia (em inglês)"
    return None


def buscar(tabela, n: int = 3, usar_resumo: bool = False) -> list[dict]:
    """Escolhe até n curiosidades para os jogadores e clubes da tabela (pela ordem)."""
    base = carregar()
    achadas: list[dict] = []
    vistos: set[str] = set()
    candidatos = []
    if "player_id" in getattr(tabela, "columns", []):
        candidatos += [("jogadores", str(int(i))) for i in tabela["player_id"]]
    if "club_id" in getattr(tabela, "columns", []):
        candidatos += [("clubes", str(int(i))) for i in tabela["club_id"]]
    for grupo, ident in candidatos:
        if len(achadas) >= n:
            break
        if (grupo, ident) in vistos:
            continue
        vistos.add((grupo, ident))
        entrada = base.get(grupo, {}).get(ident)
        if not entrada:
            continue
        link = _link(entrada)
        if entrada.get("curiosidades"):
            texto = entrada["curiosidades"][0]["texto"]
        elif usar_resumo and entrada.get("wikipedia_pt"):
            texto = resumo_wikipedia(entrada["wikipedia_pt"])
        else:
            texto = None
        if texto:
            achadas.append({"nome": entrada.get("nome", ""), "texto": texto, "link": link})
    return achadas


def html_curiosidade(item: dict) -> str:
    link = ""
    if item["link"]:
        url, rotulo = item["link"]
        link = (f'<br><a href="{escapar(url)}" target="_blank" rel="noopener">'
                f'{escapar(rotulo)}</a>')
    return (f'<div style="background:#fff8e1;color:#4e342e;border-radius:8px;padding:8px 12px;'
            f'margin:6px 0;font-family:system-ui,sans-serif">💡 <b>Curiosidade:</b> '
            f'{escapar(item["texto"])}{link}</div>')


def mostrar(tabela, n: int = 3, usar_resumo: bool = True) -> list[dict]:
    itens = buscar(tabela, n=n, usar_resumo=usar_resumo)
    for item in itens:
        exibir(html_curiosidade(item))
    return itens
