"""Mini-jogos: cada um é um arquivo HTML em jogos/, mostrado dentro do notebook.

O jogo roda dentro de um <iframe>. Quando uma partida acaba, ele manda uma
mensagem (postMessage) com os pontos. No Colab, essa mensagem vira aura
(no máximo +50 por partida). Fora do Colab, o jogo funciona, mas não dá aura.
"""

from __future__ import annotations

import json
import uuid

from . import config
from .tela import escapar

# tipo "campeao": recompensa que fica no vestiário; "treino": aparece depois de um erro.
CATALOGO = {
    "embaixadinhas": {"titulo": "Embaixadinhas", "icone": "🦶", "tipo": "campeao"},
    "goleiro_reflexo": {"titulo": "Goleiro Reflexo", "icone": "🧤", "tipo": "campeao"},
    "tabela_maluca": {"titulo": "Tabela Maluca", "icone": "📋", "tipo": "campeao"},
    "penalti": {"titulo": "Pênalti", "icone": "🥅", "tipo": "campeao"},
    "treino_rapido": {"titulo": "Treino Rápido", "icone": "⏱️", "tipo": "treino"},
}

NOME_CALLBACK = "vestiario.aura_do_jogo"
ALTURA = 560


def html_jogo(nome: str, modo: str = "campeao", dica: str = "") -> str:
    """Monta o HTML do jogo dentro de um iframe, com as configurações dele."""
    with open(config.PASTA_JOGOS / f"{nome}.html", encoding="utf-8") as arquivo:
        pagina = arquivo.read()
    ident = uuid.uuid4().hex[:8]
    configuracao = {"modo": modo, "dica": dica, "id": ident, "nome": nome}
    script = f"<script>window.CONFIG = {json.dumps(configuracao, ensure_ascii=False)};</script>"
    pagina = pagina.replace("</head>", script + "</head>", 1)
    # O iframe recebe as mensagens do jogo e repassa a aura para o Python (só no Colab).
    ponte = f"""
<script>
window.addEventListener("message", function (evento) {{
  var d = evento.data || {{}};
  if (d.tipo !== "fim_de_jogo" || d.id !== "{ident}" || d.modo !== "campeao") return;
  if (window.google && google.colab && google.colab.kernel) {{
    google.colab.kernel.invokeFunction("{NOME_CALLBACK}", ["{nome}", d.pontos], {{}});
  }}
}});
</script>"""
    return (f'<iframe srcdoc="{escapar(pagina)}" style="width:100%;max-width:520px;'
            f'height:{ALTURA}px;border:0;border-radius:14px" '
            f'sandbox="allow-scripts"></iframe>{ponte}')


def registrar_callback(funcao) -> bool:
    """No Colab, deixa o jogo mandar a aura de volta. Fora dele, não faz nada."""
    try:
        from google.colab import output
        output.register_callback(NOME_CALLBACK, funcao)
        return True
    except Exception:
        return False
