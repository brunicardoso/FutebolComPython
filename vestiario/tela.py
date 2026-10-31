"""Mostra coisas na tela do notebook. Fica separado para os testes
poderem trocar `exibir` e guardar o que seria mostrado."""

from __future__ import annotations

import html as _html

try:
    from IPython.display import HTML, display
except ImportError:  # fora do Jupyter: só imprime o texto
    HTML = None
    display = None


def exibir(conteudo_html: str) -> None:
    """Mostra um pedaço de HTML (ou imprime, se não houver Jupyter)."""
    if display is None:
        print(conteudo_html)
    else:
        display(HTML(conteudo_html))


def escapar(texto) -> str:
    return _html.escape(str(texto))


def caixa(texto_html: str, cor: str = "#1b5e20", fundo: str = "#e8f5e9",
          tamanho: str = "1.15em") -> str:
    """Uma caixinha colorida com texto grande."""
    return (f'<div style="background:{fundo};color:{cor};border-left:6px solid {cor};'
            f'padding:10px 14px;margin:8px 0;border-radius:8px;font-size:{tamanho};'
            f'font-family:system-ui,sans-serif;line-height:1.4">{texto_html}</div>')


def numero(n) -> str:
    """Formata números do jeito brasileiro: 1.350 e 2,5."""
    if isinstance(n, bool):
        return str(n)
    try:
        valor = float(n)
    except (TypeError, ValueError):
        return str(n)
    if valor.is_integer():
        return f"{int(valor):,}".replace(",", ".")
    texto = f"{valor:,.2f}".rstrip("0").rstrip(".")
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")
