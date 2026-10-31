"""Confere dados/curiosidades.json.

1. Toda curiosidade tem texto, fonte e verificado_em.
2. O link da Wikipédia de cada jogador/clube é o mesmo que o Wikidata indica
   para aquele ID do Transfermarkt (sem adivinhar pelo nome):
     P2446 = ID de jogador no Transfermarkt
     P7223 = ID de clube no Transfermarkt
3. Todos os links (Wikipédia e fontes) abrem.

Uso:
  pixi run verificar-curiosidades
  pixi run python scripts/verificar_curiosidades.py --mapear jogador 937958 clube 131
"""

from __future__ import annotations

import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from vestiario import config  # noqa: E402

PROPRIEDADES = {"jogadores": "P2446", "clubes": "P7223"}
API_WIKIDATA = "https://www.wikidata.org/w/api.php"
sessao = requests.Session()
sessao.headers["User-Agent"] = config.USER_AGENT


def mapear(grupo: str, ident: str) -> dict:
    """ID do Transfermarkt -> item do Wikidata -> páginas pt e en da Wikipédia."""
    busca = sessao.get(API_WIKIDATA, params={
        "action": "query", "list": "search", "format": "json",
        "srsearch": f"haswbstatement:{PROPRIEDADES[grupo]}={ident}"}, timeout=20).json()
    achados = busca["query"]["search"]
    if len(achados) != 1:
        return {"erro": f"{len(achados)} itens no Wikidata"}
    item = achados[0]["title"]
    entidade = sessao.get(API_WIKIDATA, params={
        "action": "wbgetentities", "ids": item, "props": "sitelinks", "format": "json"},
        timeout=20).json()["entities"][item]["sitelinks"]

    def url(site, lingua):
        if site not in entidade:
            return None
        titulo = entidade[site]["title"].replace(" ", "_")
        return f"https://{lingua}.wikipedia.org/wiki/{urllib.parse.quote(titulo)}"

    return {"wikidata": item, "wikipedia_pt": url("ptwiki", "pt"), "wikipedia_en": url("enwiki", "en")}


def abre(url: str) -> bool:
    try:
        resposta = sessao.get(url, timeout=20, allow_redirects=True)
        return resposta.status_code == 200
    except requests.RequestException:
        return False


def verificar() -> int:
    dados = json.loads(config.ARQUIVO_CURIOSIDADES.read_text(encoding="utf-8"))
    problemas = []
    for grupo in ("jogadores", "clubes"):
        for ident, entrada in dados.get(grupo, {}).items():
            nome = entrada.get("nome", ident)
            for fato in entrada.get("curiosidades", []):
                for campo in ("texto", "fonte", "verificado_em"):
                    if not fato.get(campo):
                        problemas.append(f"{nome}: curiosidade sem '{campo}'")
                if fato.get("fonte") and not abre(fato["fonte"]):
                    problemas.append(f"{nome}: fonte não abre: {fato['fonte']}")
            mapa = mapear(grupo, ident)
            if "erro" in mapa:
                problemas.append(f"{nome}: {mapa['erro']}")
                continue
            esperado = mapa["wikipedia_pt"] or mapa["wikipedia_en"]
            atual = entrada.get("wikipedia_pt") or entrada.get("wikipedia_en")
            if urllib.parse.unquote(atual or "") != urllib.parse.unquote(esperado or ""):
                problemas.append(f"{nome}: link {atual} difere do Wikidata ({esperado})")
            if entrada.get("wikipedia_en") and mapa["wikipedia_pt"]:
                problemas.append(f"{nome}: existe página em português, use wikipedia_pt")
            if atual and not abre(atual):
                problemas.append(f"{nome}: link não abre: {atual}")
            time.sleep(0.2)
    for problema in problemas:
        print("❌", problema)
    print("✅ Curiosidades conferidas." if not problemas else f"{len(problemas)} problema(s).")
    return 1 if problemas else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--mapear":
        pares = sys.argv[2:]
        for grupo, ident in zip(pares[::2], pares[1::2]):
            chave = "jogadores" if grupo.startswith("jogador") else "clubes"
            print(grupo, ident, mapear(chave, ident))
        sys.exit(0)
    sys.exit(verificar())
