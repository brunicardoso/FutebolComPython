"""Copia midia/som.js para dentro de cada jogo (os jogos precisam ser um arquivo só).

O bloco fica entre os comentários SOM-INICIO e SOM-FIM, logo no começo do
<script> principal. Rode depois de mudar midia/som.js:

    pixi run sincronizar-som
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BLOCO = re.compile(r"/\* SOM-INICIO.*?/\* SOM-FIM \*/\n", re.S)


def bloco_som() -> str:
    return (RAIZ / "midia" / "som.js").read_text(encoding="utf-8")


def sincronizar(texto: str, som: str) -> str:
    if BLOCO.search(texto):
        return BLOCO.sub(lambda _: som, texto, count=1)
    # Primeira vez: coloca logo depois do <script> do corpo da página.
    posicao = texto.index("<script>", texto.index("<body>")) + len("<script>\n")
    return texto[:posicao] + som + texto[posicao:]


def main() -> int:
    som = bloco_som()
    for jogo in sorted((RAIZ / "jogos").glob("*.html")):
        antes = jogo.read_text(encoding="utf-8")
        depois = sincronizar(antes, som)
        if depois != antes:
            jogo.write_text(depois, encoding="utf-8")
            print(f"🔊 atualizado: {jogo.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
