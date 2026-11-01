"""Procura palavras em inglês em tudo o que o aluno (ou os pais) leem.

Olha: Markdown dos notebooks, comentários e textos (strings) do código,
texto e strings dos jogos e do site, e comentários dos scripts e testes.
É uma checagem simples por lista de palavras comuns do inglês.

Uso: pixi run checar-idioma
"""

from __future__ import annotations

import io
import json
import re
import sys
import tokenize
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

PALAVRAS_INGLES = {
    "the", "and", "you", "your", "with", "this", "that", "are", "click", "press", "here",
    "welcome", "hint", "try", "again", "wrong", "correct", "score", "level", "points",
    "player", "players", "loading", "please", "next", "yes", "great", "nice", "awesome",
    "good", "job", "well", "done", "win", "lose", "lost", "won", "goalkeeper", "shot",
    "answer", "question", "check", "guess", "streak", "unlock", "unlocked", "locked",
    "save", "saved", "progress", "secret", "code", "should", "would", "will", "from",
    "into", "about", "what", "when", "where", "which", "there", "their", "they", "have",
    "has", "not", "but", "only", "each", "every", "must", "need", "returns", "return",
}
# Expressões permitidas (o meme "six seven" é o nome da piada).
# Também valem nomes de colunas do Transfermarkt e palavras-chave do Python.
PERMITIDAS = [r"six seven", r"ascending=false", r"sort_values", r"value_counts",
              r"user-agent", r"pt-br", r"cc0", r"cc by-nc-sa", r"polyform noncommercial", r"player_id", r"club_id",
              r"\band / or\b",
              # Pedaços das mensagens de erro do próprio Python (vestiario/erros.py procura por eles)
              # e o tipo de célula do Jupyter.
              r"does not match", r"maybe you meant", r'"code"',
              # O aviso do Colab e o nome do botão aparecem como o aluno vê na tela.
              r"this notebook was not authored by google", r"run anyway"]


def limpar(texto: str) -> str:
    texto = re.sub(r"https?://\S+", " ", texto)
    texto = re.sub(r"`[^`]*`", " ", texto)
    texto = re.sub(r"<[^>]*>", " ", texto)  # etiquetas HTML e SVG
    for permitida in PERMITIDAS:
        texto = re.sub(permitida, " ", texto, flags=re.IGNORECASE)
    return texto


def achar(texto: str) -> list[str]:
    return sorted({p for p in re.findall(r"[A-Za-z]+", limpar(texto)) if p.lower() in PALAVRAS_INGLES})


def textos_python(fonte: str, so_comentarios: bool = False) -> list[str]:
    # Linhas com "!" (comandos do Colab) não são Python puro.
    fonte = "\n".join("" if l.lstrip().startswith("!") else l for l in fonte.splitlines())
    partes = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(fonte).readline):
            if tok.type == tokenize.COMMENT or (tok.type == tokenize.STRING and not so_comentarios):
                partes.append(tok.string)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        partes.append(fonte)
    return partes


def textos_html(fonte: str) -> list[str]:
    estilos = re.sub(r"<style.*?</style>", " ", fonte, flags=re.S)
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", estilos, flags=re.S)
    sem_scripts = re.sub(r"<script.*?</script>", " ", estilos, flags=re.S)
    partes = [re.sub(r"<[^>]+>", " ", sem_scripts)]
    for js in scripts:
        partes += re.findall(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', js)
        partes += re.findall(r"//[^\n]*|/\*.*?\*/", js, flags=re.S)
    return partes


def coletar() -> list[tuple[str, str]]:
    itens: list[tuple[str, str]] = []
    for nb_arquivo in sorted((RAIZ / "notebooks").rglob("*.ipynb")):
        nb = json.loads(nb_arquivo.read_text(encoding="utf-8"))
        for i, celula in enumerate(nb["cells"]):
            fonte = "".join(celula["source"])
            local = f"{nb_arquivo.relative_to(RAIZ)} célula {i}"
            if celula["cell_type"] == "markdown":
                itens.append((local, fonte))
            else:
                itens += [(local, t) for t in textos_python(fonte)]
    for py in sorted((RAIZ / "vestiario").glob("*.py")):
        itens += [(str(py.relative_to(RAIZ)), t) for t in textos_python(py.read_text(encoding="utf-8"))]
    for py in sorted([*(RAIZ / "scripts").glob("*.py"), *(RAIZ / "tests").glob("*.py")]):
        itens += [(str(py.relative_to(RAIZ)), t)
                  for t in textos_python(py.read_text(encoding="utf-8"), so_comentarios=True)]
    for html in sorted([*(RAIZ / "jogos").glob("*.html"), RAIZ / "site" / "index.html"]):
        if html.exists():
            itens += [(str(html.relative_to(RAIZ)), t) for t in textos_html(html.read_text(encoding="utf-8"))]
    for json_arquivo in (RAIZ / "midia" / "reacoes.json", RAIZ / "notebooks" / "catalogo.json"):
        itens.append((str(json_arquivo.relative_to(RAIZ)), json_arquivo.read_text(encoding="utf-8")))
    return itens


def main() -> int:
    problemas = [(local, achar(texto)) for local, texto in coletar()]
    problemas = [(l, p) for l, p in problemas if p]
    for local, palavras in problemas:
        print(f"❌ {local}: {', '.join(palavras)}")
    print("✅ Nada de inglês encontrado." if not problemas else f"{len(problemas)} trecho(s) com inglês.")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
