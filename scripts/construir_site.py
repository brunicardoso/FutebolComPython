"""Gera site/catalogo.js (lido pelo site, funciona até abrindo o arquivo direto) a partir de notebooks/catalogo.json,
com os links do Colab montados a partir de vestiario/config.py.

Uso: pixi run construir-site
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

# Carrega só o config.py (sem o pacote inteiro, que precisa de pandas),
# para o site poder ser montado com um Python simples.
_spec = importlib.util.spec_from_file_location("config", RAIZ / "vestiario" / "config.py")
config = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(config)


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
