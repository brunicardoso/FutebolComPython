"""Sons das reações. Os sons são sintetizados no navegador (midia/som.js):
nenhum arquivo de áudio, nenhuma rede. Começa LIGADO; tocar no ícone 🔊 desliga
(e tocar no 🔇 liga de novo). som() e som(False) também funcionam."""

from __future__ import annotations

from functools import lru_cache

from . import config

# Qual som toca em cada tipo de reação.
SOM_DA_REACAO = {
    "boas_vindas": "apito",
    "sigma": "gol",
    "aura": "gol",
    "sequencia": "torcida",
    "yamal_danca": "torcida",
    "fim_notebook": "torcida",
    "seis_sete": "gol",
    "quase": "defesa",
    "beta": "erro",
}

_estado = {"ligado": True}

# Nome usado pelo botão 🔊/🔇 para avisar o Python (só no Colab).
NOME_CALLBACK = "vestiario.som"


def ligado() -> bool:
    return _estado["ligado"]


def ligar(sim: bool) -> None:
    _estado["ligado"] = bool(sim)


@lru_cache(maxsize=1)
def biblioteca_js() -> str:
    return (config.PASTA_MIDIA / "som.js").read_text(encoding="utf-8")


def botao(tocar: str = "") -> str:
    """Ícone 🔊/🔇 que liga e desliga o som. No Colab, avisa o Python, para as
    próximas reações e jogos também ficarem mudos (ou com som)."""
    icone = "🔊" if ligado() else "🔇"
    dica = "Desligar o som" if ligado() else "Ligar o som"
    som_ao_ligar = f"Som.tocar('{tocar}');" if tocar else "Som.tocar('clique');"
    return (f'<button aria-label="{dica}" title="{dica}" onclick="'
            f"var ligar=!Som.ligado();Som.ligar(ligar);this.textContent=ligar?'🔊':'🔇';"
            f"if(ligar){{{som_ao_ligar}}}"
            f"try{{google.colab.kernel.invokeFunction('{NOME_CALLBACK}',[ligar],{{}})}}catch(e){{}}"
            f'" style="min-width:48px;min-height:48px;border:0;border-radius:12px;'
            f'background:#eceff1;font-size:22px;cursor:pointer;margin-top:6px">{icone}</button>'
            f'<script>{biblioteca_js()}\nSom.ligar({"true" if ligado() else "false"});</script>')


def html_som(categoria: str) -> str:
    """O ícone 🔊/🔇 e, se o som estiver ligado, o som da reação.
    (O navegador pode bloquear o som antes do primeiro toque; o ícone continua lá.)"""
    nome = SOM_DA_REACAO.get(categoria)
    if not nome:
        return ""
    tocar = f'<script>Som.tocar("{nome}");</script>' if ligado() else ""
    return botao(nome) + tocar


def registrar_callback() -> bool:
    """No Colab, deixa o ícone 🔊/🔇 mudar o som no Python. Fora dele, não faz nada."""
    try:
        from google.colab import output
        output.register_callback(NOME_CALLBACK, ligar)
        return True
    except Exception:
        return False
