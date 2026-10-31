"""Gera site/catalogo.js (lido pelo site, funciona até abrindo o arquivo direto) a partir de notebooks/catalogo.json,
com os links do Colab montados a partir de vestiario/config.py.

Uso: pixi run construir-site
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from vestiario import config  # noqa: E402


def link_colab(arquivo: str) -> str:
    dono_repo = config.REPO_URL.rstrip("/").removeprefix("https://github.com/")
    return f"https://colab.research.google.com/github/{dono_repo}/blob/{config.RAMO}/{arquivo}"


def main() -> None:
    catalogo = json.loads(config.ARQUIVO_CATALOGO.read_text(encoding="utf-8"))
    for nb in catalogo["notebooks"]:
        nb["colab"] = link_colab(nb["arquivo"]) if nb["status"] == "pronto" else None
    catalogo["repo"] = config.REPO_URL
    destino = RAIZ / "site" / "catalogo.js"
    conteudo = json.dumps(catalogo, ensure_ascii=False, indent=2)
    destino.write_text(f"window.CATALOGO = {conteudo};\n", encoding="utf-8")
    print(f"Site: {destino.relative_to(RAIZ)} com {len(catalogo['notebooks'])} notebooks.")


if __name__ == "__main__":
    main()
